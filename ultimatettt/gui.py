import PySimpleGUI as sg
import numpy as np

from game import Utils, State
from exceptions import GameException


X_CHAR = '\u274C'
O_CHAR = '\u26AB'
X_COLOR = 'red'
O_COLOR = 'blue'
BACKGROUND_COLORS = ('darkgrey', 'white')
X_WON_BACKGROUND_COLOR = 'lightcoral'
O_WON_BACKGROUND_COLOR = 'cornflowerblue'
WIDTH = 3
FONT_SIZE = 25
NEXTG_COLOR = 'lightgreen'
X_TURN_STR = 'Player 1 turn as X'
O_TURN_STR = 'Player 2 turn as O'


class GraphicInterface():
    def __init__(self):
        self.state = State()
        self.layout = self.create_layout()
        self.window = self.create_window('Ultimate Tic-Tac-Toe')
        self.event_loop()

    def create_layout(self):
        layout = [[None for n in range(9)] for m in range(9)]

        for m in range(9):
            for n in range(9):
                x, y, i, j = Utils().mn_to_xyij((m, n))
                layout[m][n] = sg.Button(
                    '',
                    size=WIDTH,
                    font=f'None {FONT_SIZE}',
                    key=f'cell{x}{y}{i}{j}',
                    button_color=(
                        None, BACKGROUND_COLORS[0] if (x+y)%2 \
                            else BACKGROUND_COLORS[1]
                    )
                )
        
        layout.append([sg.Text(X_TURN_STR, key='textPlayerTurn')])
        layout.append([sg.Text('', key='textException')])
        
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

    def update_area_color(self, xy, text_color, color_if_odd, color_if_even):
        x, y = xy
        for i in range(3):
            for j in range(3):
                self.update_button_color(
                    (x, y, i, j),
                    text_color,
                    color_if_odd if (x+y)%2 else color_if_even
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
                self.update_area_color((x, y), None, *BACKGROUND_COLORS)
            else:
                bkg_color_won = [X_WON_BACKGROUND_COLOR] * 2 if state_of_area == 1 else [O_WON_BACKGROUND_COLOR] * 2
                self.update_area_color((x, y), None, *bkg_color_won)
            # change next area color
            if self.state.next_area is not None:
                self.update_area_color(self.state.next_area, None, NEXTG_COLOR, NEXTG_COLOR)
            # update texts
            self.window['textPlayerTurn'].update(X_TURN_STR if self.state.next_player==1 else O_TURN_STR)
            self.window['textException'].update('')
            
        except GameException as e:
            self.window['textException'].update(e)

    def event_loop(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event.startswith('cell'):
                xyij = tuple(map(int, event[-4:]))
                self.play(xyij)

        self.window.close()


if __name__ == '__main__':
    GraphicInterface()