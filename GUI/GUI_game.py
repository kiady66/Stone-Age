import time
import tkinter as tk
from abc import ABC
from typing import Set, List, Dict

from PIL import Image, ImageTk

from Controller import Controller
from Game.Game import Game, State
from Player import AbstractPlayer
from UI import View


class Place:
    def __init__(self, name, coord_x, coord_y):
        self.nom = name
        self.x = coord_x
        self.y = coord_y
        self.videPlein = True


class Application(tk.Frame, View, ABC):
    def __init__(self, color, game : Game, controller: Controller, master=None):
        super().__init__(master)
        self.game = game
        self.set_frame_meeplest = set()
        self.set_image_meeplest = set()
        self.set_image_meeplesn = set()
        self.set_frame_meeplesn = set()
        self.set_frame_meepleshunt = set()
        self.set_image_meepleshunt = set()
        master.protocol("WM_DELETE_WINDOW", quit)
        self.hut = list()
        self.clay_pit = list()
        self.quarry = list()
        self.hunting_ground = list()
        self.river = list()
        self.forest = list()
        self.set_image_meeplesr = set()
        self.set_frame_meeplesr = set()
        self.set_frame_meeplesf = set()
        self.set_image_meeplesf = set()
        self.set_frame_meeplesq = set()
        self.set_image_meeplesq = set()
        self.set_frame_meeplesc = set()
        self.set_image_meeplesc = set()
        self.set_frame_meeplesh = set()
        self.set_image_meeplesh = set()
        self.list_frame_carte = list()
        self.list_image_carte = list()
        self.playerColor = color
        self.master = master
        self.nb_meeple = 0
        self.selected_place = None
        self.map_button_place: Dict[tk.Button, Place] = dict()
        self.pack()
        self.controller = controller
        controller.on_place_event_action = self.place_methode

        # instanciation des places dans le terrain de chasse
        for i in range(0, 40):
            self.hunting_ground.append(Place('h' + str(i), 0.1 + (i % 5 * 0.03), 0.1 + (i / 5 * 0.05)))

        # instanciation des places dans la foret
        for i in range(0, 7):
            self.forest.append(Place('f' + str(i), 0.32 + (i % 3 * 0.03), 0.2 + (i / 3 * 0.05)))

        # instanciation des places dans la river
        for i in range(0, 7):
            self.river.append(Place('r' + str(i), 0.75 + (i % 3 * 0.03), 0.36 + (i / 3 * 0.05)))

        # instanciation des places dans la quarry
        for i in range(0, 7):
            self.quarry.append(Place('q' + str(i), 0.9 + (i % 3 * 0.03), 0.15 + (i / 3 * 0.05)))

        # instanciation des places dans la clay_pit
        for i in range(0, 7):
            self.clay_pit.append(Place('c' + str(i), 0.52 + (i % 3 * 0.03), 0.15 + (i / 3 * 0.05)))

        # instanciation des places dans la hut
        for i in range(0, 2):
            self.hut.append(Place('h' + str(i), 0.38 + (i % 2 * 0.03), 0.7 + (i / 2 * 0.05)))

        # instanciation des places dans la field
        a5 = Place('n1', 0.3, 0.55)

        self.field = [a5]

        # instanciation des places dans la toolMaker
        a6 = Place('t1', 0.55, 0.49)

        self.toolMaker = [a6]

        # Meeples color definition (image)
        self.MeepleRed = 'GUI/Image/Meeples/meepleRed.png'
        self.MeepleGreen = 'GUI/Image/Meeples/meepleGreen.png'
        self.MeepleBlue = 'GUI/Image/Meeples/meepleBlue.png'
        self.MeepleYellow = 'GUI/Image/Meeples/meepleYellow.png'

        self.frame_action = tk.Frame(self)
        self.action_realise = tk.Label(self.frame_action, text='Truc à placer son ouvrier sur...')
        self.action_realise.pack()
        self.frame_action.pack(side=tk.TOP)

        self.frame_plateau = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame_plateau, height=525, width=795, bg='#41B77F')
        self.background = ImageTk.PhotoImage(Image.open('GUI/Image/Board/plateau2.jpg'))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background)
        self.canvas.pack(expand=tk.YES)

        for i in range(0, 4):
            self.frame_card = tk.Frame(self.frame_plateau)
            self.canvas3 = tk.Canvas(self.frame_card, height=123, width=83)
            self.image_card = ImageTk.PhotoImage(Image.open('GUI/Image/Civ_Cards/IFD_8_Time.jpg'))
            self.canvas3.create_image(0, 0, anchor=tk.NW, image=self.image_card)
            self.canvas3.pack()
            self.frame_card.place(relx=0.58 + i * 0.12, rely=0.81, anchor='center')
            self.list_frame_carte.append(self.frame_card)
            self.list_image_carte.append(self.image_card)

        self.frame_plateau.pack(side=tk.LEFT)

        self.frame_joueur = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.nom_Joueur = tk.Label(self.frame_joueur, text=str(self.game.current_player), fg='red')
        self.nom_Joueur.pack()
        self.Joueur1 = dict()
        for stack in self.game.current_player.get_resources():
            self.Joueur1[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
            self.Joueur1[stack].pack()
        stack = game.settings.food
        self.Joueur1[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur1[stack].pack()
        stack = game.settings.meeple
        self.Joueur1[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur1[stack].pack()
        stack = game.settings.food_production
        self.Joueur1[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur1[stack].pack()
        stack = list(self.game.settings.set_tools)[0]
        self.Joueur1[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur1[stack].pack()

        self.nom_Joueur2 = tk.Label(self.frame_joueur, text=str(self.game.players_in_order[1]), fg='red')
        self.nom_Joueur2.pack()
        self.Joueur2 = dict()
        for stack in self.game.current_player.get_resources():
            self.Joueur2[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
            self.Joueur2[stack].pack()
        stack = game.settings.food
        self.Joueur2[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur2[stack].pack()
        stack = game.settings.meeple
        self.Joueur2[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur2[stack].pack()
        stack = game.settings.food_production
        self.Joueur2[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur2[stack].pack()
        stack = list(self.game.settings.set_tools)[0]
        self.Joueur2[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur2[stack].pack()

        self.nom_Joueur3 = tk.Label(self.frame_joueur, text=str(self.game.players_in_order[2]), fg='red')
        self.nom_Joueur3.pack()
        self.Joueur3 = dict()
        for stack in self.game.current_player.get_resources():
            self.Joueur3[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
            self.Joueur3[stack].pack()
        stack = game.settings.food
        self.Joueur3[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur3[stack].pack()
        stack = game.settings.meeple
        self.Joueur3[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur3[stack].pack()
        stack = game.settings.food_production
        self.Joueur3[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur3[stack].pack()
        stack = list(self.game.settings.set_tools)[0]
        self.Joueur3[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur3[stack].pack()

        self.nom_Joueur4 = tk.Label(self.frame_joueur, text=str(self.game.players_in_order[3]), fg='red')
        self.nom_Joueur4.pack()
        self.Joueur4 = dict()
        for stack in self.game.current_player.get_resources():
            self.Joueur4[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
            self.Joueur4[stack].pack()
        stack = game.settings.food
        self.Joueur4[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur4[stack].pack()
        stack = game.settings.meeple
        self.Joueur4[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur4[stack].pack()
        stack = game.settings.food_production
        self.Joueur4[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur4[stack].pack()
        stack = list(self.game.settings.set_tools)[0]
        self.Joueur4[stack] = tk.Label(self.frame_joueur, text=str(stack) + ' : ' + str(self.game.current_player.stacks[stack]))
        self.Joueur4[stack].pack()

        self.frame_joueur.pack(side=tk.RIGHT)

        self.frame_bottom = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.button_hunting = tk.Button(self.frame_plateau, text='hunting Ground',
                                        command=lambda: self.addMeepleHunting(self.hunting_ground, game.current_player, 1))
        self.button_hunting.pack(side=tk.LEFT)

        self.map_button_place[self.button_hunting] = game.game_board.get_place('Hunt')

        self.frame_bottom = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.button_toolMaker = tk.Button(self.frame_plateau, text='Tool Maker',
                                          command=lambda: self.addMeepleToolMaker(self.toolMaker, game.current_player, 1))
        self.button_toolMaker.pack(side=tk.LEFT)

        self.map_button_place[self.button_toolMaker] = game.game_board.get_place('Tool maker')

        self.frame_bottom = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.button_hut = tk.Button(self.frame_plateau, text='Hut',
                                    command=lambda: self.addMeepleHut(self.hut, game.current_player, 2))
        self.button_hut.pack(side=tk.LEFT)

        self.map_button_place[self.button_hut] = game.game_board.get_place('Hut')

        self.frame_bottom = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.button_field = tk.Button(self.frame_plateau, text='Field',
                                      command=lambda: self.addMeepleField(self.field, game.current_player, 1))
        self.button_field.pack(side=tk.LEFT)

        self.map_button_place[self.button_field] = game.game_board.get_place('Field')

        self.button_forest = tk.Button(self.frame_plateau, text='FOREST',
                                       command=self.test)
        self.button_forest.pack(side=tk.LEFT)

        self.map_button_place[self.button_forest] = game.game_board.get_place('Forest')

        self.button_clay = tk.Button(self.frame_plateau, text='CLAY PIT',
                                     command=lambda: self.addMeepleClay_pit(self.clay_pit, game.current_player, 1))
        self.button_clay.pack(side=tk.LEFT)

        self.map_button_place[self.button_clay] = game.game_board.get_place('Clay pit')

        self.button_quarry = tk.Button(self.frame_plateau, text='QUARRY',
                                       command=lambda: self.addMeepleQuarry(self.quarry, game.current_player, 1))
        self.button_quarry.pack(side=tk.LEFT)

        self.map_button_place[self.button_quarry] = game.game_board.get_place('Quarry')

        self.button_river = tk.Button(self.frame_plateau, text='RIVER',
                                      command=lambda: self.addMeepleRiver(self.river, game.current_player, 1))
        self.button_river.pack(side=tk.LEFT)

        self.map_button_place[self.button_river] = game.game_board.get_place('River')

        self.button_reset = tk.Button(self.frame_plateau, text='RESET', command=self.deleteMeeple)
        self.button_reset.pack(side=tk.LEFT)

        self.quit = tk.Button(self.frame_plateau, text='QUIT', fg='red',
                              command=self.master.destroy)
        self.quit.pack(side=tk.RIGHT)

        self.next_turn = tk.Button(self.frame_plateau, text='Next Turn',
                                   command=self.next_turn)
        self.next_turn.pack(side=tk.RIGHT)

        self.frame_bottom.pack(side=tk.BOTTOM)

    def test(self):
        self.selected_place = self.game.game_board.get_place('Forest')
        print(self.selected_place)

    def clickMe(self, couleur):
        print(couleur)

    def set_image(self, lienNouvelleImage):
        img = ImageTk.PhotoImage(Image.open(lienNouvelleImage))
        return img

    def change_text(self, nouveauText):
        self.config(text=nouveauText)

    def trouverPlaceVide(self, Place):
        j = 0
        i = False
        while i != True and Place.__len__() > j:
            i = Place[j].videPlein
            j = j + 1
        if Place.__len__() > j and i:
            return j
        return 0

    def obtenirCouleur(self, color : str):
        if color == 'red':
            return 'GUI/Image/Meeples/meepleRed.png'
        elif color == 'green':
            return 'GUI/Image/Meeples/meepleGreen.png'
        elif color == 'blue':
            return 'GUI/Image/Meeples/meepleBlue.png'
        elif color == 'yellow':
            return 'GUI/Image/Meeples/meepleYellow.png'

    def addMeepleForest(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesf, self.set_image_meeplesf, player)
            self.forest[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('Forest')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_forest).get_place_left() <= self.nb_meeple:
            self.button_forest['state'] = 'disabled'

    def addMeepleRiver(self, tabPlace, player, nb_meeple):

        for i in range(0, nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesr, self.set_image_meeplesr, player)
            self.river[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('River')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_river).get_place_left() <= self.nb_meeple:
            self.button_river['state'] = 'disabled'

    def addMeepleQuarry(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesq, self.set_image_meeplesq, player)
            self.quarry[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('Quarry')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_quarry).get_place_left() <= self.nb_meeple:
            self.button_quarry['state'] = 'disabled'

    def addMeepleClay_pit(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesc, self.set_image_meeplesc, player)
            self.clay_pit[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('Clay pit')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_clay).get_place_left() <= self.nb_meeple:
            self.button_clay['state'] = 'disabled'

    def addMeepleHut(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesh, self.set_image_meeplesh, player)
            self.hut[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 2
        self.selected_place = self.game.game_board.get_place('Hut')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_hut).get_place_left() <= self.nb_meeple:
            self.button_hut['state'] = 'disabled'

    def addMeepleField(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplesn, self.set_image_meeplesn, player)
            self.field[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('Field')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_field).get_place_left() <= self.nb_meeple:
            self.button_field['state'] = 'disabled'

    def create_frame(self, tabPlace, set_frame: Set, set_image: Set, player):
        meeple = self.obtenirCouleur(player.color)

        coordX = tabPlace[self.trouverPlaceVide(tabPlace) - 1].x
        coordY = tabPlace[self.trouverPlaceVide(tabPlace) - 1].y

        frame_meeples = tk.Frame(self.frame_plateau)
        self.canvast = tk.Canvas(frame_meeples, height=23, width=16)
        image_meeplest = ImageTk.PhotoImage(Image.open(meeple))
        self.canvast.create_image(0, 0, anchor=tk.NW, image=image_meeplest)
        self.canvast.pack()
        frame_meeples.place(relx=coordX, rely=coordY, anchor='center')
        set_frame.add(frame_meeples)
        set_image.add(image_meeplest)


    def addMeepleToolMaker(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace, self.set_frame_meeplest, self.set_image_meeplest, player)
            self.toolMaker[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_hunting['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1
        self.selected_place = self.game.game_board.get_place('Tool maker')

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_toolMaker).get_place_left() <= self.nb_meeple:
            self.button_toolMaker['state'] = 'disabled'

    def addMeepleHunting(self, tabPlace, player, nb_meeple):
        for i in range(0,nb_meeple):
            self.create_frame(tabPlace,self.set_frame_meepleshunt, self.set_image_meepleshunt, player)
            self.hunting_ground[self.trouverPlaceVide(tabPlace) - 1].videPlein = False

        self.button_toolMaker['state'] = 'disabled'
        self.button_hut['state'] = 'disabled'
        self.button_field['state'] = 'disabled'
        self.button_clay['state'] = 'disabled'
        self.button_quarry['state'] = 'disabled'
        self.button_river['state'] = 'disabled'
        self.button_forest['state'] = 'disabled'

        self.nb_meeple += 1

        if self.game.current_player.get_farmable_count(self.game.settings.meeple) <= self.game.game_board.get_nb_meeple_in_board(self.game.current_player) + self.nb_meeple \
                or self.map_button_place.get(self.button_hunting).get_place_left() <= self.nb_meeple:
            self.button_hunting['state'] = 'disabled'

    def setAction(self):
        self.config(text='')

    def setText(self, Objet_a_mofif, NouveauText):
        Objet_a_mofif.config(text=NouveauText)

    def deleteMeeple(self):
        # Destruction of Meeples in River
        self.destroy_set(self.set_frame_meeplesr, self.set_image_meeplesr)

        # Destruction of Meeples in Forest
        self.destroy_set(self.set_frame_meeplesf, self.set_image_meeplesf)

        # Destruction of Meeples in Quarry
        self.destroy_set(self.set_frame_meeplesq, self.set_image_meeplesq)

        # Destruction of Meeples in Clay
        self.destroy_set(self.set_frame_meeplesc, self.set_image_meeplesc)

        # Destruction of Meeples in Clay
        self.destroy_set(self.set_frame_meeplesh, self.set_image_meeplesh)

        # Destruction of Meeples in Hunt
        self.destroy_set(self.set_frame_meepleshunt, self.set_image_meepleshunt)

        self.destroy_set(self.set_frame_meeplesn, self.set_image_meeplesn)

        self.destroy_set(self.set_frame_meeplest, self.set_image_meeplest)

        self.reactive_location(self.hut)
        self.reactive_location(self.clay_pit)
        self.reactive_location(self.quarry)
        self.reactive_location(self.hunting_ground)
        self.reactive_location(self.river)
        self.reactive_location(self.forest)
        self.reactive_location(self.field)
        self.reactive_location(self.toolMaker)

    def destroy_set(self, set_frame: Set, set_image: Set):
        for frame in set_frame:
            frame.destroy()
        set_image.clear()
        set_frame.clear()  

    def reactive_location(self, list: List):
        for element in list:
            element.videPlein = True

    def afficherVide(self, table):
        print(table[self.trouverPlaceVide(table) - 1].nom)
        self.forest[self.trouverPlaceVide(table) - 1].videPlein = False

    def next_turn(self):
        if self.selected_place is not None:
            self.game.place_meeple(self.selected_place, self.nb_meeple)
            self.game.current_player.add_to_farmable_count(self.game.settings.meeple, -self.nb_meeple)

        self.game.play_IA()

        self.button_hunting['state'] = 'normal'
        self.button_toolMaker['state'] = 'normal'
        self.button_hut['state'] = 'normal'
        self.button_field['state'] = 'normal'
        self.button_clay['state'] = 'normal'
        self.button_quarry['state'] = 'normal'
        self.button_river['state'] = 'normal'
        self.button_forest['state'] = 'normal'

    def place_methode(self):
        if self.selected_place is None:
            return (None, None)
        return self.selected_place, 2

    def update(self, data=None):
        self.deleteMeeple()
        self.reactive_location(self.hut)
        self.reactive_location(self.clay_pit)
        self.reactive_location(self.quarry)
        self.reactive_location(self.hunting_ground)
        self.reactive_location(self.river)
        self.reactive_location(self.forest)
        self.reactive_location(self.field)
        self.reactive_location(self.toolMaker)

        for place in self.game.game_board.places:
            for player in place.meeples:
                if place.name == 'Forest':
                    self.addMeepleForest(self.forest, player, place.meeples.get(player))
                if place.name == 'Hut':
                    self.addMeepleHut(self.hut, player, place.meeples.get(player))
                if place.name == 'Clay pit':
                    self.addMeepleClay_pit(self.clay_pit, player, place.meeples.get(player))
                if place.name == 'Hunt':
                    self.addMeepleHunting(self.hunting_ground, player, place.meeples.get(player))
                if place.name == 'River':
                    self.addMeepleRiver(self.river, player, place.meeples.get(player))
                if place.name == 'Field':
                    self.addMeepleField(self.field, player, place.meeples.get(player))
                if place.name == 'Tool maker':
                    self.addMeepleToolMaker(self.toolMaker, player, place.meeples.get(player))
                if place.name == 'Quarry':
                    self.addMeepleQuarry(self.quarry, player, place.meeples.get(player))

        self.nb_meeple = 0
        self.selected_place = None
