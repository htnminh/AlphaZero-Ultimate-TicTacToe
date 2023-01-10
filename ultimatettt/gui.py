import PySimpleGUI as sg
import numpy as np
import pprint

from game import Utils, State
from exceptions import GameException


X_CHAR = '\u274C'
O_CHAR = '\u26AB'
X_COLOR = 'red'
O_COLOR = 'blue'
BACKGROUND_COLOR = 'white'
X_WON_BACKGROUND_COLOR = 'lightpink'
O_WON_BACKGROUND_COLOR = 'skyblue' # cornflowerblue
WIDTH = 3
FONT_SIZE = 25
NEXTG_COLOR = 'lightgreen'
X_TURN_STR = 'Player 1 turn as X'
O_TURN_STR = 'Player 2 turn as O'
PAD = 12


class GraphicInterface():
    def __init__(self):
        self.state = State()
        self.layout = self.create_layout()
        self.window = self.create_window('Ultimate Tic-Tac-Toe')
        self.event_loop()

    def create_layout(self):
        layout = [[[[None for j in range(3)] for i in range(3)] for y in range(3)] for x in range(3)]
        
        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        layout[x][y][i][j] = sg.Button(
                            '',
                            size=WIDTH,
                            font=f'None {FONT_SIZE}',
                            key=f'cell{x}{y}{i}{j}',
                            button_color=(None, BACKGROUND_COLOR)
                        )
                layout[x][y] = sg.Frame('', layout[x][y], pad=PAD, border_width=0)
        
        layout.append([sg.Text(X_TURN_STR, key='textPlayerTurn')])
        layout.append([sg.Text('', key='textException')])

        layout.insert(0, [sg.Button('New game'), sg.Button('Exit')])
        # a temporary fix for a bug where the first button of a layout is highlighted
        # no matter what button the user clicks
        layout.insert(0, [sg.Frame('', [[sg.Button()]], visible=False)])

        return layout

    def create_window(self, window_name):
        return sg.Window(window_name, self.layout)

    def update_button_color(self, xyij, text_color, bkg_color):
        x, y, i, j = xyij
        self.window[f'cell{x}{y}{i}{j}'].update(
            button_color=(text_color, bkg_color))
        
    def update_button_text(self, xyij, text):
        x, y, i, j = xyij
        self.window[f'cell{x}{y}{i}{j}'].update(text)

    def update_area_color(self, xy, text_color, bkg_color):
        x, y = xy
        for i in range(3):
            for j in range(3):
                self.update_button_color(
                    (x, y, i, j),
                    text_color,
                    bkg_color
                )

    def play(self, xyij):
        x, y, i, j = xyij 

        try:
            self.state.play((x, y, i, j))

            # update played cell
            self.update_button_text(
                xyij, X_CHAR if self.state.next_player==2 else O_CHAR)
            self.update_button_color(
                xyij, X_COLOR if self.state.next_player==2 else O_COLOR, None)
            # change color of played area to default or win color
            state_of_area = self.state.area[x, y]
            if state_of_area == 0:
                self.update_area_color((x, y), None, BACKGROUND_COLOR)
            else:
                bkg_color_won = X_WON_BACKGROUND_COLOR if state_of_area == 1 else O_WON_BACKGROUND_COLOR
                self.update_area_color((x, y), None, bkg_color_won)
            # change next area color
            if self.state.next_area is not None:
                self.update_area_color(self.state.next_area, None, NEXTG_COLOR)
            # update texts
            self.window['textPlayerTurn'].update(X_TURN_STR if self.state.next_player==1 else O_TURN_STR)
            self.window['textException'].update('')
            
        except GameException as e:
            self.window['textException'].update(e)

    def event_loop(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                self.window.close()
                break
            elif event == 'New game':
                self.window.close()
                self.__init__()
            elif event.startswith('cell'):
                xyij = tuple(map(int, event[-4:]))
                self.play(xyij)


if __name__ == '__main__':
    GraphicInterface()