FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Скопировать файл зависимостей в рабочую директорию
COPY requirements.txt /app/requirements.txt

# Обновление пакетного менеджера и установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка дополнительных зависимостей
RUN pip install --no-cache-dir aiogram

# Скопировать все файлы в рабочую директорию
COPY . .

# Команда запуска контейнера
CMD ["python", "-u", "main.py"]
