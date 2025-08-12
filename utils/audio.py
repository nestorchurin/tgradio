"""
Модуль для роботи з аудіо файлами
"""
import os
import random
from .config import RADIO_CONFIG

def get_track_name(filename):
    """Отримати назву треку з імені файлу (без розширення)"""
    return os.path.splitext(filename)[0]

def get_random_file_from_folder(folder_name):
    """Отримати випадковий аудіо файл з папки"""
    folder_path = RADIO_CONFIG["folders"][folder_name]
    if not os.path.exists(folder_path):
        return None
    
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    if not audio_files:
        return None
    
    selected_file = random.choice(audio_files)
    return os.path.join(folder_path, selected_file)

def get_random_music():
    """Повертає випадковий аудіо файл з папки playlist"""
    return get_random_file_from_folder("music")

def get_random_jingle():
    """Повертає випадковий джингл з папки jingle"""
    return get_random_file_from_folder("jingles")

def get_random_ads():
    """Повертає випадкову рекламу з папки ads"""
    return get_random_file_from_folder("ads")
