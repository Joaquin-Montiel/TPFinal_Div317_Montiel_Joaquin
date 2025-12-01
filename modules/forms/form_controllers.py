import pygame as pg
import modules.variables as var
import modules.forms.form_base as base_form
import modules.forms.form_menu as menu
import modules.forms.form_ranking as ranking
import modules.forms.form_pause as pause
import modules.forms.form_stage as stage
import modules.forms.form_name as name
import modules.forms.form_wish as wish
import modules.forms.form_configuraciones as configs


def create_form_controller(screen: pg.Surface) -> dict:
    """
    Inicializa el controlador principal de formularios (pantallas).
    Crea las instancias de todos los formularios del juego (Menú, Ranking, Stage, etc.), 
    los almacena en una lista y en el diccionario de estado global (var.dict_form_status).
    Args: -screen (pg.Surface): La superficie principal de Pygame (main_screen).
    Returns: -dict: El diccionario 'controller' que gestiona el estado de todos los formularios.
    """
    controller = {}
    controller['main_screen'] = screen

    controller['forms_list'] = [
        menu.create_form_menu(
            {
                "name": 'form_menu',
                "screen": controller.get('main_screen'),
                "active": True,
                "coord": (0,0),
                "music_path": var.MUSIC_MENU,
                "background": var.PATH_MENU,
                "screen_dimensions": var.DIMENSION_SCREEN
            }
        ),
        ranking.create_form_ranking(
            {
                "name": 'form_ranking',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_RANKING,
                "background": var.PATH_RANKING,
                "screen_dimensions": var.DIMENSION_SCREEN
            }
        ),
        configs.create_form_configs(
            {
                "name": 'form_configs',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_CONFIGS,
                "background": var.PATH_CONFIGS,
                "screen_dimensions": var.DIMENSION_SCREEN
            }
        ),
        pause.create_form_pause(
            {
                "name": 'form_pause',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_PAUSE,
                "background": var.PATH_PAUSE,
                "screen_dimensions": var.DIMENSION_SCREEN
            }
        ),
        stage.crear_form_stage(
            {
                "name": 'form_stage',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_STAGE,
                "background": var.PATH_STAGE,
                "screen_dimensions": var.DIMENSION_SCREEN,
            }
        ),
        name.create_form_name(
            {
                "name": 'form_name',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_NAME,
                "background": var.PATH_NAME_WIN,
                "screen_dimensions": var.DIMENSION_SCREEN,
            }
        ),
        wish.create_form_wish(
            {
                "name": 'form_wish',
                "screen": controller.get('main_screen'),
                "active": False,
                "coord": (0,0),
                "music_path": var.MUSIC_WISH,
                "background": var.PATH_WISH,
                "screen_dimensions": var.DIMENSION_SCREEN,
            }
        )
    ]
    base_form.set_active('form_menu') 
    return controller

def forms_update(form_controller: dict, eventos: list[pg.event.Event]) -> None:
    """
    Itera a través de todos los formularios y solo actualiza y dibuja el que está activo.
    Utiliza el patrón 'match/case' para dirigir el flujo a la función 'update' específica de cada formulario.
    Args: -form_controller (dict): El diccionario del controlador principal.
        -eventos (list[pg.event.Event]): Lista de eventos de Pygame recopilados en el game loop.
    Returns: No retorna nada.
    """
    lista_formularios = form_controller.get('forms_list')

    for form in lista_formularios:
        if form.get('active'):
            match form.get('name'):
                case 'form_menu':
                    form_menu = lista_formularios[0]
                    menu.update(form_menu)
                    menu.draw(form_menu)
                case 'form_ranking':
                    form_ranking = lista_formularios[1]
                    ranking.update(form_ranking)
                    ranking.draw(form_ranking)
                case 'form_configs':
                    form_configs = lista_formularios[2]
                    configs.update(form_configs)
                    configs.draw(form_configs)
                case 'form_pause':
                    form_pause = lista_formularios[3]
                    pause.update(form_pause)
                    pause.draw(form_pause)
                case 'form_stage':
                    form_stage = lista_formularios[4]
                    stage.update(form_stage, eventos)
                    stage.draw(form_stage)
                case 'form_name':
                    form_name = lista_formularios[5]
                    name.update(form_name, eventos)
                    name.draw(form_name)
                case 'form_wish':
                    form_wish = lista_formularios[6]
                    wish.update(form_wish)
                    wish.draw(form_wish)


def update(form_controller: dict, eventos: list[pg.event.Event]) -> None:
    """
    Función principal de actualización llamada por el Game Loop (main.py).
    Delega el control de flujo y la distribución de eventos a la función forms_update.
    Args: -form_controller (dict): El diccionario del controlador principal.
        -eventos (list[pg.event.Event]): Lista de eventos de Pygame.
    Returns: No retorna nada
    """
    forms_update(form_controller, eventos)
