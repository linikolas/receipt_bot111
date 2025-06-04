# bot.py - Telegram бот для записи чеков в CSV файл на Яндекс.Диске

import logging
import csv
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы для состояний разговора с пользователем
# Каждое число соответствует определенному этапу ввода данных
DATE, RECEIPT_NUMBER, AMOUNT, DISCOUNT, NOTE = range(5)

class ReceiptBot:
    def __init__(self, bot_token, csv_file_path):
        """
        Инициализация бота
        bot_token - токен вашего Telegram бота
        csv_file_path - путь к CSV файлу для сохранения данных
        """
        self.bot_token = bot_token
        self.csv_file_path = csv_file_path
        self.setup_csv_file()
    
    def setup_csv_file(self):
        """
        Создание CSV файла с заголовками, если он не существует
        """
        try:
            # Проверяем, существует ли файл
            if not os.path.exists(self.csv_file_path):
                # Создаем новый файл с заголовками
                with open(self.csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    # Записываем заголовки столбцов
                    headers = ["Дата", "№_чека", "Сумма", "Скидка", "Примечание"]
                    writer.writerow(headers)
                    logger.info(f"Создан новый CSV файл: {self.csv_file_path}")
            else:
                logger.info(f"Используется существующий CSV файл: {self.csv_file_path}")
                
        except Exception as e:
            logger.error(f"Ошибка при создании CSV файла: {e}")
    
    def add_receipt_to_csv(self, receipt_data):
        """
        Добавление данных чека в CSV файл
        receipt_data - словарь с данными чека
        """
        try:
            # Открываем файл в режиме добавления (append)
            with open(self.csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Подготавливаем строку данных для записи
                row_data = [
                    receipt_data['date'],      # Дата
                    receipt_data['number'],    # Номер чека
                    receipt_data['amount'],    # Сумма
                    receipt_data['discount'],  # Скидка
                    receipt_data['note']       # Примечание
                ]
                
                # Записываем строку в файл
                writer.writerow(row_data)
                logger.info(f"Добавлен чек №{receipt_data['number']} в CSV файл")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка при записи в CSV файл: {e}")
            return False

# Импортируем настройки из файла конфигурации
try:
    from config import BOT_TOKEN, CSV_FILE_PATH
except ImportError:
    # Если файл config.py не найден, используем значения по умолчанию
    BOT_TOKEN = "7978360023:AAHNg8Kt6M9jITc4sGY3wGqeRIMu6i2xcls"  # Токен от @BotFather
    CSV_FILE_PATH = "receipts.csv"     # Путь к CSV файлу

# Создаем объект бота
receipt_bot = ReceiptBot(BOT_TOKEN, CSV_FILE_PATH)

# Временное хранилище данных пользователя во время ввода
user_data_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды /start
    Начинает процесс ввода данных нового чека
    """
    user_id = update.effective_user.id
    
    # Инициализируем пустой словарь для данных пользователя
    user_data_storage[user_id] = {}
    
    await update.message.reply_text(
        "🧾 Добро пожаловать в бот учета чеков!\n\n"
        "📅 Введите дату (пример: 01.12.2024):"
    )
    
    # Переходим к первому состоянию - ввод даты
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получение даты от пользователя
    """
    user_id = update.effective_user.id
    date_text = update.message.text.strip()
    
    # Сохраняем дату как есть, без проверок
    user_data_storage[user_id]['date'] = date_text
    
    await update.message.reply_text("🧾 Введите номер чека:")
    
    # Переходим к следующему состоянию - ввод номера чека
    return RECEIPT_NUMBER

async def get_receipt_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получение номера чека от пользователя
    """
    user_id = update.effective_user.id
    receipt_number = update.message.text.strip()
    
    # Сохраняем номер чека как есть, без проверок
    user_data_storage[user_id]['number'] = receipt_number
    
    await update.message.reply_text("💰 Введите сумму:")
    
    # Переходим к следующему состоянию - ввод суммы
    return AMOUNT

async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получение суммы чека от пользователя
    """
    user_id = update.effective_user.id
    amount = update.message.text.strip()
    
    # Сохраняем сумму как есть, без проверок
    user_data_storage[user_id]['amount'] = amount
    
    await update.message.reply_text("🏷️ Введите сумму скидки:")
    
    # Переходим к следующему состоянию - ввод скидки
    return DISCOUNT

async def get_discount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получение размера скидки от пользователя
    """
    user_id = update.effective_user.id
    discount = update.message.text.strip()
    
    # Сохраняем скидку как есть, без проверок
    user_data_storage[user_id]['discount'] = discount
    
    await update.message.reply_text("📝 Добавьте примечание:")
    
    # Переходим к последнему состоянию - ввод примечания
    return NOTE

async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получение примечания и завершение ввода данных
    """
    user_id = update.effective_user.id
    note = update.message.text.strip()
    
    # Сохраняем примечание
    user_data_storage[user_id]['note'] = note
    
    # Сохраняем данные в CSV файл
    success = receipt_bot.add_receipt_to_csv(user_data_storage[user_id])
    
    if success:
        # Формируем сообщение с подтверждением
        data = user_data_storage[user_id]
        confirmation_message = (
            "✅ Данные успешно сохранены!\n\n"
            f"📅 Дата: {data['date']}\n"
            f"🧾 № чека: {data['number']}\n"
            f"💰 Сумма: {data['amount']}\n"
            f"🏷️ Скидка: {data['discount']}\n"
            f"📝 Примечание: {data['note']}\n\n"
            "Для добавления нового чека используйте команду /start"
        )
        await update.message.reply_text(confirmation_message)
    else:
        await update.message.reply_text(
            "❌ Ошибка при сохранении данных.\n"
            "Попробуйте еще раз позже или обратитесь к администратору."
        )
    
    # Очищаем временные данные пользователя
    if user_id in user_data_storage:
        del user_data_storage[user_id]
    
    # Завершаем разговор
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды / cancel - отмена ввода данных
    """
    user_id = update.effective_user.id
    
    # Очищаем временные данные
    if user_id in user_data_storage:
        del user_data_storage[user_id]
    
    await update.message.reply_text(
        "❌ Ввод данных отменен.\n"
        "Для начала ввода нового чека используйте команду /start"
    )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /help - показывает справку
    """
    help_text = (
        "🤖 Бот для учета чеков\n\n"
        "📋 Доступные команды:\n"
        "/start - Начать ввод нового чека\n"
        "/cancel - Отменить текущий ввод\n"
        "/help - Показать эту справку\n"
        "/file - Получить CSV файл с данными\n\n"
        "📝 Порядок ввода данных:\n"
        "1. Дата (например: 01.12.2024 или 01.12.2024 15:30)\n"
        "2. Номер чека (любой текст)\n"
        "3. Сумма (любой текст)\n"
        "4. Размер скидки (любой текст)\n"
        "5. Примечание (любой текст)\n\n"
        "📄 Данные сохраняются в CSV файл, который можно открыть в Excel"
    )
    await update.message.reply_text(help_text)

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправка CSV файла пользователю
    """
    try:
        # Проверяем, существует ли файл
        if os.path.exists(CSV_FILE_PATH):
            # Отправляем файл пользователю
            with open(CSV_FILE_PATH, 'rb') as file:
                await update.message.reply_document(
                    document=file,
                    filename=f"receipts_{datetime.now().strftime('%Y%m%d')}.csv",
                    caption="📄 Файл с данными чеков\n\nМожно открыть в Excel или Google Sheets"
                )
        else:
            await update.message.reply_text(
                "📄 Файл с данными пока не создан.\n"
                "Добавьте первый чек командой /start"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await update.message.reply_text(
            "❌ Ошибка при отправке файла.\n"
            "Попробуйте позже."
        )

def main():
    """
    Основная функция - запуск бота
    """
    # Создаем приложение бота
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Настраиваем обработчик разговора (ConversationHandler)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],  # Точка входа - команда /start
        states={
            # Определяем состояния и соответствующие им обработчики
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            RECEIPT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_receipt_number)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            DISCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_discount)],
            NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_note)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],  # Команда для выхода из разговора
    )
    
    # Добавляем обработчики команд
    application.add_handler(conversation_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("file", send_file))
    
    logger.info("Бот запущен и готов к работе!")
    print("Бот запущен! Нажмите Ctrl+C для остановки.")
    
    # Запуск бота
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()