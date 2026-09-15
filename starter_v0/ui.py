"""Streamlit chat UI for the Northstar Electronics sales assistant.

Run from starter_v0/:  streamlit run ui.py

The UI reuses the agent loop from chat.py, so behaviour matches the CLI. Every
turn shows the tool calls, their input args, the raw result or error, the
artifact version and provider/model, and is saved to transcripts/ in the same
JSON format as chat.py.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from chat import ARTIFACTS_DIR, ROOT, now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


PROVIDERS = ["openai", "openrouter", "anthropic", "gemini"]
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"


def new_transcript(*, version: str, provider_name: str, model: str | None, history_window: int, max_tool_rounds: int) -> tuple[dict[str, Any], Path]:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), "ui", timestamp])
    transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "interface": "streamlit_ui",
        "system_prompt": str(SYSTEM_PROMPT_PATH.relative_to(ROOT)),
        "tools": str(TOOLS_PATH.relative_to(ROOT)),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    return transcript, TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"


def run_turn(
    *,
    provider: Any,
    tools: list[dict[str, Any]],
    system_prompt: str,
    model: str | None,
    history: list[dict[str, str]],
    history_window: int,
    max_tool_rounds: int,
    user_text: str,
    turn_index: int,
) -> dict[str, Any]:
    """Run one user turn through the shared agent loop and return a transcript turn record."""
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(history, history_window),
        {"role": "user", "content": user_text},
    ]
    turn: dict[str, Any] = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    try:
        turn.update(run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=tools,
            model=model,
            max_tool_rounds=max_tool_rounds,
        ))
    except Exception as exc:  # show provider failures instead of hiding them
        turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
    turn["ended_at"] = now_iso()
    return turn


def pending_clarify(turn: dict[str, Any]) -> dict[str, Any] | None:
    """Return the clarify result the agent is waiting on, if any."""
    if turn.get("status") != "waiting_for_user":
        return None
    for event in reversed(turn.get("tool_events", [])):
        result = event.get("result")
        if isinstance(result, dict) and result.get("awaiting_user"):
            return result
    return None


def result_has_error(result: Any) -> bool:
    return isinstance(result, dict) and bool(result.get("error"))


def render_turn(st: Any, turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        status = turn.get("status")
        if status == "provider_error":
            st.error(f"Provider error — {turn.get('error')}")
            return
        for round_record in turn.get("rounds", []):
            calls = round_record.get("tool_calls", [])
            if not calls:
                continue
            label = f"Vòng {round_record['round']}: " + ", ".join(call["name"] for call in calls)
            errors = [event for event in round_record.get("tool_results", []) if result_has_error(event.get("result"))]
            with st.expander(("⚠️ " if errors else "🔧 ") + label, expanded=True):
                for event in round_record.get("tool_results", []):
                    st.markdown(f"**Tool:** `{event['tool']}`")
                    st.caption("Input args")
                    st.code(json.dumps(event.get("args", {}), ensure_ascii=False, indent=2), language="json")
                    result = event.get("result")
                    if result_has_error(result):
                        st.error(f"Tool error: {result.get('error')}")
                        st.caption("Result (error, hiển thị nguyên văn)")
                    else:
                        st.caption("Result")
                    st.code(json.dumps(result, ensure_ascii=False, indent=2, default=str), language="json")
        clarify = pending_clarify(turn)
        if clarify:
            st.info(f"**Cần bạn trả lời** ({clarify.get('response_type', 'text')}): {clarify.get('question')}")
        else:
            st.markdown(turn.get("assistant_text") or "_(không có nội dung trả lời)_")
        if status == "max_tool_rounds":
            st.warning("Dừng vì đạt số vòng tool tối đa.")
        st.caption(f"status: `{status}` · {turn.get('started_at')} → {turn.get('ended_at')}")


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="Northstar Sales Assistant", page_icon="🛒", layout="wide")
    state = st.session_state

    with st.sidebar:
        st.header("Cấu hình")
        provider_name = st.selectbox("Provider", PROVIDERS, index=0)
        version = st.text_input("Version label", value="v3")
        model_override = st.text_input("Model (để trống = mặc định của provider)", value="")
        history_window = st.number_input("History window (cặp lượt)", min_value=0, max_value=20, value=5)
        max_tool_rounds = st.number_input("Max tool rounds", min_value=1, max_value=8, value=4)
        new_chat = st.button("🆕 Cuộc hội thoại mới")

    config = (provider_name, version, model_override, int(history_window), int(max_tool_rounds))
    if new_chat or state.get("config") != config:
        try:
            provider = make_provider(provider_name)
        except Exception as exc:
            st.error(f"Không tạo được provider: {type(exc).__name__}: {exc}")
            st.stop()
        model = model_override.strip() or None
        transcript, path = new_transcript(
            version=version,
            provider_name=provider_name,
            model=model or getattr(provider, "default_model", None),
            history_window=int(history_window),
            max_tool_rounds=int(max_tool_rounds),
        )
        state.update({
            "config": config,
            "provider": provider,
            "model": model,
            "tools": to_openai_tools(load_tool_declarations(TOOLS_PATH)),
            "system_prompt": SYSTEM_PROMPT_PATH.read_text(encoding="utf-8"),
            "history": [],
            "transcript": transcript,
            "transcript_path": path,
            "queued_input": None,
        })

    transcript = state["transcript"]
    with st.sidebar:
        st.divider()
        st.subheader("Phiên bản artifact")
        st.code(transcript["artifact_version"], language="text")
        st.caption(f"prompt_hash `{transcript['prompt_hash'][:12]}` · tools_hash `{transcript['tools_hash'][:12]}`")
        st.markdown(f"**Provider/model:** `{transcript['provider']}` / `{transcript['model']}`")
        if transcript["turns"]:
            st.caption(f"Transcript: `{state['transcript_path'].relative_to(ROOT)}`")

    st.title("🛒 Northstar Electronics — Trợ lý bán hàng")
    st.caption(f"artifact `{transcript['artifact_version']}` · provider `{transcript['provider']}` · model `{transcript['model']}`")

    for turn in transcript["turns"]:
        render_turn(st, turn)

    last_clarify = pending_clarify(transcript["turns"][-1]) if transcript["turns"] else None
    if last_clarify and last_clarify.get("response_type") in {"yes_no", "choice"}:
        choices = ["Đồng ý", "Không"] if last_clarify["response_type"] == "yes_no" else list(last_clarify.get("options") or [])
        if choices:
            st.caption("Trả lời nhanh:")
            columns = st.columns(len(choices))
            for column, choice in zip(columns, choices):
                if column.button(choice, key=f"quick_{len(transcript['turns'])}_{choice}"):
                    state["queued_input"] = choice

    typed = st.chat_input("Nhập yêu cầu, ví dụ: Còn SKU-1003 ở kho Đà Nẵng không?")
    user_text = (typed or state.pop("queued_input", None) or "").strip()
    if not user_text:
        return

    with st.spinner("Đang gọi model và tool…"):
        turn = run_turn(
            provider=state["provider"],
            tools=state["tools"],
            system_prompt=state["system_prompt"],
            model=state["model"],
            history=state["history"],
            history_window=int(history_window),
            max_tool_rounds=int(max_tool_rounds),
            user_text=user_text,
            turn_index=len(transcript["turns"]) + 1,
        )
    if turn["status"] != "provider_error":
        state["history"].extend([
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": turn.get("assistant_text") or ""},
        ])
    transcript["turns"].append(turn)
    write_transcript(state["transcript_path"], transcript)
    st.rerun()


if __name__ == "__main__":
    main()
