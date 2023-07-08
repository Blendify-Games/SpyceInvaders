import pygame

import res
from res.config import (
    SPRITE_SCALE, SPRITE_SIZE
)

__SPRITE_SHEET = None

def sprite_sheet() -> 'list(surf)':
    '''load and give access to the sprite_sheet.
    the sprite sheet is cached at the first loading
    process.'''
    global __SPRITE_SHEET
    if not __SPRITE_SHEET:
        sw, sh = SPRITE_SIZE
        sheet = pygame.image.load(res.img('sprites.png')).convert_alpha()
        w, h = sheet.get_size()
        w, h = w * SPRITE_SCALE, h * SPRITE_SCALE
        sheet = pygame.transform.scale(sheet, (w, h))
        cutrect = pygame.Rect(0, 0, SPRITE_SIZE[0], SPRITE_SIZE[1])
        __SPRITE_SHEET = []
        for i in range(0, h//SPRITE_SIZE[0]):
            __SPRITE_SHEET.append([])
            cutrect.y = i*SPRITE_SIZE[0]
            for j in range(0, w//SPRITE_SIZE[1]):
                cutrect.x = j*SPRITE_SIZE[1]
                sprchunk = sheet.subsurface(cutrect)
                __SPRITE_SHEET[i].append(sprchunk)
    return __SPRITE_SHEET

def change_surf_color(surf: pygame.Surface, 
        to_color:'color_value', 
        from_color:'color_value'='#ffffff', 
        copy:bool=False) -> pygame.Surface:
    '''change a surface color, by selecting a key color
    and swapping it to other key color'''
    nsurf = surf
    to_color = pygame.Color(to_color)
    from_color = pygame.Color(from_color)
    if copy:
        nsurf = surf.copy()
    # a dumb way to avoid using PixelArray
    # because pygbag lib doesn't accept it.
    # sorry 'bout that
    w, h = nsurf.get_size()
    for y in range(0, h):
        for x in range(0, w):
            if nsurf.get_at((x, y)) == from_color:
                nsurf.set_at((x, y), to_color)
    return nsurf

def get_text(text:str) -> pygame.Surface:
    '''produces a text using the characters
    available on sprite sheet'''
    ss = sprite_sheet()
    w, h = SPRITE_SIZE
    surf = pygame.Surface((w * len(text), h))
    surf.set_colorkey((0,0,0))
    text = text.upper()
    dest = pygame.Rect(0, 0, w, h)
    for letter in text:
        i, j = res.SPRITE_MAP[letter]
        lsurf = ss[i][j]
        surf.blit(lsurf, dest)
        dest.x += w
    return surf

def __concat_sprite_line(unities:list) -> pygame.Surface:
    '''concatenate block unities in one line of sprite block'''
    w, h = SPRITE_SIZE
    img = pygame.Surface((w*len(unities), h))
    offw = 0
    seq = []
    for u in unities:
        i, j = u
        seq.append((sprite_sheet()[i][j], (w * offw, 0)))
        offw += 1
    img.blits(blit_sequence=seq)
    return img

def __manage_sprites(resp_spr:'SPRITE_MAP_value') -> pygame.Surface:
    '''decide if the sprite block is a unity, a line or a square
    and return the mounted surface'''
    w, h = SPRITE_SIZE
    # unity
    if type(resp_spr) == tuple:
        i, j = resp_spr
        return sprite_sheet()[i][j].copy()
    # line
    if type(resp_spr[0]) == tuple:
        return __concat_sprite_line(resp_spr)
    # square
    img = pygame.Surface((w*len(resp_spr[0]), h*len(resp_spr)))
    offh = 0
    seq = []
    for unities in resp_spr:
        line = __concat_sprite_line(unities)
        seq.append((line, (0, h*offh)))
        offh += 1
    img.blits(blit_sequence=seq)
    return img

def get_sprite_block(key:str) -> pygame.Surface:
    '''get a sprite block by key on SPRITE_MAP.'''
    res_spr = res.SPRITE_MAP[key]
    surf = __manage_sprites(res_spr)
    surf.set_colorkey((0,0,0))
    return surf
