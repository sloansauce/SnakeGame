import pygame
import os
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Cache for loaded resources
_resource_cache = {}

def get_image(filename):
    if filename not in _resource_cache:
        path = os.path.join(ASSETS_DIR, 'Graphics', filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            _resource_cache[filename] = image
        except pygame.error as e:
            raise FileNotFoundError(f"Failed to load image: {path}\n{e}")
    return _resource_cache[filename]

def get_sound(filename):
    if filename not in _resource_cache:
        path = os.path.join(ASSETS_DIR, 'Sounds', filename)
        try:
            sound = pygame.mixer.Sound(path)
            _resource_cache[filename] = sound
        except pygame.error as e:
            raise FileNotFoundError(f"Failed to load sound: {path}\n{e}")
    return _resource_cache[filename]

def get_music(filename):
    path = os.path.join(ASSETS_DIR, 'Sounds', filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Failed to load music: {path}")
    return path

def get_font(filename, size):
    cache_key = (filename, size)
    if cache_key not in _resource_cache:
        path = os.path.join(ASSETS_DIR, 'FONTS', filename)
        try:
            font = pygame.font.Font(path, size)
            _resource_cache[cache_key] = font
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Failed to load font {filename}. Using default font. Error: {e}")
            font = pygame.font.Font(None, size)
            _resource_cache[cache_key] = font
    return _resource_cache[cache_key]

def clear_cache():
    _resource_cache.clear()