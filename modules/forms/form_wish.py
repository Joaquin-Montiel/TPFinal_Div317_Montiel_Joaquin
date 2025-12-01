import pygame as pg 
import modules.forms.form_base as base_form
import modules.variables as var
import modules.auxiliary_functions as aux
import modules.forms.form_stage as stage
import modules.stage as stage_j
import modules.player_juego as participante
from utn_fra.pygame_widgets import(
    Label, ButtonSound, TextBox
)

def create_form_wish(dict_form_data: dict) -> dict:
    """
    Crea el formulario de Wish (Momento Bonus). Inicializa los botones para 
    confirmar o cancelar el uso del comodín.
    Args: -dict_form_data (dict): Datos de inicialización.
    Returns: -dict: El diccionario del formulario 'form_wish'.
    """
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = dict_form_data.get('jugador')
    form['type_wish'] = ''

    form['lbl_titulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=80,
                            text='Momento Bonus', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=60)
    form['lbl_subtitulo'] = Label(x=var.DIMENSION_SCREEN[0] // 2, y=370,
                            text='Selecciona el deseo o huye', screen=form.get('screen'),
                            font_path=var.PATH_SAIYAN, font_size=50)

    form['btn_wish'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2 - 200, y=450,
        text='', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SUPER_MARIO, font_size=45,
        on_click=init_wish, on_click_param=form
    )

    form['btn_cancel'] = ButtonSound(
        x=var.DIMENSION_SCREEN[0] // 2 + 200, y=450,
        text='CANCEL', screen=form.get('screen'), sound_path=var.PATH_SOUND_BUTTON,
        font_path=var.PATH_SAIYAN, font_size=45,
        on_click=resume, on_click_param='form_stage'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_subtitulo'),
        form.get('btn_wish'),
        form.get('btn_cancel')
    ]

    var.dict_form_status[form.get('name')] = form
    return form

def update_wish_type(dict_form_data: dict, wish_type: str) -> None:
    """
    Actualiza el formulario con el tipo de deseo seleccionado ('HEAL' o 'SHIELD').
    Esta función es llamada desde form_stage.py.
    Args: -dict_form_data (dict): El diccionario del formulario 'form_wish'.
        -wish_type (str): El tipo de comodín seleccionado.
    Returns: No retorna nada.
    """
    dict_form_data['type_wish'] = wish_type

    dict_form_data.get('widgets_list')[2].update_text(text=dict_form_data['type_wish'], color=pg.Color('red'))

def resume(form_name: str) -> None:
    """
    Callback para el botón 'CANCEL'. Vuelve a la pantalla de juego sin ejecutar la acción 
    del comodín. La música de Stage debe seguir sonando.
    Args: -form_name (str): El nombre del formulario de destino ('form_stage').
    Returns: No retotna nada.
    """
    base_form.cambiar_pantalla(form_name)

def init_wish(form_dict_data: dict) -> None:
    """
    Callback para el botón de confirmación. Ejecuta la lógica del comodín (HEAL o SHIELD), 
    aplica los cambios a los stats del jugador y regresa al Stage.
    Args: -form_dict_data (dict): El diccionario del formulario 'form_wish'.
    Returns: No retorna nada.
    """
    wish_type = form_dict_data.get('type_wish')
    stage = var.dict_form_status['form_stage']['stage']
    jugador =  stage.get('jugador')
    
    if wish_type == 'SHIELD':
        stage_j.modificar_estado_bonus(stage, 'shield')
        stage['shield_active'] = True
        print('SHIELD ACTIVADO')
    else:
        stage_j.modificar_estado_bonus(stage, 'heal')
        hp_inicial = participante.get_hp_inical_player(jugador)
        hp_actual = participante.get_hp_player(jugador)
        hp_perdido = hp_inicial - hp_actual

        hp_bonus = int(hp_perdido * 0.75)
        nuevo_hp = hp_actual + hp_bonus

        print(f'Anterior HP: {hp_actual} | Actual HP: {nuevo_hp}')
        participante.set_hp_player(jugador, nuevo_hp)

    resume('form_stage')

def update(form_dict_data: dict) -> None: 
    """
    Función de actualización del formulario. Delega el manejo de eventos a la base.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.update(form_dict_data)

def draw(form_dict_data: dict) -> None:
    """
    Dibuja el formulario de Wish: fondo y todos los widgets.
    Args: -form_dict_data (dict): El diccionario del formulario.
    Returns: No retorna nada.
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)



