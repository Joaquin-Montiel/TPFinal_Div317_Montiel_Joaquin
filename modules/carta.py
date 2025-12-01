import modules.auxiliary_functions as aux
import pygame as pg

def inicializar_carta(dict_carta: dict, coords: list[int]) -> dict:
    """
    Inicializa un diccionario de carta agregando variables de estado necesarias 
    para Pygame y el juego.
    Args: -dict_carta (dict): Diccionario crudo de la carta (con 'hp', 'atk', 'def', 'bonus').
        -coords (list[int]): Coordenadas iniciales (topleft) de la carta.
    Returns: -dict: El diccionario de carta inicializado y preparado para el Stage.
    """
    card = dict_carta
    card['visible'] = False
    card['coordenadas'] = coords

    card['imagen'] = None
    card['rect'] = None

    if 'bonus' not in card:
        card['bonus'] = 0

    return card

def esta_visible(dict_card: dict) -> bool:
    """
    Retorna el estado de visibilidad de la carta.
    Args: -dict_card (dict): El diccionario de la carta.
    Returns: -bool: True si la carta está boca arriba (path_frente), False si está boca abajo.
    """
    return dict_card.get('visible')

def cambiar_visibilidad(dict_card: dict) -> bool:
    """
    Alterna el estado de visibilidad de la carta (True <-> False).
    Args: -dict_card (dict): El diccionario de la carta.
    Returns: -bool: El nuevo estado de visibilidad.
    """
    dict_card['visible'] = not dict_card.get('visible')

def get_hp_carta(dict_carta: dict) -> int:
    """
    Retorna el valor de HP base de la carta.
    Args: -dict_carta (dict): El diccionario de la carta.
    Returns: -int: El valor de HP.
    """
    return dict_carta.get('hp')

def get_def_carta(dict_carta: dict) -> int:
    """
    Retorna el valor de DEF base de la carta.
    Args: -dict_carta (dict): El diccionario de la carta.
    Returns: -int: El valor de DEF.
    """
    return dict_carta.get('def')

def get_atk_carta(dict_carta: dict) -> int:
    """
    Retorna el valor de ATK base de la carta.
    Args: -dict_carta (dict): El diccionario de la carta.
    Returns: -int: El valor de ATK.
    """
    return dict_carta.get('atk')

def asignar_coordenadas_carta(dict_card: dict, coordenadas: tuple[int]) -> None:
    """
    Establece la posición (topleft) de la carta en la pantalla.
    Args: -dict_card (dict): El diccionario de la carta.
        -coordenadas (tuple[int]): Las coordenadas (x, y) de la posición.
    Returns: No retorna nada.
    """
    dict_card['coordenadas'] = coordenadas

def aplicar_bonus(valor_base: int, bonus: int) -> int:
    """
    Calcula el valor final de un stat (generalmente ATK) aplicando un porcentaje 
    de bonus.
    Args: -valor_base (int): El stat base (ej. ATK).
        -bonus (int): El porcentaje de bonus a aplicar (ej. 10 para 10%).
    Returns: -int: El valor final con el bonus aplicado.
    """
    return valor_base + int(valor_base * bonus / 100)

def draw_carta(dict_card: dict, screen: pg.Surface) -> None:
    """
    Carga la imagen de la carta (frente o reversa) según su estado de visibilidad 
    y la dibuja en la posición asignada en la pantalla.
    Args: -dict_card (dict): El diccionario de la carta.
        -screen (pg.Surface): La superficie principal de Pygame.
    Returns: No retorna nada.
    """

    if dict_card.get('visible'):
        dict_card['imagen'] =  aux.redimencionar_imagen(dict_card.get('path_frente'), 40)
    else:
        dict_card['imagen'] =  aux.redimencionar_imagen(dict_card.get('path_reverse'), 40)
    
    dict_card['rect'] = dict_card.get('imagen').get_rect()
    dict_card['rect'].topleft =  dict_card.get('coordenadas')

    screen.blit(dict_card.get('imagen'), dict_card.get('rect'))

