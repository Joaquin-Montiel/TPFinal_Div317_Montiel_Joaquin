import pygame as pg, sys 
import modules.forms.form_base as base_form
import modules.variables as var
import modules.forms.form_stage as stage
from utn_fra.pygame_widgets import(
    Label, ButtonSound
)

def create_form_menu(dict_form_data: dict) -> dict:
    """
    Crea el formulario principal del juego (Menú). Inicializa todos los widgets 
    (títulos y botones de navegación) y los agrega a la lista global de formularios.
    Args: -dict_form_data (dict): Diccionario con datos de inicialización (screen, background, etc.).
    Returns: -dict: El diccionario del formulario de Menú.
    """
    form = base_form.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=110,
                            text='Las Cartas del Dragon', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=45)
    
    form['lbl_subtitulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=180,
                            text='Menu Principal', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=45)
    
    form['btn_play'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=390,
        text='JUGAR', screen=form.get('screen'),
        sound_path=var.PATH_SOUND_BUTTON, font_path=var.PATH_SAIYAN, font_size=45,
        on_click=iniciar_stage, on_click_param='form_stage'
    )

    form['btn_ranking'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=450,
        text='RANKING', screen=form.get('screen'),
        sound_path=var.PATH_SOUND_BUTTON, font_path=var.PATH_SAIYAN, font_size=45,
        on_click=base_form.cambiar_pantalla, on_click_param='form_ranking'
    )
    
    form['btn_configs'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=570,
        text='CONFIGURACION', screen=form.get('screen'),
        sound_path=var.PATH_SOUND_BUTTON, font_path=var.PATH_SAIYAN, font_size=45,
        on_click=base_form.cambiar_pantalla, on_click_param='form_configs'
    )

    form['btn_exit'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=630,
        text='SALIR', screen=form.get('screen'),
        sound_path=var.PATH_SOUND_BUTTON, font_path=var.PATH_SAIYAN, font_size=45,
        on_click=salir_juego, on_click_param=None
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_play'),
        form.get('btn_ranking'),
        form.get('btn_configs'),
        form.get('btn_exit')
    ]

    var.dict_form_status[form.get('name')] = form
    return form

def iniciar_stage(form_name: str) -> None:
    """
    Callback para el botón 'JUGAR'. 
    Realiza el cambio de pantalla a la etapa de juego y llama a la lógica de inicialización 
    de una nueva partida.
    Args: -form_name (str): El nombre del formulario de destino ('form_stage').
    Returns: No retorna nada.
    """
    base_form.cambiar_pantalla(form_name)
    stage_form = var.dict_form_status.get(form_name)
    stage.iniciar_nueva_partida(stage_form)
    print('Estamos presionando el boton JUGAR')

def salir_juego(_) -> None:
    """
    Callback para el botón 'SALIR'. Termina la ejecución de Pygame.
    Args: _(Any): Argumento dummy requerido por el callback del widget.
    Returns: No retorna nada.
    """
    print('Saliendo del juego desde el boton')
    pg.quit()
    sys.exit()

def draw(dict_form_data: dict) -> None:
    """
    Dibuja el formulario de Menú: fondo y todos los widgets.
    Args: -dict_form_data (dict): El diccionario del formulario de Menú.
    Returns: No retorna nada.
    """
    base_form.draw(dict_form_data)
    base_form.draw_widgets(dict_form_data)

def update(dict_form_data: dict) -> None:
    """
    Función de actualización del Menú. Delega el manejo de eventos a la base.
    Args: -dict_form_data (dict): El diccionario del formulario de Menú.
    Returns: No retorna nada.
    """
    base_form.update(dict_form_data)
