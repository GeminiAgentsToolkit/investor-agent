# To Use

* Create file .env.prod and .env.dev files with the following variables inside:

```
ALPACA_API_KEY_ID=...
ALPACA_SECRET_KEY=...
TELEGRAM_TOKEN=...
TELEGRAM_CHAT_IDS=...
```

bot will ONLY respond to user from TELEGRAM_CHAT_IDS

* create sa.json with the credentials of the JSON that should be used
* set project in telegram_bot
* refactor deploy.sh
* have fun