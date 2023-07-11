import random
import pygame
import scenes

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
    __LIVES = 3
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
        for i in range(0, self.__LIVES - 1):
            cannon = Cannon(self.render_group)
            cannon.rect.topleft = (i*64 + 80, _POS_FLOOR_Y + 16)
            self.__game_chances.append(cannon)
        self.__game_chances_text = TextWrite(
            self.render_group, str(self.__LIVES),
            (48, _POS_FLOOR_Y+32)
        )
    def decrease_game_chances(self) -> int:
        if len(self.__game_chances) > 0:
            self.__game_chances.pop().remove(self.render_group)
        self.__LIVES -= 1
        self.__game_chances_text.setup_text(str(self.__LIVES))
        return self.__LIVES

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
        collided1 = pygame.sprite.spritecollide(
            self.cannon, self.__groups[3], True)
        if collided1:
            self.cannon.kill()
            return True
        player_shots = self.__groups[1].sprites()
        if player_shots:
            collided2 = pygame.sprite.spritecollideany(
                player_shots[0], self.__groups[3]
            )
            if collided2:
                player_shots[0].miss()
        return False
    def get_controls(self) -> dict:
        return {
            pygame.K_a: self.__move_left,
            pygame.K_d: self.__move_right,
            pygame.K_SPACE: self.__shoot
        }

class GameScene(Scene):
    def setup(self):
        self.__status_display = _StatusDisplay(self.render_group)
        self.invaders = {
            'shoot_probability'    : 1.5,
            'move_time'            : 900,
            'speed_up_per_kill'    : 16
        }
        self.__init_game()
    def __init_game(self):
        self._X, self._Y = _POS_INVADER
        self.invaders.update({
            OctopusInvader   : {'n': 0, 'max': 22},
            CrabInvader      : {'n': 0, 'max': 22},
            SquidInvader     : {'n': 0, 'max': 11},
            UFOInvader       : {'n': 0, 'max': 1},
            'total_invaders' : 0,
            'order'          : [UFOInvader, SquidInvader, CrabInvader, OctopusInvader],
            'last_move'      : pygame.time.get_ticks(),
            'ufo_present'    : False,
            'ufo_abs_time'   : pygame.time.get_ticks(),
            'hit_boundaries' : False,
            'go_invert'      : True,
        }) # this structure controls invaders instantiation
        self.__inv_class = self.invaders['order'].pop()
        self.__time = pygame.time.get_ticks()
        self.__time_inv_created = pygame.time.get_ticks()
        self.__iteration = self.__build_hangars
        self.__player_shot_group = pygame.sprite.Group()
        self.__enemy_group = pygame.sprite.Group()
        self.__enemy_shot_group = pygame.sprite.Group()
        self.__hangar_group = pygame.sprite.Group()
        self.__ufo_invader = None
    # game scene iterations
    def __build_hangars(self):
        for i in range(0, 4):
            hangar = Hangar(self.render_group, self.__hangar_group)
            hangar.rect.topleft = \
                (i * SPRITE_SIZE[0] * 6) + _POS_HANGAR[0], _POS_HANGAR[1]
        self.__iteration = self.__build_invaders
    def __build_invaders(self):
        global _POS_INVADER
        t = pygame.time.get_ticks()
        if t - self.__time_inv_created > 30:
            inv = self.__inv_class(self.render_group, self.__enemy_group)
            self.invaders[self.__inv_class]['n'] += 1
            if self.__inv_class == UFOInvader:
                self.__ufo_invader = inv
                inv.rect.topleft = -SPRITE_SIZE[0] * 2, self._Y-16
            else:
                inv.rect.topleft = self._X, self._Y
            self._X += SPRITE_SIZE[0] * 2
            if self.invaders[self.__inv_class]['n'] % 11 == 0:
                self._Y -= SPRITE_SIZE[1] * 2
                self._X = _POS_INVADER[0]
            if self.invaders[self.__inv_class]['n'] == \
                    self.invaders[self.__inv_class]['max']:
                if len(self.invaders['order']) < 1:
                    self.invaders['total_invaders'] = len(self.__enemy_group.sprites())
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
        global _POS_FLOOR_Y

        # decide one enemy to shoot
        if len(self.__enemy_group.sprites()) > 0 and (
            random.random() * 100 < self.invaders['shoot_probability']):
            sprite = self.__enemy_group.sprites()[
                random.randint(0, len(self.__enemy_group)-1)
            ]
            sprite.shoot(self.__enemy_shot_group, limit=(0, _POS_FLOOR_Y))
        
        # check if invader has been shot
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
        
        # move invaders
        self.__move_common_invaders()
        if self.__ufo_invader.alive():
            self.__move_ufo()

        # check if player has been killed
        if self.__player.is_player_dead():
            self.__player_was_killed()
    def __reset_game(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 2000:
            self.__iteration = self.__init_game_execution
    def __end_game(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 30:
            if len(self.__enemy_group.sprites()):
                enemy = self.__enemy_group.sprites()[0]
                enemy.remove(self.render_group, self.__enemy_group)
                if not len(self.__enemy_group.sprites()):
                    TextWrite(self.render_group, 'Game Over',
                        (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]*.4),
                        step_writing_time=200, wait_to_begin=1000)
                self.__time = t
        if t - self.__time > 5000:
            scenes.unload_current_scene()

    # game scene functionalities
    def __move_common_invaders(self):
        t = pygame.time.get_ticks()
        t2 = self.invaders['move_time'] - (
            self.invaders['total_invaders'] - len(self.__enemy_group.sprites())
        ) * self.invaders['speed_up_per_kill']
        if t - self.invaders['last_move'] > t2:
            # identify if any invader hit screen boundaries
            for invader in self.__enemy_group.sprites():
                if type(invader) != UFOInvader and \
                    (not self.invaders['hit_boundaries']) and (
                    invader.rect.left - invader.rect.w//2 < 0 or
                    invader.rect.right + invader.rect.w//2 > SCREEN_SIZE[0]):
                    self.invaders['hit_boundaries'] = True
                    break
            # if hit_boundaries go down and then go invert
            if self.invaders['hit_boundaries'] and \
                not self.invaders['go_invert']:
                for invader in self.__enemy_group.sprites():
                    if type(invader) != UFOInvader:
                        invader.move(down=True)
                        invader.change_direction()
                self.invaders['go_invert'] = True
            else:
                for invader in self.__enemy_group.sprites():
                    if type(invader) != UFOInvader:
                        invader.move()
                self.invaders['hit_boundaries'] = False
                self.invaders['go_invert'] = False
            self.invaders['last_move'] = t
    def __move_ufo(self):
        t = pygame.time.get_ticks()
        if not self.invaders['ufo_present']:
            if t - self.invaders['ufo_abs_time'] > 5000:
                if not self.invaders['ufo_present']:
                    if random.choice([True, False]):
                        self.invaders['ufo_present'] = True
                self.invaders['ufo_abs_time'] = t    
        else:
            self.invaders['ufo_present'] = \
                not self.__ufo_invader.move_until_limits()
            self.invaders['ufo_abs_time'] = t
    def __player_was_killed(self):
        self.__player = None
        game_instance().game_input.clear_key_func()
        if self.__status_display.decrease_game_chances() > 0:
            self.__time = pygame.time.get_ticks()
            self.__iteration = self.__reset_game
        else:
            self.__time = pygame.time.get_ticks()
            self.__iteration = self.__end_game
    def update(self):
        super().update()
        self.__iteration()
