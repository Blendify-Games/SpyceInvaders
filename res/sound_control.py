import res
import pygame

class OpeningMusic(pygame.mixer.Sound):
    def __init__(self):
        super().__init__(res.sound('opening.ogg'))
        self.play()

class MenuMusic(pygame.mixer.Sound):
    def __init__(self):
        super().__init__(res.sound('menu.ogg'))
        self.play(-1)

class GameMusic(pygame.mixer.Sound):
    def __init__(self):
        super().__init__(res.sound('game.ogg'))
        self.play(-1)

def play_coin():
    sound = pygame.mixer.Sound(res.sound('coin.ogg'))
    sound.play()

def play_explosion():
    sound = pygame.mixer.Sound(res.sound('explosion.ogg'))
    sound.set_volume(0.5)
    sound.play()

def play_laser():
    sound = pygame.mixer.Sound(res.sound('laser.ogg'))
    sound.play()
