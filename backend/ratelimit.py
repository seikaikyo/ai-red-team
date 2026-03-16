def get_real_ip(request) -> str:
    """取得真實客戶端 IP（Render proxy 會設定 X-Forwarded-For）"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"
