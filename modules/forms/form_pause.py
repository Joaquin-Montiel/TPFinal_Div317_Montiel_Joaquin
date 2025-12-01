import pygame as pg, sys 
import modules.forms.form_base as base_form
import modules.variables as var
import modules.forms.form_stage as stage_form
import modules.sounds as sound
from utn_fra.pygame_widgets import(
    Label, ButtonSound
)

def create_form_pause(dict_form_data: dict) -> dict:
    """
    Crea el formulario de Pausa. Inicializa los botones de control de la partida 
    y la variable para guardar el volumen de fondo al entrar.
    Args: -dict_form_data (dict): Datos de inicialización (screen, background, etc.).
    Returns: -dict: El diccionario del formulario 'form_pause'.
    """

    form = base_form.create_base_form(dict_form_data)
    form['last_volume'] = None

    form['lbl_titulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=120,
                            text=var.TITLE_GAME, screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=55)
    form['lbl_subtitulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=190,
                            text='PAUSE', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=50)
    
    form['btn_resume'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=330,
        text='RESUME', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=35,
        on_click=resume_game, on_click_param={"form": form}
    )

    form['btn_restart'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=375,
        text='RESTART STAGE', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=35,
        on_click=restart_stage, on_click_param={"form": form, "form_name": 'form_stage'}
    )
    form['btn_back'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=420,
        text='BACK TO MENU', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=35,
        on_click=base_form.cambiar_pantalla, on_click_param='form_menu'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_resume'),
        form.get('btn_restart'),
        form.get('btn_back')
    ]

    var.dict_form_status[form.get('name')] = form
    return form

def resume_game(params: dict) -> None:
    """
    Callback para el botón 'RESUME'. Vuelve a la pantalla de juego y restaura 
    el volumen de la música guardado antes de entrar a la pausa.
    Args: params (dict): Diccionario que contiene el formulario ('form') y datos del botón.
    Returns: No retorna nada.
    """
    form_pause = params.get("form")
    last_vol = form_pause.get("last_volume")

    if last_vol is not None:
        sound.set_volume(last_vol)

    sound.set_music_path(var.MUSIC_STAGE)
    sound.play_music()

    base_form.cambiar_pantalla("form_stage")
    base_form.set_active("form_stage")

def restart_stage(params: dict) -> None:
    """
    Callback para el botón 'RESTART STAGE'. Reinicia los datos de la partida 
    y vuelve a la pantalla de juego.
    Args: -params (dict): Contiene el formulario ('form') y el nombre de la pantalla ('form_name').
    Returns: No devuelve nada.
    """
    form_pause = params.get("form")
    last_vol = form_pause.get("last_volume")

    if last_vol is not None:
        sound.set_volume(last_vol)

    sound.set_music_path(var.MUSIC_STAGE)
    sound.play_music()

    base_form.cambiar_pantalla("form_stage")
    base_form.set_active("form_stage")

    form_stage = var.dict_form_status.get("form_stage")
    stage_form.iniciar_nueva_partida(form_stage)


def set_last_vol(vol: int) -> None:
    """
    Setter para el volumen del mixer de Pygame. Se usa para bajar el volumen 
    al entrar en la pausa.
    Args: -vol (int): El nivel de volumen a setear (0-100).
    Returns: No retorna nada.
    """
    if vol is None:
        return  
    sound.set_volume(vol)

def save_last_vol(form_dict_data: dict) -> None:
    """
    Guarda el volumen actual del juego en el diccionario del formulario de pausa.
    Luego, setea el volumen bajo para la pantalla de pausa.
    Args: -form_dict_data (dict): El diccionario del formulario de pausa.
    Returns: No retorna nada.
    """
    form_dict_data['last_volume'] = sound.get_actual_vol()
    set_last_vol(10)


def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Pausa: fondo y todos los widgets.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict) -> None:
    """
    Función de actualización del formulario. Delega el manejo de eventos a la base.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.update(form_dict_data)