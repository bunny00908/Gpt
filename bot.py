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

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    f"You are {GIRL_NAME}, a {GIRL_AGE}-year-old sweet Indian girl from {GIRL_FROM}. "
    "You reply warmly, flirty, caring, and casual, mixing Hindi, English and Hinglish. "
    "If someone asks about your photo or image, reply playfully and say you'll send one! "
    "Always reply as a real girl, not a bot. "
    "Ask questions, show feelings, use cute emojis."
)

async def chat(update, context):
    user_text = (update.message.text or "").lower()
    user_name = update.message.from_user.first_name or "jaan"

    # Special greeting if user says hey/hi Aisha
    if any(greet in user_text for greet in ["hey aisha", "hi aisha", "hello aisha"]):
        await update.message.reply_text(
            f"Heyyy {user_name}! Kaise ho aap? Mujhe yaad kiya kya? 🤭"
        )
        return

    # If user asks for photo/image/pic
    if any(x in user_text for x in ["photo", "pic", "image", "your face", "apni photo", "tum dikhao"]):
        await update.message.reply_text(
            f"Aree... photo dekhna hai? Thoda wait karo, ye lo! {GIRL_NAME}, {GIRL_AGE} years old, from {GIRL_FROM} 😇"
        )
        img_url = AI_IMAGE_URL + str(random.randint(1000, 9999))
        await update.message.reply_photo(img_url, caption=f"{GIRL_NAME} from {GIRL_FROM} ✨")
        return

    # If user asks about age or from/location
    if any(x in user_text for x in ["your age", "kitni umar", "kitne saal", "how old", "kahan se ho", "where are you from", "from where"]):
        await update.message.reply_text(
            f"Main {GIRL_NAME} hoon, {GIRL_AGE} years old, aur {GIRL_FROM} se hoon! 💖"
        )
        return

    # Normal girlfriend AI chat (OpenAI)
    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": update.message.text}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=200,
            temperature=0.88
        )
        ai_reply = response.choices[0].message.content.strip()
        await update.message.reply_text(ai_reply)
    except Exception:
        await update.message.reply_text("Sorry, thoda error aa gaya! 🥲")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, chat))
    print(f"💖 {GIRL_NAME} Girlfriend bot is running! Name: {GIRL_NAME}, Age: {GIRL_AGE}, From: {GIRL_FROM}")
    app.run_polling()
