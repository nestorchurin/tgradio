from pyrogram import Client, filters
import yaml
import asyncio
import os
from utils.radio import init_radio, join_voice, leave_voice, next_track, set_volume, get_volume, play_jingle, play_ads

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

app = Client(
    config["credentials"]["bot_username"],
    api_id=config["telegram_bot"][0]["api_id"],
    api_hash=config["telegram_bot"][0]["api_hash"],
    phone_number=config["telegram_bot"][0]["phone_number"], #if use user bot
    #bot_token=config["telegram_bot"][0]["bot_token"]  #if use bot token
)

admins = config["admins"]
pref = config["prefixes"]

# Створюємо фільтр для адмінів
def admin_filter(_, __, message):
    return message.from_user.id in admins

admin_filter = filters.create(admin_filter)

# Ініціалізуємо радіо модуль
init_radio(app)

@app.on_message(filters.command("radio", prefixes=pref) & admin_filter)
async def start_command(client, message):
    try:
        # Підключаємося до радіо каналу з config
        radio_channel_id = int(config["radio_channel_id"])
        track_name = await join_voice(radio_channel_id)
        await message.reply(f"🎵 Підключено до радіо каналу!\n🎶 Грає: {track_name}")
    except Exception as e:
        await message.reply(f"❌ Помилка підключення до радіо: {e}")

@app.on_message(filters.command("next", prefixes=pref) & admin_filter)
async def next_track_command(client, message):
    try:
        radio_channel_id = int(config["radio_channel_id"])
        track_name = await next_track(radio_channel_id)
        await message.reply(f"⏭️ Наступний трек: {track_name}")
    except Exception as e:
        await message.reply(f"❌ Помилка перемикання треку: {e}")

@app.on_message(filters.command("stop", prefixes=pref) & admin_filter)
async def stop_radio_command(client, message):
    try:
        # Відключаємося від радіо каналу
        radio_channel_id = int(config["radio_channel_id"])
        await leave_voice(radio_channel_id)
        await message.reply(f"⏹️ Відключено від радіо каналу!")
    except Exception as e:
        await message.reply(f"❌ Помилка відключення: {e}")

@app.on_message(filters.command("join", prefixes=pref) & admin_filter)
async def join_voice_command(client, message):
    try:
        # Отримуємо chat_id поточного чату
        chat_id = message.chat.id
        await join_voice(chat_id)
        await message.reply(f"✅ Підключено до голосового чату!")
    except Exception as e:
        await message.reply(f"❌ Помилка підключення: {e}")

@app.on_message(filters.command(["vol", "volume"], prefixes=pref) & admin_filter)
async def volume_command(client, message):
    try:
        radio_channel_id = int(config["radio_channel_id"])
        
        # Якщо є аргумент - встановлюємо гучність
        if len(message.command) > 1:
            try:
                volume = int(message.command[1])
                if 0 <= volume <= 100:
                    await set_volume(radio_channel_id, volume)
                    await message.reply(f"🔊 Гучність встановлено: {volume}%")
                else:
                    await message.reply("❌ Гучність має бути від 0 до 100%")
            except ValueError:
                await message.reply("❌ Неправильне значення гучності")
        else:
            # Показуємо поточну гучність
            current_volume = await get_volume(radio_channel_id)
            await message.reply(f"🔊 Поточна гучність: {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Помилка зміни гучності: {e}")

@app.on_message(filters.command("jingle", prefixes=pref) & admin_filter)
async def jingle_command(client, message):
    try:
        radio_channel_id = int(config["radio_channel_id"])
        jingle_played = await play_jingle(radio_channel_id)
        if jingle_played:
            await message.reply("📻 Джингл програється!")
        else:
            await message.reply("❌ Немає джинглів у папці jingle або помилка відтворення")
    except Exception as e:
        await message.reply(f"❌ Помилка програвання джингла: {e}")

@app.on_message(filters.command("ads", prefixes=pref) & admin_filter)
async def ads_command(client, message):
    try:
        radio_channel_id = int(config["radio_channel_id"])
        ads_played = await play_ads(radio_channel_id)
        if ads_played:
            await message.reply("📢 Реклама програється!")
        else:
            await message.reply("❌ Немає реклами у папці ads або помилка відтворення")
    except Exception as e:
        await message.reply(f"❌ Помилка програвання реклами: {e}")

@app.on_message(filters.command("debug", prefixes=pref) & admin_filter)
async def debug_command(client, message):
    """Команда для відлагодження - показує останні повідомлення"""
    try:
        radio_channel_id = int(config["radio_channel_id"])
        
        debug_info = "🔍 Останні 10 повідомлень у каналі:\n\n"
        count = 0
        async for msg in client.get_chat_history(radio_channel_id, limit=10):
            count += 1
            msg_type = "Service" if msg.service else "Text"
            content = msg.text[:30] if msg.text else f"Service: {type(msg.service).__name__ if msg.service else 'None'}"
            debug_info += f"{count}. ID: {msg.id} | Type: {msg_type} | Content: {content}...\n"
        
        await message.reply(debug_info)
    except Exception as e:
        await message.reply(f"❌ Помилка відлагодження: {e}")

app.run()