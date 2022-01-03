import pygame
from pygame.locals import *
import time
import random

SIZE=40

class Apple:
    def __init__(self,parent_screen):
        self.apple=pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x=random.randint(0,23)*SIZE
        self.y=random.randint(1,13)*SIZE
    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.update()
    def move(self,):
        self.x=random.randint(0,23)*SIZE
        self.y=random.randint(1,13)*SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen=parent_screen
        self.block=pygame.image.load("resources/block.jpg").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='right'
    
    def draw(self):
        self.parent_screen.fill((0,0,0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()
    
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    
    def increase(self):
        self.length+=1
        self.x.append(0)
        self.y.append(0)
    
    def game_over_sound(self):
        sound = pygame.mixer.Sound('resources/game-over.mp3')
        pygame.mixer.Sound.play(sound)
        pygame.mixer.Sound.set_volume(sound, 0.5)
    
    def walk(self):
        for i in range(self.length-1,0,-1):
                self.x[i]=self.x[i-1]
                self.y[i]=self.y[i-1]
        if self.x[0]<0 or self.x[0]>960:
            self.game_over_sound()
            raise Exception
        elif self.y[0]<0 or self.y[0]>600:
            self.game_over_sound()
            raise Exception
        else:
            if self.direction=='up':
                self.y[0]-=SIZE
            if self.direction=='down':
                self.y[0]+=SIZE
            if self.direction=='left':
                self.x[0]-=SIZE
            if self.direction=='right':
                self.x[0]+=SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.surface = pygame.display.set_mode((1000, 600))
        pygame.mixer.init()
        pygame.mixer.music.load('resources/bgmusic.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()
        self.surface.fill((0,0,0))
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
        self.load_data()

    #function to load highscore
    def load_data(self):
        with open('resources/hs.txt', 'r') as f:
            self.highscore=int(f.read())

    #function to handle snake collision
    def is_collision(self,x1,y1,x2,y2):
        if self.snake.direction=='up' or self.snake.direction=='down':
            if (y1==y2+SIZE or y1==y2-SIZE) and x1==x2:
                return True
        elif self.snake.direction=='left' or self.snake.direction=='right':
            if (x1==x2+SIZE or x1==x2-SIZE) and y1==y2:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound=pygame.mixer.Sound('resources/ding.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase()
            self.apple.move()

        for i in range(self.snake.length-1):
            if self.snake.x[0]==self.snake.x[i+1]:
                if self.snake.y[0]==self.snake.y[i+1]:
                    self.snake.game_over_sound()
                    raise Exception

    #function to display the score on the screen
    def display_score(self):
        self.cscore=self.snake.length-1
        font=pygame.font.SysFont('arial',25)
        score=font.render(f'Score: {self.cscore}',True,(255,255,255))
        self.surface.blit(score,(900,0))
        hscore = font.render(f'High Score: {self.highscore}', True, (255, 255, 255))
        self.surface.blit(hscore, (20,0))
        pygame.display.update()

    #function to handle game over event
    def show_gameover(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial', 40)
        if self.cscore>self.highscore:
            self.highscore=self.cscore
            line0=font.render('NEW HIGH SCORE!',True, (255, 255, 255))
            self.surface.blit(line0,(350, 250))
            with open('resources/hs.txt', 'w') as f:
                f.write(str(self.highscore))
            pygame.display.update()
            time.sleep(2.5)
        self.surface.fill((0,0,0))
        line1 = font.render(f'Your Score is: {self.cscore}', True, (255, 255, 255))
        self.surface.blit(line1, (390, 195))
        line2 = font.render('GAME OVER!', True, (255, 255, 255))
        self.surface.blit(line2, (400, 250))
        line3=font.render('To play again press the Enter key',True, (255, 255, 255))
        self.surface.blit(line3,(270, 300))
        pygame.display.update()

    #function to reset the game
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
    
    #main function    
    def run(self): 
        clock=pygame.time.Clock()
        running=True
        pause=False

        while running:
            clock.tick(4)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key==K_RETURN:
                        pygame.mixer.music.play()
                        pause=False
                    if pause==False:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if pause==False:
                    self.play()
            except Exception:
                pygame.mixer.music.pause()
                self.show_gameover()
                pause=True
                self.reset()

game=Game()
game.run()
