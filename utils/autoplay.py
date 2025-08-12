"""
Модуль для автоматичного відтворення радіо
Простий та надійний код без дублювання
"""
import asyncio
from .config import RADIO_CONFIG
from .pytgcalls_handler import check_connection, play_audio_file
from .audio import get_random_music, get_random_jingle, get_random_ads

# Глобальні змінні
tracks_played = 0
autoplay_running = False

async def play_jingle_now(chat_id):
    """Програти джингл миттєво"""
    jingle_file = get_random_jingle()
    if jingle_file is None:
        return False
    
    try:
        track_name = await play_audio_file(chat_id, jingle_file, "jingle")
        return True
    except Exception as e:
        print(f"Помилка програвання джингла: {e}")
        return False

async def play_ads_now(chat_id):
    """Програти рекламу миттєво"""
    ads_file = get_random_ads()
    if ads_file is None:
        return False
    
    try:
        track_name = await play_audio_file(chat_id, ads_file, "ads")
        return True
    except Exception as e:
        print(f"Помилка програвання реклами: {e}")
        return False

async def next_music_instant(chat_id):
    """Миттєво перейти на наступний музичний трек"""
    global tracks_played
    
    music_file = get_random_music()
    if music_file is None:
        raise RuntimeError("Немає аудіо файлів у папці playlist")
    
    track_name = await play_audio_file(chat_id, music_file, "music")
    
    # Збільшуємо лічільник для синхронізації з автоплей
    tracks_played += 1
    
    return track_name

async def next_with_content_check(chat_id):
    """Перейти на наступний контент з перевіркою типу (музика/реклама/джингл)"""
    global tracks_played
    
    # Збільшуємо лічільник
    tracks_played += 1
    
    # Перевіряємо, чи час для спеціального контенту
    if tracks_played % RADIO_CONFIG["ads_frequency"] == 0:
        # Час для реклами
        if await play_ads_now(chat_id):
            await asyncio.sleep(RADIO_CONFIG["ads_duration"])
        
        # Після реклами - музика
        track_name = await next_music_instant(chat_id)
        print(f"Після реклами грає: {track_name}")
        return track_name
        
    elif tracks_played % RADIO_CONFIG["jingle_frequency"] == 0:
        # Час для джингла
        if await play_jingle_now(chat_id):
            await asyncio.sleep(RADIO_CONFIG["jingle_duration"])
        
        # Після джингла - музика
        track_name = await next_music_instant(chat_id)
        print(f"Після джингла грає: {track_name}")
        return track_name
    else:
        # Звичайна музика
        music_file = get_random_music()
        if music_file is None:
            raise RuntimeError("Немає аудіо файлів у папці playlist")
        
        track_name = await play_audio_file(chat_id, music_file, "music")
        print(f"Грає: {track_name}")
        return track_name

async def auto_play_loop(chat_id):
    """Основний цикл автоматичного відтворення"""
    global tracks_played, autoplay_running
    
    # Перевіряємо, чи вже запущений цикл
    if autoplay_running:
        print("Автоплей вже працює")
        return
    
    autoplay_running = True
    print(f"Запуск автоплей для чату {chat_id}")
    
    try:
        while autoplay_running:
            # Чекаємо час треку
            await asyncio.sleep(RADIO_CONFIG["track_duration"])
            
            # Перевіряємо підключення
            if not await check_connection(chat_id):
                print("Втрачено підключення до голосового чату")
                break
            
            # Лічильник треків
            tracks_played += 1
            
            # Визначаємо тип контенту
            if tracks_played % RADIO_CONFIG["ads_frequency"] == 0:
                # Час для реклами
                if await play_ads_now(chat_id):
                    await asyncio.sleep(RADIO_CONFIG["ads_duration"])
                
                # Після реклами - музика (без збільшення лічильника)
                music_file = get_random_music()
                if music_file:
                    track_name = await play_audio_file(chat_id, music_file, "music")
                    print(f"Після реклами грає: {track_name}")
                
            elif tracks_played % RADIO_CONFIG["jingle_frequency"] == 0:
                # Час для джингла
                if await play_jingle_now(chat_id):
                    await asyncio.sleep(RADIO_CONFIG["jingle_duration"])
                
                # Після джингла - музика (без збільшення лічільника)
                music_file = get_random_music()
                if music_file:
                    track_name = await play_audio_file(chat_id, music_file, "music")
                    print(f"Після джингла грає: {track_name}")
                
            else:
                # Звичайна музика (без збільшення лічільника)
                music_file = get_random_music()
                if music_file:
                    track_name = await play_audio_file(chat_id, music_file, "music")
                    print(f"Грає: {track_name}")
                
    except asyncio.CancelledError:
        print("Автоплей зупинено")
    except Exception as e:
        print(f"Помилка автоплей: {e}")
    finally:
        autoplay_running = False
        print("Автоплей завершено")

async def stop_autoplay():
    """Зупинити автоплей"""
    global autoplay_running
    autoplay_running = False
    print("Команда зупинки автоплей")
