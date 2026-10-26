# Enchanted Pages Telegram integration

This integration lets each Encrypted Diary user connect one Telegram account. Users send `/link CODE` to the bot to link their account, then use `/save Title | entry text` or reply to a text message with `/save`. Saved messages are encrypted in a staging queue and are only moved into a diary after the user unlocks that diary and imports the selected entries. Imported titles and content are encrypted with the diary's existing Fernet key. Existing diary and entry tables are unchanged; two Telegram-specific tables are created by `init_db()`.

## 1. Rotate the exposed bot token

The token pasted in chat should be considered compromised. Revoke it through `@BotFather`, generate a replacement, and use only the replacement in your environment. Never commit the token or put it in browser JavaScript.

## 2. Install and configure

Install dependencies:

```bash
pip install -r requirements.txt
```

Set these environment variables in local development and in your Vercel project settings:

- `DATABASE_URL`: existing PostgreSQL/Neon connection string
- `SECRET_KEY`: a strong, stable random secret. Keep it unchanged; it protects Flask sessions, unlocked diary keys, and staged Telegram messages.
- `TELEGRAM_BOT_TOKEN`: the regenerated token from BotFather
- `TELEGRAM_WEBHOOK_SECRET`: a random string of at least 16 characters, using letters, numbers, underscores, or hyphens

For local development, `APP_BASE_URL` can be `http://127.0.0.1:5000` only if Telegram can reach that URL publicly; localhost itself will not work as a webhook. Use your deployed HTTPS URL or a temporary HTTPS tunnel for local testing.

## 3. Deploy and register the webhook

Deploy the Flask application first so `/telegram/webhook` is reachable over HTTPS. Then, in a terminal with `APP_BASE_URL`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_WEBHOOK_SECRET` set, run:

```bash
python set_telegram_webhook.py
```

Set `APP_BASE_URL` to the public base URL of the deployed app, with no trailing slash. The script registers `https://YOUR_APP/telegram/webhook` with Telegram and sets the webhook secret header used by the app. Do not share the output if it contains operational details.

## 4. User workflow

1. Register or log in to Encrypted Diary.
2. Open **Telegram Import** and generate a one-time connection code.
3. Open `https://t.me/EnchantedPagesBot` and send `/link YOUR_CODE` within 10 minutes.
4. Send `/save A quiet evening | Today was peaceful.` to save an entry, or reply to a text message with `/save`.
5. In Encrypted Diary, open and unlock the target diary, then click **Import Telegram**.
6. Select entries and import. The imported content is encrypted using the selected diary's key and the staging item is marked as imported.

Useful bot commands: `/start`, `/help`, `/link CODE`, `/save`, `/saved`, `/unlink`.

## Notes

- The bot only sees messages users send to it, or text messages they reply to with `/save`. It cannot read personal Telegram chat history.
- Telegram linking is per Encrypted Diary user. A Telegram account can be linked to only one Encrypted Diary account at a time.
- Staging payloads are encrypted with the app's `SECRET_KEY`; imported entries are encrypted with the diary key.
- Keep `SECRET_KEY` stable across deploys. Rotating it makes pending staged messages unreadable and invalidates existing protected unlock keys/sessions.
- The webhook route fails closed if `TELEGRAM_WEBHOOK_SECRET` is absent or the Telegram secret header does not match.
