import pygame as pg

########## CONFIGS JUEGO ##########
TITLE_GAME = 'Las cartas del Dragon'
DIMENSION_SCREEN = (1024, 768)
FPS = 30    
VOLUME_INITIAL = 20
MUSIC_ENABLED = True
WIDTH = 80
HEIGHT = 80
W_B = 60
H_B = 60
W_B_V = 250
#H_B_V = 100


########## PATH FONDOS ##########
PATH_MENU = 'modules/assets/background_forms/form_main_menu.png'
PATH_RANKING = 'modules/assets/background_forms/form_ranking.png'
PATH_CONFIGS = 'modules/assets/background_forms/form_configs.png'
PATH_PAUSE = 'modules/assets/background_forms/form_pause.png'
PATH_STAGE = 'modules/assets/background_forms/background_cards_simple.png'
PATH_NAME_LOSE = 'modules/assets/background_forms/form_enter_name_0.png'
PATH_NAME_WIN = 'modules/assets/background_forms/form_enter_name_1.png'
PATH_NAME_DRAW = 'modules/assets/background_forms/form_level_select.jpg'
PATH_WISH = 'modules/assets/background_forms/form_wish_select.png'
PATH_JSON_LEVEL = 'configs.json' 
PATH_JSON_CARTAS = 'cartas.json' 

########## PATH FONTS ##########
PATH_SAIYAN = 'modules/assets/fonts/Saiyan-Sans.ttf'
PATH_ALAGARD = 'modules/assets/fonts/alagard.ttf'
PATH_SUPER_MARIO = 'modules/assets/fonts/SuperMario256.ttf'

########## PATH IMAGE #########
PATH_ICON = 'modules/assets/extras/1_star.png'
PATH_MOUSE_POINTER = 'modules/assets/extras/golden_frieza_pointer.png'
PATH_BUTTON_PLAY = 'modules/assets/extras/btn_play_hand.png'
PATH_BUTTON_HEAL = 'modules/assets/extras/icon_heal.png'
PATH_BUTTON_SHIELD = 'modules/assets/extras/icon_shield.png'
PATH_BTN_VOLVER = 'modules/assets/extras/btn_volver.png'

########## PATH SOUND ##########
PATH_SOUND_BUTTON = 'modules/assets/audio/sounds/click_scouter.ogg'
PATH_SOUND_WRITE = 'modules/assets/audio/sounds/hit_01.ogg'

########## PATH MUSIC #########
MUSIC_MENU = 'modules/assets/audio/music/form_main_menu.ogg'
MUSIC_RANKING = 'modules/assets/audio/music/form_ranking.ogg'
MUSIC_CONFIGS = 'modules/assets/audio/music/form_options.ogg'
MUSIC_PAUSE = 'modules/assets/audio/music/form_pausa.ogg'
MUSIC_STAGE = 'modules/assets/audio/music/level_01.ogg'
MUSIC_NAME = 'modules/assets/audio/music/powerup.ogg'
MUSIC_WISH = 'modules/assets/audio/music/form_wish_select.ogg'

########## COLORES ##########
colores = {
    "amarillo": pg.Color('yellow'),
    "azul": pg.Color('blue'),
    "blanco": pg.Color('white'),
    "cian": pg.Color('cyan'),
    "naranja": pg.Color('orange'),
    "negro": pg.Color('black'),
    "rojo": pg.Color('red'),
    "rosa": pg.Color('pink'),
    "verde": pg.Color('green')
}

dict_form_status = {}

########## ARCHIVOS ##########
RANKING_CSV = 'puntaje.csv'