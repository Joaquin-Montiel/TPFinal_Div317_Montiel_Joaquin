import pygame as pg, sys 
import modules.forms.form_base as base_form
import modules.variables as var
import modules.auxiliary_functions as aux
import modules.forms.form_stage as stage
import modules.player_juego as participante
from utn_fra.pygame_widgets import(
    Label, ButtonSound, TextBoxSound
)

def create_form_name(dict_form_data: dict) -> dict:
    """
    Crea el formulario de Ingreso de Nombre (Post-partida). Inicializa los fondos 
    dinámicos y el TextBox para capturar el nombre del jugador.
    Args: -dict_form_data (dict): Datos de inicialización (screen, background, etc.).
    Returns: -dict: El diccionario del formulario 'form_name'.
    """
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = None
    form['info_submitida'] = False

    form['bg_default'] = form['surface']
    form['bg_win'] = pg.transform.scale(pg.image.load(var.PATH_NAME_WIN),var.DIMENSION_SCREEN)
    form['bg_lose'] = pg.transform.scale(pg.image.load(var.PATH_NAME_LOSE),var.DIMENSION_SCREEN)
    form['bg_draw'] = pg.transform.scale(pg.image.load(var.PATH_NAME_DRAW),var.DIMENSION_SCREEN)

    form['background_actual'] = form['bg_default']

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_SCREEN[0] // 2, y=200,
        text='Victoria!', screen=form.get('screen'),
        font_path=var.PATH_SAIYAN, font_size=60, color=var.colores.get('rojo'))
        
    form['lbl_score'] = Label(
        x=var.DIMENSION_SCREEN[0] // 2, y=300,
        text=f'{0}', screen=form.get('screen'),
        font_path=var.PATH_SUPER_MARIO, font_size=40, color=var.colores.get('rojo')
        )

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_SCREEN[0] // 2, y=360,
        text='Escriba su nombre', screen=form.get('screen'),
        font_path=var.PATH_SAIYAN, font_size=45, color=var.colores.get('rojo')
        )
    
    form['lbl_nombre_texto'] = Label(
        x=var.DIMENSION_SCREEN[0] // 2, y=415,
        text='', screen=form.get('screen'),
        font_path=var.PATH_SAIYAN, font_size=40, color=var.colores.get('rojo')
        )
    
    form['text_box'] = TextBoxSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=430,
        text=f'________', screen=form.get('screen'),
        sound_path=var.PATH_SOUND_WRITE, font_path=var.PATH_SUPER_MARIO, font_size=45, color=var.colores.get('negro')
    )

    form['btn_submit'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=490,
        text='CONFIRMAR', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON, 
        font_path=var.PATH_SAIYAN, font_size=45, color=var.colores.get('rojo'),
        on_click=submit_name, on_click_param=form
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_score'),
        form.get('lbl_subtitulo'),
        form.get('lbl_nombre_texto'),
        form.get('btn_submit')
    ]

    var.dict_form_status[form.get('name')] = form
    return form

def update_texto_victoria(form_dict_data: dict, win_status: bool, score: int) -> None:
    """
    Actualiza dinámicamente el fondo de la pantalla y el texto del título/score 
    según el resultado de la partida (VICTORIA, DERROTA, EMPATE).
    Args: -form_dict_data (dict): El diccionario del formulario 'form_name'.
        -win_status (str): El resultado de la partida.
        -score (int): El puntaje final.
    Returns: No devuelve nada.
    """
    if win_status == 'VICTORIA':
        form_dict_data['background_actual'] = form_dict_data['bg_win']
        
    elif win_status == 'DERROTA':
        form_dict_data['background_actual'] = form_dict_data['bg_lose']
    elif win_status == 'EMPATE':
        form_dict_data['background_actual'] = form_dict_data['bg_draw']
    else:
        form_dict_data['background_actual'] = form_dict_data['bg_default']
        
    form_dict_data['lbl_titulo'].update_text(text=win_status, color=var.colores.get('rojo'))
    form_dict_data['lbl_score'].update_text(text=f'SCORE: {score}', color=var.colores.get('rojo'))

def clear_text(form_data: dict) -> None:
    """
    Limpia el texto de entrada del TextBox.
    Args: -form_data (dict): El diccionario del formulario 'form_name'.
    Returns: No devuelve nada.
    """
    form_data['text_box'].writing = ''

def submit_name(form_data: dict) -> None:
    """
    Callback para el botón 'CONFIRMAR'. Setea el nombre del jugador, 
    guarda la información en el archivo CSV de ranking, y cambia a la pantalla de Ranking.
    Args: -form_data (dict): El diccionario del formulario 'form_name'.
    Returns: No retorna nada.
    """
    
    jugador = form_data.get('jugador')
    if not jugador:
        print("ERROR: jugador no seteado en form_name")
        return

    nombre_jugador = form_data.get('lbl_nombre_texto').text
    participante.set_nombre_player(jugador, nombre_jugador)
    nombre_jugador_seteado = participante.get_nombre_player(form_data.get('jugador'))
    puntaje_jugador = participante.get_score_player(form_data.get('jugador'))
    print(f'nombre jugador: {nombre_jugador_seteado} - {puntaje_jugador}')

    data_to_csv = participante.info_csv(jugador)
    aux.save_info_csv(data_to_csv)

    form_data['info_submitida'] = True
    base_form.set_active('form_ranking')

def update(form_dict_data: dict, event_list: list[pg.event.Event]) -> None:
    """
    Función de actualización principal. Maneja la entrada de teclado (TextBox) 
    y actualiza los Labels del score y del texto escrito en cada frame.
    Args: -form_dict_data (dict): El diccionario del formulario.
        -event_list (list[pg.event.Event]): Lista de eventos de Pygame.
    Returns: No retorna nada.
    """
    jugador = form_dict_data.get('jugador')
    if jugador:
        score = participante.get_score_player(jugador)

    form_dict_data.get('widgets_list')[1].update_text(text=f'SCORE: {score}', color=var.colores.get('rojo'))
    form_dict_data.get('widgets_list')[3].update_text(text=f'{form_dict_data.get("text_box").writing.upper()}', color=var.colores.get('rojo'))

    form_dict_data.get('text_box').update(event_list)
    base_form.update(form_dict_data)

def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Ingreso de Nombre. Dibuja el fondo dinámico (win/lose/draw) 
    y luego dibuja todos los widgets, incluyendo el TextBox que se maneja por separado.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    form_dict_data['screen'].blit(form_dict_data['background_actual'], (0, 0))

    for widget in form_dict_data.get('widgets_list'):
        widget.draw()

    form_dict_data.get('text_box').draw()
