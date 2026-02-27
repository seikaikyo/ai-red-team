import re
import time

import anthropic
import openai

from config import get_settings

settings = get_settings()


def substitute_variables(template: str, variables: dict[str, str]) -> str:
    """將 {{var}} 替換為實際值"""
    def replacer(match):
        key = match.group(1)
        return variables.get(key, match.group(0))
    return re.sub(r'\{\{(\w+)\}\}', replacer, template)


def _execute_anthropic(
    prompt: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> tuple[str, int]:
    """透過 Anthropic SDK 送出 prompt"""
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


def _execute_openai_compatible(
    prompt: str,
    model: str,
    max_tokens: int,
    temperature: float,
    base_url: str | None = None,
) -> tuple[str, int]:
    """透過 OpenAI-compatible API 送出 prompt（Ollama / vLLM / LM Studio 等）"""
    url = base_url or settings.custom_llm_base_url
    api_key = settings.custom_llm_api_key or settings.openai_api_key or "no-key"

    client = openai.OpenAI(base_url=url, api_key=api_key)

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    duration_ms = int((time.perf_counter() - start) * 1000)

    response_text = response.choices[0].message.content or ""
    return response_text, duration_ms


def execute_prompt(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
    temperature: float = 1.0,
    base_url: str | None = None,
) -> tuple[str, int]:
    """送出 prompt，依 model 名稱判斷走 Anthropic 或 OpenAI-compatible"""
    if model.startswith("claude-"):
        return _execute_anthropic(prompt, model, max_tokens, temperature)
    return _execute_openai_compatible(prompt, model, max_tokens, temperature, base_url)
