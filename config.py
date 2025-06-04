# config.py - Файл с настройками бота

# Настройки Telegram бота
# Получите токен у @BotFather в Telegram
BOT_TOKEN = "7978360023:AAHNg8Kt6M9jITc4sGY3wGqeRIMu6i2xcls"

# Настройки файла данных
# Путь к CSV файлу для сохранения данных
# Если указать путь в папке Яндекс.Диска, файл будет автоматически синхронизироваться
CSV_FILE_PATH = "receipts.csv"  # Можно изменить на путь к Яндекс.Диску

# Пример для Яндекс.Диска (раскомментируйте и измените путь):
# CSV_FILE_PATH = r"C:\Users\ВашеИмя\YandexDisk\receipts.csv"

# Настройки логирования
LOG_LEVEL = "INFO"  # Уровень логирования: DEBUG, INFO, WARNING, ERROR