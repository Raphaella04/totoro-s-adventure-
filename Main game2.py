# Animated Coins images by Clint Bellanger 
# https://opengameart.org/content/animated-coins

# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

import pygame
import engine
import button

def drawText(t, x, y):
    text = font.render(t, True, GREEN, WHITE)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x,y)
    screen.blit(text, text_rectangle)

pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Totoro\'s Adventure")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

#define colours
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
GREY = (210,210,210)
PINK = (252,131,245)

#game states = playing // win // lose
game_state = 'playing'

entities = []

#player
player_image = pygame.image.load('dino_images/dino1_02.png')
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.2

player_width = 45
player_height = 52

player_direction = 'right'
player_state = 'idle'


#platform

platforms = [
             #middle
             pygame.Rect((100,300),(400,50)),
             #left
             pygame.Rect((100,250),(50,50)),
             #right
             pygame.Rect((450,250),(50,50))]

#coins
coin_image = pygame.image.load('coins/coin1_0.png')
coin_animation = engine.Animation([
    pygame.image.load('coins/coin_0.png'),
    pygame.image.load('coins/coin_1.png'),
    pygame.image.load('coins/coin_2.png'),
    pygame.image.load('coins/coin_3.png'),
    pygame.image.load('coins/coin_4.png'),
    pygame.image.load('coins/coin_5.png'),
    pygame.image.load('coins/coin_6.png'),
    pygame.image.load('coins/coin_7.png')])
    
coins = [
        pygame.Rect((100,200),(39,18)),
        pygame.Rect((200,200),(39,18))]

coin1 = engine.Entity
coin1.position = engine.Position(100,200,39,18)
coin1Animation = engine.Animation([
    pygame.image.load('coins/coin_0.png'),
    pygame.image.load('coins/coin_1.png'),
    pygame.image.load('coins/coin_2.png'),
    pygame.image.load('coins/coin_3.png'),
    pygame.image.load('coins/coin_4.png'),
    pygame.image.load('coins/coin_5.png'),
    pygame.image.load('coins/coin_6.png'),
    pygame.image.load('coins/coin_7.png')])

coin1.animations = engine.Animations()
coin1.animations.add('idle', coin1Animation)

coin2 = engine.Entity
coin2.position = engine.Position(200,250,39,18)
coin2Animation = engine.Animation([
    pygame.image.load('coins/coin_0.png'),
    pygame.image.load('coins/coin_1.png'),
    pygame.image.load('coins/coin_2.png'),
    pygame.image.load('coins/coin_3.png'),
    pygame.image.load('coins/coin_4.png'),
    pygame.image.load('coins/coin_5.png'),
    pygame.image.load('coins/coin_6.png'),
    pygame.image.load('coins/coin_7.png')])

coin2.animations = engine.Animations()
coin2.animations.add('idle', coin1Animation)

entities.append(coin1)
entities.append(coin2)

#soots
soot_image = pygame.image.load('soot_images/soot_2.png')
soots = [
        pygame.Rect((400,240),(27,29)),
        pygame.Rect((430,255),(27,29))]

lives = 5
heart_image = pygame.image.load('coins/heart.png')

score = 0    

running = True
while running:
# game loop

    #------
    #input
    #------
    
    #check for quit
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    if game_state == 'playing':
        
            
        new_player_x = player_x
        new_player_y = player_y
        
        #player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            new_player_x -= 2
            player_direction = 'left'
        if keys[pygame.K_d]:
            new_player_x += 2
            player_direction = 'right'
        if keys[pygame.K_w] and player_on_ground:
            player_speed = -5


    #-------
    #update
    #-------

    if game_state =='playing':

        #update coin animation
        coin_animation.update() 
    
        #horizontal movement
        new_player_rect = pygame.Rect(new_player_x,player_y,player_width,player_height)
        x_collision = False
        
        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break
            
        if x_collision == False:
            player_x = new_player_x
            
        #vertical movement

        player_speed += player_acceleration    
        new_player_y += player_speed

        new_player_rect = pygame.Rect(player_x,new_player_y,player_width,player_height)
        y_collision = False
        player_on_ground = False
        
        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                #if the platform is below the player 
                if p[1] > new_player_y:
                    #stick the player to the platform
                    player_y = p[1] - player_height
                    player_on_ground = True
                break
        print(player_on_ground)
        
        if y_collision == False:
            player_y = new_player_y

            
        #see if any coins have been collected
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for c in coins:
            if c.colliderect(player_rect):
                coins.remove(c)
                score += 1
                if score>= 2:
                    game_state = 'win'
        

        #see if the player has hit the enemy
        for s in soots:
            if s.colliderect(player_rect):
                lives -= 1
                #reset player position
                player_x = 300
                player_y = 0
                player_speed = 0
                # change the game state
                #if no lives remaining
                if lives <= 0:
                    game_state = 'lose'
    #-----    
    #draw
    #-----

    
    
    #background
    screen.fill(WHITE)

    #platforms
    for p in platforms: 
        pygame.draw.rect(screen, YELLOW, p)

    for entity in entities:
        s = entity.state
        a = entity.animation.animationList[s]
        a.draw(screen, entity.position.rect.x, entity.position.rect.y, False, False)

    #enemies
    for s in soots:
        screen.blit(soot_image, (s.x, s.y)) 

        
    #player
    if player_direction == 'right':
        screen.blit(player_image,(player_x,player_y))
    elif player_direction == 'left':
        screen.blit(pygame.transform.flip(player_image, True, False),(player_x,player_y))

    #player info display

     
    #score
    screen.blit(coin_image,(20, 50))
    drawText(str(score), 60, 52)
         
    #lives
    for l in range(lives):
        screen.blit(heart_image, (20 + (l*50),5))
    
    if game_state == 'win':
        #draw win text
        
        drawText("You win!", 50, 50)
    if game_state == 'lose':
        #draw lose
        drawText("You lose!", 50, 50)
      
    #present screen
    pygame.display.flip()
    
    clock.tick(90)
    
    
#quit game
pygame.quit()






