import pygame
from config import *

class Tablero:
    def __init__(self):
        '''
        Inicializa los casilleros especiales del tablero con sus valores y colores.
        '''
        self.casilleros_especiales = {
            3: {"valor": 1, "color": DORADO},
            6: {"valor": 1, "color": DORADO},
            9: {"valor": 2, "color": DORADO},
            12: {"valor": 2, "color": DORADO},
            15: {"valor": 1, "color": DORADO},
            18: {"valor": 1, "color": DORADO},
            21: {"valor": 2, "color": DORADO},
            24: {"valor": 2, "color": DORADO},
            27: {"valor": 1, "color": DORADO}
        }

    def dibujar(self, posicion, jugador, puntaje, tiempo_restante):
        '''
        Dibuja el tablero completo, incluyendo casillas, jugador y datos del estado del juego.

        Parámetros:
        - posicion: casilla actual del jugador (int)
        - jugador: nombre del jugador (str)
        - puntaje: puntaje actual (int)
        - tiempo_restante: segundos restantes para responder (int)
        '''
        pantalla = pygame.display.get_surface()
        fuente = pygame.font.SysFont("Arial", 14, bold=True)

        self.dibujar_fondo(pantalla)
        self.dibujar_filas(pantalla, fuente)
        self.dibujar_jugador(pantalla, posicion)
        self.dibujar_info(pantalla, jugador, puntaje, tiempo_restante)

    def dibujar_fondo(self, pantalla):
        '''
        Dibuja el fondo del área del tablero.
        '''
        pygame.draw.rect(pantalla, BLANCO, (MARGEN_TABLERO, MARGEN_TABLERO, ANCHO - 2*MARGEN_TABLERO, ALTO - 2*MARGEN_TABLERO))
        pygame.draw.rect(pantalla, NEGRO, (MARGEN_TABLERO, MARGEN_TABLERO, ANCHO - 2*MARGEN_TABLERO, ALTO - 2*MARGEN_TABLERO), 2)

    def dibujar_filas(self, pantalla, fuente):
        '''
        Dibuja las dos filas de casillas (1-15 y 16-30), con sus colores y valores.

        Parámetros:
        - pantalla: superficie de pygame donde se dibuja
        - fuente: fuente usada para mostrar valores en las casillas
        '''
        for fila in range(2):
            for i in range(15):
                casillero_num = i + 1 + (fila * 15)
                x = 100 + i * 40
                y = 100 + (fila * 50)

                if fila == 0:
                    color = ROJO if i == 0 else VERDE_CLARO
                else:
                    color = AZUL if i == 14 else VERDE_CLARO

                if casillero_num in self.casilleros_especiales:
                    color = self.casilleros_especiales[casillero_num]["color"]
                    valor = self.casilleros_especiales[casillero_num]["valor"]
                else:
                    valor = 0

                pygame.draw.rect(pantalla, color, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO))
                pygame.draw.rect(pantalla, NEGRO, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO), 1)

                valor_texto = fuente.render(str(valor), True, NEGRO)
                pantalla.blit(valor_texto, (
                    x + ANCHO_CASILLERO // 2 - valor_texto.get_width() // 2,
                    y + ANCHO_CASILLERO // 2 - valor_texto.get_height() // 2
                ))

    def dibujar_jugador(self, pantalla, posicion):
        '''
        Dibuja la ficha del jugador en su posición actual.

        Parámetros:
        - pantalla: superficie de pygame donde se dibuja
        - posicion: casilla actual del jugador (int)
        '''
        if 1 <= posicion <= 15:
            x = 100 + (posicion - 1) * 40
            y = 100
        elif 16 <= posicion <= 30:
            x = 100 + (posicion - 16) * 40
            y = 150
        else:
            return  

        pygame.draw.circle(pantalla, ROJO, (x + ANCHO_CASILLERO//2, y + ANCHO_CASILLERO//2), 12)
        pygame.draw.circle(pantalla, NEGRO, (x + ANCHO_CASILLERO//2, y + ANCHO_CASILLERO//2), 12, 1)

    def dibujar_info(self, pantalla, jugador, puntaje, tiempo_restante):
        '''
        Dibuja la información del jugador debajo del tablero: nombre, puntaje y tiempo.

        Parámetros:
        - pantalla: superficie de pygame donde se dibuja
        - jugador: nombre del jugador (str)
        - puntaje: puntaje actual (int)
        - tiempo_restante: segundos restantes para responder (int)
        '''
        info_x = 60
        info_y = 500
        fuente = pygame.font.SysFont("Arial", TAMANO_FUENTE_MED, bold=True)

        jugador_texto = fuente.render(f"Jugador: {jugador}", True, NEGRO)
        pantalla.blit(jugador_texto, (info_x, info_y))

        puntaje_texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        pantalla.blit(puntaje_texto, (info_x, info_y + 30))

        tiempo_texto = fuente.render(f"Tiempo: {tiempo_restante}", True, NEGRO)
        pantalla.blit(tiempo_texto, (info_x, info_y + 60))
