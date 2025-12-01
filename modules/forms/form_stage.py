import pygame as pg
import modules.forms.form_base as base_form
import modules.forms.form_wish as wish
import modules.variables as var
import modules.carta as carta
import modules.player_juego as particip
import modules.stage as stage_juego
import modules.sounds as sound
import modules.forms.form_name as name
from utn_fra.pygame_widgets import(
    Label, ButtonImageSound
)

def crear_form_stage(dict_form_data: dict):
    """
    Crea el formulario de la Etapa de Juego. Inicializa todos los 
    widgets estáticos (Stats, Timer, Score) y los botones de acción y bonus (Heal/Shield).
    Args: -dict_form_data (dict): Datos de inicialización (screen, background, etc.).
    Returns: -dict: El diccionario del formulario 'form_stage'.
    """
    form = base_form.create_base_form(dict_form_data)

    form["stage_restart"] = False
    form["time_finished"] = False
    form["actual_level"] = 1

    form["stage"] = stage_juego.initialize_stage(pantalla=form.get('screen'), nro_stage=form.get('actual_level'))
    form["jugador"] = form['stage']['jugador']
    form["clock"] = pg.time.Clock()

    form['lbl_timer'] = Label(
        x=50, y=25,
        text=f'{stage_juego.obtener_tiempo(form.get("stage"))}', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_SUPER_MARIO, font_size=30)
    form['lbl_score'] = Label(
        x=745, y=25,
        text=f'Score: 0', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_SUPER_MARIO, font_size=30, color=var.colores.get('rosa')
    )
    form['lbl_carta_e'] = Label(
        x=300, y=360,
        text=f'HP: ATK: DEF:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_SUPER_MARIO, font_size=20, color=var.colores.get('verde')
    )
    form['lbl_carta_j'] = Label(
        x=300, y=710,
        text=f'HP: ATK: DEF:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_SUPER_MARIO, font_size=20, color=var.colores.get('verde')
    )
    #STAT Enemigo
    form['lbl_enemigo_hp'] = Label(
        x=100, y=190,
        text=f'HP:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('rojo')
    )
    form['lbl_enemigo_atk'] = Label(
        x=100, y=220,
        text=f'ATK:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('rojo')
    )
    form['lbl_enemigo_def'] = Label(
        x=100, y=250,
        text=f'DEF:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('rojo')
    )
    form['lbl_cartas_restantes_e'] = Label(
        x=100, y=295,
        text=f'Restan: ', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('rojo')
    )
    #STAT Jugador
    form['lbl_jugador_hp'] = Label(
        x=100, y=540,
        text=f'HP:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('verde')
    )
    form['lbl_jugador_atk'] = Label(
        x=100, y=570,
        text=f'ATK:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('verde')
    )
    form['lbl_jugador_def'] = Label(
        x=100, y=600,
        text=f'DEF:', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('verde')
    )
    form['lbl_cartas_restantes_j'] = Label(
        x=100, y=650,
        text=f'Restan: ', screen=form.get('screen'),
        align='topleft', font_path=var.PATH_ALAGARD, font_size=20, color=var.colores.get('verde')
    )

    form['btn_play_game'] = ButtonImageSound(
        x=var.DIMENSION_SCREEN[0] // 2 + 450, y=var.DIMENSION_SCREEN[0] // 2 - 100,
        width=var.WIDTH, height=var.HEIGHT, text='', screen=form.get('screen'),
        image_path=var.PATH_BUTTON_PLAY, sound_path=var.PATH_SOUND_BUTTON,
        font_size=35, on_click=jugar_mano, on_click_param=form)
    
    #Bonus
    form['btn_heal'] = ButtonImageSound(
        x=var.DIMENSION_SCREEN[0] // 2 + 450, y=var.DIMENSION_SCREEN[0] // 2 + 100,
        width=var.W_B, height=var.H_B, text='HEAL', screen=form.get('screen'),
        image_path=var.PATH_BUTTON_HEAL, sound_path=var.PATH_SOUND_BUTTON,
        font_size=35, on_click=call_wish_form, on_click_param={'form': form ,'wish':'HEAL'})
    
    form['btn_shield'] = ButtonImageSound(
        x=var.DIMENSION_SCREEN[0] // 2 + 450, y=var.DIMENSION_SCREEN[0] // 2 + 170,
        width=var.W_B, height=var.H_B ,text='SHIELD', screen=form.get('screen'),
        image_path=var.PATH_BUTTON_SHIELD, sound_path=var.PATH_SOUND_BUTTON,
        font_size=35, on_click=call_wish_form, on_click_param={'form': form ,'wish':'SHIELD'})

    form['widgets_list'] = [
        form.get('lbl_timer'),
        form.get('lbl_score'),
        form.get('lbl_carta_e'),
        form.get('lbl_carta_j'),
        form.get('lbl_enemigo_hp'),
        form.get('lbl_enemigo_atk'),
        form.get('lbl_enemigo_def'),
        form.get('lbl_cartas_restantes_e'),
        form.get('lbl_jugador_hp'),
        form.get('lbl_jugador_atk'),
        form.get('lbl_jugador_def'),
        form.get('lbl_cartas_restantes_j'),
        form.get('btn_play_game')
    ]

    form['widgets_list_bonus'] = [
        form.get('btn_heal'),
        form.get('btn_shield')
    ]

    var.dict_form_status[form.get('name')] = form
    return form


def jugar_mano(form_dict_data: dict) -> None:
    """
    Callback para el botón 'PLAY'. Ejecuta la lógica de una sola ronda de batalla.
    Compara el ataque de las cartas, resta stats y verifica si la partida termina.
    Args: -form_dict_data (dict): El diccionario del formulario 'form_stage'.
    Returns: No retorna nada.
    """
    stage = form_dict_data.get('stage')

    resultado = stage_juego.jugar_mano(stage)

    if resultado is None:
        if stage_juego.esta_finalizado(stage):
            mostrar_form_name(stage)
        return 

    critical, ganador_mano = resultado
    print(f'El ganador de la mano es: {ganador_mano}')

def mostrar_form_name(stage) -> None:
    """
    Función que se llama cuando la partida termina. Calcula el resultado final 
    (VICTORIA/DERROTA/EMPATE) y redirige a la pantalla de Ingreso de Nombre ('form_name').
    Args: -stage (dict): El diccionario del Stage que contiene 'jugador', 'ganador', etc.
    Returns: No retorna nada.
    """
    ganador = stage_juego.obtener_ganador(stage)
    form_name = var.dict_form_status.get('form_name')

    jugador = stage.get('jugador')
    score_final = particip.get_score_player(jugador)

    form_name['jugador'] = jugador

    if ganador is None:
        name.update_texto_victoria(form_name, 'EMPATE', score_final)
        base_form.set_active('form_name')
        return
    elif particip.get_nombre_player(ganador) != 'Enemigo':
        name.update_texto_victoria(form_name, 'VICTORIA', score_final)
        base_form.set_active('form_name')
        return
    else:
        name.update_texto_victoria(form_name, 'DERROTA', score_final)
        base_form.set_active("form_name")


def iniciar_nueva_partida(form_dict_data: dict) -> None:
    """
    Llamado desde el menú (JUGAR) o el menú de pausa (RESTART). 
    Inicializa todos los datos del Stage y el mazo.
    Args: -form_dict_data (dict): El diccionario del formulario 'form_stage'.
    Returns: No retorna nada.
    """
    pantalla = form_dict_data.get('screen')
    nivel = form_dict_data['stage']['nro_stage']
    form_dict_data['stage'] = stage_juego.restar_stage(pantalla=pantalla, nro_stage=nivel)
    form_dict_data['jugador'] = form_dict_data['stage']['jugador']

def call_wish_form(params: dict) -> None:
    """
    Callback para los botones HEAL y SHIELD. Muestra el formulario de Wish 
    (donde el usuario puede confirmar o cancelar el uso del comodín).
    Args: -params (dict): Contiene el formulario ('form') y el tipo de deseo ('wish':'HEAL'/'SHIELD').
    Returns: No retorna nada.
    """
    form_dict_data = params.get('form')
    wish_type = params.get('wish')

    wish_form = var.dict_form_status.get('form_wish')

    wish.update_wish_type(wish_form, wish_type)
    base_form.cambiar_pantalla('form_wish')


def update_score(form_dict_data: dict) -> None:
    """
    Actualiza el Label del Score total en la interfaz.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    participante = form_dict_data.get('stage').get('jugador')
    score = participante.get('score')
    form_dict_data.get('lbl_score').update_text(text=f'Score: {score}', color=var.colores.get('rosa'))

def update_info_card(form_dict_data: dict) -> None:
    """
    Actualiza los Labels que muestran el HP/ATK/DEF de la última carta jugada 
    tanto por el jugador como por el enemigo.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    mazo_enemigo = form_dict_data.get('stage').get('enemigo').get('cartas_mazo_usadas')
    mazo_jugador = form_dict_data.get('stage').get('jugador').get('cartas_mazo_usadas')

    if mazo_enemigo and mazo_jugador:

        ultima_carta_e = particip.get_carta_actual_player(form_dict_data.get('stage').get('enemigo'))
        ultima_carta_j = particip.get_carta_actual_player(form_dict_data.get('stage').get('jugador'))

        form_dict_data['lbl_carta_e'].update_text(
            f"HP: {carta.get_hp_carta(ultima_carta_e)} ATK: {carta.get_atk_carta(ultima_carta_e)} DEF: {carta.get_def_carta(ultima_carta_e)}",
            var.colores.get('rojo')
        )
        form_dict_data['lbl_carta_j'].update_text(
            f"HP: {carta.get_hp_carta(ultima_carta_j)} ATK: {carta.get_atk_carta(ultima_carta_j)} DEF: {carta.get_def_carta(ultima_carta_j)}",
            var.colores.get('verde')
        )

def update_lbl_jugador(form_dict_data: dict, tipo_jugador, color: str = 'rojo') -> None:
    """
    Actualiza los Labels que muestran las estadísticas totales (HP, ATK, DEF) 
    del participante (jugador o enemigo).
    Args: -form_dict_data (dict): El diccionario del formulario.
        -tipo_jugador (str): Clave para acceder al participante ('jugador' o 'enemigo').
        -color (str): Color para el texto (ej. 'verde' para jugador, 'rojo' para enemigo).
    Returns: No retorna nada.
    """
    participante = form_dict_data.get('stage').get(tipo_jugador)

    form_dict_data[f'lbl_{tipo_jugador}_hp'].update_text(text=f'HP: {particip.get_hp_player(participante)}', color=var.colores.get(color))
    form_dict_data[f'lbl_{tipo_jugador}_atk'].update_text(text=f'ATK: {particip.get_attack_player(participante)}', color=var.colores.get(color))
    form_dict_data[f'lbl_{tipo_jugador}_def'].update_text(text=f'DEF: {particip.get_defense_player(participante)}', color=var.colores.get(color))

def events_handler(events: list[pg.event.Event]) -> None:
    """
    Maneja eventos específicos del Stage, como la pausa del juego (tecla ESCAPE).
    Args: -events (list[pg.event.Event]): Lista de eventos de Pygame.
    Returns: No retorna nada.
    """
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                form_pause = var.dict_form_status['form_pause']
                form_pause['last_volume'] = sound.get_actual_vol()

                base_form.cambiar_pantalla("form_pause")
                base_form.set_active('form_pause')

def draw_bonus_widgets(form_dict_data: dict) -> None:
    """
    Dibuja los botones de Heal y Shield solo si están disponibles para el jugador 
    en el Stage actual.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    widget_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')
    if stage.get('heal_available'):
        widget_bonus[0].draw()
    if stage.get('shield_available'):
        widget_bonus[1].draw()

def update_bonus_widgets(form_dict_data) -> None:
    """
    Actualiza los botones de Heal y Shield solo si están disponibles.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    widget_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')
    if stage.get('heal_available'):
        widget_bonus[0].update()
    if stage.get('shield_available'):
        widget_bonus[1].update()

def update_cartas_restantes(form_dict_data) -> None:
    """
    Actualiza los Labels que muestran la cantidad de cartas restantes en el mazo 
    de cada participante.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    stage = form_dict_data.get('stage')

    jugador = stage.get('jugador')
    enemigo = stage.get('enemigo')

    cartas_j = len(particip.get_cartas_restantes_player(jugador))
    cartas_e = len(particip.get_cartas_restantes_player(enemigo))

    form_dict_data['lbl_cartas_restantes_j'].update_text(
        text=f'Cartas: {cartas_j}', color=var.colores.get('verde')
    )

    form_dict_data['lbl_cartas_restantes_e'].update_text(
        text=f'Cartas: {cartas_e}', color=var.colores.get('rojo')
    )

def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Stage (Batalla). Dibuja el fondo, las cartas jugadas, 
    los widgets estáticos y los botones de bonus.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.draw(form_dict_data)
    stage_juego.draw_jugadores(form_dict_data.get('stage'))
    base_form.draw_widgets(form_dict_data)
    draw_bonus_widgets(form_dict_data)

def update(form_dict_data: dict, eventos: list[pg.event.Event]) -> None:
    """
    Función principal de actualización del Stage, llamada en cada frame del game loop.
    Controla el timer, la lógica de la partida, actualiza la interfaz y maneja la finalización.
    Args: -form_dict_data (dict): El diccionario del formulario.
        -eventos (list[pg.event.Event]): Lista de eventos de Pygame.
    Returns: No retorna nada.
    """
    form_dict_data['lbl_timer'].update_text(f'{stage_juego.obtener_tiempo(form_dict_data.get("stage"))}', var.colores.get('rosa'))

    base_form.update(form_dict_data)
    resultado = stage_juego.update(form_dict_data.get('stage'))
    if resultado == "FINISHED":
        mostrar_form_name(form_dict_data.get('stage'))
        return

    update_info_card(form_dict_data)
    update_lbl_jugador(form_dict_data, tipo_jugador='jugador', color='verde')
    update_score(form_dict_data)
    update_lbl_jugador(form_dict_data, tipo_jugador='enemigo', color='rojo')
    update_cartas_restantes(form_dict_data)
    update_bonus_widgets(form_dict_data)
    events_handler(eventos)


