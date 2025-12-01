import pygame as pg, sys 
import modules.forms.form_base as base_form
import modules.variables as var
import modules.auxiliary_functions as aux
from utn_fra.pygame_widgets import(
    Label, Button, ButtonImageSound
)

def create_form_ranking(dict_form_data: dict) -> dict:
    """
    Crea el formulario de Ranking. Inicializa las listas para almacenar los datos 
    del archivo y los widgets de la interfaz gráfica.
    Args: -dict_form_data (dict): Datos de inicialización (screen, background, etc.).
    Returns: -dict: El diccionario del formulario 'form_ranking'.
    """
    form = base_form.create_base_form(dict_form_data)

    form['lista_ranking_file'] = []

    form['lista_ranking_GUI'] = []

    form['data_loaded'] = False

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_SCREEN[0] // 2, y=110,
        text='TOP Ten Ranking', screen=form.get('screen'),
        font_path=var.PATH_SAIYAN, font_size=50, color=var.colores.get('rosa')
    )

    form['btn_volver'] = ButtonImageSound(
        x=var.DIMENSION_SCREEN[0] // 2, y=655, width=var.W_B_V, height=var.H_B, text='', screen=form.get('screen'),
        image_path=var.PATH_BTN_VOLVER, sound_path=var.PATH_SOUND_BUTTON,
        on_click=cambiar_pantalla, on_click_param=[form,'form_menu']
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_volver')
    ]

    var.dict_form_status[form.get('name')] = form
    return form


def cambiar_pantalla(param_list: list) -> None:
    """
    Callback para el botón 'VOLVER'. Redirige al Menú Principal y limpia 
    los datos internos del formulario para que se recarguen la próxima vez que se acceda.
    Args: -param_list (list): Lista que contiene [0] el formulario y [1] el nombre de destino.
    Returns: No retorna nada.
    """
    form_ranking = param_list[0]
    form_name = param_list[1]
    
    print('Saliendo del formulario ranking')
    form_ranking['data_loaded'] = False
    form_ranking['lista_ranking_GUI'] = []
    form_ranking['lista_ranking_file'] = []
    base_form.cambiar_pantalla(form_name)

def init_ranking_data(form_dict_data: dict) -> None:
    """
    Crea dinámicamente los objetos Label (widgets) para mostrar los datos del ranking 
    (Posición, Nombre y Score) obtenidos del archivo CSV.
    Args: -form_dict_data (dict): El diccionario del formulario que contiene 'lista_ranking_file'.
    Returns: No retorna nada.
    """
    matriz = form_dict_data.get('lista_ranking_file')

    y_coord_inicial =  200
    for indice_fila in range(len(matriz)):
        fila = matriz[indice_fila]
        
        posicion = Label(
            x=var.DIMENSION_SCREEN[0] // 2 - 150, y=y_coord_inicial,
            text=f'{indice_fila + 1}', screen=form_dict_data.get('screen'),
            font_path=var.PATH_SUPER_MARIO, font_size=35, color=var.colores.get('rosa'))
        nombre = Label(
            x=var.DIMENSION_SCREEN[0] // 2 - 30, y=y_coord_inicial,
            text=fila[0], screen=form_dict_data.get('screen'),
            font_path=var.PATH_SAIYAN, font_size=35, color=var.colores.get('rosa'))

        score = Label(
            x=var.DIMENSION_SCREEN[0] // 2 + 110, y=y_coord_inicial,
            text=f'{fila[1]}', screen=form_dict_data.get('screen'),
            font_path=var.PATH_SUPER_MARIO, font_size=30, color=var.colores.get('rosa'))

        y_coord_inicial += 42

        form_dict_data['lista_ranking_GUI'].append(posicion)
        form_dict_data['lista_ranking_GUI'].append(nombre)
        form_dict_data['lista_ranking_GUI'].append(score)


def inicializar_ranking_archivo(form_dict_data: dict) -> None:
    """
    Carga el Top 10 de puntajes desde el archivo CSV usando el módulo auxiliar.
    Si los datos ya están cargados ('data_loaded' = True), no hace nada.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    if not form_dict_data.get('data_loaded'):
        form_dict_data['lista_ranking_file'] = aux.cargar_ranking(var.RANKING_CSV, top=10)
        init_ranking_data(form_dict_data)
        form_dict_data['data_loaded'] = True

def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Ranking. Dibuja el fondo, los widgets estáticos 
    y luego los widgets del ranking dinámico.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    #widgets lbl ranking
    for widget in form_dict_data.get('lista_ranking_GUI'):
        widget.draw()

def update(form_dict_data: dict) -> None:
    """
    Función de actualización del Ranking. Se asegura de que los datos se carguen 
    y los widgets se creen solo una vez cuando el formulario se vuelve activo.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    if not form_dict_data.get('data_loaded'):
        inicializar_ranking_archivo(form_dict_data)
    base_form.update(form_dict_data)

