import pygame
from Constantes import *
from Funciones import *
pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load(r"SEGUNDO PARCIAL - PYGAME\texturas\textura_fondo.jpg"), VENTANA)
cuadrado_nombre = crear_elemento_juego(AZUL, 250, 30, 120, 200)
cuadrado_general = crear_elemento_juego(BLANCO, 340, 220, 90, 60)
puntaje_rectangulo = crear_elemento_juego(GRIS_OSCURO, 200, 30, 120, 120)

def mostrar_fin_de_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """Muestra la pantalla final del juego donde el jugador puede ver su puntaje y escribir su nombre. También permite validar la entrada y confirmar el nombre ingresado antes de continuar.

    Parámetros:
        pantalla (pygame.Surface): Superficie principal donde se dibuja la pantalla de fin de juego.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de Pygame capturados (teclado, cerrar ventana, etc.).
        datos_juego (dict): Diccionario que contiene los datos y estado actual del juego.

    Retorna:
        str: Estado posterior al procesamiento de la pantalla:
            - "terminado": Si aún no se completó la validación del nombre.
            - "confirmacion": Si el nombre es válido y se presiona ENTER para continuar.
    """
    pantalla.fill(GRIS)
    retorno = "terminado"
    
    if datos_juego['bandera_nombre_error'] == True:
        SONIDO_EXTRA.play()
        cuadrado_general['superficie'].fill(BLANCO)
        datos_juego['bandera_nombre_error'] = False
        pygame.time.delay(2000)
        
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            mostrar_texto(cuadrado_general['superficie'], "Antes de salir: ¡Guarde su nombre!", (20, 180), FUENTE_TEXTO, ROJO)
            datos_juego['bandera_nombre_error'] = True
            
        elif evento.type == pygame.KEYDOWN:
            bloc_mayuscula = pygame.key.get_mods() & pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            
            if letra_presionada == "backspace" and len(datos_juego['nombre']) > 0:
                datos_juego['nombre'] = datos_juego['nombre'][: -1]
                cuadrado_nombre['superficie'].fill(AZUL)
                
            elif letra_presionada == "space":
                datos_juego['nombre'] += " "
            
            elif len(letra_presionada) == 1 and len(datos_juego['nombre']) < 10:
                if bloc_mayuscula != 0:
                    datos_juego['nombre'] += letra_presionada.upper()
                else:
                    datos_juego['nombre'] += letra_presionada

            elif letra_presionada == "return":
                if len(datos_juego['nombre']) > 3:
                    retorno = "confirmacion"
                else:
                    mostrar_texto(cuadrado_general['superficie'], "Su nombre debe contener al menos 4 palabras.", (20, 180), FUENTE_TEXTO, ROJO)
                    datos_juego['bandera_nombre_error'] = True
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadrado_general['superficie'], cuadrado_general['rectangulo'])
    pantalla.blit(cuadrado_nombre['superficie'], cuadrado_nombre['rectangulo'])
    pantalla.blit(puntaje_rectangulo['superficie'], puntaje_rectangulo['rectangulo'])

    mostrar_texto(cuadrado_general['superficie'],f"> Su puntaje fue: ",(20, 20), FUENTE_MENU, ROJO)
    mostrar_texto(puntaje_rectangulo['superficie'], f"{datos_juego["puntuacion"]}", (40, 0), FUENTE_MENU, BLANCO)
    mostrar_texto(cuadrado_general['superficie'], "> Escriba su nombre:", (20, 100), FUENTE_MENU, ROJO)
    mostrar_texto(cuadrado_nombre['superficie'], datos_juego['nombre'], (5, 10), FUENTE_TEXTO, BLANCO)
    
    if retorno == "confirmacion":
        cuadrado_general['superficie'].fill(BLANCO)
        cuadrado_nombre['superficie'].fill(AZUL)
        puntaje_rectangulo['superficie'].fill(GRIS_OSCURO)
        datos_juego['bandera_nombre_error'] = False

    return retorno

