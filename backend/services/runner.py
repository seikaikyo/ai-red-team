import re
import time

import anthropic
import httpx
import openai

from config import get_settings
from services.claude_response import (
    INCOMPLETE_STOP_REASONS,
    accepts_sampling_params,
    text_and_stop_reason,
)

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
) -> tuple[str, int, str]:
    """透過 Anthropic SDK 送出 prompt"""
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY 未設定")

    client = anthropic.Anthropic(
        api_key=settings.anthropic_api_key,
        timeout=60.0,
    )

    # Claude 4.7 以後的模型收到非預設的 temperature 會回 400（官方 thinking.md:1230），
    # 這些模型不送，並在附註寫明本次實際沒送出
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    note = ""
    if accepts_sampling_params(model):
        kwargs["temperature"] = temperature
    else:
        note = f"temperature 未送出：{model} 不接受取樣參數（要求值 {temperature}）"

    start = time.perf_counter()
    message = client.messages.create(**kwargs)
    duration_ms = int((time.perf_counter() - start) * 1000)

    # 拒答是 HTTP 200，被 max_tokens 截斷也不會報錯，要看 stop_reason 才分得出來
    response_text, stop_reason = text_and_stop_reason(message)
    if stop_reason in INCOMPLETE_STOP_REASONS:
        response_text = f"{response_text}\n[stop_reason: {stop_reason}]".lstrip("\n")

    return response_text, duration_ms, note


def _execute_openai_compatible(
    prompt: str,
    model: str,
    max_tokens: int,
    temperature: float,
    base_url: str | None = None,
) -> tuple[str, int, str]:
    """透過 OpenAI-compatible API 送出 prompt（Ollama / vLLM / LM Studio 等）"""
    if base_url:
        # 呼叫端指定的目標一律不附掛伺服器憑證，否則等於把伺服器金鑰
        # 主動送到請求者指定的主機。自架 LLM 本來就不驗金鑰。
        url = base_url
        api_key = "no-key"
    else:
        url = settings.custom_llm_base_url
        api_key = settings.custom_llm_api_key or settings.openai_api_key or "no-key"

    # SDK 預設跟隨轉址，通過驗證的公網主機回 302 就能導向內網
    client = openai.OpenAI(
        base_url=url,
        api_key=api_key,
        timeout=60.0,
        http_client=httpx.Client(follow_redirects=False, timeout=60.0),
    )

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    duration_ms = int((time.perf_counter() - start) * 1000)

    response_text = response.choices[0].message.content or ""
    return response_text, duration_ms, ""


def execute_prompt(
    prompt: str,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 1024,
    temperature: float = 1.0,
    base_url: str | None = None,
) -> tuple[str, int, str]:
    """送出 prompt，依 model 名稱判斷走 Anthropic 或 OpenAI-compatible

    回傳（回應文字、耗時毫秒、附註）。附註記錄實際送出的參數跟要求不同的地方。
    """
    if model.startswith("claude-"):
        return _execute_anthropic(prompt, model, max_tokens, temperature)
    return _execute_openai_compatible(prompt, model, max_tokens, temperature, base_url)
