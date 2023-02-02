import pygame
from settings import *
from support import *
from pygame.image import load
from editor import Editor

class Main:
    #initialises pygame and creating a display surface and a clock
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.imports()

        self.editor = Editor()

        #cursor
        surf = load('../NEA/cursors/mouse.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0,0), surf)
        pygame.mouse.set_cursor(cursor)

    def imports(self):
        self.land_tiles = import_folder('../NEA/terrain/floor')
        print(self.land_tiles)
        
    def run(self):
        #creating a while loop, we ar getting the time, events and displaying the window.
         while True:
            dt = self.clock.tick() / 1000
              
            self.editor.run(dt)
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.run()




