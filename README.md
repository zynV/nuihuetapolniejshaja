# Patreon Telegram Bot

Telegram-бот с интеграцией через OAuth2 с платформой Patreon для автоматического предоставления доступа к приватным каналам в зависимости от уровня подписки пользователя.

## 🚀 Возможности

- Авторизация пользователей через Patreon OAuth2
- Автоматическое определение уровня подписки
- Выдача одноразовых ссылок для вступления в приватные каналы
- Хранение данных пользователей в SQLite
- Логирование всех действий

## 🛠️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/patreon-telegram-bot.git
cd patreon-telegram-bot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
pip install -r requirements.txt
```

3. Создайте файл `.env` в корневой директории проекта:
```env
BOT_TOKEN=your_telegram_bot_token
PATREON_CLIENT_ID=your_patreon_client_id
PATREON_CLIENT_SECRET=your_patreon_client_secret
PATREON_REDIRECT_URI=http://localhost:8000/callback
DATABASE_URL=sqlite:///database/auth.db
LOG_LEVEL=INFO
LOG_FILE=logs/auth.log
```

4. Создайте необходимые директории:
```bash
mkdir -p database logs web/templates web/static
```

## 🚀 Запуск

1. Запустите веб-сервер:
```bash
uvicorn web.web_main:app --host 0.0.0.0 --port 8000
```

2. В отдельном терминале запустите бота:
```bash
python bot/bot_main.py
```

## 📝 Использование

1. Пользователь запускает бота командой `/start`
2. Бот отправляет ссылку для авторизации через Patreon
3. После успешной авторизации пользователь получает одноразовую ссылку для вступления в канал
4. Доступ к каналу предоставляется в зависимости от уровня подписки на Patreon

## 🔧 Настройка

### Конфигурация каналов

В файле `config.py` настройте соответствие уровней подписки и ID каналов:

```python
TIER_TO_CHANNEL = {
    'tier1': 'channel_id_1',
    'tier2': 'channel_id_2',
    'tier3': 'channel_id_3',
}
```

### Логирование

Логи сохраняются в директории `logs/`:
- `auth.log` - логи веб-сервера
- `bot.log` - логи Telegram бота

## 📄 Лицензия

MIT License 