import pygame as pg
import modules.variables as var
import modules.carta as carta
import modules.auxiliary_functions as aux
from functools import reduce


def initialize_player(pantalla: pg.Surface, nombre: str = 'PC') -> dict:
    """
    Inicializa el diccionario de datos de un nuevo participante (Jugador o Enemigo). 
    Establece stats base y configura las estructuras de mazo.
    Args: -pantalla (pg.Surface): La superficie de Pygame.
        -nombre (str, optional): Nombre del participante. Defaults to 'PC'.
    Returns: -dict: El diccionario 'player' con todas las claves de estado inicializadas.
    """
    player = {}
    player['nombre'] = nombre
    player['hp_inicial'] = 1
    player['hp_actual'] = 1
    player['attack'] = 1
    player['defense'] = 1
    player['score'] = 0

    player['mazo_asignado'] = []
    player['cartas_mazo'] = []
    player['cartas_mazo_usadas'] = []

    player['screen'] = pantalla
    player['pos_carta_inicial'] = (0,0)
    player['pos_carta_jugada'] = (0,0)    

    return player

def get_hp_player(player: dict) -> int:
    """Retorna la salud actual del participante (HP actual)."""
    return player.get('hp_actual')

def get_hp_inical_player(player: dict) -> int:
    """Retorna la salud inicial (HP máximo) del participante."""
    return player.get('hp_inicial')

def get_attack_player(player: dict) -> int:
    """Retorna el valor de ataque total del participante."""
    return player.get('attack')

def get_defense_player(player: dict) -> int:
    """Retorna el valor de defensa total del participante."""
    return player.get('defense')

def get_nombre_player(player: dict) -> int:
    """Retorna el nombre del participante."""
    return player.get('nombre')

def get_score_player(player: dict) -> int:
    """Retorna el puntaje actual del participante."""
    return player.get('score')

def get_cartas_iniciales_player(player: dict) -> list[dict]:
    """Retorna la lista de cartas asignadas originalmente (mazo_asignado)."""
    return player.get('mazo_asignado')

def get_cartas_jugadas_player(player: dict) -> list[dict]:
    """Retorna la lista de cartas que ya fueron jugadas."""
    return player.get('cartas_mazo_usadas')

def get_cartas_restantes_player(player: dict) -> list[dict]:
    """Retorna la lista de cartas que quedan en el mazo de juego."""
    return player.get('cartas_mazo')

def get_coordenadas_mazo_inicial(player: dict):
    """Retorna las coordenadas (x, y) de la pila del mazo."""
    return player.get('pos_carta_inicial')

def get_coordenadas_mazo_jugada(player: dict):
    """Retorna las coordenadas (x, y) del área de carta jugada."""
    return player.get('pos_carta_jugada')

def get_carta_actual_player(player: dict):
    """
    Retorna la última carta jugada (la carta visible en el área de juego).
    Returns: -dict: El diccionario de la carta o None si la lista está vacía (no se ha jugado ninguna carta).
    """
    usadas = player.get('cartas_mazo_usadas')
    if not usadas:
        return None
    return usadas[-1]

def set_nombre_player(player: dict, nuevo_nombre) -> None:
    """Establece un nuevo nombre al participante."""
    player['nombre'] = nuevo_nombre

def setear_stat_player(player: dict, stat: str, valor: int) -> None:
    """Establece un valor a un stat específico (clave dinámica)."""
    player[stat] = valor

def set_cartas_player(player: dict, lista_cartas: list[dict]) -> None:
    """
    Asigna un nuevo mazo al participante, copia las cartas para el mazo de juego 
    y setea las coordenadas iniciales de las cartas.
    """
    if lista_cartas is None:
        lista_cartas = []

    for carta_b in lista_cartas:
        carta_b['coordenadas'] = get_coordenadas_mazo_inicial(player)

    player['mazo_asignado'] = lista_cartas
    player['cartas_mazo'] = lista_cartas.copy()

def set_score_player(player: dict, score: int) -> None:
    """Establece el puntaje del jugador."""
    player['score'] = score

def set_hp_player(player: dict, hp_actual: int) -> None:
    """Establece un nuevo valor de HP actual (usado para HEAL o daño directo)."""
    player['hp_actual'] = hp_actual

def add_score_player(player: dict, score: int) -> None:
    """Suma puntos al score actual del jugador."""
    player['score'] += score

def asignar_stats_iniciales_player(player: dict) -> None:
    """
    Calcula los stats iniciales totales (HP, ATK, DEF) sumando los stats 
    de todas las cartas del mazo asignado, usando la función auxiliar 'reducir'.
    """
    player['hp_inicial'] = aux.reducir(
        carta.get_hp_carta,
        player.get('mazo_asignado')
    )

    player['hp_actual'] = player['hp_inicial']

    player['attack'] = aux.reducir(
        carta.get_hp_carta,
        player.get('mazo_asignado')
    )

    player['defense'] = aux.reducir(
        carta.get_hp_carta,
        player.get('mazo_asignado')
    )

def chequear_valor_negativo(stat: int) -> int:
    """Asegura que un stat (HP, ATK, DEF) nunca sea negativo. Retorna 0 si es menor a 0."""
    if stat < 0:
        return 0
    else:
        return stat

def restar_stats_player(player: dict, carta_g: dict, is_critico: bool) -> None:
    """
    Resta stats al participante perdedor de la mano (HP, ATK, DEF). 
    El cálculo del daño se realiza con el ATK de la carta ganadora menos la DEF de la carta perdedora.
    Args: -player (dict): El diccionario del participante perdedor.
        -carta_g (dict): El diccionario de la carta ganadora (para calcular el daño).
        -is_critico (bool): True si el ataque es un golpe crítico (x3 damage).
    Returns: No retorna nada.
    """
    damage_mul = 1
    if is_critico:
        damage_mul = 3

    carta_jugador = player.get('cartas_mazo_usadas')[-1]
    damage = carta.get_atk_carta(carta_g) - carta.get_def_carta(carta_jugador)
    damage *= damage_mul

    player['hp_actual'] = chequear_valor_negativo(player.get('hp_actual') - damage) 
    player['attack'] -= carta.get_atk_carta(carta_jugador)
    player['defense'] -= carta.get_def_carta(carta_jugador)

def jugar_carta(player: dict) -> None:
    """
    Mueve la carta superior del mazo de juego ('cartas_mazo') al mazo de usadas ('cartas_mazo_usadas').
    Args: -player (dict): El diccionario del participante.
    Returns: No devuelve nada.
    """
    mazo = player.get('cartas_mazo')
    if mazo:
        carta_actual = mazo.pop()
        carta.cambiar_visibilidad(carta_actual)
        carta.asignar_coordenadas_carta(carta_actual, get_coordenadas_mazo_jugada(player))
        player.get('cartas_mazo_usadas').append(carta_actual)

        player['cartas_mazo'] = mazo

def info_csv(player: dict) -> str:
    """
    Genera la línea de texto formateada para guardar el ranking en el archivo CSV.
    Args: -player (dict): El diccionario del participante.
    Returns: -str: La línea de texto con Nombre, Score y salto de línea (ej: "Joaquin,15000\n").
    """
    return f'{get_nombre_player(player)}, {player.get("score")}\n'

def reiniciar_data_player(player_j: dict) -> None:
    """
    Resetea todos los stats y listas de cartas del jugador/enemigo a valores iniciales de partida.
    Llamado al iniciar/reiniciar un Stage.
    Args: -player_j (dict): El diccionario del participante.
    Returns: No retorna nada.
    """
    set_score_player(player_j, 0)
    set_cartas_player(player_j, list())
    player_j['cartas_mazo_usadas'].clear()
    setear_stat_player(player_j, 'hp_inicial', 0)
    setear_stat_player(player_j, 'hp_actual', 0)
    setear_stat_player(player_j, 'attack', 0)
    setear_stat_player(player_j, 'defense', 0)


def draw_player(player: dict, screen: pg.Surface) -> None:
    """
    Dibuja la carta superior del mazo (boca abajo) y la carta jugada (boca arriba) 
    en la pantalla de juego.
    Args: -player (dict): El diccionario del participante.
        -screen (pg.Surface): La pantalla de Pygame.
    Returns: No retorna nada.
    """
    if player.get('cartas_mazo'):
        carta.draw_carta(player.get('cartas_mazo')[-1], screen)
    if player.get('cartas_mazo_usadas'):
        carta.draw_carta(player.get('cartas_mazo_usadas')[-1], screen)
