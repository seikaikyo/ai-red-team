"""讀 Claude 回應的文字與結束原因

官方要求（claude-platform 文件，2026-11-19 對照）：
- 依區塊 type 挑文字，不讀 content[0]：Opus 5、Sonnet 5 以後沒帶 thinking 也會先思考，
  第一塊可能是 thinking（build-with-claude/prompt-engineering/claude-prompting-best-practices.md:779）
- 每次讀 stop_reason：拒答是 HTTP 200 加 refusal，不是錯誤（build-with-claude/handling-stop-reasons.md:1783）；
  思考算進 max_tokens，上限太小會在出文字前停住（models/fable-5-2/migration-guide.md:95）
"""

INCOMPLETE_STOP_REASONS = ("refusal", "max_tokens")

# Claude 4.7 以後的模型收到非預設的 temperature、top_p、top_k 會回 400
# （build-with-claude/thinking.md:1230）。前綴比對，新版本落在同一家族就涵蓋到。
SAMPLING_UNSUPPORTED_PREFIXES = (
    "claude-opus-4-7",
    "claude-opus-4-8",
    "claude-opus-5",
    "claude-sonnet-5",
    "claude-haiku-5",
    "claude-fable-",
    "claude-mythos-",
)


def text_and_stop_reason(message) -> tuple[str, str | None]:
    """收集所有 text 區塊的文字，連同 stop_reason 一起回傳"""
    parts = [
        getattr(block, "text", "")
        for block in (getattr(message, "content", None) or [])
        if getattr(block, "type", None) == "text"
    ]
    return "".join(parts), getattr(message, "stop_reason", None)


def accepts_sampling_params(model: str) -> bool:
    return not model.startswith(SAMPLING_UNSUPPORTED_PREFIXES)
