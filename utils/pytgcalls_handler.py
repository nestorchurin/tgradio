"""
Модуль для роботи з PyTgCalls
"""
import os
from pyrogram import Client
from pytgcalls import PyTgCalls
import asyncio
from .config import RADIO_CONFIG
from .audio import get_track_name

# Глобальні змінні
pytg = None
is_started = False
current_volume = RADIO_CONFIG["default_volume"]
client_instance = None

def init_pytgcalls(client: Client):
    """Ініціалізувати PyTgCalls"""
    global pytg, client_instance
    pytg = PyTgCalls(client)
    client_instance = client

async def start_pytgcalls():
    """Запустити PyTgCalls якщо ще не запущений"""
    global is_started
    if pytg is None:
        raise RuntimeError("PyTgCalls не ініціалізовано")
    
    if not is_started:
        await pytg.start()
        is_started = True

async def play_audio_file(chat_id, file_path, content_type="music"):
    """Програти аудіо файл"""
    if pytg is None:
        raise RuntimeError("PyTgCalls не ініціалізовано")
    
    await pytg.play(chat_id, file_path)
    
    # Повертаємо назву треку без зміни назви чату
    content_name = get_track_name(os.path.basename(file_path))
    # print(f"Програємо {content_type}: {content_name}")  # Відключаємо, щоб не дублювати
    
    return content_name

async def change_volume(chat_id, volume):
    """Змінити гучність"""
    global current_volume
    if pytg is None:
        raise RuntimeError("PyTgCalls не ініціалізовано")
    
    await pytg.change_volume_call(chat_id, volume)
    current_volume = volume

async def leave_call(chat_id):
    """Вийти з голосового чату"""
    if pytg is None:
        raise RuntimeError("PyTgCalls не ініціалізовано")
    
    await pytg.leave_call(chat_id)

async def check_connection(chat_id):
    """Перевірити підключення до голосового чату"""
    try:
        await pytg.change_volume_call(chat_id, current_volume)
        return True
    except:
        return False
