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
        # 跳過驗證必須是顯式決定。用資料庫種類推測執行環境會讓正式部署
        # 在金鑰被清空時靜默全開。
        if settings.allow_insecure_auth:
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
    ipaddress.ip_network("100.64.0.0/10"),  # CGNAT
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # IPv6 private
    ipaddress.ip_network("fe80::/10"),  # IPv6 link-local
]


def _normalize_ip(
    ip: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    """IPv4-mapped IPv6（::ffff:127.0.0.1）還原成 IPv4。

    ipaddress 對跨版本的比對一律回 False，不還原就會讓 ::ffff:169.254.169.254
    這類位址整份繞過封鎖清單。
    """
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        return ip.ipv4_mapped
    return ip


def _is_private_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """檢查 IP 是否在封鎖的內網範圍內"""
    ip = _normalize_ip(ip)
    # is_global 涵蓋私網、loopback、link-local 與其他保留網段，
    # 下面的清單是明列的第二道，兩者取聯集。
    if not ip.is_global:
        return True
    return any(ip.version == net.version and ip in net for net in _BLOCKED_NETWORKS)


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

    # 本機開發指向自架 LLM 時才放行私網目標，正式部署維持封鎖
    if get_settings().allow_private_base_url:
        return url

    # 禁止 localhost 變體
    if re.match(r"^(localhost|.*\.local|.*\.internal)$", hostname, re.IGNORECASE):
        raise HTTPException(
            status_code=400,
            detail="base_url cannot point to localhost or internal hosts",
        )

    # DNS 解析後驗證所有回傳的 IP（防止 DNS rebinding）
    default_port = 443 if parsed.scheme == "https" else 80
    try:
        addr_infos = socket.getaddrinfo(
            hostname, parsed.port or default_port, proto=socket.IPPROTO_TCP
        )
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="base_url hostname cannot be resolved")

    for _, _, _, _, sockaddr in addr_infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if _is_private_ip(ip):
            raise HTTPException(
                status_code=400,
                detail="base_url cannot point to private/internal networks",
            )

    return url
