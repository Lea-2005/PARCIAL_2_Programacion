import pygame
import random
import os
import json
from datetime import datetime
from Constantes import *
pygame.init()

def leer_csv_preguntas(nombre: str, lista: list) -> bool:
    """Lee un archivo CSV con preguntas y las agrega a una lista como diccionarios.

    Parámetros:
        nombre (str): Ruta del archivo CSV.
        lista (list): Lista donde se agregan las preguntas.

    Retorna:
        bool: True si se cargó correctamente, False si no se encontró el archivo.
    """
    if os.path.exists(nombre) == True:
        with open(nombre,"r", encoding="utf-8") as archivo:
            archivo.readline()

            for linea in archivo:
                diccionario_preguntas = crear_diccionario_preguntas(linea)
                lista.append(diccionario_preguntas)
        retorno = True
    else:
        retorno = False

    return retorno

def crear_diccionario_preguntas(linea: str, separador: str =",") -> dict:
    """Convierte una línea del archivo CSV en un diccionario con campos de pregunta y respuestas.

    Parámetros:
        linea (str): línea de texto del archivo CSV.
        separador (str): carácter separador (por defecto coma).

    Retorna:
        dict: Diccionario con la pregunta, respuestas y la opción correcta.
    """
    linea = linea.replace("\n","")
    
    lista_datos = linea.split(separador)
    preguntas = {}
    preguntas["pregunta"] = lista_datos[0]
    preguntas["respuesta_1"] = lista_datos[1]
    preguntas["respuesta_2"] = lista_datos[2]
    preguntas["respuesta_3"] = lista_datos[3]
    preguntas["respuesta_4"] = lista_datos[4]
    preguntas["respuesta_correcta"] = int(lista_datos[5])
    
    return preguntas

def mezclar_lista(lista_preguntas: list) -> None:
    """Mezcla aleatoriamente las preguntas de una lista.

    Parámetros:
        lista_preguntas (list): Lista a mezclar.
    """
    random.shuffle(lista_preguntas)

def mostrar_texto(surface: pygame.Surface, text: str, pos: tuple[int, int], font: pygame.font, color: tuple[int, int, int] = pygame.Color('black')):
    """Muestra texto multilínea ajustado al ancho de la superficie.

    Parámetros:
        surface (pygame.Surface): Superficie donde se dibuja el texto.
        text (str): Texto a mostrar.
        pos (tuple): Posición inicial (x, y).
        font (pygame.font): Fuente usada.
        color (tuple): Color del texto.
    """
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def detectar_click(lista: list, pos: tuple[int, int]) -> int | None:
    """Detecta cuál botón fue clickeado en una lista de elementos.

    Parámetros:
        lista (list): Lista de elementos con 'rectangulo'.
        pos (tuple): Posición del mouse.

    Retorna:
        int | None: Índice del botón clickeado o None si no hubo click.
    """
    retorno = None

    for i in range(len(lista)):
        opcion = lista[i]
    
        if opcion['rectangulo'].collidepoint(pos):
            retorno = i
        
    return retorno

def crear_elemento_juego(color: tuple[int, int, int], ancho: int, alto: int, pos_x: int, pos_y: int) -> dict:
    """Crea un elemento del juego con una superficie de color sólido y su correspondiente rectángulo.

    Parámetros:
        color (tuple[int, int, int]): Color RGB de la superficie.
        ancho (int): Ancho en píxeles del elemento.
        alto (int): Alto en píxeles del elemento.
        pos_x (int): Posición horizontal (X) del rectángulo.
        pos_y (int): Posición vertical (Y) del rectángulo.

    Retorna:
        dict: Diccionario con las claves 'superficie' y 'rectangulo'.
    """
    elemento_juego = {}

    superficie = pygame.Surface((ancho, alto))
    superficie.fill(color)
    elemento_juego['superficie'] = superficie
    elemento_juego['rectangulo'] = pygame.Rect(pos_x, pos_y, ancho, alto)
    
    return elemento_juego

def crear_lista_respuestas(color: tuple[int, int, int], ancho: int, alto: int, pos_x: int, pos_y: int) -> list:
    """Crea una lista de 4 elementos del juego que representan posibles respuestas con posiciones verticales desplazadas.

    Parámetros:
        color (tuple[int, int, int]): Color RGB de los elementos.
        ancho (int): Ancho en píxeles de cada respuesta.
        alto (int): Alto en píxeles de cada respuesta.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y inicial.

    Retorna:
        list: Lista con 4 elementos (diccionarios) de tipo respuesta.
    """
    lista_respuestas = []

    for i in range(4):
        respuesta = crear_elemento_juego(color,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(respuesta)
        pos_y += 50    

    return lista_respuestas

def crear_lista_comodines(color: tuple[int, int, int], ancho: int, alto: int, pos_x: int, pos_y: int)-> list:
    """Crea una lista de 4 comodines con posiciones horizontales desplazadas.

    Parámetros:
        color (tuple[int, int, int]): Color RGB de los comodines.
        ancho (int): Ancho de cada comodín.
        alto (int): Alto de cada comodín.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y fija para todos.

    Retorna:
        list: Lista de 4 comodines (diccionarios).
    """
    lista_comodines = []

    for i in range(4):
        comodin = crear_elemento_juego(color, ancho, alto, pos_x, pos_y)
    
        lista_comodines.append(comodin)

        pos_x += 74

    return lista_comodines

def dibujar_elemento(pantalla: pygame.Surface, lista: list) -> None:
    """Dibuja en pantalla todos los elementos de la lista.

    Parámetros:
        pantalla (pygame.Surface): Superficie donde se dibujarán los elementos.
        lista (list): Lista de elementos con 'superficie' y 'rectangulo'.
    """
    for elemento in lista:
        pantalla.blit(elemento['superficie'], elemento['rectangulo'])

def aplicar_comodin(comodin: int, datos_juego: dict, pregunta_actual: dict) -> None:
    """Aplica el efecto del comodín seleccionado si está disponible.

    Parámetros:
        comodin (int): Índice del comodín (0: bomba, 1: saltar turno, 2: x2, 3: doble intento).
        datos_juego (dict): Diccionario con el estado del juego.
        pregunta_actual (dict): Pregunta actual en juego.
    """
    match comodin:
        case 0: 
            if datos_juego['comodines']['bomba']:
                datos_juego['bandera']['bomba'] = True
                usar_bomba(pregunta_actual, datos_juego)
                datos_juego['comodines']['bomba'] = False
        case 1: 
            if datos_juego['comodines']['saltar_turno']:
                datos_juego['indice'] += 1
                datos_juego['tiempo_restante'] = 20
                datos_juego['bandera_respuesta'] = True
                datos_juego['respuestas_eliminadas'] = []
                datos_juego['comodines']['saltar_turno'] = False
        case 2: 
            if datos_juego['comodines']['X2']:
                datos_juego['bandera']['X2'] = True
                datos_juego['comodines']['X2'] = False
        case 3: 
            if datos_juego['comodines']['doble_intento']:
                datos_juego['bandera']['doble_intento'] = True
                datos_juego['comodines']['doble_intento'] = False

def usar_bomba(pregunta_actual: dict, datos_juego: dict):
    """Elimina dos respuestas incorrectas si el comodín bomba está activo.

    Parámetros:
        pregunta_actual (dict): Pregunta actual con la respuesta correcta.
        datos_juego (dict): Diccionario con el estado del juego, incluidas respuestas eliminadas.
    """
    if datos_juego['comodines']['bomba'] == True:
        indice_respuestas = [0, 1, 2, 3]

        respuesta_correcta = pregunta_actual['respuesta_correcta'] - 1

        indice_respuestas.remove(respuesta_correcta)
        respuesta_incorrecta = random.choice(indice_respuestas)

        indice_respuestas.remove(respuesta_incorrecta)

        datos_juego['respuestas_eliminadas'] = indice_respuestas

def verificar_respuesta(datos_juego: dict, pregunta_actual: dict, respuesta: int) -> bool:
    """Verifica si la respuesta del jugador es correcta y actualiza puntuación y vidas.

    Parámetros:
        datos_juego (dict): Estado actual del juego.
        pregunta_actual (dict): Pregunta con la respuesta correcta.
        respuesta (int): Índice de la respuesta seleccionada (0 a 3).

    Retorna:
        bool: True si la respuesta es correcta, False si es incorrecta.
    """
    if pregunta_actual['respuesta_correcta'] == (respuesta + 1):
        if datos_juego['bandera']['X2'] == True:
            datos_juego['puntuacion'] += PUNTUACION_ACIERTO * 2
            datos_juego['bandera']['X2'] = False
        else:
            datos_juego['puntuacion'] += PUNTUACION_ACIERTO   
        retorno = True         
    else:
        datos_juego['puntuacion'] -= PUNTUACION_ERROR
        datos_juego['vidas'] -= 1
        retorno = False
        
    return retorno

def crear_lista_menu(color: tuple[int, int, int], ancho: int, alto: int, pos_x: int, pos_y: int) -> list:
    """Crea una lista de botones para el menú.

    Parámetros:
        color (tuple[int, int, int]): Color RGB de los botones.
        ancho (int): Ancho de cada botón.
        alto (int): Alto de cada botón.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y inicial.

    Retorna:
        list: Lista de botones del menú.
    """
    lista_menu = []

    for i in range(4):
        botones = crear_elemento_juego(color, ancho, alto, pos_x, pos_y)
        lista_menu.append(botones)

        pos_y += 80

    return lista_menu

def crear_lista_confirmacion(color: tuple[int, int, int], ancho: int, alto: int, pos_x: int, pos_y: int)-> list:
    """Crea una lista de botones para la confirmación de acción.

    Parámetros:
        color (tuple[int, int, int]): Color RGB de los botones.
        ancho (int): Ancho inicial de los botones.
        alto (int): Alto de los botones.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y inicial.

    Retorna:
        list: Lista de botones de confirmación.
    """
    lista_comodines = []
    conteo = 0
    for i in range(3):
        comodin = crear_elemento_juego(color, ancho, alto, pos_x, pos_y)
        lista_comodines.append(comodin)

        pos_x += 95
        conteo += 1
        if conteo == 2:
            ancho += 50

    return lista_comodines

def actualizar_cuadro_partida(cuadrado_general: dict, cuadrado_pregunta: dict, lista_respuestas: list):
    """Limpia las superficies del cuadro general, de la pregunta y de las respuestas.

    Parámetros:
        cuadrado_general (dict): Cuadro general de juego.
        cuadrado_pregunta (dict): Cuadro donde se muestra la pregunta.
        lista_respuestas (list): Lista de respuestas a limpiar.
    """
    cuadrado_general['superficie'].fill(GRIS)
    cuadrado_pregunta['superficie'].fill(BLANCO)

    for respuesta in lista_respuestas:
        respuesta['superficie'].fill(BLANCO)

def actualizar_cuadro_confirmacion(cuadrado_confirmacion: dict, rectangulo_informacion: dict, lista_confirmacion: list):
    """Limpia las superficies de los cuadros de confirmación.

    Parámetros:
        cuadrado_confirmacion (dict): Cuadro de confirmación principal.
        rectangulo_informacion (dict): Rectángulo de información.
        lista_confirmacion (list): Lista de botones de confirmación.
    """
    cuadrado_confirmacion["superficie"].fill(BLANCO)
    rectangulo_informacion["superficie"].fill(GRIS)
    
    for boton in lista_confirmacion:
        boton["superficie"].fill(GRIS)

def generar_json(nombre_archivo: str, lista: list) -> bool:
    """Guarda una lista en formato JSON si no está vacía.

    Parámetros:
        nombre_archivo (str): Nombre del archivo JSON.
        lista (list): Lista a guardar.

    Retorna:
        bool: True si se guardó correctamente, False si la lista estaba vacía.
    """
    if type(lista) == list and len(lista) > 0:
        with open(nombre_archivo, "w") as archivo:
            json.dump(lista, archivo, indent = 4)
        retorno = True
    else:
        retorno = False
    
    return retorno

def leer_json(nombre_archivo: str) -> list:
    """Lee un archivo JSON si existe.

    Parámetros:
        nombre_archivo (str): Nombre del archivo JSON.

    Retorna:
        list: Lista cargada desde el archivo o lista vacía si no existe.
    """
    lista = []
    
    if os.path.exists(nombre_archivo) == True:
        with open(nombre_archivo, "r") as archivo:
            lista = json.load(archivo)
    
    return lista

def guardar_ranking(datos_juegos: dict, lista_ranking: list) -> None:
    """Agrega los datos del juego actual al ranking, incluyendo fecha.

    Parámetros:
        datos_juegos (dict): Diccionario con nombre y puntuación.
        lista_ranking (list): Lista del ranking actual.
    """
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")

    datos = {
        "nombre": datos_juegos["nombre"],
        "puntuacion": datos_juegos["puntuacion"],
        "fecha": fecha
    }
    lista_ranking.append(datos)

def ordenar_mayor_a_menor(lista_ranking: list) -> None:
    """Ordena la lista de ranking de mayor a menor puntuación.

    Parámetros:
        lista_ranking (list): Lista de rankings a ordenar.
    """
    for izq in range(len(lista_ranking) - 1):
        for der in range((izq + 1), len(lista_ranking)):        
            if lista_ranking[izq]["puntuacion"] < lista_ranking[der]["puntuacion"]:
              
                intercambiar_elementos(lista_ranking, izq, der)

def intercambiar_elementos(array_participantes: list, izq: int, der: int) -> None:
    """Intercambia dos elementos en una lista.

    Parámetros:
        array_participantes (list): Lista de elementos.
        izq (int): Índice del primer elemento.
        der (int): Índice del segundo elemento.
    """
    auxiliar = array_participantes[izq]
    array_participantes[izq] = array_participantes[der]
    array_participantes[der] = auxiliar

def mostrar_top_10(lista_ranking: list) -> bool:
    """Muestra por consola el top 10 de jugadores del ranking.

    Parámetros:
        lista_ranking (list): Lista de jugadores.

    Retorna:
        bool: True si hay elementos para mostrar, False en caso contrario.
    """
    if type(lista_ranking) == list and len(lista_ranking) > 0:
        ordenar_mayor_a_menor(lista_ranking)
        contador = 0

        for datos in lista_ranking[:10]:
            print(f"- Top {contador + 1}:")
            print(f"Nombre: {datos["nombre"]}")
            print(f"Puntuación: {datos["puntuacion"]}")
            print(f"Fecha: {datos["fecha"]}\n")
            contador += 1
            
        retorno = True
    else:
        retorno = False

    return retorno

def crear_lista_ranking(primer_color: tuple, segundo_color: tuple, tercer_color: tuple, cuarto_color: tuple, ancho: int, alto: int, pos_x: int, pos_y: int) -> list:
    """Crea una lista de elementos visuales para el ranking, con distintos colores según la posición.

    Parámetros:
        primer_color (tuple): Color RGB del primer lugar.
        segundo_color (tuple): Color RGB del segundo lugar.
        tercer_color (tuple): Color RGB del tercer lugar.
        cuarto_color (tuple): Color RGB del resto del ranking.
        ancho (int): Ancho de cada elemento.
        alto (int): Alto de cada elemento.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y inicial.

    Retorna:
        list: Lista de 10 elementos de ranking.
    """
    lista_comodines = []
    
    for i in range(10):
        color = primer_color

        if i > 4:
            color = cuarto_color
        elif i > 2:
            color = tercer_color
        elif i > 0:
            color = segundo_color

        comodin = crear_elemento_juego(color, ancho, alto, pos_x, pos_y)
        lista_comodines.append(comodin)

        pos_y += 45
        
    return lista_comodines

def actualizar_cuadro_ranking(cuadrado_general_ranking: dict, lista_posiciones: list) -> None:
    """Limpia y actualiza el fondo del cuadro de ranking y sus posiciones.

    Parámetros:
        cuadrado_general_ranking (dict): Superficie principal del ranking.
        lista_posiciones (list): Lista de elementos del ranking a limpiar.
    """
    cuadrado_general_ranking["superficie"].fill(BLANCO)
    
    for posicion in range (len(lista_posiciones)):
        color = DORADO

        if posicion > 4:
            color = GRIS_OSCURO
        elif posicion > 2:
            color = GRIS
        elif posicion > 0:
            color = BRONCE
        lista_posiciones[posicion]["superficie"].fill(color)

def reiniciar_valores(datos_juego: dict) -> None:
    """Reinicia todos los valores del juego al estado inicial.

    Parámetros:
        datos_juego (dict): Diccionario que contiene el estado del juego.
    """
    datos_juego["nombre"] = ""
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["indice"] = 0
    datos_juego["tiempo_restante"] = 20 
    datos_juego["respuestas_eliminadas"] = []
    datos_juego["bandera_respuesta"] = False
    datos_juego["contador_aciertos"] = 0
    datos_juego["bandera_nombre_error"] = False
    datos_juego["bandera_confirmacion"] = False
    datos_juego["comodines"] = {
        "bomba": True,
        "saltar_turno": True,
        "X2": True,
        "doble_intento": True
    }
    datos_juego["bandera"] = {
        "doble_intento": False,
        "X2": False,
        "bomba": False
    }

def crear_elemento_juego_textura(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    """Crea un elemento del juego usando una imagen como textura.

    Parámetros:
        textura (str): Ruta de la imagen (relativa o absoluta).
        ancho (int): Ancho en píxeles del elemento.
        alto (int): Alto en píxeles del elemento.
        pos_x (int): Posición X del rectángulo.
        pos_y (int): Posición Y del rectángulo.

    Retorna:
        dict: Diccionario con las claves 'superficie' (imagen escalada) y 'rectangulo'.
    """
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = pygame.Rect(pos_x,pos_y,ancho,alto)
    
    return elemento_juego

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int):
    """Reasigna una nueva textura a un elemento del juego, actualizando su superficie.

    Parámetros:
        elemento_juego (dict): Elemento al que se le cambiará la textura.
        textura (str): Ruta de la nueva imagen.
        ancho (int): Nuevo ancho del elemento.
        alto (int): Nuevo alto del elemento.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))