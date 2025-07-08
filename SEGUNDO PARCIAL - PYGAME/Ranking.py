import pygame
from Constantes import *
from Funciones import *

pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load(r"SEGUNDO PARCIAL - PYGAME\texturas\textura_2.jpg"), VENTANA)

cuadrado_general_ranking = crear_elemento_juego(BLANCO, 370, 470, 65, 5)
lista_posiciones = crear_lista_ranking(DORADO, BRONCE, GRIS, GRIS_OSCURO, 300, 30, 85, 12)
boton_atras = crear_elemento_juego(ROJO, 20, 20, 400, 10)

def mostrar_ranking(pantalla: pygame.Surface, lista_ranking: list, cola_eventos: list[pygame.event.Event], lista_posiciones: list) -> str:
    """Muestra en pantalla el ranking de los jugadores con sus nombres, puntajes y fechas. También permite volver al menú principal mediante un botón.

    Parámetros:
        pantalla (pygame.Surface): Superficie principal donde se dibuja el ranking.
        lista_ranking (list): Lista de diccionarios que contiene los datos del ranking (nombre, puntuación, fecha).
        cola_eventos (list[pygame.event.Event]): Lista de eventos capturados (ej: clics del mouse, cerrar ventana).
        lista_posiciones (list): Lista de elementos visuales donde se dibujarán las posiciones del ranking.

    Retorna:
        str: Estado posterior a la visualización:
            - "ranking": si no hubo interacción del usuario.
            - "menu": si el usuario hace clic en el botón de volver.
            - "salir": si se cierra la ventana del juego.
    """
    retorno = "ranking"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_atras['rectangulo'].collidepoint(evento.pos):
                retorno = "menu"
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadrado_general_ranking["superficie"], cuadrado_general_ranking["rectangulo"])
    dibujar_elemento(pantalla, lista_posiciones)

    for i in range(len(lista_ranking)):
        texto = f"{lista_ranking[i]['nombre']} | {lista_ranking[i]['puntuacion']} | {lista_ranking[i]['fecha']}"
        mostrar_texto(lista_posiciones[i]["superficie"], texto, (10, 10), FUENTE_TEXTO, NEGRO)

    mostrar_texto(boton_atras['superficie'], "<", (5,0), FUENTE_TEXTO, BLANCO)
    pantalla.blit(boton_atras['superficie'], boton_atras['rectangulo'])

    if retorno != "ranking":
        actualizar_cuadro_ranking(cuadrado_general_ranking, lista_posiciones)

    return retorno
