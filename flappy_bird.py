import pygame
from pygame.locals import *
import random

clock = pygame.time.Clock()
fps = 60

pygame.init()

screen_width = 864
screen_height = 956

screen = pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("Flappy Bird")

#define font:
font = pygame.font.SysFont("Bauhaus 93" , 60)

#define colors:
white = (255 , 255 , 255)

# Define game variables:
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #millisecond
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
speed_up_time = 0
speed_up_duration = 5000 #millisecond
original_scrool_speed = scroll_speed


#load images:
bg = pygame.image.load("img/bg.png")
ground_image = pygame.image.load("img/ground.png")
button_img = pygame.image.load("img/restart.png")

#Write to score onto the screen:
def draw_text(text , font , text_col , x , y):
    img = font.render(text , True  , text_col)
    screen.blit(img , (x ,y))

def reset_game():
    global scroll_speed
    scroll_speed = original_scrool_speed
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

#Create energy and check collusion with pipes:
def create_energy():
    energy = Energy()

    while check_collusion_with_pipes(energy):
        energy.rect.y = random.randint(100 , screen_height - 100)
    energy_group.add(energy)

def check_collusion_with_pipes():
    for pipe in pipe_group:
        if energy.rect.colliderect(pipe.rect):
            return True
    return False


class Bird(pygame.sprite.Sprite):
    def __init__(self , x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0 #Hangi görselin aktif oldugunu kontrol ediyoruz başlangıcta 0, 1. görsel.
        self.counter = 0
        for num in range(1,4): # 3 resim var 
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index] #self.index birinci resimden başlıyor.
        self.rect = self.image.get_rect() #resmi (kuşu) karenin içine alıyoruz (temsili)
        self.rect.center = [x , y]
        self.vel = 0
        self.clicked = False

    def update(self):

        #Gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        
        if game_over == False:
            #Jumping stiuation for mouse:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #[0] mouse sol tık == 1 olursa(tıklanırsa)
                self.clicked = True
                self.vel = -10
            
            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False
        
            

            #handle the animation:
            self.counter += 1
            flap_cooldown = 5 #Animasyondaki görselin kaç karede bir değişecegini ayarlıyoruz

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            
            #rotate the bird:
            self.image = pygame.transform.rotate(self.images[self.index] , self.vel * -2) # kafa harekteini sağlıyor.
        else:
            self.image = pygame.transform.rotate(self.images[self.index] , -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self , x, y, position ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # position 1 is from the top , -1 is from the bottom.
        if position == 1:
            self.image = pygame.transform.flip(self.image , False , True) #x eksenini çevirmiyoruz False , y eksenini çeviriyoruz True.
            self.rect.bottomleft = [x , y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x , y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #ekrandan çıkan pipe'ları yok etmek için.
            self.kill()


class Button():
    def __init__(self, x , y , image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

    def draw(self):

        action = False

        #get mouse position:
        pos = pygame.mouse.get_pos()
        #check if mouse is over the button:
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: #Mouse sol tık basıldıgında.
                action = True

        #draw button
        screen.blit(self.image , (self.rect.x , self.rect.y))

        return action
    
class Energy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/energy.png")
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(100 , screen_height - 100)
        self.speed = 5

    def update(self):
        if self.speed > 0:
            self.speed = 5
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def draw(self , screen):
        screen.blit(self.image , self.rect)

    


energy_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100 , int(screen_height / 2)) # x ,y koordinatı

bird_group.add(flappy)

#create restart button instance
button = Button(screen_width // 2 - 50 , screen_height // 2 - 100 , button_img)


run = True

while run:

    clock.tick(fps)

    #draw background:
    screen.blit(bg , (0,0)) #to show any image to screen , use blit function in pygame

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)
    
    # draw energy and update energy:
    energy_group.update()
    energy_group.draw(screen)

    #draw the ground:
    screen.blit(ground_image , (ground_scroll,768))

    #Check the score:

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False: #pipe'in sol tarafını geçtigi, sağ tarafını geçmediği durum
                pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    draw_text(str(score) , font , white , int(screen_width / 2)  , 35)

    #look for collusion:
    if pygame.sprite.groupcollide(bird_group , pipe_group , False , False) or flappy.rect.top < 0:  # 1. false bird_group , 2. pipe_group
        game_over = True

    # check if bird has hit the ground:
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    
    if game_over == False and flying == True:
        #generate new pipes:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100 , 100)
            btm_pipe = Pipe(screen_width , int(screen_height / 2) + pipe_height , -1)
            top_pipe = Pipe(screen_width , int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll the ground:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 36:
            ground_scroll = 0 #Zemin |36|'dan büyük olursa, zemini yeniden olusturuyoruz (zeminin normal büyüklüğü 36)

        pipe_group.update()

        #Energy:
        if random.randint(1 , 100 )  == 1:
            print("Energy created")
            energy = Energy()
            energy_group.add(energy)

        if pygame.sprite.spritecollide(flappy , energy_group , False):
            print("Energy collected")
            scroll_speed += 4
            speed_up_time = pygame.time.get_ticks() #get_ticks() : measure time
            energy_group.empty()

    if scroll_speed > original_scrool_speed:
        if pygame.time.get_ticks() - speed_up_time >= speed_up_duration:
            scroll_speed = original_scrool_speed

    #check for game over and reset:
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

        # Jumping with space press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying = True
                flappy.vel = -10 #update fonksiyonunda self.vel class'ın içinden o anda çalısılan nesneyi(bird) ifade etti ,
                                 # ancak burada sınıfın dısında olusturdugumuz nesneyi(flappy) kullanarak aynı özelliklere
                                 # ve metodlara eriştik flappy.vel = class'ın içindeki self.vel. 

    pygame.display.update()

pygame.quit()