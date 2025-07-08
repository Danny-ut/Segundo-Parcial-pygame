import pygame
from config import *

class Tablero:
    def __init__(self):
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
        pantalla = pygame.display.get_surface()
        
        # Fondo del tablero
        pygame.draw.rect(pantalla, BLANCO, (MARGEN_TABLERO, MARGEN_TABLERO, ANCHO - 2*MARGEN_TABLERO, ALTO - 2*MARGEN_TABLERO))
        pygame.draw.rect(pantalla, NEGRO, (MARGEN_TABLERO, MARGEN_TABLERO, ANCHO - 2*MARGEN_TABLERO, ALTO - 2*MARGEN_TABLERO), 2)
        
        # Dibujar casillas 1-15 (fila superior)
        for i in range(15):
            x = 100 + i * 40
            y = 100
            
            # Alternar colores
            color = AZUL_CLARO if i % 2 == 0 else VERDE_CLARO
            
            # Verificar si es casillero especial
            if (i+1) in self.casilleros_especiales:
                color = self.casilleros_especiales[i+1]["color"]
            
            pygame.draw.rect(pantalla, color, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO))
            pygame.draw.rect(pantalla, NEGRO, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO), 1)
            
            num_texto = pygame.font.SysFont("Arial", TAMANO_FUENTE_PEQ).render(str(i+1), True, NEGRO)
            pantalla.blit(num_texto, (x + ANCHO_CASILLERO//2 - num_texto.get_width()//2, 
                                    y + ANCHO_CASILLERO//2 - num_texto.get_height()//2))
        
        # Dibujar casillas 16-30 (fila inferior)
        for i in range(15, 30):
            x = 100 + (i - 15) * 40
            y = 150
            
            # Alternar colores (invertido para la fila inferior)
            color = VERDE_CLARO if (i - 15) % 2 == 0 else AZUL_CLARO
            
            # Verificar si es casillero especial
            if (i+1) in self.casilleros_especiales:
                color = self.casilleros_especiales[i+1]["color"]
            
            pygame.draw.rect(pantalla, color, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO))
            pygame.draw.rect(pantalla, NEGRO, (x, y, ANCHO_CASILLERO, ANCHO_CASILLERO), 1)
            
            num_texto = pygame.font.SysFont("Arial", TAMANO_FUENTE_PEQ).render(str(i+1), True, NEGRO)
            pantalla.blit(num_texto, (x + ANCHO_CASILLERO//2 - num_texto.get_width()//2, 
                                    y + ANCHO_CASILLERO//2 - num_texto.get_height()//2))
        
        # Dibujar jugador
        if 1 <= posicion <= 15:
            x = 100 + (posicion - 1) * 40
            y = 100
        elif 16 <= posicion <= 30:
            x = 100 + (posicion - 16) * 40
            y = 150
        
        pygame.draw.circle(pantalla, ROJO, (x + ANCHO_CASILLERO//2, y + ANCHO_CASILLERO//2), 12)
        pygame.draw.circle(pantalla, NEGRO, (x + ANCHO_CASILLERO//2, y + ANCHO_CASILLERO//2), 12, 1)
        
        # Información del jugador
        info_y = 470
        jugador_texto = pygame.font.SysFont("Arial", TAMANO_FUENTE_MED, bold=True).render(f"Jugador: {jugador}", True, NEGRO)
        pantalla.blit(jugador_texto, (MARGEN_TABLERO, info_y))
        
        puntaje_texto = pygame.font.SysFont("Arial", TAMANO_FUENTE_MED, bold=True).render(f"Puntaje: {puntaje}", True, NEGRO)
        pantalla.blit(puntaje_texto, (MARGEN_TABLERO, info_y + 30))
        
        tiempo_texto = pygame.font.SysFont("Arial", TAMANO_FUENTE_MED, bold=True).render(f"Tiempo: {tiempo_restante}", True, NEGRO)
        pantalla.blit(tiempo_texto, (MARGEN_TABLERO, info_y + 60))