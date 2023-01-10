import PySimpleGUI as sg
import numpy as np

from game import Utils, State
from exceptions import \
    BoardWonException, AreaWonException, AreaWrongException, CellPlayedException


X_CHAR = '\u274C'
O_CHAR = '\u26AB'
X_COLOR = 'red'
O_COLOR = 'blue'
BACKGROUND_COLORS = ('darkgrey', 'white')
WIDTH = 3
FONT_SIZE = 25
NEXTG_COLOR = 'lightgreen'


class GraphicInterface():
    def __init__(self):
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
        
        layout.append([sg.Text('',key='text')])
        
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

    def event_loop(self):
        state = State()

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event.startswith('cell'):
                x, y, i, j = xyij = tuple(map(int, event[-4:]))

                try:
                    state.play((x, y, i, j))
                    self.update_button_text(
                        xyij, X_CHAR if state.next_player==2 else O_CHAR)
                    self.update_button_color(
                        xyij, X_COLOR if state.next_player==2 else O_COLOR, None)
                    self.update_area_color((x, y), None, *BACKGROUND_COLORS)
                    if state.next_area is not None:
                        self.update_area_color(state.next_area, None, NEXTG_COLOR, NEXTG_COLOR)
                    
                    # TODO
                    print(state)
                except (BoardWonException, AreaWonException, AreaWrongException, CellPlayedException) as e:
                    print(e)  # TODO

        self.window.close()


if __name__ == '__main__':
    GraphicInterface()