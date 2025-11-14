from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 *Welcome!*\n\n"
        "Send me any *movie name*, and I'll fetch complete details for you!",
        parse_mode="Markdown"
    )


# Movie search handler
async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()

    if not movie_name:
        await update.message.reply_text("⚠️ Please type a movie name.")
        return

    encoded_name = urllib.parse.quote(movie_name)
    url = f"http://www.omdbapi.com/?t={encoded_name}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url).json()
    except Exception as e:
        await update.message.reply_text("❌ Error connecting to OMDB API. Try again later.")
        return

    if response.get("Response") != "True":
        await update.message.reply_text("❌ Movie not found. Please try another title.")
        return

    title = response.get("Title", "N/A")
    year = response.get("Year", "N/A")
    rating = response.get("imdbRating", "N/A")
    plot = response.get("Plot", "N/A")
    poster = response.get("Poster", "N/A")

    # Download button (You can replace with your real link)
    keyboard = [
        [InlineKeyboardButton("📥 Download", url="https://example.com/download-link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"🎬 *{title}* ({year})\n"
        f"⭐ **IMDb:** {rating}\n\n"
        f"📝 *Storyline:*\n{plot}"
    )

    # If poster is available and not "N/A"
    if poster != "N/A":
        await update.message.reply_photo(
            photo=poster,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


# Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie_search))

if __name__ == "__main__":
    print("🤖 Bot running...")
    app.run_polling()
