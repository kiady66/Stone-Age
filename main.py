import Controller
from Game.Game import Game
from UI import TextUI
from XMLReader import XMLReader


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    XMLReader('./game_elements-StoneAge.xml')
    game_setup = XMLReader.read()
    print(f'Hi, welcome to {game_setup.game_name} game!')
    controller = Controller.Controller()
    all_places = list(game_setup.game_board_setup.places)
    all_places += game_setup.game_board_setup.building_places
    all_places += game_setup.game_board_setup.civilization_places
    view = TextUI(set(all_places), controller)
    game = Game(game_setup, controller)
    game.view = view
    controller.game = game
    game.run()
