# 🚀 Швидкий старт

🔗 **GitHub:** https://github.com/nestorchurin/tgradio

## ⚠️ ВАЖЛИВО: Це userbot (працює від вашого Telegram акаунта)

## Мінімальні кроки для запуску радіо бота

### 0. Клонування
```bash
git clone https://github.com/nestorchurin/tgradio.git
cd tgradio
```

### 1. Встановлення
```bash
pip install -r requirements.txt
winget install Gyan.FFmpeg
```

Або вручну:
```bash
pip install pyrogram pytgcalls pyyaml
winget install Gyan.FFmpeg
```

### 2. Структура папок
```
tgbot/
├── playlist/    # Додайте музичні файли (.mp3)
├── jingle/      # Додайте джингли (.mp3) 
├── ads/         # Додайте рекламу (.mp3)
└── config.yml   # Налаштування
```

### 3. Конфігурація (config.yml)
```yaml
telegram_bot:
  - api_id: YOUR_API_ID           # my.telegram.org
    api_hash: YOUR_API_HASH       # my.telegram.org  
    bot_token: ANY_TOKEN          # Не використовується для userbot
    phone_number: "+YOUR_PHONE"   # ВАШ номер телефону

admins:
  - YOUR_USER_ID                  # @userinfobot

radio_channel_id: "CHANNEL_ID"   # ID каналу з мінусом

radio_settings:
  jingle_frequency: 3             # Джингл кожні 3 треки
  ads_frequency: 7                # Реклама кожні 7 треків
  track_duration: 180             # 3 хв на трек
  default_volume: 5               # 5% гучність

prefixes: "$"
```

### 4. Запуск
```bash
python main.py
```

### 5. Команди
- `$radio` - Запустити радіо
- `$next` - Наступний трек  
- `$vol 50` - Гучність 50%
- `$stop` - Зупинити

### 6. Готово! 🎉
Бот автоматично грає музику, джингли та рекламу за розкладом.

## ⚠️ Важливі нюанси Userbot:

- При першому запуску може попросити код з SMS
- Бот працює від вашого акаунта (ваше ім'я буде в голосовому чаті)
- Не можна використовувати Telegram на телефоні одночасно
- Команди пишіть в тому ж каналі, де запущено радіо
- Бот буде онлайн, поки працює програма
