import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menuEditor import Menu

class Editor:
    def __init__(self):

        #main setup
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}
         
        #navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        #support lines
        self.support_line_surf = pygame.Surface((WIDTH,HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        #selection
        self.selection_index = 2
        self.last_selected_cell = None

        #menu
        self.menu = Menu()
        
    #support
    def get_current_cell(self):
        #checking how far the cells are away from the origin pint
        distance_to_origin = vector(mouse_pos()) - self.origin

        if distance_to_origin.x > 0:  
            col = int(distance_to_origin.x / TILE_SIZE)
        else:
            col = int(distance_to_origin.x / TILE_SIZE) - 1

        if distance_to_origin.y > 0:  
            row = int(distance_to_origin.y / TILE_SIZE)
        else:
            row = int(distance_to_origin.y / TILE_SIZE) - 1

        return col, row

    def event_loop(self):
        #event loop
        #close the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.canvas_add()

    def pan_input(self,event):

        #middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            #we are getting the distance of the two, the offset is the vector 
            self.pan_offset = vector(mouse_pos()) - self.origin
            
        if not mouse_buttons()[1]:
            self.pan_active = False

        #mouse wheel
        #controlling how the origin moves using the mouse wheel and the control 
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
            
        #panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset()

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index +=1
            if event.key == pygame.K_LEFT:
                self.selection_index -=1
                
        self.selection_index = max(2,min(self.selection_index,18))

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            self.selection_index = self.menu.click(mouse_pos(), mouse_buttons())
    
    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()):
            current_cell = self.get_current_cell()
            if current_cell != self.last_selected_cell:

                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index)
                else:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                self.last_selected_cell = current_cell      
            
    #drawing 
    def draw_tile_lines(self):
        # drawing the grid the mouse is
        cols = WIDTH // TILE_SIZE
        rows = HEIGHT // TILE_SIZE

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)

        self.support_line_surf.fill('green')
        
        for col in range(cols + 1):
            #drawing the columns
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x,0), (x,HEIGHT))

        for row in range(rows + 1):
            #drawing the rows
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0,y), (WIDTH,y ))

        self.display_surface.blit(self.support_line_surf,(0,0))

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE

            if tile.has_void:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('black')
                self.display_surface.blit(test_surf,pos)
                
            if tile.has_terrain:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('green')
                self.display_surface.blit(test_surf,pos)
                
            if tile.coin:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('yellow')
                self.display_surface.blit(test_surf,pos)

            if tile.enemy:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('brown')
                self.display_surface.blit(test_surf,pos)
            
    #update
    def run(self,dt): # dt = delta time
        self.event_loop()

        #drawing
        self.display_surface.fill("gray")
        self.draw_level()
        self.draw_tile_lines()
    
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

        self.menu.display(self.selection_index)

class CanvasTile:
    def __init__(self,tile_id):

        #terrain
        self.has_terrain = False
        self.terrain_neighbours = []

        #void
        self.has_void = False
        self.void_on_top = False

        #coin
        self.coin = None

        #enemy
        self.enemy = None

        #objects
        self.objects = []

        self.add_id(tile_id)

    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            #setting the value for each variables
            case 'terrain': self.has_terrain = True
            case 'void': self.has_water = True
            case 'coin' : self.coin = tile_id
            case 'enemy' : self.enemy = tile_id


        

    
        








        
        

