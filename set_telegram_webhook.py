import os
import secrets
import requests

base_url = os.getenv("APP_BASE_URL", "").strip().rstrip("/")
token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "").strip()

if not base_url or not token or not secret:
    raise SystemExit("Set APP_BASE_URL, TELEGRAM_BOT_TOKEN, and TELEGRAM_WEBHOOK_SECRET first.")
if len(secret) < 16:
    raise SystemExit("TELEGRAM_WEBHOOK_SECRET should be at least 16 characters long.")

response = requests.post(
    f"https://api.telegram.org/bot{token}/setWebhook",
    json={
        "url": f"{base_url}/telegram/webhook",
        "secret_token": secret,
        "allowed_updates": ["message", "edited_message"],
        "drop_pending_updates": False,
    },
    timeout=20,
)
response.raise_for_status()
print(response.json())
