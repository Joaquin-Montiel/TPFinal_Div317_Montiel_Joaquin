import pygame as pg
import modules.variables as var
import modules.sounds as sound

def create_base_form(form_data: dict) -> dict:
    """
    Crea la estructura base de un formulario (pantalla) en Pygame.
    Inicializa el nombre, estado activo, carga el fondo, escala la superficie 
    y calcula el rectángulo de posición.
    Args: -form_data (dict): Diccionario que contiene datos iniciales como 'name', 
        'screen', 'background', 'screen_dimensions', 'coord' y 'music_path'.
    Returns:
        dict: Un diccionario de formulario inicializado, listo para agregar widgets.
    """
    form = {
        "name": form_data.get('name'),
        "screen": form_data.get('screen'),
        "active": form_data.get('active', False),
        "music_path": form_data.get('music_path'),
        "widgets_list": []
    }
    background = pg.image.load(form_data.get('background')).convert_alpha()
    background = pg.transform.scale(background, form_data.get('screen_dimensions'))
    form["surface"] = background
    form["rect"] = form.get('surface').get_rect()
    form["rect"].topleft = form_data.get('coord')
    return form

def draw_widgets(form_data: dict) -> None:
    """
    Dibuja todos los widgets contenidos en la 'widgets_list' del formulario en la pantalla de Pygame.
    Args: -form_data (dict): El diccionario del formulario actual.
    Returns: No retorna nada.
    """
    for widget in form_data.get('widgets_list'):
        widget.draw()

def update_widgets(form_data: dict) -> None:
    """
    Ejecuta el método 'update()' en todos los widgets del formulario.
    Esto permite que los botones, etiquetas o campos de texto reaccionen a eventos (mouse, teclado) en cada frame.
    Args: -form_data (dict): El diccionario del formulario actual.
    Returns: No retorna nada.
    """
    for widget in form_data.get('widgets_list'):
        widget.update()


def set_active(form_name: str, change_music: bool = True) -> None: 
    """
    Establece un formulario como activo y desactiva todos los demás.
    Centraliza el control de la música al cambiar de pantalla.
    Args: -form_name (str): El nombre del formulario a activar (clave en dict_form_status).
        -change_music (bool, optional): Si es True, detiene la música anterior e inicia la música de la nueva pantalla. 
        Útil para menús de pausa (False). Defaults to True.
    Returns: No retorna nada.
    """
    for form in var.dict_form_status.values():
        if form.get('active'):
            
            if change_music:
                music_off() 
            
            form['active'] = False
            
    form_active = var.dict_form_status[form_name]
    form_active['active'] = True

    if change_music:
        music_on(form_active) 


def music_on(form_dict_data: dict) -> None:
    """
    Inicia la reproducción de la música asociada al formulario actual, 
    si el control global de música está habilitado (var.MUSIC_ENABLED).
    Args: -form_dict_data (dict): El diccionario del formulario activo que contiene 'music_path'.
    Returns: No retorna nada.
    """
    if not var.MUSIC_ENABLED:
        return
    
    path_music = form_dict_data.get('music_path')
    sound.set_music_path(path_music)
    sound.play_music()

def music_off():
    """
    Detiene la reproducción de la música de fondo en Pygame, 
    si el control global de música está habilitado.
    Returns: No retorna nada.
    """
    if not var.MUSIC_ENABLED:
        return
    sound.stop_music()

def cambiar_pantalla(form_name: str, change_music: bool = True) -> None:
    """
    Función de callback utilizada por los botones para iniciar el cambio de pantalla.
    Delega la lógica principal a set_active().
    Args: -form_name (str): El nombre del formulario de destino.
        -change_music (bool, optional): Indica si la música debe cambiar/reiniciarse. Defaults to True.
    Returns: No retorna nada.
    """
    set_active(form_name, change_music)

def update(form_data: dict) -> None:
    """
    Función principal de actualización de la lógica del formulario.
    Delega el manejo de eventos y estado de los widgets.
    Args: -form_data (dict): El diccionario del formulario actual.
    Returns: No retorna nada.
    """
    update_widgets(form_data)

def draw(form_data: dict) -> None:
    """
    Función principal de dibujo del formulario. 
    Dibuja primero el fondo y luego delega el dibujo de los widgets.
    Args: -form_data (dict): El diccionario del formulario actual.
    Returns: No retorna nada.
    """
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))