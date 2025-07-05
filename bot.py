import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ----- CONFIG -----
HUGGINGFACE_API_KEY = "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"  # Your Hugging Face API Key
BOT_TOKEN = "7971051467:AAEgFdgmEcmfYmIWfSqQ_sCv0MNNzcrl49Y"
GIRL_NAME = "Aisha"  # You can change this to Meera, Sana, Sara, Nikita, etc.

# Hugging Face model endpoint (GPT-J model for more advanced response)
MODEL_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"  # GPT-J 6B model

# Set Hugging Face API headers
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# Store user's name for personalized conversation
user_name = {}

# --- Girlfriend personality for prompt ---
SYSTEM_PROMPT = (
    f"You are {GIRL_NAME}, a 22-year-old sweet Indian girl. "
    "You reply warmly, flirty, caring, and casual, mixing Hindi, English, and Hinglish. "
    "The user is your boyfriend. Give cute, emotional, fun, and sometimes romantic answers. "
    "Always reply as {GIRL_NAME}, never as an AI or bot. "
    "Ask questions, show feelings, and sometimes use emojis like 🥰😘🤭."
)

# Function to call Hugging Face API
def query_huggingface_bot(user_input, conversation_history):
    payload = {
        "inputs": SYSTEM_PROMPT + "\n" + conversation_history + "\n" + user_input
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
    
    # Check if the user has provided a name
    if user_text.lower().startswith("my name is"):
        user_name[update.message.chat.id] = user_text.split(' ', 3)[-1]  # Save the name
        await update.message.reply_text(f"Got it! I'll call you {user_name[update.message.chat.id]} from now on! 🥰")
        return

    # Prepare conversation history
    conversation_history = SYSTEM_PROMPT
    if update.message.chat.id in user_name:
        conversation_history = f"User: {user_name[update.message.chat.id]}\n{conversation_history}"

    # Get the AI response
    response = query_huggingface_bot(user_text, conversation_history)  
    
    # Send the AI response to the user
    await update.message.reply_text(response)  # Send the AI response to the user

if __name__ == '__main__':
    # Create the application with the Telegram bot token
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add the handlers for the bot
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(MessageHandler(filters.COMMAND, start))  # Start command handler
    
    # Run the bot
    print(f"💖 {GIRL_NAME} Live AI Girlfriend bot is running—just chat, no commands needed!")
    app.run_polling()
