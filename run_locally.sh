#!/usr/bin/env bash

# Налаштування
LOG_FILE="script.log"
GOOGLE_CREDENTIALS_PATH="./sa.json"

# Функція для відключення VPN та очищення ENV при виході
cleanup() {
    # Очищення ENV
    unset GOOGLE_APPLICATION_CREDENTIALS
    exit
}

# Обробка сигналів для коректного завершення скрипта
trap cleanup SIGINT SIGTERM

# Перенаправлення виводу скрипта у файл журналу та в термінал
exec > >(tee -a "$LOG_FILE") 2>&1

# Перевірка наявності файлу sa.json
if [ ! -f "$GOOGLE_CREDENTIALS_PATH" ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Файл $GOOGLE_CREDENTIALS_PATH не знайдено."
    cleanup
fi

# Підготовка ENV
export GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_CREDENTIALS_PATH"
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Змінна GOOGLE_APPLICATION_CREDENTIALS встановлена."

# Перевірка наявності main.py
if [ ! -f "main.py" ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Файл main.py не знайдено."
    cleanup
fi

# Запуск додатку
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Запуск main.py..."
python3 main.py

# Перевірка успішності виконання main.py
if [ $? -ne 0 ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Додаток main.py завершився з помилкою."
    cleanup
else
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Додаток main.py завершився успішно."
fi

# Відключення VPN та очищення ENV після завершення роботи
cleanup
