import webbrowser
from tkinter import *


class Interface(Frame):
    """Main window.
    All the widgets are stocked as attributs of the window"""

    def __init__(self, window, colorList):
        window.protocol("WM_DELETE_WINDOW", quit)
        Frame.__init__(self, window)
        self.color_selected = None
        self.pack(fill=BOTH)

        self.message = Label(self, text='Menu Stone Age v0.1')
        self.message.pack(side='top')

        self.button_play = Button(self, text='Jouer', fg='blue', command=self.meeple)
        self.button_play.pack(side='top', padx='0', pady='0')

        self.button_quit = Button(self, text='Quitter', fg='red', command=self.quit)
        self.button_quit.pack(side='right')

        self.button_rules = Button(self, text='Règles du jeu', fg='green', command=self.webopen)
        self.button_rules.pack(side='right')

        self.button_credits = Button(self, text='Crédits', fg='purple', command=self.credits)
        self.button_credits.pack(side='left')

        self.button_return = Button(self, text='Retour', command=self.forget)
        self.button_return.pack(side='left')

        self.textcredits = Label(self, text='Rémi Domingue, Lucas Besse, Kiady Raveloson, Simon Chaval, '
                                            'Therry Soulié, Tom Lacombe, Bastien Benard')

        self.meeple = Listbox(window)

        self.askmeeple = Label(self, text='Choisir une couleur de meeple :', padx='30', pady='10')
        for i in range(len(colorList)):
            self.meeple.insert(i, colorList[i])

    def forget(self):
        self.textcredits.pack_forget()
        self.meeple.pack_forget()
        self.meeple.selection_clear('active')
        self.askmeeple.pack_forget()

    def webopen(self):
        webbrowser.open('./GUI/Rules.pdf')

    def credits(self):
        self.textcredits.pack(padx='30', pady='30')

    def meeple(self):
        if not self.meeple.curselection():
            self.askmeeple.pack(side='bottom')
            self.meeple.pack()
        else:
            self.color_selected = self.meeple.get(self.meeple.curselection())
            self.quit()
