from typing import Set

from Action import ActionType
from Game.Game import Game, State
from GameSetup.GameSetup import GameSetup
from Player import HumanPlayer, IAPlayer, AbstractPlayer
from XMLreader import XMLreader


def test_place_meeples_state():
    assert True


def test_take_meeples_state(capsys):
    game = createGameFromXML()
    game.state = State.PLACE_MEEPLES
    input_values = [2]

    def mock_input(s):
        return input_values.pop(0)
    Game.input = mock_input
    game.test()
    out, err = capsys.readouterr()
    ''' game.take_meeples_state()
    assert game.state == State.TAKE_MEEPLES '''


def test_one_player_take_meeples():

    assert True


def test_feed_meeples_state():
    game = createGameFromXML()
    game.state = State.TAKE_MEEPLES
    player = game.players_in_order[0]
    player.set_farmable_count(game.settings.food, 6)
    game.feed_meeples_state()
    assert game.state == State.FEED_MEEPLES
    assert player.get_farmable_count(game.settings.food) == 1
    game.feed_meeples_state()
    assert player.get_farmable_count(game.settings.food) == 0


def test_generate_actions():
    assert True


def test_generate_place_actions():
    assert True


def test_generate_take_actions():
    game = createGameFromXML()
    game.state = State.TAKE_MEEPLES
    player = game.players_in_order[0]
    for place in game.game_board.places:
        if place.name == 'Forest':
            place_forest = place
            place.meeples[player] = 3
        if place.name == 'Hunt':
            place_hunt = place
            place.meeples[player] = 2
    list_action = game.generate_take_actions()
    for action in list_action:
        assert action.action_type == ActionType.TAKE_MEEPLES
        if action.place == place_forest:
            assert action.place.meeples[player] == 3
        elif action.place == place_hunt:
            assert action.place.meeples[player] == 2
        else:
            assert False


def test_is_end():
    assert True


def test_execute_action():
    assert True


def test_execute_place_action():
    assert True


def test_execute_take_action():
    assert True


def test_get_resource_from_place():
    assert True


def createListPlayer(game_setup: GameSetup) -> Set[AbstractPlayer]:
    set_player: Set[AbstractPlayer] = set()
    set_player.add(HumanPlayer(game_setup, game_setup.player_colors[0], 0))
    for index in range(1, len(game_setup.player_colors)):
        set_player.add(IAPlayer(game_setup, game_setup.player_colors[index], 0))
    return set_player


def createGameFromXML() -> Game:
    XMLreader('/Users/simonchaval/PycharmProjects/stone-age/game_elements-StoneAge.xml')
    game_setup = XMLreader.read()
    return Game(game_setup, createListPlayer(game_setup))