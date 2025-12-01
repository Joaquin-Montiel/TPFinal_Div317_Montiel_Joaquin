import pygame.mixer as mixer
import modules.variables as var

music_configs = {"actual_music_path": ''}

def set_music_path(music_path: str) -> None:
    """
    Establece la ruta del archivo de música a reproducir.
    Args: -music_path (str): Ruta completa al archivo de audio (MP3, OGG, etc.).
    Returns: No retorna nada.
    """
    music_configs['actual_music_path'] = music_path

def play_music() -> None:
    """
    Carga y reproduce la música de fondo almacenada en 'actual_music_path'.
    La reproduce en bucle infinito (-1) y con un tiempo de fade-in.
    Returns: No retorna nada.
    """
    if music_configs.get('actual_music_path'):
        mixer.music.load(music_configs.get('actual_music_path'))
        mixer.music.play(-1, 0, 2500)

def stop_music() -> None:
    """
    Detiene la música de fondo con un efecto de 'fadeout'.
    Returns: No retorna nada.
    """
    if music_configs.get('actual_music_path'):
        mixer.music.fadeout(500)


def get_actual_vol() -> int:
    """
    Obtiene el nivel de volumen actual del mixer de Pygame y lo retorna 
    en una escala de 0 a 100.
    Returns: -int: El nivel de volumen actual (0-100).
    """
    actual_volumen = mixer.music.get_volume() * 100
    return int(actual_volumen)

def set_volume(volumen: int) -> None:
    """
    Establece el nivel de volumen del mixer de Pygame. Convierte el valor 
    de la escala 0-100 (entero) a la escala 0.0-1.0 (flotante) que usa Pygame.
    Args: -volumen (int): El nivel de volumen deseado (0 a 100).
    Returns: No retorna nada.
    """
    actual_vol = volumen / 100
    actual_vol = round(actual_vol, 1)
    mixer.music.set_volume(actual_vol) 