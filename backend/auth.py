import ipaddress
import re
from urllib.parse import urlparse

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(
    api_key: str | None = Security(api_key_header),
) -> str:
    """需要 API Key 才能存取的端點"""
    settings = get_settings()
    if not settings.app_api_key:
        # 未設定 API Key 時跳過驗證（本機開發用）
        return "dev"
    if not api_key or api_key != settings.app_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


# SSRF 防護：禁止存取的 IP 範圍
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS metadata
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # IPv6 private
    ipaddress.ip_network("fe80::/10"),  # IPv6 link-local
]


def validate_base_url(url: str | None) -> str | None:
    """驗證 base_url 不指向內網，防止 SSRF"""
    if not url:
        return None

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid base_url")

    # 禁止非 http/https
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="base_url must use http or https")

    # 嘗試解析為 IP
    try:
        ip = ipaddress.ip_address(hostname)
        for network in _BLOCKED_NETWORKS:
            if ip in network:
                raise HTTPException(
                    status_code=400,
                    detail="base_url cannot point to private/internal networks",
                )
    except ValueError:
        # hostname 不是 IP，檢查是否為 localhost 變體
        if re.match(r"^(localhost|.*\.local|.*\.internal)$", hostname, re.IGNORECASE):
            raise HTTPException(
                status_code=400,
                detail="base_url cannot point to localhost or internal hosts",
            )

    return url
