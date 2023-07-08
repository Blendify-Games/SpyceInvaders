import pygame

import scenes
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene
from scenes.opening_scene import OpeningScene
from res.config import SCREEN_SIZE, GAME_NAME

class GameInput(object):
    '''
    This class handles keyboard and mouse events.
    '''
    def __init__(self):
        self.__quit = self.__no_operation
        self.__key_func = {}
    def __no_operation(self):
        pass
    def set_keypressing(self, key_func_pairs: dict):
        '''
        Setup a keypressing listener for a key.
        set_keypressing must receive a dict containing
        pairs of pygame.keys and listeners. For example:
        ginput.set_keypressing({pygame.K_t: listener})
        To remove listener you can use a pair like:
        {pygame.K_t: None}
        or call clear_key_func
        '''
        self.__key_func.update(key_func_pairs)
        for k, f in key_func_pairs.items():
            if not f:
                self.__key_func[k] = self.__no_operation
    def set_quit_listener(self, listener:'function'):
        '''
        Set a listener for quit (X button) event.
        If listener = None then quit operation will
        be not executed anymore
        '''
        self.__quit = listener if listener else self.no_operation
    def clear_key_func(self):
        '''
        Removes all listeners for all keys.
        '''
        self.__key_func = {}
    def listen(self):
        '''
        Listen for mouse and keyboard events
        '''
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                self.__quit()
        for k, func in self.__key_func.items():
            if pygame.key.get_pressed()[k]:
                func()

class Game(object):
    '''
    Handle game stuff. Can be controled everywhere by
    accessing game_instance
    '''
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_NAME)
        self.screen.fill('black')
        self.running = False
        self.game_input = GameInput()
        self.game_input.set_quit_listener(self.quit)
        self.clock = pygame.Clock()
    def quit(self):
        ''' set running to false '''
        self.running = False
    def iterate(self) -> bool:
        ''' performs one iteration of the game
        and returns true if game still running '''
        if not self.running:
            scenes.boot_scene(OpeningScene())
            self.running = True
        self.game_input.listen()
        scenes.current_scene_update()
        self.clock.tick(60)
        return self.running
