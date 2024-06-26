import pygame

from gameobj.invaders import (
    OctopusInvader, SquidInvader,
    CrabInvader, UFOInvader
)
from game_instance import game_instance
from res.config import SCREEN_SIZE, GAME_NAME
from res.sound_control import MenuMusic, play_coin
from scenes import Scene, boot_scene
from scenes.game_scene import GameScene
from scenes.instructions_scene import InstructionsScene
from scenes.writing import TextWrite, Figure

class _Menu():
    def __init__(self, render_group:pygame.sprite.Group):
        self.__render_group = render_group
        self.__build_top()
        self.__build_middle()
        self.__build_bottom()
        self.__time = pygame.time.get_ticks()
    def __build_top(self):
        text = TextWrite(self.__render_group, GAME_NAME,
                (SCREEN_SIZE[0]*0.5, SCREEN_SIZE[1]*0.1),
                step_writing_time=100)
    def __build_middle(self):
        text = TextWrite(self.__render_group, '*INVADER SCORE TABLE*')
        text.rect.centery = SCREEN_SIZE[1]*0.25
        self.invaders = []
        invader = UFOInvader(self.__render_group)
        invader.rect.center = SCREEN_SIZE[0]*0.33, SCREEN_SIZE[1]*0.39
        text = TextWrite(self.__render_group, '= ? mystery',
                (SCREEN_SIZE[0]*0.546, SCREEN_SIZE[1]*0.39),
                step_writing_time=50, wait_to_begin=2000)
        self.invaders.append(invader)
        invader = SquidInvader(self.__render_group)
        invader.rect.center = SCREEN_SIZE[0]*0.33, SCREEN_SIZE[1]*0.47
        text = TextWrite(self.__render_group, '= 30 POINTS',
                (SCREEN_SIZE[0]*0.544, SCREEN_SIZE[1]*0.47),
                step_writing_time=50, wait_to_begin=3500)
        self.invaders.append(invader)
        invader = CrabInvader(self.__render_group)
        invader.rect.center = SCREEN_SIZE[0]*0.33, SCREEN_SIZE[1]*0.55
        text = TextWrite(self.__render_group, '= 20 POINTS',
                (SCREEN_SIZE[0]*0.544, SCREEN_SIZE[1]*0.55),
                step_writing_time=50, wait_to_begin=4500)
        self.invaders.append(invader)
        invader = OctopusInvader(self.__render_group)
        invader.rect.center = SCREEN_SIZE[0]*0.33, SCREEN_SIZE[1]*0.63
        text = TextWrite(self.__render_group, '= 10 POINTS',
                (SCREEN_SIZE[0]*0.544, SCREEN_SIZE[1]*0.63),
                step_writing_time=50, wait_to_begin=5500)
        self.invaders.append(invader)
    def __build_bottom(self):
        self.credits_text = TextWrite(self.__render_group, 
                'credit 00', (SCREEN_SIZE[0]*0.5, SCREEN_SIZE[1]*0.9))
        text = TextWrite(self.__render_group, '<press space to continue>')
        text.rect.centery = SCREEN_SIZE[1]*0.8
        Figure(self.__render_group, '?-help',
                centerpos=(SCREEN_SIZE[0]*.09, SCREEN_SIZE[1]*.95), 
                fadein=True)
    def update_invaders(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 500:
            for inv in self.invaders:
                inv.update_sprite()
            self.__time = t

class MenuScene(Scene):
    def __init__(self):
        self.__mus = MenuMusic()
        super().__init__()
    def setup(self):
        self.__mus.set_volume(1)
        self.menu = _Menu(self.render_group)
        self.__time_pressed_init = None
        game_instance().game_input.set_keypressing({
            pygame.K_SPACE: self.start_game,
            pygame.K_h: self.show_instructions
        })
    def resume_execution(self):
        self.setup()
    def when_unload_do(self):
        self.render_group.empty()
    def show_instructions(self):
        game_instance().game_input.clear_key_func()
        boot_scene(InstructionsScene(), cache_previous=True)
    def start_game(self):
        self.menu.credits_text.setup_text('credit 01')
        if not self.__time_pressed_init:
            play_coin()
            self.__time_pressed_init = pygame.time.get_ticks()
    def update(self):
        super().update()
        self.menu.update_invaders()
        t = pygame.time.get_ticks()
        if self.__time_pressed_init and t - self.__time_pressed_init > 1000:
            self.__mus.set_volume(0)
            game_instance().game_input.clear_key_func()
            boot_scene(GameScene(), cache_previous=True)
