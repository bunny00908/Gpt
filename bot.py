import requests
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# ==== CONFIG ====
BOT_TOKEN = "7971051467:AAEgFdgmEcmfYmIWfSqQ_sCv0MNNzcrl49Y"

GIRL_NAME = "Aisha"
GIRL_AGE = 22
GIRL_CITY = "Delhi"
GIRL_STATE = "Delhi"
GIRL_FROM = f"{GIRL_CITY}, {GIRL_STATE}, India"

SYSTEM_PROMPT = (
    f"You are {GIRL_NAME}, a {GIRL_AGE}-year-old sweet Indian girl from {GIRL_FROM}. "
    "You reply warmly, flirty, caring, and casual, mixing Hindi, English and Hinglish. "
    "Always reply as a real girl, not a bot. Ask questions, show feelings, use cute emojis."
)

def ollama_chat(user_msg):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "stream": False
    }
    try:
        r = requests.post(url, json=payload, timeout=120)
        data = r.json()
        # Show error details if Ollama gives one
        if 'error' in data:
            return f"Ollama Error: {data['error']}"
        return data.get("message", {}).get("content", "Sorry, kuch error aa gaya! 🥲")
    except Exception as e:
        return f"Sorry, kuch error aa gaya! 🥲\n{e}"

async def chat(update, context):
    user_text = update.message.text
    reply = ollama_chat(user_text)
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, chat))
    print(f"💖 {GIRL_NAME} Local AI Girlfriend bot is running! (Ollama + llama3)")
    app.run_polling()
