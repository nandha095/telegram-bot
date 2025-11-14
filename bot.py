from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome! Send me a movie name to search."
    )


async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()
    encoded = urllib.parse.quote(movie_name)

    url = f"http://www.omdbapi.com/?t={encoded}&apikey={OMDB_API_KEY}"

    try:
        data = requests.get(url).json()
    except:
        await update.message.reply_text("❌ API Error. Try again later.")
        return

    if data.get("Response") != "True":
        await update.message.reply_text("❌ Movie not found.")
        return

    title = data.get("Title", "N/A")
    year = data.get("Year", "N/A")
    rating = data.get("imdbRating", "N/A")
    plot = data.get("Plot", "N/A")
    poster = data.get("Poster", "N/A")

    caption = f"🎬 *{title} ({year})*\n⭐ IMDb: {rating}\n\n📝 {plot}"

    buttons = [
        [InlineKeyboardButton("📥 Download", url="https://example.com/download")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

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


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie_search))

if __name__ == "__main__":
    print("🤖 Bot running...")
    app.run_polling()
