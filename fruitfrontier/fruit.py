import pygame
import random
import re

#Constants/Colors
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
PINK = (255, 50, 255)

pygame.init()

#Displays the screen and sets the font
#loads the contact sound
screen_width = 800
screen_height = 600
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Calibri', 40)
game_over_font = pygame.font.SysFont('Calibri', 70)
high_score_font = pygame.font.SysFont('Calibri', 40)
begin_font = pygame.font.SysFont('Calibri', 30)

pygame.display.set_caption("Fruit Frontier!")

#Loads star positions into a list
def load_stars(lst,xbeg, xend, ybeg, yend):
    for i in range(20):
        x = random.randrange(xbeg,xend)
        y = random.randrange(ybeg, yend)
        lst.append([x,y])
    return lst

#Draws the stars from that load_stars creates
def draw_stars(stars):
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 4)

class Banana(pygame.sprite.Sprite):
 
    def __init__(self):
 
        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self) 
 
        # Loads the banana image and makes it blend in with the background
        self.image = pygame.image.load('images/banana2.png').convert()
        self.image.set_colorkey(BLACK)
 
        # Fetch the rectangle object that has the dimensions of the image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

class Orange(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self) 

        # Loads the orange image and makes it blend in with the background
        self.image = pygame.image.load('images/orange2.png').convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        
class Coconut (pygame.sprite.Sprite):
    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/coconut.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()

class Shield (pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/shield.png').convert()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()

class Pineapple (pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/pineapple.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()

class Spike (pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/spike.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()

class Grape (pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/grapes.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()

class Pomegranate (pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/pom.png').convert()
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        
class Collision (pygame.sprite.Sprite):
    def __init__(self, width, height):

        # Call the parent class (Sprite) constructor
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.set_colorkey(BLACK)
        #self.image.fill(RED)
        
        self.rect = self.image.get_rect()

def main_game_loop():    

    #SOUNDS
    laser = pygame.mixer.Sound("sound/laser2.wav")
    impact = pygame.mixer.Sound("sound/dead.wav")
    contact = pygame.mixer.Sound("sound/object.wav")

    pygame.mixer.music.load('sound/background.ogg')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()

    #Opens the highscore file and stores the high score
    f = open('highscore.txt', 'r+')
    high_score = f.read()

    # Sprites lists
    orange_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    spikes = pygame.sprite.Group()

    for i in range(10):
        # This represents an orange
        orange = Orange()
 
        # Set a random location for the orange
        orange.rect.x = random.randrange(screen_width, 2 * screen_width)
        orange.rect.y = random.randrange(screen_height - 40)
 
        # Add the orange to the list of objects
        orange_list.add(orange)
        all_sprites_list.add(orange)

    #The speed of the oranges
    orange_speed = 2

    # Creates the objects of the game
    banana = Banana()
    coconut = Coconut()
    pineapple = Pineapple()
    shield = Shield()
    grape = Grape()
    pom = Pomegranate()
    all_sprites_list.add(banana)

    #keep track of whether objects are already there
    coco_alive = False
    shield_present = False
    pineapple_present = False
    spikes_present = False
    grape_present = False
    rainbow_present = False
    logo_present = True

    #object widths
    coco_width = 50
    pineapple_width = 65
    grape_width = 54

    #times (in milliseconds)
    pom_time = 4000
    spike_time1 = 800
    spike_time2 = 0
    rainbow_time = 20000

    #will make sure that only some events hapeen once
    lock = 0
    pom_lock = 0
    pom_timer1 = 500
    pom_timer2 = 0

    #loads all of the collisions into the appropriate lists
    collisions_list = []

    collision1 = Collision(45,1)
    collision2 = Collision(65,1)
    collision3 = Collision(20,1)

    collisions_list.append(collision1)
    collisions_list.append(collision2)
    collisions_list.append(collision3)

    for collision in collisions_list:
        all_sprites_list.add(collision)

    #Loads the stars in 4 quadrants to avoid drawing on the planet
    stars1 = []
    stars2 = []
    stars3 = []
    stars4 = []

    load_stars(stars1,0,313,0,screen_height)
    load_stars(stars2,0,screen_width,374,screen_height)
    load_stars(stars3,0,screen_width,0,216)
    load_stars(stars4,466,screen_width,0,screen_height)

    #appends all of the star lists into one so that we can iterate through
    galaxy_stars = []
    galaxy_stars.append(stars1)
    galaxy_stars.append(stars2)
    galaxy_stars.append(stars3)
    galaxy_stars.append(stars4)

    #Loads the logo
    logo = pygame.image.load('images/logo.PNG').convert()
    logo.set_colorkey(BLACK)
    alpha = 0

    #Loads CUANIMATION
    cuanimation = pygame.image.load('images/cuanimation.PNG').convert()
    cuanimation.set_colorkey(WHITE)
    
    #Loads the background
    background_image = pygame.image.load('images/apple.PNG').convert()
    background_image.set_colorkey(BLACK)

    #Loads the Game Over
    gameover_img = pygame.image.load('images/gameover.PNG').convert()
    gameover_img.set_colorkey(BLACK)
    
    #loads the dead banana
    dead_banana = pygame.image.load('images/dead_banana.PNG').convert()
    dead_banana.set_colorkey(BLACK)

    #loads the rainbow background
    rainbow = pygame.image.load('images/rainbow.png')
    angle = 0

    #starting position and speed of banana
    banana.rect.x = 0
    banana.rect.y = 300

    banana_xspeed = 0
    banana_yspeed = 0

    #creates a list of all of the items that have been hit
    final_hit_list = []

    # Loop until the user clicks the close button.
    done = False

    #keeps track of whether the player is dead or not
    #dead_count will make sure that the screen does not pause more than once
    dead = False
    dead_count = 0

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    score = 0

    #handles the logo before going into the game
    while logo_present:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                logo_present = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    logo_present = False
                
        screen.fill(BLACK)

        draw_stars(stars1)
        draw_stars(stars2)
        draw_stars(stars3)
        draw_stars(stars4)
        
        logo.set_alpha(alpha)
        screen.blit(logo, (0,-60))

        cuanimation.set_alpha(alpha)
        screen.blit(cuanimation, (220,screen_height/2 + 50))

        if alpha > 255:
            begin = begin_font.render("Press Space to Begin", True, GREEN)
            screen.blit(begin, (screen_width/2 - 130,screen_height - 100))
        
        #handles the fade
        alpha += 1
            
        pygame.display.flip()
 
        clock.tick(60) 

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
             #plays music if not dead
            elif event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play() 
            #checks to see if the user presses down on a key
            #doesn't let the player move if they're dead
            elif not dead:
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT:
                        banana_xspeed = -3
                    if event.key == pygame.K_RIGHT:
                        banana_xspeed = 3
                    if event.key == pygame.K_UP:
                        banana_yspeed = -3
                    if event.key == pygame.K_DOWN:
                        banana_yspeed = 3
                    if spikes_present:
                        #activates the spikes
                        if event.key == pygame.K_SPACE:
                            laser.play()
                            spike = Spike()
                            spikes.add(spike)
                            spike.rect.x = banana.rect.x + 30
                            spike.rect.y = banana.rect.y
            #checks to see if the user lets go of a key
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        banana_xspeed = 0
                    if event.key == pygame.K_RIGHT:
                        banana_xspeed = 0
                    if event.key == pygame.K_UP:
                        banana_yspeed = 0
                    if event.key == pygame.K_DOWN:
                        banana_yspeed = 0
            else:
                #allows the player to restart the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dead = False
                        dead_count = 0
                        score = 0
                        pom_timer2 = 0
                        orange_speed = 2
                        spike_time2 = 0

                        f = open('highscore.txt', 'r+')
                        high_score = f.read()

                        for orange in orange_list:
                            orange.rect.x = random.randrange(screen_width, 2 * screen_width)
                            orange.rect.y = random.randrange(screen_height - 40)
                            
                        coco_alive = False
                        grape_present = False
                        pineapple_present = False
                        spikes_present = False

                        all_sprites_list.remove(coconut)
                        all_sprites_list.remove(pineapple)
                        all_sprites_list.remove(grape)

                        for spike in spikes:
                            spikes.remove(spike)
                            all_sprites_list.remove(spike)
                            
                        coconut.rect.x = -100    
                        grape.rect.x = -100
                        pineapple.rect.x = -100

                        all_sprites_list.add(banana)
                        banana.rect.x = 0
                        banana.rect.y = screen_height/2
   
        # Set the player object location
        banana.rect.x += banana_xspeed 
        banana.rect.y += banana_yspeed

        #moves the stars across space
        for star_list in galaxy_stars:
            for star in star_list:
                star[0] -= 1
                if star[0] < 0:
                    star[0] = screen_width
                    star[1] = random.randrange(0,screen_height)
    
        #Prevents the banana from moving out of the screen
        if not dead:
            if banana.rect.x < 0:
                banana.rect.x += 3
            if banana.rect.x + 105 > screen_width:
                banana.rect.x -= 6
            elif banana.rect.y < -25:
                banana.rect.y += 7 
            elif banana.rect.y + 50 > screen_height:
                banana.rect.y -= 7

        # See if the player has collided with an orange, then kills the player.
        # if the shield is up, take away the shield, redraw the player, and reposition it randomly
        for collision in collisions_list:
            for orange in orange_list:
                if pygame.sprite.collide_rect(collision,orange):
                    if shield_present:
                        impact.play()
                        shield_present = False
                        all_sprites_list.remove(shield)
                        banana.rect.x = random.randrange(screen_width)
                        banana.rect.y = random.randrange(screen_height)
                        all_sprites_list.add(banana)
                    else:
                        dead = True

        #have the squares follow the banana
        #squares serve as collision detection 
        collision1.rect.x = banana.rect.x + 8
        collision1.rect.y = banana.rect.y + 15

        collision2.rect.x = banana.rect.x + 15 
        collision2.rect.y = banana.rect.y + 35

        collision3.rect.x = banana.rect.x + 70 
        collision3.rect.y = banana.rect.y

        #Adds the coconut if the probability hits if no other powerup is present. The probability is 1/800
        if not coco_alive and not shield_present and not spikes_present and not rainbow_present:
            coconut_chance = random.randrange(1200)
            if coconut_chance == 9:
                all_sprites_list.add(coconut)
                coconut.rect.x = 2 * screen_width
                coconut.rect.y = random.randrange(screen_height - 20)
                coco_alive = True
        else:
            #moves the coconut if its alive
            coconut.rect.x -= orange_speed

        #detects the collision between the banana, coconut, grapes
        for collision in collisions_list:
                if pygame.sprite.collide_rect(collision,coconut):
                    contact.play()
                    coco_alive = False
                    shield_present = True
                if pygame.sprite.collide_rect(collision,pineapple):
                    contact.play()
                    pineapple_present = False
                    spikes_present = True
                if pygame.sprite.collide_rect(collision,grape):
                    contact.play()
                    grape_present = False
                    rainbow_present = True

        #deletes coconut if it reaches the end of the screen
        if coconut.rect.x + coco_width < 0:
            all_sprites_list.remove(coconut)
            coco_alive = False

        # moves the invisible coconut and pineapple out of sight
        # removes any chance of another shield coming out while the current one is activated
        # removes the original banana sketch from sight and replaces it with the shield sketch
        if shield_present:
            all_sprites_list.remove(coconut)
            all_sprites_list.remove(banana)
            all_sprites_list.remove(pineapple)  
            coconut.rect.y = -100
            pineapple.rect.y = -100
            grape.rect.y = -100
            all_sprites_list.add(shield)
            shield.rect.x = banana.rect.x
            shield.rect.y = banana.rect.y
        
        # instantantiates the pineapple if no other powerup or pineapple is present
        if not shield_present and not pineapple_present and not spikes_present and not rainbow_present: 
            pineapple_chance = random.randrange(1500)
            if pineapple_chance == 9:
                all_sprites_list.add(pineapple)
                pineapple.rect.x = 2 * screen_width
                pineapple.rect.y = random.randrange(screen_height - 20)
                pineapple_present = True
        else:
            #moves the pineapple if its alive
            pineapple.rect.x -= orange_speed

        #deletes pineapple if it reaches the end of the screen
        if pineapple.rect.x + pineapple_width < 0:
            all_sprites_list.remove(pineapple)
            pineapple_present = False

        # gets rid of other powerups if the spikes are on
        if spikes_present:
            #doubles the speed once if the player eats a pineapple
            #lock makes sure that the speed is only doubled once per pineapple
            all_sprites_list.remove(pineapple)
            all_sprites_list.remove(coconut)
            all_sprites_list.remove(grape)
            coconut.rect.y = -100
            pineapple.rect.y = -100
            grape.rect.y = -100
            #timer2 = pygame.time.get_ticks()
            #makes sure the spikes only last for a given amount of time
            if spike_time1 - spike_time2 < 0:
                spikes_present = False
                spike_time2 = 0
            else:
                spike_time2 += 1

        #loads the spikes
        #checks if the spikes hit an orange
        for spike in spikes:
            all_sprites_list.add(spike)
            spike.rect.x += 5
            for orange in orange_list:
                if pygame.sprite.collide_rect(spike,orange):
                    orange.rect.x = screen_width
                    orange.rect.y = random.randrange(screen_height - 40)
                    spike.rect.y = -100

        #makes the grapes
        if not shield_present and not grape_present and not spikes_present and not rainbow_present: 
            grape_chance = random.randrange(2000)
            if grape_chance == 9:
                all_sprites_list.add(grape)
                grape.rect.x = 2 * screen_width
                grape.rect.y = random.randrange(screen_height - 20)
                grape_present = True
        else:
            #moves the pineapple if its alive
            grape.rect.x -= orange_speed

        #deletes pineapple if it reaches the end of the screen
        if grape.rect.x + grape_width < 0:
            all_sprites_list.remove(grape)
            grape_present = False

        #gets rid of other powerups if rainbow present
        if rainbow_present:
            if lock == 0:
                timer1 = pygame.time.get_ticks()
                lock = 1
            all_sprites_list.remove(pineapple)
            all_sprites_list.remove(coconut)
            all_sprites_list.remove(grape)
            coconut.rect.y = -100
            pineapple.rect.y = -100
            grape.rect.y = -100

            #makes sure the rainbow only last for a given amount of time
            timer2 = pygame.time.get_ticks()
            if timer2 - timer1 > rainbow_time:
                rainbow_present = False
                lock = 0

            #send the collision detectors away
            for collision in collisions_list:
                collision.rect.y = -500

        # --- Drawing code should go here
 
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(BLACK)

        #draws the stars
        draw_stars(stars1)
        draw_stars(stars2)
        draw_stars(stars3)
        draw_stars(stars4)

        #draws the apple nebula
        screen.blit(background_image, (0,0))

        #draws the oranges
        for item in orange_list:
            item.rect.x -= orange_speed
            #returns the oranges to the front of the screen
            if item.rect.x + 94 < 0:
                item.rect.x = screen_width
                item.rect.y = random.randrange(screen_height - 40)
    
        #draws rainbow
        if rainbow_present:
            #takes care of the rainbow rotation
            angle += 10
            new_rainbow = pygame.transform.rotate(rainbow, angle)
            rainbow_rect = new_rainbow.get_rect()
            rainbow_rect.center = (400,300)
            screen.blit(new_rainbow, rainbow_rect)
            timer2 = pygame.time.get_ticks()
        
            #makes sure the rainbow only last for a given amount of time
            if timer2 - timer1 > rainbow_time:
                rainbow_present = False
                lock = 0

         # Draw all the spites
        all_sprites_list.draw(screen)

        #draws and updates the score board.
        #makes the game FASTER every 1000 points!!!
        if not dead:
            score += 1    
        if score % 1000 == 0:
            orange_speed += 1
        text = font.render(str(score), True, GREEN)
        screen.blit(text, (700,30))

        #checks for a new highscore
        if int(high_score) < score:
            #overwrites the old highscore with the new one 
            high_score = re.sub('\d+', str(score), high_score)
            f.seek(0)
            f.write(high_score)
            f.truncate()

            pom.rect.x = (screen_width/2) - 80
            all_sprites_list.add(pom)

            if pom_timer1 - pom_timer2 > 0:
                new_high_score = high_score_font.render("NEW HIGHSCORE", True, PINK)
                screen.blit(new_high_score, (screen_width/2, 0))
                pom_timer2 += 1
            else:
                all_sprites_list.remove(pom)
            
        high_score_display = 'Highscore: ' + high_score
    
        #makes sure that the screen doesn't keep delaying after the initial pause
        #creates the dead_banana in the same place as the banana, updates the position
        #prints game over if the banana hits an orange
        if dead:
            if dead_count == 0:
                impact.play()
                pygame.time.delay(800)
                dead_count = 1

            for collision in collisions_list:
                collision.rect.y = -623

            for spike in spikes:
                spikes.remove(spike)
                all_sprites_list.remove(spike)
            
            all_sprites_list.remove(banana)
            all_sprites_list.remove(pom)
            
            screen.blit(dead_banana, (banana.rect.x,banana.rect.y))
            banana_xspeed, banana_yspeed = 0, 0
            banana.rect.x -= orange_speed
        
            screen.blit(gameover_img, (screen_width/2 - 180,20))
            high_score_display = high_score_font.render(high_score_display, True, RED)
            restart = high_score_font.render("Press Space to Restart", True, BLUE)
            screen.blit(high_score_display, (screen_width/2 - 180,80))
            screen.blit(restart, (screen_width/2 - 180,screen_height/2 + 85))
        
            f.close()
 
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # --- Limit to 60 frames per second
        clock.tick(60)

    f.close()
main_game_loop()
#Exits the screen safely
pygame.quit()


