import pygame
import sys
import random
import json
from pygame.locals import *
from preguntas import *
from tablero import *

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpientes y Escaleras - Trivia")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
GRIS = (200, 200, 200)
DORADO = (255, 215, 0)
VERDE_OSCURO = (0, 100, 0)
ROJO_OSCURO = (139, 0, 0)
AZUL_CLARO = (173, 216, 230)

# Fuentes
fuente = pygame.font.SysFont("Arial", 20)
fuente_mediana = pygame.font.SysFont("Arial", 24, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 36, bold=True)

# Estados del juego
MENU = 0
JUGANDO = 1
PUNTAJES = 2
FIN_JUEGO = 3

class Juego:
    def __init__(self):
        self.estado = MENU
        self.jugador = ""
        self.puntaje = 0
        self.posicion = 15
        self.tiempo_restante = 15
        self.ultimo_tiempo = 0
        self.mensaje = ""
        self.mostrar_mensaje = False
        self.tiempo_mensaje = 0
        self.preguntas = preguntas
        self.tablero = tablero
        self.cargar_puntajes()
        self.cargar_recursos()
        self.inicializar_tablero_especial()
    
    def cargar_recursos(self):
        try:
            self.sonido_correcto = pygame.mixer.Sound("correcto.wav")
            self.sonido_incorrecto = pygame.mixer.Sound("incorrecto.wav")
        except:
            print("Sonidos no encontrados. Continuando sin ellos.")
    
    def cargar_puntajes(self):
        try:
            with open("puntajes.json", "r") as archivo:
                self.puntajes = json.load(archivo)
        except:
            self.puntajes = []
    
    def guardar_puntaje(self):
        self.puntajes.append({"nombre": self.jugador, "puntaje": self.puntaje})
        self.puntajes.sort(key=lambda x: x["puntaje"], reverse=True)
        with open("puntajes.json", "w") as archivo:
            json.dump(self.puntajes, archivo)
    
    def obtener_pregunta_aleatoria(self):
        return random.choice(self.preguntas)
    
    def inicializar_tablero_especial(self):
        # Definir casilleros especiales duales (pueden ser escalera o serpiente)
        # Cada casillero especial tiene un valor (1 o 2)
        self.casilleros_especiales = {
            3: {"valor": 1},   # Casillero especial tipo 1
            6: {"valor": 1},  # Casillero especial tipo 1
            9: {"valor": 2},   # Casillero especial tipo 2
            12: {"valor": 2}, # Casillero especial tipo 2
            15: {"valor": 1},
            18: {"valor": 1},
            21: {"valor": 2},
            24: {"valor": 2},
            27: {"valor": 1}
        }

    
    def dibujar_menu(self):
        pantalla.fill(AZUL_CLARO)
        
        titulo = fuente_grande.render("Serpientes y Escaleras", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        pygame.draw.rect(pantalla, BLANCO, (ANCHO//2 - 150, 200, 300, 40))
        nombre_texto = fuente_mediana.render(f"Nombre: {self.jugador}", True, NEGRO)
        pantalla.blit(nombre_texto, (ANCHO//2 - 140, 210))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 300, 200, 50))
        jugar_texto = fuente_mediana.render("Jugar", True, NEGRO)
        pantalla.blit(jugar_texto, (ANCHO//2 - jugar_texto.get_width()//2, 315))
        
        pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 100, 370, 200, 50))
        puntajes_texto = fuente_mediana.render("Ver Puntajes", True, NEGRO)
        pantalla.blit(puntajes_texto, (ANCHO//2 - puntajes_texto.get_width()//2, 385))
        
        pygame.draw.rect(pantalla, ROJO, (ANCHO//2 - 100, 440, 200, 50))
        salir_texto = fuente_mediana.render("Salir", True, NEGRO)
        pantalla.blit(salir_texto, (ANCHO//2 - salir_texto.get_width()//2, 455))
    
    def dibujar_tablero(self):
        # Fondo del tablero
        pygame.draw.rect(pantalla, BLANCO, (50, 50, 700, 500))
        pygame.draw.rect(pantalla, NEGRO, (50, 50, 700, 500), 2)
        
        # Dibujar casillas 1-15 (fila superior)
        for i in range(15):
            x = 100 + i * 40
            y = 100
            color = AZUL_CLARO
            
            if self.tablero[i]["tipo"] == "serpiente_verde":
                color = VERDE_OSCURO
                
            pygame.draw.rect(pantalla, color, (x, y, 30, 30))
            pygame.draw.rect(pantalla, NEGRO, (x, y, 30, 30), 1)
            
            num_texto = fuente.render(str(i+1), True, NEGRO)
            pantalla.blit(num_texto, (x + 15 - num_texto.get_width()//2, y + 15 - num_texto.get_height()//2))
        
        # Dibujar casillas 16-30 (fila inferior)
        for i in range(15, 30):
            x = 100 + (i - 15) * 40
            y = 150
            color = AZUL_CLARO
            
            if self.tablero[i]["tipo"] == "escalera_normal":
                color = GRIS
                
            pygame.draw.rect(pantalla, color, (x, y, 30, 30))
            pygame.draw.rect(pantalla, NEGRO, (x, y, 30, 30), 1)
            
            num_texto = fuente.render(str(i+1), True, NEGRO)
            pantalla.blit(num_texto, (x + 15 - num_texto.get_width()//2, y + 15 - num_texto.get_height()//2))
        
        # Dibujar jugador
        if 1 <= self.posicion <= 15:
            x = 100 + (self.posicion - 1) * 40
            y = 100
        elif 16 <= self.posicion <= 30:
            x = 100 + (self.posicion - 16) * 40
            y = 150
        
        pygame.draw.circle(pantalla, ROJO, (x + 15, y + 15), 12)
        pygame.draw.circle(pantalla, NEGRO, (x + 15, y + 15), 12, 1)
        
        # Información del jugador
        info_y = 470
        jugador_texto = fuente_mediana.render(f"Jugador: {self.jugador}", True, NEGRO)
        pantalla.blit(jugador_texto, (50, info_y))
        
        puntaje_texto = fuente_mediana.render(f"Puntaje: {self.puntaje}", True, NEGRO)
        pantalla.blit(puntaje_texto, (50, info_y + 30))
        
        tiempo_texto = fuente_mediana.render(f"Tiempo: {self.tiempo_restante}", True, NEGRO)
        pantalla.blit(tiempo_texto, (50, info_y + 60))
    
    def dibujar_pregunta(self):
        # Área de pregunta
        pygame.draw.rect(pantalla, BLANCO, (100, 250, 600, 120))
        pygame.draw.rect(pantalla, NEGRO, (100, 250, 600, 120), 2)
        
        # Pregunta
        pregunta_texto = fuente_mediana.render(self.pregunta_actual["pregunta"], True, NEGRO)
        pantalla.blit(pregunta_texto, (110, 260))
        
        # Opciones
        for i, opcion in enumerate(self.pregunta_actual["opciones"]):
            opcion_x = 150 + i * 200
            pygame.draw.rect(pantalla, AMARILLO, (opcion_x, 320, 150, 40))
            pygame.draw.rect(pantalla, NEGRO, (opcion_x, 320, 150, 40), 2)
            
            opcion_texto = fuente.render(opcion, True, NEGRO)
            pantalla.blit(opcion_texto, (opcion_x + 75 - opcion_texto.get_width()//2, 340 - opcion_texto.get_height()//2))
    
    def dibujar_mensaje(self):
        if self.mostrar_mensaje and pygame.time.get_ticks() - self.tiempo_mensaje < 2000:
            mensaje_rect = pygame.Rect(ANCHO//2 - 200, ALTO//2 - 25, 400, 50)
            pygame.draw.rect(pantalla, AMARILLO, mensaje_rect)
            pygame.draw.rect(pantalla, NEGRO, mensaje_rect, 2)
            
            mensaje_texto = fuente_mediana.render(self.mensaje, True, NEGRO)
            pantalla.blit(mensaje_texto, (ANCHO//2 - mensaje_texto.get_width()//2, ALTO//2 - mensaje_texto.get_height()//2))
    
    def dibujar_puntajes(self):
        pantalla.fill(BLANCO)
        
        titulo = fuente_grande.render("Mejores Puntajes", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        if not self.puntajes:
            texto = fuente_mediana.render("No hay puntajes aún", True, NEGRO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 150))
        else:
            for i, puntaje in enumerate(self.puntajes[:10]):
                texto = fuente_mediana.render(f"{i+1}. {puntaje['nombre']}: {puntaje['puntaje']}", True, NEGRO)
                pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 120 + i * 40))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 550, 200, 40))
        volver_texto = fuente_mediana.render("Volver al Menú", True, NEGRO)
        pantalla.blit(volver_texto, (ANCHO//2 - volver_texto.get_width()//2, 560))
    
    def dibujar_fin_juego(self):
        pantalla.fill(BLANCO)
        
        titulo = fuente_grande.render("Fin del Juego", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        resultado_texto = fuente_mediana.render(f"{self.jugador}, tu puntaje final es: {self.puntaje}", True, NEGRO)
        pantalla.blit(resultado_texto, (ANCHO//2 - resultado_texto.get_width()//2, 200))
        
        posicion = 1
        for p in self.puntajes:
            if p["puntaje"] > self.puntaje:
                posicion += 1
        
        posicion_texto = fuente_mediana.render(f"Tu posición en el ranking: {posicion}", True, NEGRO)
        pantalla.blit(posicion_texto, (ANCHO//2 - posicion_texto.get_width()//2, 250))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 350, 200, 50))
        menu_texto = fuente_mediana.render("Volver al Menú", True, NEGRO)
        pantalla.blit(menu_texto, (ANCHO//2 - menu_texto.get_width()//2, 365))
    
    def manejar_eventos_menu(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_BACKSPACE:
                self.jugador = self.jugador[:-1]
            elif evento.unicode.isprintable():
                self.jugador += evento.unicode
        
        elif evento.type == MOUSEBUTTONDOWN:
            x, y = evento.pos
            
            if ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 300 <= y <= 350:
                if self.jugador.strip():
                    self.estado = JUGANDO
                    self.pregunta_actual = self.obtener_pregunta_aleatoria()
                    self.ultimo_tiempo = pygame.time.get_ticks()
            
            elif ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 370 <= y <= 420:
                self.estado = PUNTAJES
            
            elif ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 440 <= y <= 490:
                pygame.quit()
                sys.exit()
    
    def manejar_eventos_jugando(self, evento):
        if evento.type == MOUSEBUTTONDOWN:
            x, y = evento.pos
            
            for i in range(3):
                if 150 + i * 200 <= x <= 150 + i * 200 + 150 and 320 <= y <= 360:
                    self.verificar_respuesta(i)
        
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                self.estado = FIN_JUEGO
                self.guardar_puntaje()
    
    def verificar_respuesta(self, opcion):
        correcta = opcion == self.pregunta_actual["correcta"]
        movimiento = 1
        mensaje = ""

        if correcta:
            self.puntaje += 10
            if hasattr(self, 'sonido_correcto'):
                self.sonido_correcto.play()
            mensaje = "¡Respuesta correcta!"
            
            # Avanzar
            nueva_pos = self.posicion + movimiento
            nueva_pos = min(nueva_pos, 30)
            
            # Verificar si cayó en casillero especial (actuará como escalera)
            if nueva_pos in self.casilleros_especiales:
                valor = self.casilleros_especiales[nueva_pos]["valor"]
                nueva_pos = min(nueva_pos + valor, 30)
                mensaje += f" ¡Escalera! avanzas {valor} casilleros"
        else:
            if hasattr(self, 'sonido_incorrecto'):
                self.sonido_incorrecto.play()
            mensaje = "Respuesta incorrecta"
            
            # Retroceder
            nueva_pos = self.posicion - movimiento
            nueva_pos = max(nueva_pos, 1)
            
            # Verificar si cayó en casillero especial (actuará como serpiente)
            if nueva_pos in self.casilleros_especiales:
                valor = self.casilleros_especiales[nueva_pos]["valor"]
                nueva_pos = max(nueva_pos - valor, 1)
                mensaje += f" ¡Serpiente! Retrocedes {valor} casilleros "

        self.posicion = nueva_pos
        self.mensaje = mensaje
        self.mostrar_mensaje = True
        self.tiempo_mensaje = pygame.time.get_ticks()

        if self.posicion >= 30:
            self.estado = FIN_JUEGO
            self.puntaje += 50
            self.guardar_puntaje()
        else:
            self.pregunta_actual = self.obtener_pregunta_aleatoria()
            self.tiempo_restante = 15
            self.ultimo_tiempo = pygame.time.get_ticks()
    
    def actualizar_tiempo(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_tiempo >= 1000:
            self.tiempo_restante -= 1
            self.ultimo_tiempo = ahora
            
            if self.tiempo_restante <= 0:
                self.verificar_respuesta(-1)
    
    def resetear_juego(self):
        self.puntaje = 0
        self.posicion = 1
        self.tiempo_restante = 15
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.estado == MENU:
                    self.manejar_eventos_menu(evento)
                elif self.estado == JUGANDO:
                    self.manejar_eventos_jugando(evento)
                elif self.estado == PUNTAJES:
                    if evento.type == MOUSEBUTTONDOWN:
                        x, y = evento.pos
                        if ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 550 <= y <= 590:
                            self.estado = MENU
                elif self.estado == FIN_JUEGO:
                    if evento.type == MOUSEBUTTONDOWN:
                        x, y = evento.pos
                        if ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 350 <= y <= 400:
                            self.estado = MENU
                            self.resetear_juego()
            
            if self.estado == JUGANDO:
                self.actualizar_tiempo()
            
            if self.estado == MENU:
                self.dibujar_menu()
            elif self.estado == JUGANDO:
                pantalla.fill(BLANCO)
                self.dibujar_tablero()
                self.dibujar_pregunta()
                self.dibujar_mensaje()
            elif self.estado == PUNTAJES:
                self.dibujar_puntajes()
            elif self.estado == FIN_JUEGO:
                self.dibujar_fin_juego()
            
            pygame.display.flip()
            reloj.tick(60)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()