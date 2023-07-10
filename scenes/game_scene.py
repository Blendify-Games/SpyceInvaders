import random
import pygame

from scenes import Scene

from game_instance import game_instance
from gameobj.invaders import (
    OctopusInvader, SquidInvader,
    CrabInvader, UFOInvader
)
from gameobj.hangar import Hangar
from gameobj.cannon import Cannon
from res.config import SCREEN_SIZE, ENTITY_COLORS
from res.util import sprite_sheet, get_text, change_surf_color
from res.util import SPRITE_SIZE
from scenes.writing import TextWrite

# position of the first invader to be blitted
_POS_INVADER = (160, 352)
_X, _Y = _POS_INVADER
# position of the first hangar to be blitted
_POS_HANGAR = (175, 544)
# floor
_POS_FLOOR_Y = 704
# player initial center position
_POS_PLAYER = (SCREEN_SIZE[0]//2, _POS_FLOOR_Y-48)

class _ScoreBoard(TextWrite):
    def __init__(self, render_group:pygame.sprite.Group):
        text = TextWrite(render_group, 'Score', 
                    (SCREEN_SIZE[0]*0.70, SCREEN_SIZE[1]*0.96))
        change_surf_color(text.image, '#f59342')
        super().__init__(render_group, '<0000>', 
                    (SCREEN_SIZE[0]*0.88, SCREEN_SIZE[1]*0.96))
        self.score_points = 0
    def add_to_score(self, v:int):
        self.score_points += v
        self.setup_text(f'<{self.score_points:04d}>')

class _StatusDisplay(object):
    def __init__(self, render_group:pygame.sprite.Group):
        self.render_group = render_group
        self.score_board = _ScoreBoard(render_group)
        self.__built_floor_line()
        self.__build_game_chances_display()
    def __built_floor_line(self):
        self.floor_line = pygame.sprite.Sprite(self.render_group)
        self.floor_line.image = pygame.Surface((SCREEN_SIZE[0], 4))
        pygame.draw.line(self.floor_line.image, 
                        ENTITY_COLORS['floor_line'],
                        (0, 0), (SCREEN_SIZE[0], 0), 4)
        self.floor_line.rect = self.floor_line.image.get_rect()
        self.floor_line.rect.topleft = (0, _POS_FLOOR_Y)
    def __build_game_chances_display(self):
        self.__game_chances = []
        for i in range(0, 2):
            cannon = Cannon(self.render_group)
            cannon.rect.topleft = (i*64 + 80, _POS_FLOOR_Y + 16)
            self.__game_chances.append(cannon)
        self.__game_chances_text = TextWrite(
            self.render_group, str(len(self.__game_chances)+1),
            (48, _POS_FLOOR_Y+32)
        )
    def decrease_game_chances(self) -> int:
        if len(self.__game_chances) > 1:
            self.__game_chances.pop().remove(self.render_group)
        self.__game_chances_text.setup_text(str(len(self.__game_chances)+1))
        return len(self.__game_chances)

class _PlayerControl(object):
    __SPEED = 5
    def __init__(self, 
        render_group:pygame.sprite.Group,
        player_shot_group:pygame.sprite.Group,
        enemy_group:pygame.sprite.Group,
        enemy_shot_group:pygame.sprite.Group):
        self.__groups = [render_group, player_shot_group, 
                        enemy_group, enemy_shot_group]
        self.cannon = Cannon(self.__groups[0])
        self.cannon.rect.center = _POS_PLAYER
        self.__time_shot = pygame.time.get_ticks()
    def __move_left(self):
        if(self.cannon.rect.left - self.__SPEED > 0):
            self.cannon.rect.move_ip(-self.__SPEED, 0)
    def __move_right(self):
        if(self.cannon.rect.right + self.__SPEED < SCREEN_SIZE[0]):
            self.cannon.rect.move_ip(self.__SPEED, 0)
    def __shoot(self):
        # shoot only if previous shot is gone
        if not len(self.__groups[1]):
            self.cannon.shoot(self.__groups[1])
    def is_player_dead(self) -> bool:
        collided1 = pygame.sprite.spritecollideany(
            self.cannon, self.__groups[3])
        if collided1:
            self.cannon.kill()
            collided1.remove(*self.__groups)
            return True
        return False
    def get_controls(self) -> dict:
        return {
            pygame.K_a: self.__move_left,
            pygame.K_d: self.__move_right,
            pygame.K_SPACE: self.__shoot
        }

class GameScene(Scene):
    def setup(self):
        self.invaders = {
            OctopusInvader   : {'sprites': [], 'max': 22},
            CrabInvader      : {'sprites': [], 'max': 22},
            SquidInvader     : {'sprites': [], 'max': 11},
            UFOInvader       : {'sprites': [], 'max': 1},
            'order'          : [UFOInvader, SquidInvader, CrabInvader, OctopusInvader]
        }
        self.hangars = []
        self.__inv_class = self.invaders['order'].pop()
        self.__time = pygame.time.get_ticks()
        self.__time_inv_created = pygame.time.get_ticks()
        self.__iteration = self.__build_hangars
        self.__player_shot_group = pygame.sprite.Group()
        self.__enemy_group = pygame.sprite.Group()
        self.__enemy_shot_group = pygame.sprite.Group()

    # game scene iterations
    def __build_hangars(self):
        for i in range(0, 4):
            hangar = Hangar(self.render_group)
            hangar.rect.topleft = \
                (i * SPRITE_SIZE[0] * 6) + _POS_HANGAR[0], _POS_HANGAR[1]
            self.hangars.append(hangar)
        self.__iteration = self.__build_bottom
    def __build_bottom(self):
        self.__status_display = _StatusDisplay(self.render_group)
        self.__iteration = self.__build_invaders
    def __build_invaders(self):
        global _POS_INVADER, _X, _Y
        t = pygame.time.get_ticks()
        if t - self.__time_inv_created > 30:
            inv = self.__inv_class(self.render_group, self.__enemy_group)
            self.invaders[self.__inv_class]['sprites'].append(inv)
            if self.__inv_class == UFOInvader:
                inv.rect.topleft = -SPRITE_SIZE[0] * 0, _Y-16
            else:
                inv.rect.topleft = _X, _Y
            _X += SPRITE_SIZE[0] * 2
            if len(self.invaders[self.__inv_class]['sprites']) % 11 == 0:
                _Y -= SPRITE_SIZE[1] * 2
                _X = _POS_INVADER[0]
            if len(self.invaders[self.__inv_class]['sprites']) == \
                    self.invaders[self.__inv_class]['max']:
                if len(self.invaders['order']) < 1:
                    self.__iteration = self.__init_game_execution
                else:
                    self.__inv_class = self.invaders['order'].pop()
            self.__time_inv_created = t
    def __init_game_execution(self):
        self.__iteration = self.__game_execution
        self.__player = _PlayerControl(self.render_group, 
                                        self.__player_shot_group,
                                        self.__enemy_group,
                                        self.__enemy_shot_group)
        game_instance().game_input.set_keypressing(
            self.__player.get_controls()
        )
    def __game_execution(self):
        if random.randint(0, 1000) < 20:
            sprite = self.__enemy_group.sprites()[
                random.randint(0, len(self.__enemy_group)-1)
            ]
            sprite.shoot(self.__enemy_shot_group)
        if len(self.__player_shot_group):
            killed = pygame.sprite.groupcollide(
                self.__player_shot_group,
                self.__enemy_group,
                True, False
            )
            for k, v in killed.items():
                self.__status_display.score_board.add_to_score(
                    v[0].SCORE_POINT
                )
                v[0].kill()
                break
        if self.__player.is_player_dead():
            self.__player_was_killed()
    def __reset_game(self):
        pass
    def __end_game(self):
        pass
    # game scene functionalities
    def __player_was_killed(self):
        self.__player = None
        game_instance().game_input.clear_key_func()
        if self.__status_display.decrease_game_chances() > 0:
            self.__iteration = self.__reset_game
        else:
            self.__iteration = self.__end_game
    def update(self):
        super().update()
        self.__iteration()
