__GAME_INSTANCE = None

class GameNotInitializedException(Exception):
    def __init__(self, msg='Game was not initialized.'):
        self.message = msg
        super().__init__(self.message)
    def __repr__(self):
        return self.message

def game_instance_entry(game_instance: 'Game'):
    global __GAME_INSTANCE
    if not __GAME_INSTANCE:
        __GAME_INSTANCE = game_instance

def game_instance() -> 'Game':
    global __GAME_INSTANCE
    if not __GAME_INSTANCE:
        raise GameNotInitializedException()
    return __GAME_INSTANCE
