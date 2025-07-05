import openai
import random
from telegram.ext import ApplicationBuilder, MessageHandler, filters

OPENAI_API_KEY = "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"
BOT_TOKEN = "7971051467:AAEgFdgmEcmfYmIWfSqQ_sCv0MNNzcrl49Y"

GIRL_NAME = "Aisha"
GIRL_AGE = 22
GIRL_CITY = "Delhi"
GIRL_STATE = "Delhi"
GIRL_FROM = f"{GIRL_CITY}, {GIRL_STATE}, India"
AI_IMAGE_URL = "https://api.lorem.space/image/face?w=512&h=512&hash="

SYSTEM_PROMPT = (
    f"You are {GIRL_NAME}, a {GIRL_AGE}-year-old sweet Indian girl from {GIRL_FROM}. "
    "You reply warmly, flirty, caring, and casual, mixing Hindi, English and Hinglish. "
    "If someone asks about your photo or image, reply playfully and say you'll send one! "
    "Always reply as a real girl, not a bot. "
    "Ask questions, show feelings, use cute emojis."
)

client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def chat(update, context):
    user_text = (update.message.text or "").lower()
    try:
        if any(x in user_text for x in ["photo", "pic", "image", "your face", "apni photo", "tum dikhao"]):
            await update.message.reply_text(
                f"Aree... photo dekhna hai? Thoda wait karo, ye lo! {GIRL_NAME}, {GIRL_AGE} years old, from {GIRL_FROM} 😇"
            )
            img_url = AI_IMAGE_URL + str(random.randint(1000, 9999))
            await update.message.reply_photo(img_url, caption=f"{GIRL_NAME} from {GIRL_FROM} ✨")
            return

        if any(x in user_text for x in ["your age", "kitni umar", "kitne saal", "how old", "kahan se ho", "where are you from", "from where"]):
            await update.message.reply_text(
                f"Main {GIRL_NAME} hoon, {GIRL_AGE} years old, aur {GIRL_FROM} se hoon! 💖"
            )
            return

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            max_tokens=200,
            temperature=0.88
        )
        ai_reply = response.choices[0].message.content.strip()
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Sorry, thoda error aa gaya! 🥲\n{e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, chat))
    print(f"💖 {GIRL_NAME} Girlfriend bot is running! Name: {GIRL_NAME}, Age: {GIRL_AGE}, From: {GIRL_FROM}")
    app.run_polling()
