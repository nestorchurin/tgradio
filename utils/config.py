"""
Конфігурація радіо бота
"""
import yaml
import os

def load_config():
    """Завантажити конфігурацію з config.yml"""
    config_path = "config.yml"
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.yml не знайдено")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Глобальна конфігурація
CONFIG = load_config()
RADIO_CONFIG = CONFIG["radio_settings"]
