import pygame as pg
import random as rd
import modules.variables as var
import modules.carta as carta
import modules.player_juego as participante
import modules.auxiliary_functions as aux

def initialize_stage( pantalla: pg.Surface, nro_stage: int) -> dict:
    """
    Inicializa el diccionario principal del Stage (área de juego). Crea las estructuras 
    de datos para la partida, los jugadores y los flags de bonus.
    Args: -pantalla (pg.Surface): La superficie de Pygame.
        -nro_stage (int): El número de nivel actual.
    Returns: -dict: El diccionario stage_data inicializado.
    """
    stage_data = {}
    stage_data['nro_stage'] = nro_stage
    stage_data['configs'] = {}
    stage_data['data_cargada'] = False

    stage_data['cartas_mazo_inicial_e'] = []
    stage_data['cartas_mazo_inicial_j'] = []
    stage_data['cartas_mazo_preparadas_e'] = []
    stage_data['cartas_mazo_preparadas_j'] = []
    
    stage_data['ruta_mazo'] = ''
    stage_data['screen'] = pantalla

    stage_data['jugador'] = participante.initialize_player(pantalla, nombre='Player')
    stage_data['enemigo'] = participante.initialize_player(pantalla, nombre='Enemigo')
    
    stage_data['cantidad_cartas_jugadores'] = 0

    stage_data['heal_available'] = True
    stage_data['shield_available'] = True

    stage_data['juego_finalizado'] = False
    stage_data['puntaje_guardado'] = False
    stage_data['last_timer'] = pg.time.get_ticks()
    stage_data['ganador'] = None

    return stage_data

def timer_update(stage_data: dict) -> None:
    """
    Controla el decremento del temporizador de la partida (cada 1 segundo).
    Args: -stage_data (dict): El diccionario del Stage.
    Returns: No retorna nada.
    """
    if stage_data['stage_timer'] > 0:
        tiempo_actual = pg.time.get_ticks()

        if tiempo_actual - stage_data['last_timer'] > 1000:
            stage_data['stage_timer'] -= 1
            stage_data['last_timer'] = tiempo_actual

def obtener_tiempo(stage_data: dict):
    """Retorna el tiempo restante de la partida."""
    return stage_data.get('stage_timer')

def restar_stage(pantalla: pg.Surface, nro_stage: int) -> dict:
    """
    Reinicia el Stage a un nuevo estado de partida ( Stage Restart ).
    Llama a la inicialización y a la carga de datos.
    Args: -pantalla (pg.Surface): Superficie de Pygame.
        -nro_stage (int): Número del nivel actual.
    Returns: -dict: El nuevo diccionario stage_data.
    """
    stage_data = initialize_stage(pantalla, nro_stage)

    initialize_data_stage(stage_data)
    return stage_data

def initialize_data_stage(stage_data: dict) -> None:
    """
    Secuencia completa de inicialización de datos y configuraciones del Stage.
    """
    print('Estoy cargando los datos del stage')
    aux.load_configs_stage(stage_data) 
    aux.load_bd_cartas(stage_data)

    participante.setear_stat_player(stage_data.get('enemigo'), 'pos_carta_inicial', stage_data.get('coods_inicial_mazo_enemigo'))
    participante.setear_stat_player(stage_data.get('enemigo'), 'pos_carta_jugada', stage_data.get('coods_final_mazo_enemigo'))

    participante.setear_stat_player(stage_data.get('jugador'), 'pos_carta_inicial', stage_data.get('coods_inicial_mazo_player'))
    participante.setear_stat_player(stage_data.get('jugador'), 'pos_carta_jugada', stage_data.get('coods_final_mazo_player'))

    generar_mazo(stage_data)
    barajar_mazo(stage_data)

def generar_mazo(stage_data: dict) -> None:
    """
    Inicializa los objetos Carta a partir de los diccionarios de stats cargados 
    (cartas_mazo_inicial_e/j) y los agrega a las listas de cartas preparadas.
    """
    for carta_inicial_e, carta_inicial_j in zip(
        stage_data.get('cartas_mazo_inicial_e'),
        stage_data.get('cartas_mazo_inicial_j')
    ):
        carta_power_e = carta.inicializar_carta(carta_inicial_e, (0,0))
        carta_power_j = carta.inicializar_carta(carta_inicial_j, (0,0))
        stage_data.get('cartas_mazo_preparadas_e').append(carta_power_e)
        stage_data.get('cartas_mazo_preparadas_j').append(carta_power_j)

def barajar_mazo(stage_data: dict) -> None:
    """
    Baraja las cartas preparadas y las asigna a los mazos de juego del Jugador y Enemigo.
    Luego, calcula y asigna los stats totales iniciales (HP, ATK, DEF) a cada participante.
    """
    if not stage_data.get('juego_finalizado'):
        asignar_cartas_stage(stage_data, stage_data.get('jugador'))
        asignar_cartas_stage(stage_data, stage_data.get('enemigo'))

        participante.asignar_stats_iniciales_player(stage_data.get('jugador'))
        participante.asignar_stats_iniciales_player(stage_data.get('enemigo'))

        stage_data['data_cargada'] = True

def asignar_cartas_stage(stage_data: dict, participante_j: dict) -> None:
    """
    Asigna una porción de cartas preparadas al mazo de un participante (Jugador o Enemigo).
    Args:-stage_data (dict): El diccionario del Stage.
        -participante_j (dict): El diccionario del participante (jugador o enemigo).
    Returns: No retorna nada.
    """
    cant_cartas = stage_data.get('cantidad_cartas_jugadores')
    if participante.get_nombre_player(participante_j) != 'Enemigo':
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_j'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_j')[:cant_cartas]
    else:
        rd.shuffle(stage_data.get('cartas_mazo_preparadas_e'))
        cartas_participante = stage_data.get('cartas_mazo_preparadas_e')[:cant_cartas]

    participante.set_cartas_player(participante_j, cartas_participante)


def modificar_estado_bonus(stage_data: dict, bonus: str) -> None:
    """
    Deshabilita un comodín (HEAL o SHIELD) una vez que ha sido usado,
    cambiando su flag de 'available' a False.
    Args: -stage_data (dict): El diccionario del Stage.
        -bonus (str): El tipo de bonus a deshabilitar ('heal' o 'shield').
    Returns: No retorna nada.
    """
    stage_data[f'{bonus}_available'] = False


def hay_jugadores_con_cartas(stage_data: dict) -> bool:
    """Verifica si al menos un participante aún tiene cartas en su mazo de juego."""
    jugador_con_cartas = participante.get_cartas_restantes_player(stage_data.get('jugador'))
    enemigo_con_cartas = participante.get_cartas_restantes_player(stage_data.get('enemigo'))
    return jugador_con_cartas or enemigo_con_cartas

def setear_ganador(stage_data: dict, player: dict) -> None:
    """Establece el diccionario del ganador y activa el flag de juego finalizado.""" 
    stage_data['ganador'] = player
    stage_data['juego_finalizado'] = True

def get_stats(stage_data: dict) -> tuple:
    """
    Retorna las estadísticas clave necesarias para chequear las condiciones de victoria.
    Returns: -tuple: (jugador_dict, enemigo_dict, hp_jugador, hp_enemigo, cartas_restantes_j, cartas_restantes_e)
    """
    jugador = stage_data['jugador']
    enemigo = stage_data['enemigo']

    hp_j = participante.get_hp_player(jugador)
    hp_e = participante.get_hp_player(enemigo)

    cartas_j = len(participante.get_cartas_restantes_player(jugador))
    cartas_e = len(participante.get_cartas_restantes_player(enemigo))

    return jugador, enemigo, hp_j, hp_e, cartas_j, cartas_e


def check_win_by_time(stage_data: dict) -> str | None:
    """
    Verifica la condición de victoria por tiempo agotado. Gana el participante 
    con mayor HP si el tiempo llega a 0.
    """
    tiempo = stage_data.get('stage_timer')
    jugador, enemigo, hp_j, hp_e, cartas_j, cartas_e = get_stats(stage_data)

    if tiempo > 0:
        return None
    
    empate = check_empate(stage_data)
    if empate:
        stage_data['ganador'] = None
        stage_data['juego_finalizado'] = True
        return 'EMPATE'

    if hp_j > hp_e:
        ganador = jugador
    else:
        ganador = enemigo

    setear_ganador(stage_data, ganador)
    return ganador

def check_win_by_stats(stage_data: dict) -> dict | str:
    """
    Verifica las condiciones de victoria/derrota por stats (HP a cero o quedarse sin cartas).
    """
    jugador, enemigo, hp_j, hp_e, cartas_j, cartas_e = get_stats(stage_data)

    empate = check_empate(stage_data)
    if empate:
        stage_data["ganador"] = None
        stage_data["juego_finalizado"] = True
        return "EMPATE"

    if (hp_j <= 0 or (cartas_j == 0 and cartas_e > 0)):
        setear_ganador(stage_data, enemigo)
        return enemigo
    elif (hp_e <= 0 or (cartas_e == 0 and cartas_j > 0)):
        setear_ganador(stage_data, jugador)
        return jugador

def check_empate(stage_data: dict) -> str | None:
    """
    Verifica las condiciones de EMPATE:
    1. Ambos HP <= 0 y tienen el mismo HP.
    2. Ambos se quedan sin cartas y tienen el mismo HP.
    3. El tiempo llega a 0 y tienen el mismo HP.
    """
    jugador, enemigo, hp_j, hp_e, cartas_j, cartas_e = get_stats(stage_data)

    if hp_j <= 0 and hp_e <= 0:
        if hp_j == hp_e:
            return 'EMPATE'

    
    if cartas_j == 0 and cartas_e == 0:
        if hp_j ==  hp_e:
            return 'EMPATE'

    if stage_data['stage_timer'] <= 0 and hp_j == hp_e:
        return 'EMPATE'

    return None

def chequear_ganador(stage_data: dict) -> dict | None:
    """
    Función de control que verifica si alguna condición de finalización de juego se cumple.
    """
    ganador = check_win_by_time(stage_data)
    if ganador is not None:
        return ganador
    
    ganador = check_win_by_stats(stage_data)
    if ganador is not None:
        return ganador
    return None


def es_golpe_critico() -> bool:
    """Determina aleatoriamente si el ataque actual es un golpe crítico (x3 de daño)."""
    critical = rd.choice([False, False, False, True])
    return critical

def comparar_damage(stage_data: dict) -> tuple[bool, str] | None:
    """
    Compara el ATK de las cartas jugadas, aplica el bonus, calcula el daño y 
    lo resta al participante perdedor.
    Returns: -tuple[bool, str] | None: (is_critical: bool, ganador_mano: 'PC'/'PLAYER'), o None si no hay cartas.
    """
    ganador_mano = None
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')
    critical = False
    carta_jugador = participante.get_carta_actual_player(jugador)
    carta_enemigo = participante.get_carta_actual_player(enemigo)

    if carta_enemigo and carta_jugador:
        critical = es_golpe_critico()
        atk_jugador = carta.aplicar_bonus(carta.get_atk_carta(carta_jugador), carta_jugador['bonus'])
        def_jugador = carta.aplicar_bonus(carta.get_def_carta(carta_jugador), carta_jugador['bonus'])
        atk_enemigo = carta.aplicar_bonus(carta.get_atk_carta(carta_enemigo), carta_enemigo['bonus'])
        def_enemigo = carta.aplicar_bonus(carta.get_def_carta(carta_enemigo), carta_enemigo['bonus'])

        if atk_enemigo > atk_jugador:
            ganador_mano = 'PC'
            if stage_data.get('shield_active'):
                print('SHIELD ACTIVADO -> Bloqueo de daño recibido.')
                stage_data['shield_active'] = False
            else:
                participante.restar_stats_player(jugador, carta_enemigo, critical)
        else:
            ganador_mano = 'PLAYER'
            score = atk_jugador - def_enemigo

            damage = score
            damage = max(0, damage)

            participante.restar_stats_player(enemigo, carta_jugador, critical)
            participante.add_score_player(jugador, damage)

    return critical, ganador_mano

def esta_finalizado(stage_data: dict) -> bool:
    """Retorna True si la partida ha terminado."""
    return stage_data.get('juego_finalizado')

def obtener_ganador(stage_data: dict) -> dict | None:
    """Retorna el diccionario del participante ganador (o None si es empate)."""
    return stage_data.get('ganador')

def jugar_mano_stage(stage_data: dict) -> None:
    """Ejecuta la acción de jugar una carta para cada participante."""
    participante.jugar_carta(stage_data.get('jugador'))
    participante.jugar_carta(stage_data.get('enemigo'))

def jugar_mano(stage_data: dict) -> tuple | None:
    """
    Función principal de ejecución de una mano completa de cartas. 
    Llamada por el botón 'PLAY HAND'.
    """
    if not stage_data.get('juego_finalizado'):
        jugar_mano_stage(stage_data)
        critical, ganador_mano = comparar_damage(stage_data)
        chequear_ganador(stage_data)
        return critical, ganador_mano
    return None

def draw_jugadores(stage_data: dict) -> None:
    """Dibuja las cartas visibles (las últimas jugadas) en la pantalla."""
    participante.draw_player(stage_data.get('jugador'), stage_data.get('screen'))
    participante.draw_player(stage_data.get('enemigo'), stage_data.get('screen'))

def update(stage_data: dict) -> str | None:
    """
    Función de actualización del Stage llamada en cada frame.
    Controla el timer y la finalización del juego.
    """
    timer_update(stage_data)
    if stage_data['stage_timer'] <= 0 and not stage_data['juego_finalizado']:
        ganador = chequear_ganador(stage_data)
        if ganador is not None:
            return

    if stage_data['juego_finalizado']:
        return "FINISHED"
    
    return None
