
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import fitz  # PyMuPDF
import tempfile

DEFAULT_THUMB_PATH = "thumbs/default.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("שלח לי קובץ PDF או EPUB ואני אוסיף לו תמונת תצוגה (thumbnail) לפי התמונה שהגדרת.")

async def set_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_path = os.path.join("thumbs", "default.jpg")
        await file.download_to_drive(file_path)
        await update.message.reply_text("תמונת ברירת מחדל הוגדרה בהצלחה.")
    else:
        await update.message.reply_text("שלח תמונה כתגובה לפקודה /set_thumbnail.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.lower().endswith((".pdf", ".epub")):
        await update.message.reply_text("פורמט לא נתמך. שלח PDF או EPUB בלבד.")
        return

    file = await context.bot.get_file(document.file_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(document.file_name)[1]) as tmp:
        await file.download_to_drive(tmp.name)

        if not os.path.exists(DEFAULT_THUMB_PATH):
            await update.message.reply_text("לא הוגדרה תמונת ברירת מחדל. השתמש בפקודה /set_thumbnail.")
            return

        thumb = Image.open(DEFAULT_THUMB_PATH).convert("RGB")
        thumb_path = tmp.name + "_thumb.jpg"
        thumb.save(thumb_path)

        if tmp.name.endswith(".pdf"):
            doc = fitz.open(tmp.name)
            doc.set_metadata({"title": document.file_name})
            doc.set_toc([])
            img_rect = fitz.Rect(0, 0, 100, 100)
            img = open(thumb_path, "rb").read()
            doc.insert_image(img_rect, stream=img)
            output_path = tmp.name.replace(".pdf", "_with_thumb.pdf")
            doc.save(output_path)
            doc.close()
        else:
            output_path = tmp.name  # לא מטפל ב-EPUB בשלב זה

        await update.message.reply_document(InputFile(output_path, filename=os.path.basename(output_path)))
        os.remove(tmp.name)

if __name__ == "__main__":
    os.makedirs("thumbs", exist_ok=True)
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_thumbnail", set_thumbnail))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.PHOTO, set_thumbnail))
    app.run_polling()
