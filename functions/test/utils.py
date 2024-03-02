from gamesetmatch.player import Player

def create_dummy_player():
    p = Player.create_dummy_player()
    return p


def create_register_player_request_object( p : Player):
    player = p.to_dict()
    return player