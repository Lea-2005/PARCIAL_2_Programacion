import pygame
from Constantes import *
from Funciones import *
pygame.init()

fondo_pantalla = pygame.transform.scale(pygame.image.load(r"SEGUNDO PARCIAL - PYGAME\texturas\textura_3.jpg"), VENTANA)
cuadrado_confirmacion = crear_elemento_juego(BLANCO, 340, 300, 90, 110)
rectangulo_informacion = crear_elemento_juego(GRIS, 280, 40, 120, 240)
lista_confirmacion = crear_lista_confirmacion(GRIS, 40, 40, 120, 350)
texto_botones = ["SI", "NO", "VOLVER"]

def mostrar_recuadro_confirmacion(pantalla: pygame.surface, cuadrado_confirmacion: dict, datos_juego: dict, cola_eventos: list[pygame.event.Event], lista_ranking: list[dict]) -> str:
    """Muestra una interfaz para que el jugador confirme si desea guardar su puntuación en el ranking. Permite guardar, no guardar o volver a la pantalla anterior si lo desea.

    Parámetros:
        pantalla (pygame.Surface): Superficie principal donde se dibuja la ventana de confirmación.
        cuadrado_confirmacion (dict): Elemento visual principal del recuadro de confirmación.
        datos_juego (dict): Diccionario con los datos actuales del jugador (nombre, puntuación, banderas).
        cola_eventos (list[pygame.event.Event]): Lista de eventos de Pygame para manejar interacciones del jugador.
        lista_ranking (list[dict]): Lista del ranking de jugadores ya registrados.

    Retorna:
        str: Estado posterior a la selección del jugador:
            - "reiniciar": si elige guardar ("SI") o no guardar ("NO").
            - "terminado": si elige "VOLVER" a la pantalla anterior.
            - "confirmacion": si aún no se ha tomado una decisión.
    """
    pantalla.fill(GRIS_OSCURO)
    retorno = "confirmacion"

    if datos_juego["bandera_confirmacion"]:
        actualizar_cuadro_confirmacion(cuadrado_confirmacion, rectangulo_informacion, lista_confirmacion)
        datos_juego["bandera_confirmacion"] = False

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            confirmacion_click = detectar_click(lista_confirmacion, evento.pos)

            if confirmacion_click == 0:
                guardar_ranking(datos_juego, lista_ranking)
                generar_json("partidas.json", lista_ranking)
                retorno = "reiniciar"
            elif confirmacion_click == 1:
                retorno = "reiniciar"
            elif confirmacion_click == 2:
                retorno = "terminado"
            datos_juego["bandera_confirmacion"] = True
    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(cuadrado_confirmacion["superficie"], cuadrado_confirmacion["rectangulo"])
    pantalla.blit(rectangulo_informacion["superficie"], rectangulo_informacion["rectangulo"])
    dibujar_elemento(pantalla, lista_confirmacion)

    for i in range(3):
        mostrar_texto(lista_confirmacion[i]["superficie"], texto_botones[i], (10,10), FUENTE_TEXTO, NEGRO)

    mostrar_texto(cuadrado_confirmacion["superficie"], "¿Quieres guardar tu información en el ranking?", (20, 20), FUENTE_MENU, NEGRO)
    mostrar_texto(rectangulo_informacion["superficie"], f"{datos_juego["nombre"]}   |   {datos_juego["puntuacion"]}", (20, 10), FUENTE_TEXTO, NEGRO)

    if retorno != "confirmacion":
        actualizar_cuadro_confirmacion(cuadrado_confirmacion, rectangulo_informacion, lista_confirmacion)
        
    return retorno