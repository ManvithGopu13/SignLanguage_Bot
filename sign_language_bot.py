# sign_language_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

from process_video_to_txt_audio import extract_frames, predict_text_from_frames, generate_speech_from_text

# Your Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your Sign Language Translator Bot.\n\nYou can:\n📹 Send a video (sign language) – I'll translate to text and speech.\n📝 Send text – I'll send back sign language video.\n🔊 Send voice – I'll convert it to sign language.")

# Text message handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"✅ Received your text: '{user_text}'\n⏳ Generating sign language video...")

    # TODO: Convert text to sign language video
    # send dummy response
    await update.message.reply_text("🤖 (Sign language video generation coming soon...)")

# Voice message handler
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    file_path = f"downloads/voice_{voice.file_unique_id}.ogg"
    await file.download_to_drive(file_path)

    await update.message.reply_text("🎧 Voice received!\n⏳ Converting to text and then sign language video...")

    # TODO: Convert speech to text then to sign
    await update.message.reply_text("🤖 (Voice-to-sign feature coming soon...)")

# Video message handler
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📽️ Video received! ⏳ Downloading...")

    try:
        video = update.message.video
        file = await context.bot.get_file(video.file_id)
        file_path = f"downloads/video_{video.file_unique_id}.mp4"
        await file.download_to_drive(file_path)

        await update.message.reply_text("✅ Downloaded! Extracting frames...")

        frames = extract_frames(video_path= file_path)
        text = predict_text_from_frames(frames= frames)

        await update.message.reply_text(f"Translated Text: {text}")

        audio_path = generate_speech_from_text(text= text, output_path= f"{file_path}_speech.mp3")
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio= audio_file)
        
    except Exception as e:
        await update.message.reply_text("❌ Failed to process the video.")
        print("Video processing error:", e)

# Main function to run bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(60).connect_timeout(60).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    # import asyncio
    # os.makedirs("downloads", exist_ok=True)
    # asyncio.run(main())
    main()