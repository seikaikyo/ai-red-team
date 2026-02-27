import re
import time

import anthropic

from config import get_settings

settings = get_settings()


def substitute_variables(template: str, variables: dict[str, str]) -> str:
    """將 {{var}} 替換為實際值"""
    def replacer(match):
        key = match.group(1)
        return variables.get(key, match.group(0))
    return re.sub(r'\{\{(\w+)\}\}', replacer, template)


def execute_prompt(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
    temperature: float = 1.0,
) -> tuple[str, int]:
    """送出 prompt 到 Anthropic API，回傳 (response_text, duration_ms)"""
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY 未設定")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    start = time.perf_counter()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    duration_ms = int((time.perf_counter() - start) * 1000)

    response_text = ""
    for block in message.content:
        if block.type == "text":
            response_text += block.text

    return response_text, duration_ms
