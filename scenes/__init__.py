import pygame

from game_instance import game_instance

__PREVIOUS_SCENES    = []
__CONTEXT_SCENE      = None

class NoSceneBootedException(Exception):
    def __init__(self, msg='There\'s no scene booted.'):
        self.message = msg
        super().__init__(self.message)
    def __repr__(self):
        return self.message

class Scene(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.render_group = pygame.sprite.Group()
        self.setup()
    def setup(self):
        raise NotImplementedError()
    def resume_execution(self):
        pass
    def when_unload_do(self):
        pass
    def update(self):
        self.render_group.update()

def boot_scene(scene: Scene, cache_previous:bool = False):
    global __CONTEXT_SCENE, __PREVIOUS_SCENES
    if __CONTEXT_SCENE:
        __CONTEXT_SCENE.when_unload_do()
        if cache_previous:
            __PREVIOUS_SCENES.append(__CONTEXT_SCENE)
    __CONTEXT_SCENE = scene

def unload_current_scene():
    global __CONTEXT_SCENE, __PREVIOUS_SCENES
    scene = __CONTEXT_SCENE
    if __PREVIOUS_SCENES:
        __CONTEXT_SCENE = __PREVIOUS_SCENES.pop()
        __CONTEXT_SCENE.resume_execution()
        scene.when_unload_do()
    else:
        game_instance().quit()

def current_scene_update():
    global __CONTEXT_SCENE, __PREVIOUS_SCENES
    if not __CONTEXT_SCENE:
        raise NoSceneBootedException()
    __CONTEXT_SCENE.screen.fill('black')
    __CONTEXT_SCENE.update()
    __CONTEXT_SCENE.render_group.draw(__CONTEXT_SCENE.screen)
    pygame.display.flip()
