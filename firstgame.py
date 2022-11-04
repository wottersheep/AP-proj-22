import pygame
from sys import exit
from random import randint

def display_score():    
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: 
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in  obstacle_list if obstacle.x>-100]

        return obstacle_list
    else: return []
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True        

def player_animation():
    global player_surf, player_index

    if player_rect.bottom <300:
      #play jump  when in air
      player_surf = player_jump
    else:
        #play walking animation when player is on floor
        player_index+=0.1
        if player_index>=len(player_walk): player_index=0
        player_surf = player_walk[int(player_index)]

    

pygame.init()       #very important

screen = pygame.display.set_mode((800,400))                                                                                                         #main screen kind of like canvas
pygame.display.set_caption('Runner')                                                                                                                #setting the name of the main screen
clock = pygame.time.Clock()                                                                                                                         #making a clock object for frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf',50)                                                                                               #making a font object, arguments(font,size)
game_active = False
start_time = 0
score = 0


#test_surface = pygame.Surface((100,200))        #making a surface to be displayed on the main screen
#test_surface.fill('Red')                        #filling the second screen with red colour

sky_surface = pygame.image.load('graphics/sky.png').convert()    #importing image and giving its address
ground_surface = pygame.image.load('graphics/ground.png').convert()

"""score_surface = test_font.render('My game', False,(64,64,64))   actually creating the surface, arguments(text, anti-aliasing true or false, colour)
score_rect= score_surface.get_rect(center = (400,50))"""

#OBSTACLE

#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]


#fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []


#player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))

player_gravity= 0

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)      #this is used to transform the image, arguments(surface, angle,scale )
player_stand_rect = player_stand.get_rect(center = (400,200))

endText_surf = test_font.render("Welcome to Runner",False,(111,196,169))
endText_rect = endText_surf.get_rect(center = (400,40))

spacebar_surf = test_font.render("Press SPACE to start!",False,'Black')
spacebar_surf = pygame.transform.rotozoom(spacebar_surf,0,1.5)
spacebar_rect = spacebar_surf.get_rect(center = (400,350))


#timer
obstacle_timer = pygame.USEREVENT + 1               #creating a custom user event, needs to be in caps, add +1 to avoid conflict with other events
pygame.time.set_timer(obstacle_timer,1700)           #argument (event you want to occur, intervals)

snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,200)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)


while True:                                     
    
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:                               #for loop to quit the game when user wants to just cut the window
            pygame.quit()
            exit()                                                  #using exit to quit the while loop as well to avoid getting error
        
        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):             #Code to determine when the mouse cursor collides with the player rectangle with the help of event loop
                    player_gravity=-20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity=-20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time=int(pygame.time.get_ticks()/1000)
                
        if game_active:
            if event.type == obstacle_timer:                        #this if block randomly generates enemies
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index==0 : snail_frame_index=1
                else: snail_frame_index=0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index==0 : fly_frame_index=1
                else: fly_frame_index=0
                fly_surf = fly_frames[fly_frame_index]


    if game_active:
        #connecting main screen with another surface
        screen.blit(sky_surface,(0,0))                 #This line decides the coordinates of the surface and takes arguments as  (name of surface),position of surface 
        screen.blit(ground_surface,(0,300))
        """pygame.draw.rect(screen,'#c0e8ec',score_rect)               #To draw a rectangle, takes 3 arguments: the surface you want to draw on, the color, the rectangle
        pygame.draw.rect(screen,'#c0e8ec',score_rect,10)              
        
        
        screen.blit(score_surface,score_rect)"""

        score = display_score()
        
        '''SNAIL MOVEMENT
        snail_rect.left-=4
        if snail_rect.right<=0 : snail_rect.left=800'''

        
        

        #PLAYER

        player_gravity += 1
        player_rect.y+=player_gravity
        if player_rect.bottom >= 300 : player_rect.bottom=300
        player_animation()
        screen.blit(player_surf,player_rect)
       

        #OBSTACLE MOVEMENT
        obstacle_rect_list =   obstacle_movement(obstacle_rect_list)
        
        #COLLISION

        game_active=collisions(player_rect,obstacle_rect_list)
        #if snail_rect.colliderect(player_rect):
            #game_active=False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)

        score_message = test_font.render(f'Your score : {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(endText_surf,endText_rect)

        if score==0:
            screen.blit(spacebar_surf,spacebar_rect)
        else:
            screen.blit(score_message,score_message_rect)

    

    """if player_rect.colliderect(snail_rect):                      prints true if colliison else false, but will give true for every frame of collision so needs some tweaking
            print("Collision")"""
    
    #rect1.collidepoint((x,y))                                       Another method to detect collision, won't be used often but helpful in cases of mouse movement/ interaction detection

    """mouse_pos= pygame.mouse.get_pos()                             
    if player_rect.collidepoint(mouse_pos):                         Code to determine when the mouse cursor collides with the player rectangle with pygame.mouse
        print(pygame.mouse.get_pressed())"""

    #print(pygame.key.get_pressed())                                 gives the status of all the keys on the keyboard in terms of true or false
    
    """keys = pygame.key.get_pressed()                                
    if keys[pygame.K_SPACE]:
        print("jump")"""

    pygame.display.update()

    clock.tick(60)              #actually setting the frame rate