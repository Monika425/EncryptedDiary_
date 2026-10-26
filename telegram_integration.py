import json
import os
from datetime import datetime

import requests
from cryptography.fernet import Fernet, InvalidToken

from crypto import get_master_key
from database import execute, execute_returning, fetch_one


def bot_request(method, data=None):
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")
    response = requests.post(
        f"https://api.telegram.org/bot{token}/{method}",
        json=data or {},
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(result.get("description", "Telegram API request failed."))
    return result.get("result")


def encrypt_staging(value):
    return Fernet(get_master_key()).encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_staging(value):
    return Fernet(get_master_key()).decrypt(value.encode("utf-8")).decode("utf-8")


def send_message(chat_id, text):
    return bot_request("sendMessage", {"chat_id": chat_id, "text": text})


def handle_update(update):
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat_id = message.get("chat", {}).get("id")
    telegram_user_id = message.get("from", {}).get("id")
    text = (message.get("text") or "").strip()
    if not chat_id or not telegram_user_id or not text:
        return

    command, _, args = text.partition(" ")
    command = command.split("@", 1)[0].lower()

    if command == "/start":
        send_message(chat_id, "Welcome to Enchanted Pages!\n\n1. Open Encrypted Diary and connect Telegram.\n2. Copy the one-time code shown there.\n3. Send /link YOUR_CODE here.\n4. Send /save followed by a title, a pipe (|), and your entry text.\n\nExample:\n/save A quiet evening | Today was peaceful.")
        return

    if command == "/help":
        send_message(chat_id, "Commands:\n/link CODE — connect this Telegram account to your Encrypted Diary account.\n/save Title | entry text — securely stage an entry for import.\n/save — when replying to a message, save the replied-to text as an entry.\n/saved — show how many entries are waiting to be imported.\n/unlink — disconnect this Telegram account.")
        return

    if command == "/link":
        code = args.strip().upper()
        if not code:
            send_message(chat_id, "Open Encrypted Diary → Telegram Import to generate a connection code, then send /link YOUR_CODE.")
            return
        row = fetch_one(
            "SELECT user_id, code_expires_at FROM telegram_links WHERE link_code = %s",
            (code,),
        )
        if not row or not row["code_expires_at"] or row["code_expires_at"] <= datetime.utcnow():
            send_message(chat_id, "That connection code is invalid or expired. Generate a new code in Encrypted Diary.")
            return
        execute(
            "UPDATE telegram_links SET telegram_user_id = %s, link_code = NULL, code_expires_at = NULL, linked_at = %s WHERE user_id = %s",
            (telegram_user_id, datetime.utcnow(), row["user_id"]),
        )
        send_message(chat_id, "Connected successfully! Messages you save with /save will be available only to the Encrypted Diary account you linked.")
        return

    if command == "/unlink":
        row = fetch_one("SELECT user_id FROM telegram_links WHERE telegram_user_id = %s", (telegram_user_id,))
        if not row:
            send_message(chat_id, "This Telegram account is not linked to Encrypted Diary.")
            return
        execute(
            "UPDATE telegram_links SET telegram_user_id = NULL, linked_at = NULL, link_code = NULL, code_expires_at = NULL WHERE telegram_user_id = %s",
            (telegram_user_id,),
        )
        send_message(chat_id, "Telegram has been disconnected from Encrypted Diary. Your previously saved entries remain in your diary import queue.")
        return

    if command == "/saved":
        row = fetch_one("SELECT id FROM telegram_links WHERE telegram_user_id = %s", (telegram_user_id,))
        if not row:
            send_message(chat_id, "Connect your account first from Encrypted Diary → Telegram Import.")
            return
        count = fetch_one("SELECT COUNT(*) AS total FROM telegram_saved WHERE user_id = %s AND imported_at IS NULL", (row["user_id"],))
        send_message(chat_id, f"You have {int(count['total'])} saved entr{'y' if int(count['total']) == 1 else 'ies'} waiting to import into your diary.")
        return

    if command == "/save":
        row = fetch_one("SELECT user_id FROM telegram_links WHERE telegram_user_id = %s", (telegram_user_id,))
        if not row:
            send_message(chat_id, "Connect your account first: open Encrypted Diary → Telegram Import, copy the code, then send /link YOUR_CODE.")
            return
        payload = args.strip()
        if not payload and message.get("reply_to_message"):
            payload = (message["reply_to_message"].get("text") or "").strip()
        if "|" in payload:
            title, content = payload.split("|", 1)
            title, content = title.strip(), content.strip()
        else:
            title, content = "Telegram Memory", payload
        if not content:
            send_message(chat_id, "Use /save Title | your entry text. You can also reply to a text message with /save.")
            return
        if len(title) > 200:
            title = title[:200]
        if len(content) > 20000:
            send_message(chat_id, "That entry is too long. Please keep each entry under 20,000 characters.")
            return
        payload_json = json.dumps({"title": title or "Telegram Memory", "content": content}, ensure_ascii=False)
        execute(
            "INSERT INTO telegram_saved (user_id, telegram_user_id, encrypted_payload, created_at) VALUES (%s, %s, %s, %s)",
            (row["user_id"], telegram_user_id, encrypt_staging(payload_json), datetime.utcnow()),
        )
        send_message(chat_id, "Saved securely to your import queue. Open Encrypted Diary → Telegram Import to choose a diary and encrypt it into your journal.")
        return

    if not text.startswith("/"):
        row = fetch_one("SELECT user_id FROM telegram_links WHERE telegram_user_id = %s", (telegram_user_id,))
        if row:
            send_message(chat_id, "Want to keep this in your diary? Send /save Title | your message, or reply to this message with /save.")
        else:
            send_message(chat_id, "Welcome! Link your account from Encrypted Diary → Telegram Import, then use /save to stage entries.")
