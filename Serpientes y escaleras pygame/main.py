import pygame
from juego import Juego

def main():
    pygame.init()
    pygame.mixer.init()
    
    juego = Juego()
    juego.ejecutar()

main()