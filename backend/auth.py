import hmac
import ipaddress
import re
import socket
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
        if settings.database_url.startswith("sqlite"):
            # 本機 SQLite 開發環境允許跳過驗證
            return "dev"
        raise HTTPException(status_code=503, detail="Server misconfigured: API key not set")
    if not api_key or not hmac.compare_digest(api_key, settings.app_api_key):
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


def _is_private_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """檢查 IP 是否在封鎖的內網範圍內"""
    for network in _BLOCKED_NETWORKS:
        if ip in network:
            return True
    return False


def validate_base_url(url: str | None) -> str | None:
    """驗證 base_url 不指向內網，防止 SSRF（含 DNS rebinding 防護）"""
    if not url:
        return None

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid base_url")

    # 禁止非 http/https
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="base_url must use http or https")

    # 禁止 localhost 變體
    if re.match(r"^(localhost|.*\.local|.*\.internal)$", hostname, re.IGNORECASE):
        raise HTTPException(
            status_code=400,
            detail="base_url cannot point to localhost or internal hosts",
        )

    # DNS 解析後驗證所有回傳的 IP（防止 DNS rebinding）
    try:
        addr_infos = socket.getaddrinfo(hostname, parsed.port or 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="base_url hostname cannot be resolved")

    for family, _, _, _, sockaddr in addr_infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if _is_private_ip(ip):
            raise HTTPException(
                status_code=400,
                detail="base_url cannot point to private/internal networks",
            )

    return url
