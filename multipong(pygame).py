#Importerer nødvendige pakker
import pygame as pg
import sys
import random

# Konstanter
WIDTH = 400  # Bredden til vinduet
HEIGHT = 600 # Høyden til vinduet

SIZE = (WIDTH, HEIGHT) # Størrelsen til vinduet

# Frames Per Second (bilder per sekund)
FPS = 60

# Farger (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (100, 100, 255)
GREY = (142, 142, 142)

#liste for å oppdatere alle ballene
balls = []

colors = [RED, GREEN, BLUE]

#antall baller, for å styre farten til ballene
number = 0

#spillklasse
class Game():
    def __init__(self):
        #starter pygame, og lager spillerobjektet, med spillets overflate som input (slik at spilleren kan ha tilgang på den)
        pg.init()
        pg.font.init()
        self.surface = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.running = True
        self.player = Player(self.surface) 
        self.font = pg.font.SysFont("Arial", 26)

        self.lag_ball() #lager en ball
        
    def lag_ball(self):
        global balls #for at funksjonen skal skjønne at balls er en global variabel,
                     #og ikke en lokal variabel vi lager i funksjonen
        ball = Ball(self)  # lager ball, med spillobjektet som input, slik at den har tilgang på skjerm osv
        balls.append(ball)
        
    def display_lives(self):
        #viser antall liv
        lives_img = self.font.render(f"Antall liv: {lives}", True, WHITE)
        self.surface.blit(lives_img, (WIDTH - 150, 10))
    
    def update(self):
        self.clock.tick(FPS)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                self.running = False  # Spillet skal avsluttes
        
        self.surface.fill(BLACK)
        for ball in balls: #oppdaterer alle ballene
            ball.update()
            ball.draw()
        #oppdaterer spiller   
        self.player.update()
        self.player.draw()
        
        self.display_lives()
        pg.display.flip()  # Oppdaterer vinduet
        

class Ball():
    def __init__(self, game): #tar inn spillobjektet for å få tilgang til lag_ball metoden
        global number
        number += 1
        self.game = game
        self.x = random.randint(10, WIDTH - 20)
        self.y = 10
        self.vx = random.uniform(-number,number)
        self.vy = random.uniform(0,number)
        self.center = (self.x, self.y)
        self.radius = 10
        self.color = random.choice(colors)
        
        while self.vx == 0:
            self.vx = random.uniform(-number,number)
        
        while self.vy == 0:
            self.vy = random.uniform(0,number)
        
    def update(self):
        global lives
        global balls
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        elif self.x > WIDTH:
            self.x = WIDTH
            self.vx *= -1
            
        if self.y < 10:
            self.y = 10
            self.vy *= -1
            
        elif self.y + self.radius > HEIGHT:
            lives-=1
            balls.remove(self)
            game.lag_ball()
            if lives ==0:
                self.game.running = False
        
        self.center = (self.x, self.y)
        self.check_collision()
    
    def check_collision(self):
        player = self.game.player
        if player.y < self.y < player.y + player.height and player.x < self.x < player.x + player.width:
            self.y = player.y
            self.vy *= -1
            self.game.lag_ball()
    
    def draw(self):
        pg.draw.circle(self.game.surface, self.color, self.center, self.radius)
        

class Player():
    def __init__(self, surface):
        self.width = 80
        self.height = 20
        self.color = LIGHTBLUE
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.vx = 0
        self.surface = surface
        
    def update(self):
        self.vx = 0
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT]:
            self.vx = self.speed
        
        self.x += self.vx
        
        if self.x + self.width >= WIDTH:
            self.x = WIDTH - self.width  # Sørger for at den ikke stikker av
        if self.x <= 0:
            self.x = 0
            
    def draw(self):
        pg.draw.rect(self.surface, self.color, [self.x, self.y, self.width, self.height]) 
    
lives = 10


game = Game()

while game.running:
    game.update()
pg.quit()