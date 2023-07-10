import os
import pygame

_RD = os.path.join(os.path.dirname(__file__))
''' 
in this map you should represent the sprite as:
if sprite is an unity: use one tuple of i, j index
if sprite is a line: use one list of unities
if sprite is a square: use one list of lines
use res.util.get_sprite to load resource.
'''
SPRITE_MAP = {
    # window icon
    'icon'              : [[(11, 7), (11, 7)],
                            [(1, 0), (1, 1)]],
    # player cannon
    'cannon'            : [(3, 5), (3, 6)],
    # invaders
    'squid_1'           : [(0, 0), (0, 1)],
    'squid_2'           : [(0, 2), (0, 3)],
    'crab_1'            : [(0, 4), (0, 5)],
    'crab_2'            : [(0, 6), (0, 7)],
    'octopus_1'         : [(1, 0), (1, 1)],
    'octopus_2'         : [(1, 2), (1, 3)],
    'ufo'               : [(3, 3), (3, 4)],
    # carrying-Y squid
    'squid-x_1'         : [(11, 2), (11, 3)], # with no y
    'squid-x_2'         : [(11, 4), (11, 5)], # with no y
    'squid-ý_1'         : [(5, 0), (5, 1)], # ý is inverted y
    'squid-ý_2'         : [(5, 2), (5, 3)],
    'squid-y_1'         : [(5, 4), (5, 5)],
    'squid-y_2'         : [(5, 6), (5, 7)],
    # explosions
    'explosion_0'       : [(1, 4), (1, 5)],
    'explosion_1'       : (2, 4),
    'explosion_2'       : (3, 7),
    'explosion_3'       : [(2, 5), (2, 6), (2, 7)],
    'explosion_4'       : [(4, 3), (4, 4)],
    'explosion_5'       : [(4, 5), (4, 6)],
    # shots
    'shot_0'            : [(1, 6), (1, 7)],
    'shot_1'            : [(2, 0), (2, 1)],
    'shot_2'            : [(2, 2), (2, 3)],
    'shot_3'            : [(11, 6), (11, 7)],
    # hangar
    'hangar'            : [[(3, 0), (3, 1), (3, 2)], 
                           [(4, 0), (4, 1), (4, 2)]],
    # characters
    'A'                 : (6, 0),
    'B'                 : (6, 1),
    'C'                 : (6, 2),
    'D'                 : (6, 3),
    'E'                 : (6, 4),
    'F'                 : (6, 5),
    'G'                 : (6, 6),
    'H'                 : (6, 7),
    'I'                 : (7, 0),
    'J'                 : (7, 1),
    'K'                 : (7, 2),
    'L'                 : (7, 3),
    'M'                 : (7, 4),
    'N'                 : (7, 5),
    'O'                 : (7, 6),
    'P'                 : (7, 7),
    'Q'                 : (8, 0),
    'R'                 : (8, 1),
    'S'                 : (8, 2),
    'T'                 : (8, 3),
    'U'                 : (8, 4),
    'V'                 : (8, 5),
    'W'                 : (8, 6),
    'X'                 : (8, 7),
    'Y'                 : (9, 0),
    'Ý'                 : (4, 7), #inverted Y
    'Z'                 : (9, 1),
    '0'                 : (9, 2),
    '1'                 : (9, 3),
    '2'                 : (9, 4),
    '3'                 : (9, 5),
    '4'                 : (9, 6),
    '5'                 : (9, 7),
    '6'                 : (10, 0),
    '7'                 : (10, 1),
    '8'                 : (10, 2),
    '9'                 : (10, 3),
    '<'                 : (10, 4),
    '>'                 : (10, 5),
    '='                 : (10, 6),
    '*'                 : (10, 7),
    '?'                 : (11, 0),
    '-'                 : (11, 1),
    ' '                 : (12, 0)
}

def img(img_name) -> str:
    '''returns image resource full path'''
    return os.path.join(_RD, 'img', img_name)

def load_img(img_name) -> pygame.Surface:
    return pygame.image.load(img(img_name)).convert_alpha()