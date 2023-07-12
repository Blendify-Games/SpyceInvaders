import pygame
import scenes

from game_instance import game_instance
from res.config import SCREEN_SIZE
from scenes import Scene
from scenes.writing import TextWrite, Figure

class InstructionsScene(Scene):
    def setup(self):
        Figure(self.render_group, 'a-button', 
                centerpos=(SCREEN_SIZE[0]*.3, SCREEN_SIZE[1]*.3),
                fadein=True)
        Figure(self.render_group, '->', 
                centerpos=(SCREEN_SIZE[0]*.35, SCREEN_SIZE[1]*.295),
                fadein=True)
        TextWrite(self.render_group, 'move left',
                    centerpos=(SCREEN_SIZE[0]*.53, SCREEN_SIZE[1]*.295),
                    step_writing_time=100)
        Figure(self.render_group, 'd-button', 
                centerpos=(SCREEN_SIZE[0]*.3, SCREEN_SIZE[1]*.4),
                fadein=True)
        Figure(self.render_group, '->', 
                centerpos=(SCREEN_SIZE[0]*.35, SCREEN_SIZE[1]*.395),
                fadein=True)
        TextWrite(self.render_group, 'move right',
                    centerpos=(SCREEN_SIZE[0]*.545, SCREEN_SIZE[1]*.395),
                    step_writing_time=100, wait_to_begin=1000)
        Figure(self.render_group, 'space-btn', 
                centerpos=(SCREEN_SIZE[0]*.26, SCREEN_SIZE[1]*.5),
                fadein=True)
        Figure(self.render_group, '->', 
                centerpos=(SCREEN_SIZE[0]*.35, SCREEN_SIZE[1]*.495),
                fadein=True)
        TextWrite(self.render_group, 'cannon shoot',
                    centerpos=(SCREEN_SIZE[0]*.58, SCREEN_SIZE[1]*.495),
                    step_writing_time=100, wait_to_begin=2000)
        Figure(self.render_group, 'q-button', 
                centerpos=(SCREEN_SIZE[0]*.3, SCREEN_SIZE[1]*.6),
                fadein=True)
        Figure(self.render_group, '->', 
                centerpos=(SCREEN_SIZE[0]*.35, SCREEN_SIZE[1]*.595),
                fadein=True)
        TextWrite(self.render_group, 'back to menu',
                    centerpos=(SCREEN_SIZE[0]*.58, SCREEN_SIZE[1]*.595),
                    step_writing_time=100, wait_to_begin=3000)
        
        game_instance().game_input.set_keypressing({
            pygame.K_q: self.__leave_instructions_scene
        })
    def __leave_instructions_scene(self):
        game_instance().game_input.clear_key_func()
        scenes.unload_current_scene()
    def update(self):
        super().update()
