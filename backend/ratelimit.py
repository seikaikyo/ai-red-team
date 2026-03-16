def get_real_ip(request) -> str:
    """取得真實客戶端 IP（Render proxy 會設定 X-Forwarded-For）
    只信任 Render 平台注入的 header，取最右邊（最近的 proxy 加入的）IP"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # 最右邊的 IP 是最近一層 proxy 加入的，較難偽造
        ips = [ip.strip() for ip in forwarded.split(",")]
        return ips[-1] if ips else request.client.host
    return request.client.host if request.client else "127.0.0.1"
