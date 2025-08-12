"""
Головний модуль радіо бота
Об'єднує всі компоненти для зручного використання
"""
import asyncio
from .config import CONFIG, RADIO_CONFIG
from .audio import get_random_music
from .pytgcalls_handler import (
    init_pytgcalls, 
    start_pytgcalls, 
    play_audio_file,
    change_volume,
    leave_call,
    current_volume
)
from .autoplay import auto_play_loop, play_jingle_now, play_ads_now, next_music_instant, stop_autoplay

# Глобальна змінна для task автоплей
autoplay_task = None

def init_radio(client):
    """Ініціалізувати радіо модуль"""
    init_pytgcalls(client)

async def join_voice(chat_id):
    """Підключитися до голосового чату та почати радіо"""
    global autoplay_task
    
    try:
        # Запускаємо PyTgCalls
        await start_pytgcalls()
        
        # Отримуємо перший трек
        music_file = get_random_music()
        if music_file is None:
            raise RuntimeError("Немає аудіо файлів у папці playlist")
        
        # Підключаємося до голосового чату з музикою
        track_name = await play_audio_file(chat_id, music_file, "music")
        
        # Встановлюємо дефолтну гучність
        await change_volume(chat_id, RADIO_CONFIG["default_volume"])
        
        # Зупиняємо попередній автоплей, якщо він був
        if autoplay_task and not autoplay_task.done():
            await stop_autoplay()
            autoplay_task.cancel()
        
        # Запускаємо новий автоплей
        autoplay_task = asyncio.create_task(auto_play_loop(chat_id))
        
        print(f"Успішно підключено до голосового чату: {chat_id}")
        print(f"Грає: {track_name}")
        print(f"Гучність: {current_volume}%")
        return track_name
        
    except Exception as e:
        print(f"Помилка підключення до голосового чату {chat_id}: {e}")
        raise e

async def leave_voice(chat_id):
    """Відключитися від голосового чату"""
    global autoplay_task
    
    try:
        # Зупиняємо автоплей
        await stop_autoplay()
        if autoplay_task and not autoplay_task.done():
            autoplay_task.cancel()
            autoplay_task = None
        
        await leave_call(chat_id)
        print(f"Відключено від голосового чату: {chat_id}")
    except Exception as e:
        print(f"Помилка відключення від голосового чату {chat_id}: {e}")
        raise e

async def next_track(chat_id):
    """Перемкнути на наступний трек"""
    try:
        track_name = await next_music_instant(chat_id)
        print(f"Вручну перемкнуто на: {track_name}")
        return track_name
    except Exception as e:
        print(f"Помилка перемикання треку: {e}")
        raise e

async def set_volume(chat_id, volume):
    """Встановити гучність від 0 до 100"""
    try:
        await change_volume(chat_id, volume)
        print(f"Гучність змінено на: {volume}%")
    except Exception as e:
        print(f"Помилка зміни гучності: {e}")
        raise e

async def get_volume(chat_id):
    """Отримати поточну гучність"""
    return current_volume

async def play_jingle(chat_id):
    """Програти випадковий джингл"""
    return await play_jingle_now(chat_id)

async def play_ads(chat_id):
    """Програти випадкову рекламу"""
    return await play_ads_now(chat_id)
