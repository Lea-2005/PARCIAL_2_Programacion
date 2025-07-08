import pygame
from Partida import *
from Funciones import *

pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load(r"SEGUNDO PARCIAL - PYGAME\texturas\textura_1.jpg"), VENTANA)

lista_menu = crear_lista_menu(AZUL, 250, 50, 120, 100)
texto_botones = ["JUGAR", "RANKING", "AJUSTES", "SALIR"]

def mostrar_menu(pantalla: pygame.Surface, cola_eventos: pygame.event.Event) -> str:
    """Muestra la pantalla principal del menú del juego, con opciones como JUGAR, RANKING, AJUSTES y SALIR. Detecta la opción seleccionada por el usuario y retorna el estado correspondiente.

    Parámetros:
        pantalla (pygame.Surface): Superficie principal donde se dibuja el menú.
        cola_eventos (pygame.event.Event): Lista de eventos capturados (mouse, cierre de ventana, etc.).

    Retorna:
        str: Estado siguiente según la opción seleccionada:
            - "jugar": si se presiona el botón JUGAR.
            - "ranking": si se presiona el botón RANKING.
            - "ajustes": si se presiona el botón AJUSTES.
            - "salir": si se cierra la ventana o se presiona SALIR.
            - "menu": si no se selecciona ninguna opción.
    """
    retorno = "menu"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            SONIDO_BOTON.play()
            menu_click = detectar_click(lista_menu, evento.pos)

            match menu_click:
                case 0:
                    retorno = "jugar"
                case 1:
                    retorno = "ranking"
                case 2:
                    retorno = "ajustes"
                case 3:
                    retorno = "salir"
    pantalla.blit(fondo_pantalla,(0,0))
    dibujar_elemento(pantalla, lista_menu)

    for i in range(4):
        mostrar_texto(lista_menu[i]['superficie'], texto_botones[i], (60, 10), FUENTE_MENU, BLANCO)

    return retorno