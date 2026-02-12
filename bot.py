from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from config import TOKEN, ADMIN_ID
from db import next_leave_id, save_report
from pdf_engine import build_pdf


FIELDS = [
    ("name", "الاسم"),
    ("national_id", "رقم الهوية"),
]

ASK = 0


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [["إنشاء تقرير"]]
    await update.message.reply_text(
        "لوحة النظام",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True),
    )


async def new_report(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["data"] = {}
    ctx.user_data["i"] = 0
    ctx.user_data["data"]["leave_id"] = next_leave_id()

    await update.message.reply_text(FIELDS[0][1])
    return ASK


async def collect(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    i = ctx.user_data["i"]
    key, _ = FIELDS[i]

    ctx.user_data["data"][key] = update.message.text
    i += 1

    if i == len(FIELDS):
        data = ctx.user_data["data"]

        pdf_path = build_pdf("templates/seha.pdf", data)
        save_report(data)

        await update.message.reply_document(open(pdf_path, "rb"))
        return ConversationHandler.END

    ctx.user_data["i"] = i
    await update.message.reply_text(FIELDS[i][1])
    return ASK


app = ApplicationBuilder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^إنشاء"), new_report)],
    states={
        ASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect)]
    },
    fallbacks=[],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)

print("✅ BOT STARTED")
app.run_polling()
