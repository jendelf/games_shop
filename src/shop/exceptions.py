class GameNotFound(Exception):
    def __init__(self, game_id):
        self.game_id = game_id
        self.message = {f"Game with id {game_id} wasn't found"}
        super(). __init__(self.message)

class GameAlreadyExist(Exception):
    def __init__(self, title: str):
        self.title = title
        self.message = {f"You can not add {title} because it's already exist"}
        super(). __init__(self.message)

class PermissionDenied(Exception):
    def __init__(self, title: str):
        self.title = title
        self.message = {f"You don't have rights to delete this game!"}