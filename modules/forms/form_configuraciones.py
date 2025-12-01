import pygame as pg
import modules.forms.form_base as base_form
import modules.variables as var
import modules.sounds as sound
from utn_fra.pygame_widgets import(
    Label, ButtonSound
)

def create_form_configs(dict_form_data: dict) -> dict:
    """
    Crea el formulario de Configuraciones. Inicializa los widgets para controlar 
    la activación/desactivación de la música y el nivel de volumen.
    Args: -dict_form_data (dict): Diccionario con datos de inicialización.
    Returns: -dict: El diccionario del formulario de Configuraciones.
    """
    form = base_form.create_base_form(dict_form_data)
    
    form['lbl_titulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=135,
                            text='Configuraciones', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=70)
    
    form['btn_music_on'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=345,
        text='MUSIC ON', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=40,
        on_click=activar_music, on_click_param=form)

    form['btn_music_off'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=395,
        text='MUSIC OFF', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=40,
        on_click=deactivate_music, on_click_param=form)
    
    form['lbl_volumen'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=450,
                            text=f'{sound.get_actual_vol()}', screen=form.get('screen'),
                            font_path=var.PATH_SUPER_MARIO, font_size=30)
    
    form['btn_vol_down'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2 - 70, y=450,
        text='<', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SUPER_MARIO, font_size=30,
        on_click=modificar_vol, on_click_param=(-10))
    
    form['btn_vol_up'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2 + 70, y=450,
        text='>', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SUPER_MARIO, font_size=30,
        on_click=modificar_vol, on_click_param=10)
    
    form['btn_volver'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=500,
        text='VOLVER', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=40,
        on_click=cambiar_pantalla, on_click_param='form_menu')
    
    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_music_on'),
        form.get('btn_music_off'),
        form.get('lbl_volumen'),
        form.get('btn_vol_down'),
        form.get('btn_vol_up'),
        form.get('btn_volver')
    ]

    var.dict_form_status[form.get('name')] = form
    return form

def modificar_vol(volumen: int) -> None:
    """
    Callback para los botones de volumen (< y >). Modifica el volumen actual 
    del mixer de Pygame en pasos de +/- 10 unidades (escala de 0 a 100).
    Args: -volumen (int): La cantidad a sumar o restar (-10 o +10).
    Returns: No retorna nada.
    """
    volumen_actual = sound.get_actual_vol()
    if volumen_actual > 0 and volumen < 0 or\
        volumen_actual < 100 and volumen > 0:
        volumen_actual += volumen
        sound.set_volume(volumen_actual)

def activar_music(form_dict_data: dict) -> None:
    """
    Callback para el botón 'MUSIC ON'. Habilita la bandera global de música 
    y llama a music_on para iniciar la reproducción del formulario actual.
    Args: -form_dict_data (dict): El formulario (para pasar a base_form.music_on).
    Returns: No retorna nada.
    """
    var.MUSIC_ENABLED = True
    base_form.music_on(form_dict_data)

def deactivate_music(_) -> None:
    """
    Callback para el botón 'MUSIC OFF'. Deshabilita la bandera global de música 
    y detiene la reproducción.
    Args: _ (Any): Argumento dummy del callback.
    Returns: No retorna nada.
    """
    var.MUSIC_ENABLED = False
    
    base_form.music_off()
    sound.stop_music()

def cambiar_pantalla(form_name: str) -> None:
    """
    Callback para el botón 'VOLVER'. Cambia la pantalla a la especificada.
    Args: -form_name (str): El nombre del formulario de destino ('form_menu').
    Returns: No retorna nada.
    """
    base_form.set_active(form_name)

def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Configuraciones: fondo y todos los widgets.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict) -> None:
    """
    Función de actualización del formulario. Su principal función es actualizar 
    el Label que muestra el volumen actual en cada frame, ya que este valor 
    puede ser modificado por los botones VOL + / VOL -.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    lbl_vol: Label = form_dict_data.get('widgets_list')[3]
    lbl_vol.update_text(text=f'{sound.get_actual_vol()}', color=pg.Color('red'))
    base_form.update(form_dict_data)