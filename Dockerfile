FROM python:3.11-slim

WORKDIR /app

RUN echo "$(cat .env.prod)" > /app/.env

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "./telegram_bot.py"]
