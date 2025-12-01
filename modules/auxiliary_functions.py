import json, os, pygame as pg, random as rd
import modules.variables as var

def mapear_valores(matriz: list[list], columna_a_mapear: int, callback) -> None:
    """
    Función de orden superior que aplica una función de transformación (callback) 
    a una columna específica de una matriz (lista de listas).
    Se usa para convertir strings (scores) a enteros en el ranking.
    Args: -matriz (list[list]): La matriz de datos (ranking).
        -columna_a_mapear (int): El índice de la columna a transformar (ej. 1 para el Score).
        -callback (function): La función de transformación a aplicar (ej. parsear_entero).
    Returns: No retorna nada.
    """
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][columna_a_mapear]
        matriz[indice_fila][columna_a_mapear] = callback(valor)

def parsear_entero(valor: str) -> int:
    """
    Intenta convertir una cadena de texto a entero. Usada para la limpieza de Scores.
    Args: -valor (str): La cadena a convertir (puede ser un número o texto).
    Returns: -int: El valor como entero si es un dígito, o la cadena original si es texto (ej. el encabezado).
    """
    valor = valor.strip()

    if valor.isdigit():
        return int(valor)
    return valor

#def cargar_ranking(file_path: str, top: int = 10):
#    ranking = []
#    with open(file_path, 'r',encoding='utf-8') as file:
#        texto = file.read()
#
#        for linea in texto.split('\n'):
#            if linea:
#                lista_datos = linea.split(',')
#                ranking.append(lista_datos)
#    
#    mapear_valores(ranking, columna_a_mapear=1, callback=parsear_entero)
#    ranking = ranking[1:]
#    ranking.sort(key=lambda fila: fila[1], reverse=True)
#    return ranking[:top]

def cargar_ranking(file_path: str, top: int = 10) -> list:
    """
    Carga, limpia y ordena el ranking de jugadores desde un archivo CSV.
    Args: -file_path (str): Ruta al archivo CSV.
        -top (int, optional): Número máximo de entradas a retornar. Defaults to 10.
    Returns: -list: Una matriz de ranking ordenada por score (de mayor a menor), sin el encabezado.
    """
    ranking = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for linea in file:
            linea = linea.strip()

            if linea == '':
                continue

            partes = linea.split(',')

            nombre = partes[0].strip()
            score = partes[1].strip()

            if nombre == "" or score == "":
                continue

            ranking.append([nombre, score])

    mapear_valores(ranking, columna_a_mapear=1, callback=parsear_entero)

    if ranking and ranking[0][0].lower() == "nombre":
        ranking = ranking[1:]

    ranking.sort(key=lambda fila: fila[1], reverse=True)

    return ranking[:top]


def load_configs(file_path: str) -> dict:
    """
    Carga y devuelve el contenido de un archivo JSON de configuraciones.
    Args: -file_path (str): Ruta al archivo JSON.
    Returns: -dict: El diccionario de configuraciones.
    """
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_configs_stage(stage_data: dict) -> None:
    """
    Carga las configuraciones específicas del Stage (niveles) desde el JSON global 
    y las asigna a las claves del diccionario stage_data.
    Args: -stage_data (dict): El diccionario de datos del Stage actual.
    Returns: No retorna nada.
    """
    if not stage_data.get('juego_finalizado') and not stage_data.get('data_cargada'):
        configs_globales = load_configs(var.PATH_JSON_LEVEL)
        configs_nivel = configs_globales.get('nivel_1')

        stage_data['stage_timer'] = configs_nivel.get('stage_timer')

        stage_data['ruta_mazos'] = configs_nivel.get('ruta_mazos')
        stage_data['nombre_mazo_enemigo'] = configs_nivel.get('mazo_enemigo')
        stage_data['nombre_mazo_jugador'] = configs_nivel.get('mazo_player')
        stage_data['ruta_mazo_jugador'] = configs_nivel.get('ruta_mazo_player')
        stage_data['coods_inicial_mazo_enemigo'] = configs_nivel.get('coordenadas_mazo_enemigo')
        stage_data['coods_inicial_mazo_player'] = configs_nivel.get('coordenadas_mazo_player')
        stage_data['coods_final_mazo_enemigo'] = configs_nivel.get('coordenadas_finales_enemigo')
        stage_data['coods_final_mazo_player'] = configs_nivel.get('coordenadas_finales_player')
        stage_data['cantidad_cartas_jugadores'] = configs_nivel.get('cantidad_cartas_jugadores')


def generar_bd_cartas(path_mazo: str) -> dict:
    """
    Genera la Base de Datos de Cartas leyendo las imágenes desde la estructura de directorios
    y extrayendo los stats (HP, ATK, DEF, Bonus) de los nombres de archivo.
    Args: -path_mazo (str): Ruta al directorio raíz que contiene las carpetas de mazos.
    Returns: -dict: Un diccionario {'cartas': {deck_name: [lista de dicts de cartas]}}
    """
    cartas_dict = {
        "cartas": {}
    }

    for root, dir, files in os.walk(path_mazo):
        reverse_path = ''
        deck_cards = []
        deck_name = ''
        for carta in files:
            card_path = os.path.join(root, carta)
            deck_name = root.replace('\\', '/').split('/')[-1]
            print(f'DECK NAME: {deck_name}')

            if 'reverse' in card_path:
                reverse_path = card_path.replace('\\', '/')
            else:
                card_path = card_path.replace('\\', '/')
                filename = carta

                filename = filename.replace('.png', '')
                datos_crudos = filename.split('_')

            #1.0_HP_6500_ATK_13000_DEF_7000_10.png
            datos_card = {
                'id': datos_crudos[0],
                'hp': int(datos_crudos[2]),
                'atk': int(datos_crudos[4]),
                'def': int(datos_crudos[6]),
                'bonus': int(datos_crudos[7]),
                'path_frente': card_path,
                'path_reverse': ''
            }

            deck_cards.append(datos_card)
        
        for index_carta in range(len(deck_cards)):
            deck_cards[index_carta]['path_reverse'] = reverse_path

        if deck_name:
            cartas_dict['cartas'][deck_name] = deck_cards

    return cartas_dict

def save_cards(ruta_archivo: str, dict_cards: dict) -> None:
    """
    Guarda el diccionario de la Base de Datos de Cartas en un archivo JSON para 
    evitar tener que escanear los directorios cada vez que se inicia el juego.
    Args: -ruta_archivo (str): Ruta al archivo JSON de destino.
        -dict_cards (dict): El diccionario de la BD de cartas.
    Returns: No retorna nada.
    """
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        json.dump(dict_cards, file, indent=4)

def save_info_csv(informacion: str) -> None:
    """
    Guarda la información de un jugador (Nombre, Score) en el archivo CSV de ranking.
    Args: -informacion (str): La línea formateada a guardar (ej: "Joaquin, 15000\n").
    Returns: No retorna nada.
    """
    with open(var.RANKING_CSV, 'a', encoding='utf-8') as file:
        file.write(informacion)
        print(f'INFORMACION GUARDADA -> {informacion}')

def elegir_mazo_random(dict_catas: dict) -> str:
    """
    Selecciona aleatoriamente el nombre de un mazo disponible de la BD de cartas.
    Args: -dict_catas (dict): El diccionario completo de cartas (con clave 'cartas').
    Returns: str: El nombre del mazo seleccionado.
    """
    info_posibles_mazos = dict_catas.get('cartas')
    posibles_mazos = list(info_posibles_mazos.keys())
    mazo_seleccionado = rd.choice(posibles_mazos)
    print(f'Mazo seleccionado: {mazo_seleccionado}')
    return mazo_seleccionado

def load_bd_cartas(stage_data: dict) -> None:
    """
    Carga la Base de Datos de Cartas. Prioriza la carga desde el archivo JSON pre-generado. 
    Si el archivo no existe, genera la BD escaneando los directorios y la guarda.
    Args: -stage_data (dict): El diccionario del Stage actual.
    Returns: No retorna nada.
    """
    if not stage_data.get('juego_finalizado'):
        if os.path.exists(var.PATH_JSON_CARTAS) and os.path.isfile(var.PATH_JSON_CARTAS):
            print('================================== CARGANDO BD CARTAS DESDE FILE ==================================')
            cartas = load_configs(var.PATH_JSON_CARTAS)

            stage_data['nombre_mazo_enemigo'] = elegir_mazo_random(cartas)
            stage_data['nombre_mazo_jugador'] = elegir_mazo_random(cartas)

            stage_data['cartas_mazo_inicial_e'] = cartas.get('cartas').get(stage_data.get('nombre_mazo_enemigo'))
            stage_data['cartas_mazo_inicial_j'] = cartas.get('cartas').get(stage_data.get('nombre_mazo_jugador'))
        else:
            print('================================== CARGANDO BD CARTAS DESDE DIR ==================================')
            cartas = generar_bd_cartas(stage_data.get('ruta_mazos'))
            save_cards(var.PATH_JSON_CARTAS, cartas)
            stage_data['cartas_mazo_inicial_e'] = cartas.get('cartas').get(stage_data.get('nombre_mazo_enemigo'))
            stage_data['cartas_mazo_inicial_j'] = cartas.get('cartas').get(stage_data.get('nombre_mazo_jugador'))


def redimencionar_imagen(path_img: str, porcentaje_a_ajustar: int) -> pg.Surface:
    """
    Carga una imagen de Pygame y la escala a un nuevo tamaño basado en un porcentaje.
    Args: -path_img (str): Ruta al archivo de imagen.
        -porcentaje_a_ajustar (int): Porcentaje de escalado (ej. 50 para la mitad del tamaño).
    Returns:
        pg.Surface: La superficie de Pygame con la imagen redimensionada.
    """
    imagen = pg.image.load(path_img)
    ancho = imagen.get_width()
    alto = imagen.get_height()
    escala = float(porcentaje_a_ajustar / 100)
    
    nuevo_ancho = int(ancho * escala)
    nuevo_alto = int(alto * escala)

    imagen_nueva = pg.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
    return imagen_nueva

def reducir(callback, iterable: list):
    """
    Implementación simple de la función 'reduce'. Aplica una función de suma/acumulación 
    (callback) a los elementos de un iterable para obtener un total (ej. la suma de stats).
    Args: -callback (function): Función que devuelve el valor a sumar de cada elemento.
        -iterable (list): La lista de elementos (ej. la lista de diccionarios de cartas).
    Returns: -int: La suma total de los valores procesados.
    """
    if not iterable:
        return 0
    
    suma = 0
    for elemento in iterable:
        suma += callback(elemento)

    return suma
