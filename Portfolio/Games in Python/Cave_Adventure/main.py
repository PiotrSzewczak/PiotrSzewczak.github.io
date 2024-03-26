import pygame, os, random, math, time, cmath
from pygame.locals import *
from pygame import mixer

pygame.init()
#MAIN SETTINGS
fps=60
clock = pygame.time.Clock()
clock.tick(fps)
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
game = True
actual_display = "menu_button"
obstacles = []
moving_sprites = pygame.sprite.Group()
speed_moving = 14
mouse_control = False
button_control = True
background_gaming = pygame.image.load("images/backgrounds/background_gaming.png")
#SOUNDS
theme_song = "sounds/theme_song.mp3"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(theme_song)
pygame.mixer.music.play(-3)
game_over = mixer.Sound("sounds/game_over.mp3")
click_sound = mixer.Sound("sounds/click_sound.mp3")

def write_text(txt, x, y, size):
    cz = pygame.font.SysFont("Arial Heavy", size)
    rend = cz.render (txt, 1, (255, 255, 255))
    screen.blit(rend, (x,y))

class Obstacle ():
    def __init__ (self, x, width):
        self.x = x
        self.width = width
        self.y_up = 0
        self.height_up = random.randint (150, 250)
        self.space = random.randint(250, 450)
        self.y_down = self.height_up+self.space
        self.height_down = height - self.y_down
        self.color = (13, random.randint(0,73), random.randint(104,113))
        self.shape_up = pygame.Rect (self.x, self.y_up, self.width, self.height_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)

    def draw_obstacle(self):
        pygame.draw.rect(screen, self.color, self.shape_up, 0)
        pygame.draw.rect(screen, self.color, self.shape_down, 0)
    def moving(self, v):
        self.x = self.x - v
        self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
    def collision(self,player):
        if self.shape_up.colliderect(player) or self.shape_down.colliderect(player):
            return True

        else:
            return False

class Rocket (pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("images/rocket01/rocket_1.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.x = x
        self.y = y
        self.width = 135
        self.height = 65
        self.shape = pygame.Rect (self.x, self.y, self.width, self.height)

    def update(self):
        self.current_sprite = self.current_sprite + 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def draw_rocket (self):
        screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move_rocket (self, v):
        self.y = self.y + v
        self.shape = pygame.Rect (self.x, self.y, self.width, self.height)
        pygame.display.update()

player = Rocket (250,250)
moving_sprites.add(player)
dy = 0

for i in range(41):
    obstacles.append(Obstacle (i*width/40, width/40) )

while game is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit ()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and button_control == True:
                dy = -5
            if event.key == pygame.K_DOWN and button_control == True:
                dy = 5
            if event.key == pygame.K_LEFT:
                if actual_display == "menu_mouse":
                    actual_display = "menu_button"
                    click_sound.play()
            if event.key == pygame.K_RIGHT:
                if actual_display == "menu_button":
                    actual_display = "menu_mouse"
                    click_sound.play()
            if event.key == pygame.K_SPACE:
                if actual_display != "gaming":
                    click_sound.play()
                    pygame.mixer.music.play(-2)
                    player = Rocket (250,250)
                    dy = 0
                    actual_display = "gaming"
                    scores = 0
        if mouse_control == True:
            pressed_keys = pygame.mouse.get_pressed()
            if (pressed_keys[0]):
                dy = -5
            if (pressed_keys[2]):
                dy = 5

    screen.fill ((0,0,0))
    if actual_display == "menu_button":
        mouse_control = False
        button_control = True
        background = pygame.image.load(os.path.join("images/backgrounds/backround_button.png"))
        screen.blit (background, (0, 0))
        pygame.display.update()
    if actual_display == "menu_mouse":
        mouse_control = True
        button_control = False
        background = pygame.image.load(os.path.join("images/backgrounds/backround_mouse.png"))
        screen.blit (background, (0, 0))
        pygame.display.update()
    elif actual_display == "gaming":
        screen.blit(background_gaming, (0, 0))
        for p in obstacles:
            p.moving(speed_moving)
            p.draw_obstacle()
            if p.collision(player.shape):
                pygame.mixer.music.stop()
                game_over.play()
                actual_display = "end_of_game"
        for p in obstacles:
            if p.x <= -p.width:
                obstacles.remove(p)
                obstacles.append((Obstacle (width, width/20)))
                scores = scores + math.fabs(dy)
                speed_moving = speed_moving + scores/1000000

        moving_sprites.update()
        player.draw_rocket()
        player.move_rocket(dy)
        moving_sprites.draw(screen)
        player.update()

    elif actual_display == "end_of_game":
        end_game_background = pygame.image.load(os.path.join("images/backgrounds/end_game_background.png"))
        screen.blit(end_game_background, (0, 0))
        final_score = "TWÓJ WYNIK TO : " + str(int(scores))
        write_text(final_score, 850, 669, 51)
        pygame.display.update()








