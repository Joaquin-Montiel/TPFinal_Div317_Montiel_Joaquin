import pygame as pg
import sys
from modules import variables as var
from modules import player_juego
import modules.sounds as sound
import modules.forms.form_controllers as form_controller


def dragon_ball():
    """
    Inicializa el sistema principal del juego Dragon Ball Card Battle.
    Esta función configura e inicia todos los elementos centrales del juego:
    - Inicializa Pygame y configura la ventana principal.
    - Carga el ícono, título y dimensiones de pantalla.
    - Crea el controlador de formularios (UI Controller), que administra
        pantallas, menús y formularios interactivos.
    - Inicia el loop principal del juego, encargado de:
        -Capturar eventos del usuario.
        -Actualizar la lógica de los formularios activos.
        -Renderizar la pantalla.
    El loop continúa ejecutándose hasta que el jugador cierra la ventana.
    Una vez finalizado, se cierra Pygame y se termina la ejecución del programa.
    No recibe parámetros y no retorna ningún valor.
    """
    
    pg.init()

    pg.display.set_caption(var.TITLE_GAME)
    icon = pg.image.load(var.PATH_ICON)
    pg.display.set_icon(icon)
    screen_game = pg.display.set_mode(var.DIMENSION_SCREEN)

    clock = pg.time.Clock()
    sound.set_volume(var.VOLUME_INITIAL)

    datos_juego = {}

    controlador_ui = form_controller.create_form_controller(screen_game, datos_juego)
    running = True

    while running:
        eventos = pg.event.get()
        clock.tick(var.FPS)

        for evento in eventos:
            if evento.type == pg.QUIT:
                running = False

        form_controller.update(controlador_ui, eventos)
        pg.display.flip()
    pg.quit()
    sys.exit()
