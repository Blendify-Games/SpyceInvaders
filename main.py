import asyncio
import pygame
from game import Game
from game_instance import (
    game_instance_entry, game_instance
)

async def main():
    pygame.init()
    game_instance_entry(Game())
    while game_instance().iterate():
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
