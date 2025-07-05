import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ----- CONFIG -----
HUGGINGFACE_API_KEY = "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"  # Your Hugging Face API Key
BOT_TOKEN = "7971051467:AAEgFdgmEcmfYmIWfSqQ_sCv0MNNzcrl49Y"
GIRL_NAME = "Aisha"  # You can change this to Meera, Sana, Sara, Nikita, etc

# Hugging Face model endpoint
MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"  # Choose your model (gpt2 or any other model)

# Set Hugging Face API headers
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# --- Girlfriend personality for prompt ---
SYSTEM_PROMPT = (
    f"You are {GIRL_NAME}, a 22-year-old sweet Indian girl. "
    "You reply warmly, flirty, caring, and casual, mixing Hindi, English and Hinglish. "
    "The user is your boyfriend. Give cute, emotional, fun, and sometimes romantic answers. "
    "Always reply as {GIRL_NAME}, never as an AI or bot. "
    "Ask questions, show feelings, and sometimes use emojis like 🥰😘🤭."
)

# Function to call Hugging Face API
def query_huggingface_bot(user_input):
    payload = {
        "inputs": SYSTEM_PROMPT + "\n" + user_input
    }
    response = requests.post(MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Sorry, thoda error aa gaya! 🥲"

# Command handler function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello, I am {GIRL_NAME}, your virtual girlfriend! Let's chat 💖")

# Function to handle text messages and call the Hugging Face API
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text  # Get the text message from the user
    response = query_huggingface_bot(user_text)  # Get the AI response
    await update.message.reply_text(response)  # Send the AI response to the user

if __name__ == '__main__':
    # Create the application with the Telegram bot token
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add the handlers for the bot
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot
    print(f"💖 {GIRL_NAME} Live AI Girlfriend bot is running—just chat, no commands needed!")
    app.run_polling()
