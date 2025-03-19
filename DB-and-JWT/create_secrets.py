import secrets

SECRET_KEY = secrets.token_urlsafe(32)

print(SECRET_KEY)

# 為什麼選擇 32 => 32 個字節提供了 256 位的隨機性
# 這樣的長度被認為是非常安全的，足夠用來作為密鑰來簽署和驗證 JWT