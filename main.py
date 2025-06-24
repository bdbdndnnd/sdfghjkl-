from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re

# Токен и юзернейм для отправки заявок
TOKEN = '7557154777:AAFUkmd6Jurjm2-HOrN6m_R6JAJZ1xbNtpI'  # Вставь сюда свой токен
MANAGER_USERNAME = 'hhhltewcbut'  # Менеджер, которому бот отправляет заявку

# Извлечение возраста из текста
def extract_age(message_text):
    matches = re.findall(r'\b\d{1,2}\b', message_text)
    for match in matches:
        age = int(match)
        if 5 <= age <= 100:
            return age
    return None

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Согласен', 'Несогласен']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    text = (
        "Я работаю в компании KINGDOM.\n\n"
        "И предлагаю тебе два вида заработка БЕЗ КАКИХ ЛИБО ВЛОЖЕНИЙ\n\n"
        "Первый - работа на переводах денежных средств. Очень простая работа.\n"
        "Второй - на приглашении людей в компанию. Работа посложнее.\n"
        "Заработок от 500 до 5000 в день!\n\n"
        "Если согласен - так и напиши, и я перенаправлю тебя к нашему менеджеру Кире! 💓"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if text == 'согласен':
        await update.message.reply_text(
            "Поняла, тогда напиши в ответ на это сообщение свой юзернейм, свой возраст и свое имя, "
            "если ты нам подходишь, мы тебе обязательно напишем"
        )
        context.user_data['awaiting_info'] = True

    elif text == 'несогласен':
        await update.message.reply_text("Жаль, что ты отказался. Если передумаешь — просто напиши /start 😊")

    else:
        if context.user_data.get('awaiting_info'):
            age = extract_age(update.message.text)
            if age is None:
                await update.message.reply_text("Пожалуйста, укажи свой возраст числом, чтобы мы могли тебя оценить.")
                return
            if age < 14:
                await update.message.reply_text("К сожалению, наш проект доступен только с 14 лет.")
            else:
                user = update.message.from_user
                message_to_manager = f"Заявка от @{user.username}:\n{text}"
                await context.bot.send_message(chat_id='@' + MANAGER_USERNAME, text=message_to_manager)
                await update.message.reply_text(
                    "Благодарю тебя за интерес! 💓\n\n"
                    "Напиши нашему менеджеру @zermoc для получения более подробной информации и устройства на работу 🫀\n\n"
                    "Напиши ей в формате: «я от @mashi_kss»\n\n"
                    "У Киры большая занятость, поэтому прошу не переживать, если она долго не отвечает! "
                    "Лучше всего почаще дублировать сообщения — она обязательно ответит тебе, ответит на все твои вопросы и примет тебя на работу! 💕\n\n"
                    "Если у тебя останутся вопросы — не стесняйся, пиши мне: @mashi_kss 😊"
                )
            context.user_data['awaiting_info'] = False
        else:
            await update.message.reply_text("Пожалуйста, выбери 'Согласен' или 'Несогласен'.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# Точка входа
if __name__ == '__main__':
    main()
