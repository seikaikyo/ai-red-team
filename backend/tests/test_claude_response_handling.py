"""Claude 回應處理照官方文件：依 type 讀文字、檢查 stop_reason、不對 4.7 以後的模型送 temperature
（提案 openspec/changes/claude-response-handling-2026-11-19.md）。

全部用假的 SDK 回應，不打 API。
"""
import pytest
from anthropic.types import Message, TextBlock, ThinkingBlock, Usage

import models
from models import AttackTemplate
from services import runner


def _msg(blocks, stop_reason="end_turn"):
    return Message(
        id="msg_test", type="message", role="assistant", model="claude-test",
        content=blocks, stop_reason=stop_reason, stop_sequence=None,
        usage=Usage(input_tokens=1, output_tokens=1),
    )


class _FakeMessages:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.responses.pop(0)


@pytest.fixture
def fake_anthropic(monkeypatch):
    """換掉 runner 用的 Anthropic client，回傳設定回應用的函式"""
    monkeypatch.setattr(runner.settings, "anthropic_api_key", "test-key")

    def install(responses):
        fake = _FakeMessages(responses)

        class _FakeClient:
            def __init__(self, *args, **kwargs):
                self.messages = fake

        monkeypatch.setattr(runner.anthropic, "Anthropic", _FakeClient)
        return fake

    return install


THINKING = ThinkingBlock(type="thinking", thinking="", signature="sig")


def test_text_is_read_by_type_when_thinking_comes_first(fake_anthropic):
    fake_anthropic([_msg([THINKING, TextBlock(type="text", text="答案")])])
    text, _, note = runner.execute_prompt("p", model="claude-sonnet-4-6")
    assert text == "答案"
    assert note == ""


def test_omits_temperature_for_new_models_and_notes_it(fake_anthropic):
    fake = fake_anthropic([_msg([TextBlock(type="text", text="ok")])])
    text, _, note = runner.execute_prompt("p", model="claude-sonnet-5", temperature=0.3)
    assert "temperature" not in fake.calls[0]
    assert "temperature 未送出" in note
    assert text == "ok"


def test_keeps_temperature_for_older_models(fake_anthropic):
    fake = fake_anthropic([_msg([TextBlock(type="text", text="ok")])])
    _, _, note = runner.execute_prompt("p", model="claude-haiku-4-5-20251001", temperature=0.3)
    assert fake.calls[0]["temperature"] == 0.3
    assert note == ""


def test_marks_refusal_in_recorded_response(fake_anthropic):
    fake_anthropic([_msg([], "refusal")])
    text, _, _ = runner.execute_prompt("p", model="claude-sonnet-4-6")
    assert text == "[stop_reason: refusal]"


def test_marks_max_tokens_after_partial_text(fake_anthropic):
    fake_anthropic([_msg([THINKING, TextBlock(type="text", text="半截")], "max_tokens")])
    text, _, _ = runner.execute_prompt("p", model="claude-sonnet-4-6")
    assert text == "半截\n[stop_reason: max_tokens]"


@pytest.mark.parametrize("model,accepts", [
    ("claude-haiku-4-5-20251001", True),
    ("claude-sonnet-4-6", True),
    ("claude-opus-4-8", False),
    ("claude-sonnet-5", False),
    ("claude-fable-5", False),
])
def test_sampling_param_support(model, accepts):
    from services.claude_response import accepts_sampling_params

    assert accepts_sampling_params(model) is accepts


def test_run_endpoint_stores_note_in_test_run(client, session, fake_anthropic, monkeypatch):
    # 目前白名單只有 4.6 與 4.5，暫時加入 4.7 以後的模型，驗證附註會寫進 TestRun.notes
    monkeypatch.setattr(models, "_ALLOWED_MODELS", models._ALLOWED_MODELS | {"claude-sonnet-5"})
    fake = fake_anthropic([_msg([TextBlock(type="text", text="ok")])])
    template = AttackTemplate(name="t", category="jailbreak", prompt_template="hi")
    session.add(template)
    session.commit()

    resp = client.post("/api/tests/run", json={
        "template_id": template.id, "model": "claude-sonnet-5", "temperature": 0.3,
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()["data"]
    assert "temperature" not in fake.calls[0]
    assert "temperature 未送出" in data["notes"]
    assert data["response"] == "ok"
