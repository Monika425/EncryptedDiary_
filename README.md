# Enchanted Pages – Encrypted Diary

## About the Project

Enchanted Pages is a Python-based diary web application where users can create multiple diaries, write personal entries, and keep their content private using passwords and encryption.

I wanted to make a diary application that feels more personal than a regular notes app, so I went with a fantasy-inspired journal design. I also integrated Telegram so users can quickly save their thoughts through a bot and import them into their diaries.

## Features

- User registration and login
- Create and manage multiple diaries
- Password-protected diaries
- Encrypt diary entries using Fernet
- Create, edit, and view entries
- Connect Telegram accounts
- Save notes through the Telegram bot
- Import saved Telegram notes into diaries

## Tech Stack

- Python and Flask
- PostgreSQL and Neon
- HTML, CSS, JavaScript, and Jinja
- Fernet encryption and PBKDF2
- Telegram Bot API
- Vercel for deployment

## How It Works

Users log in, create a diary, and add entries. The entry titles and content are encrypted before being stored in PostgreSQL. Users need to unlock their diaries to access their protected content.

The Telegram bot allows users to link their accounts using a temporary code. They can send notes through commands like `/save`, check pending notes, and import them into a selected diary.

## Project Structure

- `app.py` – Main Flask application and routes
- `crypto.py` – Encryption and decryption
- `database.py` – Database connection and queries
- `telegram_integration.py` – Telegram bot commands and note importing
- `set_telegram_webhook.py` – Telegram webhook setup
- `templates/` – HTML pages
- `static/` – CSS and JavaScript files

## Development Prompts

These are the main prompts I used during development, rewritten to capture the requirements. For these, I'd ask another chat for the proper prompts then copy paste them here.

**1. Building the application**

"Build a Python Flask diary application where users can register, log in, create multiple password-protected diaries, and manage entries. Encrypt diary content before storing it in the database."

**2. Improving the UI**

"Redesign the existing UI to look like an actual diary or journal. Keep the backend, architecture, and existing functionality unchanged."

**3. Fantasy theme**

"Make the theme richer and more polished with a fantasy-inspired journal design, consistent styling, icons, and diary wallpapers."

**4. Telegram integration**

"Integrate a Telegram bot so every registered user can connect their account, save notes through Telegram, view pending notes, and import selected notes into their diaries."

**5. Deployment and setup**

"Help configure the Telegram bot, environment variables, webhook, and deployment while preserving the existing application."

## Future Improvements

I plan to add better input validation, sensible content limits, pagination for large diaries, and additional testing to improve performance and reliability.

## Conclusion

This project combines web development, database management, encryption, and API integration to create a personal digital diary. My main goal was to make it private, easy to use, and convenient for users to save their thoughts whenever they want.
