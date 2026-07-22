import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ===== НАСТРОЙКИ (ТВОИ ДАННЫЕ) =====
TOKEN = "8986361509:AAGowng4swOGP1gFNwYcaAn_lDOiQwNEzAc"  # СЛИТЫЙ ТОКЕН — СРАЗУ ЗАМЕНИ!
ADMIN_CHAT_ID = -5317499603  # ТВОЙ ЧАТ АЙДИ

# ===== ОБРАБОТЧИК ФОТО =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]  # БЕРЁМ САМОЕ КАЧЕСТВЕННОЕ ФОТО
    
    # ФОРМИРУЕМ ПОДПИСЬ
    caption = (
        f"📸 Новое фото от {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
    )
    if user.username:
        caption += f"👤 Username: @{user.username}\n"
    if update.message.caption:
        caption += f"💬 Текст: {update.message.caption}"
    
    try:
        # ОТПРАВЛЯЕМ ФОТО АДМИНУ
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=photo.file_id,
            caption=caption
        )
        # ОТВЕЧАЕМ ПОЛЬЗОВАТЕЛЮ
        await update.message.reply_text(
            "✅ Ваше фото отправлено в поддержку! Мы свяжемся с вами в ближайшее время.",
            quote=True
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}", quote=True)

# ===== ОБРАБОТЧИК ДЛЯ /START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Привет! Я бот HomePhoto.**\n\n"
        "📸 Отправьте мне фото, и я передам его в службу поддержки.\n"
        "🖼️ Вы также можете отправить фото как файл.\n\n"
        "📌 _Фото хранятся 30 дней._",
        parse_mode="Markdown"
    )

# ===== ЗАПУСК =====
def main():
    app = Application.builder().token(TOKEN).build()
    
    # РЕГИСТРИРУЕМ ОБРАБОТЧИКИ
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
    
    print("🤖 Бот HomePhoto запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
