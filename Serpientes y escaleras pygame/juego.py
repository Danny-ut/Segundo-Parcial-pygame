import pygame
import json
import random
from pygame.locals import *
from config import *
from tablero import *
from preguntas import *

class Juego:
    def __init__(self):
        '''
        Inicializa los atributos principales del juego, incluyendo el estado, jugador, puntaje,
        temporizador, tablero, sonidos, fuentes y puntajes previos.
        '''
        self.estado = MENU
        self.jugador = ""
        self.puntaje = 0
        self.posicion = POSICION_INICIAL
        self.tiempo_restante = TIEMPO_PREGUNTA
        self.ultimo_tiempo = 0
        self.mensaje = ""
        self.mostrar_mensaje = False
        self.tiempo_mensaje = 0
        self.preguntas = preguntas
        self.tablero = Tablero()
        self.cargar_puntajes()
        self.cargar_recursos()
        self.inicializar_fuentes()
        self.esperando_confirmacion = False
        self.respuesta_confirmacion = None
        self.pregunta_actual = None  
        
    def inicializar_fuentes(self):
        '''
        Carga las fuentes de texto que se usarán para mostrar textos en pantalla,
        con diferentes tamaños y estilos.
        '''
        self.fuente_peq = pygame.font.SysFont("Arial", TAMANO_FUENTE_PEQ)
        self.fuente_med = pygame.font.SysFont("Arial", TAMANO_FUENTE_MED, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", TAMANO_FUENTE_GRANDE, bold=True)
    
    def cargar_recursos(self):
        '''
        Intenta cargar los archivos de sonido para respuestas correctas e incorrectas.
        Si no los encuentra, el juego continúa sin sonidos.
        '''
        try:
            self.sonido_correcto = pygame.mixer.Sound("sonidos/correcto.wav")
            self.sonido_incorrecto = pygame.mixer.Sound("sonidos/incorrecto.wav")
        except:
            print("Sonidos no encontrados. Continuando sin ellos.")
    
    def cargar_puntajes(self):
        '''
        Carga los puntajes guardados desde un archivo JSON.
        Si el archivo no existe o hay error, inicia con una lista vacía.
        '''
        try:
            with open("puntajes.json", "r") as archivo:
                self.puntajes = json.load(archivo)
        except:
            self.puntajes = []
    
    def guardar_puntaje(self):
        '''
        Agrega el puntaje actual al ranking, lo ordena y lo guarda en el archivo JSON.
        '''
        self.puntajes.append({"nombre": self.jugador, "puntaje": self.puntaje})
        self.puntajes.sort(key=lambda x: x["puntaje"], reverse=True)
        with open("puntajes.json", "w") as archivo:
            json.dump(self.puntajes, archivo)
    
    def obtener_pregunta_aleatoria(self):
        '''
        Devuelve una pregunta aleatoria de la lista de preguntas cargadas.
        '''
        return random.choice(self.preguntas)
    
    def dibujar_menu(self):
        '''
        Dibuja el menú principal, que incluye el título, campo de nombre,
        y los botones de Jugar, Ver Puntajes y Salir.
        '''
        pantalla = pygame.display.get_surface()
        pantalla.fill(AZUL_CLARO)
        
        titulo = self.fuente_grande.render("Serpientes y Escaleras", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        pygame.draw.rect(pantalla, BLANCO, (ANCHO//2 - 150, 200, 300, 40))
        nombre_texto = self.fuente_med.render(f"Nombre: {self.jugador}", True, NEGRO)
        pantalla.blit(nombre_texto, (ANCHO//2 - 140, 210))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 300, 200, 50))
        jugar_texto = self.fuente_med.render("Jugar", True, NEGRO)
        pantalla.blit(jugar_texto, (ANCHO//2 - jugar_texto.get_width()//2, 315))
        
        pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 100, 370, 200, 50))
        puntajes_texto = self.fuente_med.render("Ver Puntajes", True, NEGRO)
        pantalla.blit(puntajes_texto, (ANCHO//2 - puntajes_texto.get_width()//2, 385))
        
        pygame.draw.rect(pantalla, ROJO, (ANCHO//2 - 100, 440, 200, 50))
        salir_texto = self.fuente_med.render("Salir", True, NEGRO)
        pantalla.blit(salir_texto, (ANCHO//2 - salir_texto.get_width()//2, 455))
    
    def dibujar_pregunta(self):
        '''
        Muestra la pregunta actual en pantalla, dividida en líneas si es necesario,
        junto con las opciones de respuesta.
        '''
        pantalla = pygame.display.get_surface()
        pygame.draw.rect(pantalla, AZUL_CLARO, (50, 200, 800, 150))
        pygame.draw.rect(pantalla, NEGRO, (50, 200, 800, 150), 2)
        
        pregunta_lines = self.wrap_text(self.pregunta_actual["pregunta"], self.fuente_med, 780)
        for i, line in enumerate(pregunta_lines):
            pregunta_texto = self.fuente_med.render(line, True, NEGRO)
            pantalla.blit(pregunta_texto, (60, 210 + i * 30))
        
        # Opciones
        for i, opcion in enumerate(self.pregunta_actual["opciones"]):
            opcion_x = 100 + i * 250
            pygame.draw.rect(pantalla, AMARILLO, (opcion_x, 350, 200, 40))
            pygame.draw.rect(pantalla, NEGRO, (opcion_x, 350, 200, 40), 2)
            
            opcion_texto = self.fuente_peq.render(opcion, True, NEGRO)
            pantalla.blit(opcion_texto, (opcion_x + 100 - opcion_texto.get_width()//2, 370 - opcion_texto.get_height()//2))
    
    def wrap_text(self, text, font, max_width):
        '''
        Divide un texto largo en múltiples líneas que no excedan el ancho máximo indicado.
        Parámetros:
        - text: texto completo a dividir
        - font: fuente usada para medir el ancho del texto
        - max_width: ancho máximo por línea en píxeles
        '''
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width = font.size(test_line)[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def dibujar_confirmacion(self):
        '''
        Dibuja la ventana emergente para confirmar si el jugador desea continuar
        después de responder una pregunta.
        '''
        pantalla = pygame.display.get_surface()
        confirm_rect = pygame.Rect(ANCHO//2 - 200, ALTO//2 - 75, 400, 150)
        pygame.draw.rect(pantalla, AMARILLO, confirm_rect)
        pygame.draw.rect(pantalla, NEGRO, confirm_rect, 3)
        
        pregunta_texto = self.fuente_med.render("¿Queres seguir jugando?", True, NEGRO)
        pantalla.blit(pregunta_texto, (ANCHO//2 - pregunta_texto.get_width()//2, ALTO//2 - 50))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 150, ALTO//2, 120, 40))
        si_texto = self.fuente_med.render("Sí", True, NEGRO)
        pantalla.blit(si_texto, (ANCHO//2 - 90 - si_texto.get_width()//2, ALTO//2 + 20 - si_texto.get_height()//2))
        
        pygame.draw.rect(pantalla, ROJO, (ANCHO//2 + 30, ALTO//2, 120, 40))
        no_texto = self.fuente_med.render("No", True, NEGRO)
        pantalla.blit(no_texto, (ANCHO//2 + 90 - no_texto.get_width()//2, ALTO//2 + 20 - no_texto.get_height()//2))
    
    def dibujar_mensaje(self):
        '''
        Muestra un mensaje temporal en el centro de la pantalla durante 2 segundos,
        como feedback visual tras una respuesta.
        '''
        if self.mostrar_mensaje and pygame.time.get_ticks() - self.tiempo_mensaje < 2000:
            pantalla = pygame.display.get_surface()
            mensaje_rect = pygame.Rect(ANCHO//2 - 400, ALTO//2 - 25, 800, 50)
            pygame.draw.rect(pantalla, GRIS, mensaje_rect)
            pygame.draw.rect(pantalla, NEGRO, mensaje_rect, 2)
            
            mensaje_texto = self.fuente_med.render(self.mensaje, True, NEGRO)
            pantalla.blit(mensaje_texto, (ANCHO//2 - mensaje_texto.get_width()//2, ALTO//2 - mensaje_texto.get_height()//2))
    
    def dibujar_puntajes(self):
        '''
        Muestra los mejores puntajes guardados, ordenados, y una opción para volver al menú.
        '''
        pantalla = pygame.display.get_surface()
        pantalla.fill(BLANCO)
        
        titulo = self.fuente_grande.render("Mejores Puntajes", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        if not self.puntajes:
            texto = self.fuente_med.render("No hay puntajes aún", True, NEGRO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 150))
        else:
            for i, puntaje in enumerate(self.puntajes[:10]):
                texto = self.fuente_med.render(f"{i+1}. {puntaje['nombre']}: {puntaje['puntaje']}", True, NEGRO)
                pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 120 + i * 40))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 550, 200, 40))
        volver_texto = self.fuente_med.render("Volver al Menú", True, NEGRO)
        pantalla.blit(volver_texto, (ANCHO//2 - volver_texto.get_width()//2, 560))
    
    def dibujar_fin_juego(self):
        '''
        Dibuja la pantalla de fin del juego, mostrando el puntaje final del jugador
        y su posición en el ranking.
        '''
        pantalla = pygame.display.get_surface()
        pantalla.fill(BLANCO)
        
        titulo = self.fuente_grande.render("Fin del Juego", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        resultado_texto = self.fuente_med.render(f"{self.jugador}, tu puntaje final es: {self.puntaje}", True, NEGRO)
        pantalla.blit(resultado_texto, (ANCHO//2 - resultado_texto.get_width()//2, 200))
        
        posicion = 1
        for p in self.puntajes:
            if p["puntaje"] > self.puntaje:
                posicion += 1
        
        posicion_texto = self.fuente_med.render(f"Tu posición en el ranking: {posicion}", True, NEGRO)
        pantalla.blit(posicion_texto, (ANCHO//2 - posicion_texto.get_width()//2, 250))
        
        pygame.draw.rect(pantalla, VERDE, (ANCHO//2 - 100, 350, 200, 50))
        menu_texto = self.fuente_med.render("Volver al Menú", True, NEGRO)
        pantalla.blit(menu_texto, (ANCHO//2 - menu_texto.get_width()//2, 365))
    
    def manejar_eventos_menu(self, evento):
        '''
        Gestiona los eventos que ocurren en el menú: ingreso de nombre por teclado,
        clics sobre los botones de Jugar, Ver Puntajes o Salir.
        Parámetros:
        - evento: evento de teclado o mouse capturado por pygame
        '''
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
    
    def verificar_respuesta(self, opcion):
        '''
        Evalúa si la respuesta seleccionada es correcta o no, reproduce sonidos,
        muestra mensajes y actualiza la posición del jugador según reglas del tablero.
        Parámetros:
        - opcion: índice de la opción seleccionada (0, 1, 2) o -1 si se acabó el tiempo
        '''
        correcta = opcion == self.pregunta_actual["correcta"]
        movimiento = 1
        mensaje = ""

        if correcta:
            self.puntaje += PUNTOS_ACIERTO
            if hasattr(self, 'sonido_correcto'):
                self.sonido_correcto.play()
            mensaje = "¡Respuesta correcta!"
            
            nueva_pos = self.posicion + movimiento
            nueva_pos = min(nueva_pos, CASILLEROS_TOTALES)
            
            if nueva_pos in self.tablero.casilleros_especiales:
                valor = self.tablero.casilleros_especiales[nueva_pos]["valor"]
                nueva_pos = min(nueva_pos + valor, CASILLEROS_TOTALES)
                mensaje += f" ¡Escalera! avanzas {valor} casilleros"
        else:
            if hasattr(self, 'sonido_incorrecto'):
                self.sonido_incorrecto.play()
            mensaje = "Respuesta incorrecta"
            
            nueva_pos = self.posicion - movimiento
            nueva_pos = max(nueva_pos, 1)
            
            if nueva_pos in self.tablero.casilleros_especiales:
                valor = self.tablero.casilleros_especiales[nueva_pos]["valor"]
                nueva_pos = max(nueva_pos - valor, 1)
                mensaje += f" ¡Serpiente! Retrocedes {valor} casilleros"

        self.posicion = nueva_pos
        self.mensaje = mensaje
        self.mostrar_mensaje = True
        self.tiempo_mensaje = pygame.time.get_ticks()
        self.esperando_confirmacion = True
        self.respuesta_confirmacion = None
        
        if self.posicion == 1:
            self.estado = FIN_JUEGO
            self.mensaje = "¡Has caído al inicio! Fin del juego."
            self.guardar_puntaje()
        elif self.posicion >= CASILLEROS_TOTALES:
            self.estado = FIN_JUEGO
            self.puntaje += PUNTOS_META
            self.guardar_puntaje()
        else:
            self.pregunta_actual = self.obtener_pregunta_aleatoria()
            self.tiempo_restante = TIEMPO_PREGUNTA  
            self.ultimo_tiempo = pygame.time.get_ticks()
    
    def manejar_eventos_jugando(self, evento):
        '''
        Gestiona los eventos durante la partida: clics en respuestas, escape para salir,
        o confirmar si se desea continuar tras responder.
        Parámetros:
        - evento: evento de pygame (mouse o teclado)
        '''
        if self.esperando_confirmacion:
            if evento.type == MOUSEBUTTONDOWN:
                x, y = evento.pos
                
                # Botón Sí
                if ANCHO//2 - 150 <= x <= ANCHO//2 - 30 and ALTO//2 <= y <= ALTO//2 + 40:
                    self.esperando_confirmacion = False
                    if self.posicion == 1:
                        self.estado = FIN_JUEGO
                        self.guardar_puntaje()
                    elif self.posicion >= CASILLEROS_TOTALES:
                        self.estado = FIN_JUEGO
                        self.puntaje += PUNTOS_META
                        self.guardar_puntaje()
                    else:
                        self.pregunta_actual = self.obtener_pregunta_aleatoria()
                        self.tiempo_restante = TIEMPO_PREGUNTA
                        self.ultimo_tiempo = pygame.time.get_ticks()
                
                # Botón No
                elif ANCHO//2 + 30 <= x <= ANCHO//2 + 150 and ALTO//2 <= y <= ALTO//2 + 40:
                    self.esperando_confirmacion = False
                    self.estado = FIN_JUEGO
                    self.guardar_puntaje()
        
        elif evento.type == MOUSEBUTTONDOWN:
            x, y = evento.pos
            
            for i in range(3):
                if 150 + i * 250 <= x <= 150 + i * 250 + 200 and 350 <= y <= 390:
                    self.verificar_respuesta(i)
        
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                self.estado = FIN_JUEGO
                self.guardar_puntaje()
    
    def actualizar_tiempo(self):
        '''
        Reduce el contador de tiempo cada segundo. Si llega a cero, verifica automáticamente
        la respuesta como incorrecta.
        '''
        if not self.esperando_confirmacion:  
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_tiempo >= 1000:
                self.tiempo_restante -= 1
                self.ultimo_tiempo = ahora
            
                if self.tiempo_restante <= 0:
                    self.tiempo_restante = 0
                    self.verificar_respuesta(-1)
    
    def resetear_juego(self):
        '''
        Reinicia el juego para comenzar una nueva partida, restableciendo puntaje, posición
        y tiempo restante.
        '''
        self.puntaje = 0
        self.posicion = POSICION_INICIAL
        self.tiempo_restante = TIEMPO_PREGUNTA
    
    def ejecutar(self):
        '''
        Función principal que ejecuta el juego. Controla el bucle de eventos, 
        renderiza pantallas y actualiza el estado del juego según la interacción del usuario.
        '''
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Serpientes y Escaleras - Trivia")
        reloj = pygame.time.Clock()
        
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                
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
            
            pantalla.fill(BLANCO)
            
            if self.estado == MENU:
                self.dibujar_menu()
            elif self.estado == JUGANDO:
                self.tablero.dibujar(self.posicion, self.jugador, self.puntaje, self.tiempo_restante)
                if not hasattr(self, 'esperando_confirmacion') or not self.esperando_confirmacion:
                    self.dibujar_pregunta()
                else:
                    self.dibujar_confirmacion()
                self.dibujar_mensaje()
            elif self.estado == PUNTAJES:
                self.dibujar_puntajes()
            elif self.estado == FIN_JUEGO:
                self.dibujar_fin_juego()
            
            pygame.display.flip()
            reloj.tick(60)