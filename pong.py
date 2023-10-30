import winsound
import time
import sys
import pygame
from pygame.locals import *
pygame.init()

pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((1100,700))

class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.surf = pygame.Surface((25,125))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()

    def update(self, pressedKeys):
        if self == player1:
            if pressedKeys[K_w]:
                self.rect.move_ip(0,-5)
            if pressedKeys[K_s]:
                self.rect.move_ip(0,5)

        elif self == player2:
            if pressedKeys[K_UP]:
                self.rect.move_ip(0,-5)
            if pressedKeys[K_DOWN]:
                self.rect.move_ip(0,5)

class ball(pygame.sprite.Sprite):
    def __init__(self):
        super(ball, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill ((255,255,255))
        self.rect = self.surf.get_rect()
        self.velocityx = 5
        self.velocityy = 0

    def update(self, pressedKeys):
        if self.rect.centery >= 687 or self.rect.centery <= 13:
            self.velocityy = self.velocityy * -1
            winsound.PlaySound('pong.wav', winsound.SND_ASYNC | winsound.SND_ALIAS )

        if self.velocityx < 0:
            if self.rect.colliderect(player1) and self.rect.left + 5 == player1.rect.right:
                self.velocityx = self.velocityx * -1
                winsound.PlaySound('pong.wav', winsound.SND_ASYNC | winsound.SND_ALIAS )
        elif self.velocityx >= 0:
            if self.rect.colliderect(player2) and self.rect.right - 5 == player2.rect.left:
                self.velocityx = self.velocityx * -1
                winsound.PlaySound('pong.wav', winsound.SND_ASYNC | winsound.SND_ALIAS )

        if self.velocityy >= 0:
            if self.rect.colliderect(player1):
                if pressedKeys[K_w] and not player1.rect.top <= 0:
                    self.velocityy -= 2
                elif pressedKeys[K_s] and not player1.rect.bottom >= 700:
                    self.velocityy += 2
            if self.rect.colliderect(player2):
                if pressedKeys[K_UP] and not player2.rect.top <= 0:
                    self.velocityy -= 2
                elif pressedKeys[K_DOWN] and not player2.rect.bottom >= 700:
                    self.velocityy += 2
                    
        elif self.velocityy < 0:
            if self.rect.colliderect(player1):
                if pressedKeys[K_w] and not player1.rect.top <= 0:
                    self.velocityy -= 2
                elif pressedKeys[K_s] and not player1.rect.bottom >= 700:
                    self.velocityy += 2
            if self.rect.colliderect(player2):
                if pressedKeys[K_UP] and not player2.rect.top <= 0:
                    self.velocityy -= 2
                elif pressedKeys[K_DOWN] and not player2.rect.bottom >= 700:
                    self.velocityy += 2

        self.rect.move_ip(self.velocityx, self.velocityy)

player1 = player()
player2 = player()
ball = ball()

screenRect = screen.get_rect()

gameloop = True

clock = pygame.time.Clock()

player1.rect.center = (100, 350)
player2.rect.center = (1000, 350)
ball.rect.center = (550, 350)

loose = False

player1Score = 0
player2Score = 0

time.sleep(1)

while gameloop == True:
    player1.rect.clamp_ip(screenRect)
    player2.rect.clamp_ip(screenRect)
    ball.rect.clamp_ip(screenRect)
    screen.fill((0,0,0))
    screen.blit(player1.surf,player1.rect)
    screen.blit(player2.surf,player2.rect)
    screen.blit(ball.surf,ball.rect)
    
    font = pygame.font.SysFont(None, 30)
    player1Text = font.render(str(player1Score), True, (255, 255, 255), None)
    player2Text = font.render(str(player2Score), True, (255, 255, 255), None)
    player1TextRect = player1Text.get_rect()
    player2TextRect = player1Text.get_rect()
    player1TextRect.center = (50, 50)
    player2TextRect.center = (1050, 50)
    screen.blit(player1Text, player1TextRect)
    screen.blit(player2Text, player2TextRect)

    if ball.rect.centerx >= 1087 or ball.rect.centerx <= 13:
        if ball.rect.centerx >= 1087:
            player1Score += 1
        else:
            player2Score += 1
        screen.fill((0,0,0))
        screen.blit(player1.surf,player1.rect)
        screen.blit(player2.surf,player2.rect)
        pygame.display.flip()
        time.sleep(2)
        player1.rect.center = (100, 350)
        player2.rect.center = (1000, 350)
        ball.velocityy = 0
        ball.rect.center = (550, 350)
    pygame.display.flip()

    pressedKeys = pygame.key.get_pressed()

    ball.update(pressedKeys)

    player1.update(pressedKeys)
    player2.update(pressedKeys)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameloop = False
                pygame.quit()
                print(player1Score)
                print(player2Score)
            if event.key == K_TAB:
                pause = True
                while pause == True:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                gameloop = False
                                pygame.quit()
                                print(player1Score)
                                print(player2Score)
                                pause = False
                            if event.key == K_TAB:
                                pause = False
                        elif event.type == QUIT:
                            gameloop = False
                            pygame.quit()
                            print(player1Score)
                            print(player2Score)
                            pause = False
        elif event.type == QUIT:
            gameloop = False
            pygame.quit()
            print(player1Score)
            print(player2Score)

    if player1Score == 10:
        print('PLAYER 1 WINS')
        print(player1Score)
        print(player2Score)
        gameloop = False
        pygame.quit()
    elif player2Score == 10:
        print('PLAYER 2 WINS')
        print(player1Score)
        print(player2Score)
        gameloop = False
        pygame.quit()

    clock.tick(60)
