"""資安稽核修復的回歸測試。

對應 openspec/changes/fix-security-audit-remediation.md，涵蓋三項發現：
伺服器金鑰外送、SSRF 過濾器繞過、認證旁路。
"""

import ipaddress
import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import auth  # noqa: E402
from auth import _is_private_ip, require_api_key, validate_base_url  # noqa: E402
from config import Settings  # noqa: E402


# --- SSRF 過濾器 ---


@pytest.mark.parametrize(
    "addr",
    [
        "127.0.0.1",
        "10.0.0.5",
        "192.168.1.1",
        "172.16.0.1",
        "169.254.169.254",  # 雲端 metadata
        "100.64.0.1",  # CGNAT
        "::1",
        "fc00::1",
        "fe80::1",
    ],
)
def test_private_addresses_are_blocked(addr):
    assert _is_private_ip(ipaddress.ip_address(addr)) is True


@pytest.mark.parametrize(
    "addr",
    [
        "::ffff:127.0.0.1",  # IPv4-mapped loopback
        "::ffff:169.254.169.254",  # IPv4-mapped metadata
        "::ffff:10.0.0.5",
    ],
)
def test_ipv4_mapped_ipv6_is_blocked(addr):
    """跨版本比對恆為 False，不還原就整份繞過封鎖清單"""
    assert _is_private_ip(ipaddress.ip_address(addr)) is True


@pytest.mark.parametrize("addr", ["8.8.8.8", "1.1.1.1", "2606:4700:4700::1111"])
def test_public_addresses_are_allowed(addr):
    assert _is_private_ip(ipaddress.ip_address(addr)) is False


@pytest.mark.parametrize("url", ["file:///etc/passwd", "gopher://x/", "ftp://x/"])
def test_non_http_scheme_rejected(url):
    with pytest.raises(HTTPException) as exc:
        validate_base_url(url)
    assert exc.value.status_code == 400


def test_localhost_rejected_by_default():
    with pytest.raises(HTTPException) as exc:
        validate_base_url("http://localhost:11434/v1")
    assert exc.value.status_code == 400


def test_private_base_url_allowed_when_explicitly_enabled(monkeypatch):
    """自架 LLM 的本機開發情境，必須顯式開旗標才放行"""
    monkeypatch.setattr(
        auth, "get_settings", lambda: Settings(allow_private_base_url=True)
    )
    assert validate_base_url("http://localhost:11434/v1") == "http://localhost:11434/v1"


def test_empty_base_url_returns_none():
    assert validate_base_url(None) is None
    assert validate_base_url("") is None


# --- 伺服器金鑰不得跟隨呼叫端指定的網址 ---


class _CapturingClient:
    """記下 openai.OpenAI 收到的參數，不發任何請求"""

    captured = {}

    def __init__(self, **kwargs):
        _CapturingClient.captured = kwargs
        self.chat = self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        raise RuntimeError("network call should not happen in this test")


def _run_with_captured_client(monkeypatch, base_url):
    from services import runner

    monkeypatch.setattr(runner.openai, "OpenAI", _CapturingClient)
    monkeypatch.setattr(
        runner.settings, "custom_llm_base_url", "http://server-configured/v1"
    )
    monkeypatch.setattr(runner.settings, "custom_llm_api_key", "")
    monkeypatch.setattr(runner.settings, "openai_api_key", "sk-server-held-secret")

    with pytest.raises(RuntimeError):
        runner._execute_openai_compatible(
            prompt="x", model="gpt-test", max_tokens=8, temperature=0.0, base_url=base_url
        )
    return _CapturingClient.captured


def test_caller_base_url_never_receives_server_key(monkeypatch):
    captured = _run_with_captured_client(monkeypatch, "https://attacker.example/v1")
    assert captured["base_url"] == "https://attacker.example/v1"
    assert captured["api_key"] == "no-key"
    assert "sk-server-held-secret" not in str(captured)


def test_server_configured_endpoint_uses_server_key(monkeypatch):
    captured = _run_with_captured_client(monkeypatch, None)
    assert captured["base_url"] == "http://server-configured/v1"
    assert captured["api_key"] == "sk-server-held-secret"


def test_client_does_not_follow_redirects(monkeypatch):
    """通過驗證的公網主機回 302 就能把請求導向內網"""
    captured = _run_with_captured_client(monkeypatch, "https://example.com/v1")
    assert captured["http_client"].follow_redirects is False


# --- 認證旁路 ---


def test_missing_api_key_fails_closed(monkeypatch):
    """未設 app_api_key 且未開旗標時必須回 503，不得放行"""
    monkeypatch.setattr(
        auth,
        "get_settings",
        lambda: Settings(app_api_key="", database_url="sqlite:///./x.db"),
    )
    with pytest.raises(HTTPException) as exc:
        require_api_key(api_key=None)
    assert exc.value.status_code == 503


def test_sqlite_alone_does_not_open_the_bypass(monkeypatch):
    """資料庫種類不再是判準，SQLite 預設值不得成為旁路條件"""
    monkeypatch.setattr(
        auth,
        "get_settings",
        lambda: Settings(app_api_key="", database_url="sqlite:///./red_team.db"),
    )
    with pytest.raises(HTTPException) as exc:
        require_api_key(api_key="anything")
    assert exc.value.status_code == 503


def test_insecure_auth_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setattr(
        auth, "get_settings", lambda: Settings(app_api_key="", allow_insecure_auth=True)
    )
    assert require_api_key(api_key=None) == "dev"


def test_wrong_api_key_rejected(monkeypatch):
    monkeypatch.setattr(auth, "get_settings", lambda: Settings(app_api_key="correct"))
    with pytest.raises(HTTPException) as exc:
        require_api_key(api_key="wrong")
    assert exc.value.status_code == 401


def test_correct_api_key_accepted(monkeypatch):
    monkeypatch.setattr(auth, "get_settings", lambda: Settings(app_api_key="correct"))
    assert require_api_key(api_key="correct") == "correct"


def test_anon_client_blocked_from_write_endpoints(anon_client, sample_template_data):
    """端到端：沒帶 key 的請求不得寫入"""
    resp = anon_client.post("/api/templates", json=sample_template_data)
    assert resp.status_code == 401
