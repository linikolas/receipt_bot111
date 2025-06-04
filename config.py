
# config.py - Файл конфигурации для Telegram бота
import os

# Токен вашего бота от @BotFather
# Берется из переменной окружения для безопасности
BOT_TOKEN = os.getenv('BOT_TOKEN', '7719346499:AAGsFv4w2W4sCjiID-aQCu6rbigb6dFuKu0')

# Путь к CSV файлу для сохранения данных
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', 'receipts.csv')

# Дополнительные настройки
LOG_LEVEL = "INFO"
MAX_FILE_SIZE_MB = 50
