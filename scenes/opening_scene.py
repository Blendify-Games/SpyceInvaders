import pygame
from res.config import SCREEN_SIZE
from res.util import get_sprite_block, get_text
from scenes import Scene, boot_scene
from scenes.menu_scene import MenuScene
from scenes.writing import TextWrite

class _CarryingLetterSquid(pygame.sprite.Sprite):
    def __init__(self, render_group: pygame.sprite.Group):
        super().__init__(render_group)
        self.state = 'squid-x'
        self.state_index = 0
        self.image_list = {
            'squid-x': [get_sprite_block('squid-x_1'),
                       get_sprite_block('squid-x_2')],
            'squid-ý': [get_sprite_block('squid-ý_1'),
                        get_sprite_block('squid-ý_2')],
            'squid-y': [get_sprite_block('squid-y_1'), 
                        get_sprite_block('squid-y_2')]
        }
        self.image = self.image_list[self.state][self.state_index]
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_SIZE[0]
        self.rect.centery = SCREEN_SIZE[1]//2
        self.__time = pygame.time.get_ticks()
    def set_state(self, state_name:str):
        self.state = state_name
        self.state_index = 0
        self.image = self.image_list[self.state][self.state_index]
    def get_state(self) -> str:
        return self.state
    def move(self, x:int):
        self.rect.left += x
        t = pygame.time.get_ticks()
        if t - self.__time > 100:
            self.state_index = (self.state_index + 1) % len(
                self.image_list[self.state]
            )
            self.image = self.image_list[self.state][self.state_index]
            self.__time = t

class _IntroTextAnimation():
    def __init__(self, render_group:pygame.sprite.Group):
        self.__text_spr = TextWrite(render_group, 'Blendifý Games')
        self.__squid = _CarryingLetterSquid(render_group)
        self.__time = pygame.time.get_ticks()
        self.iterating = self.state1
        self.state_running = False
        self.__state_params = None
    def state1(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.__state_params = {
                'textalpha': 0
            }
            self.state_running = True
        self.__text_spr.image.set_alpha(
            self.__state_params['textalpha']
        )
        t = pygame.time.get_ticks()
        if t - self.__time > 50:
            self.__state_params['textalpha'] += 10
            self.__time = t
        if self.__text_spr.image.get_alpha() == 255:
            self.iterating = self.state2
            self.__state_params = None
            self.state_running = False
        return True
    def state2(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.state_running = True
        if self.__squid.rect.left > SCREEN_SIZE[0]//2:
            self.__squid.move(-3)
        else:
            self.__squid.set_state('squid-ý')
            self.__text_spr.setup_text('Blendif  Games')
            self.iterating = self.state3
            self.state_running = False
        return True
    def state3(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.state_running = True
        t = pygame.time.get_ticks()
        if t - self.__time > 300:
            if self.__squid.rect.left < SCREEN_SIZE[0]:
                self.__squid.move(3)
            else:
                self.__squid.set_state('squid-y')
                self.iterating = self.state4
                self.state_running = False
        return True
    def state4(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.state_running = True
        t = pygame.time.get_ticks()
        if t - self.__time > 300:
            if self.__squid.rect.left > SCREEN_SIZE[0]//2-1:
                self.__squid.move(-3)
            else:
                self.__text_spr.setup_text('Blendify Games')
                self.__squid.set_state('squid-x')
                self.iterating = self.state5
                self.state_running = False
        return True
    def state5(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.state_running = True
        t = pygame.time.get_ticks()
        if t - self.__time > 300:
            if self.__squid.rect.left < SCREEN_SIZE[0]:
                self.__squid.move(3)
            else:
                self.iterating = self.state6
                self.state_running = False
        return True
    def state6(self):
        if not self.state_running:
            self.__time = pygame.time.get_ticks()
            self.__state_params = {
                'textalpha': 255
            }
            self.state_running = True
        self.__text_spr.image.set_alpha(
            self.__state_params['textalpha']
        )
        t = pygame.time.get_ticks()
        if t - self.__time > 50:
            self.__state_params['textalpha'] -= 10
            self.__time = t
        if self.__text_spr.image.get_alpha() == 0:
            return False
        return True


class OpeningScene(Scene):
    def setup(self):
        self.anim = _IntroTextAnimation(self.render_group)
    def update(self):
        super().update()
        if not self.anim.iterating():
            boot_scene(MenuScene())
