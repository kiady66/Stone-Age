# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
import time
import tkinter as tk

import Controller
from GUI.GUI_game import Application
from GUI.GUI_menu import Interface
from Game.Game import Game
from UI import TextUI
from XMLReader import XMLReader

# Press the green button in the gutter to run the script.

XMLReader('./game_elements-StoneAge.xml')
game_setup = XMLReader.read()
print(f'Hi, welcome to {game_setup.game_name} game!')
controller = Controller.Controller()
game = Game(game_setup, controller)
controller.game = game

class Main(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game

    def run(self):
        self.game.run()


if __name__ == '__main__':
    root = tk.Tk()
    interface = Interface(root, game.settings.player_colors)
    root.title(game.settings.game_name + ' - Menu')
    interface.mainloop()
    root.destroy()

    if interface.color_selected is not None:
        couleurJoueur = interface.color_selected
        color = game.current_player.color
        for player in game.players_in_order:
            if player.color == couleurJoueur:
                player.color = game.current_player.color

        game.current_player.color = couleurJoueur
        root = tk.Tk()
        app = Application(couleurJoueur, game, controller, master=root)
        game.view = app
        Main(game).start()

        app.mainloop()
    else:
        print("Quit")
