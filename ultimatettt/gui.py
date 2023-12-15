import webbrowser

import PySimpleGUI as sg
import numpy as np

from original_game import LogicUtils, OriginalGame
from implemented_Game import ImplementationUtils, ImplementedGame
from implemented_NeuralNet import NNetWrapper
from MCTS import MCTS
from exceptions import GameException
from main import args


MODEL_FOLDER = 'model ver22'
MODEL_FILENAME = 'best.pth.tar'

X_CHAR = '\u274C'
O_CHAR = '\u26AB'
X_COLOR = 'red'
O_COLOR = 'blue'
BACKGROUND_COLOR = 'white'
X_WON_BACKGROUND_COLOR = 'lightpink'
O_WON_BACKGROUND_COLOR = 'skyblue'
DRAW_BACKGROUND_COLOR = 'darkgrey'
WIDTH = 3
FONT_SIZE = 22
NEXT_AREA_COLOR = 'lightgreen'
X_TURN_STR = 'Player 1 turn as X'
O_TURN_STR = 'Player 2 turn as O'
DEFAULT_TEXT_EXCEPTION = 'None'
PAD = 11

PROJECT_NAME = 'An AlphaZero Implementation of Ultimate Tic-Tac-Toe'
PROJECT_TEXT = \
"""Hoang Tran Nhat Minh\t\t\tData Science and Artificial Intelligence - K65
Project 1 of Semester 2022.1\t\tHanoi University of Science and Technology
Instructed by Dr. Tran Nguyen Ngoc\t\tSchool of Information and Communication Technology"""


class GraphicInterface():
    def __init__(self, mode='Human vs AI',
                 start_window=True, start_event_loop=True,
                 full_gui=True, theme='DarkGrey6', debug_printing=False):
        
        sg.theme(theme)
        self.mode = mode
        # if set full_gui to False, shows a simpler GUI for report
        self.full_gui = full_gui
        self.debug_printing = debug_printing

        self.original_game = OriginalGame()
        self.layout = self.create_layout()
        
        if start_window:
            self.window = self.create_window('Ultimate Tic-Tac-Toe')

        if start_event_loop:
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
        
        layout.append([
            sg.Frame('Turn', [[
                sg.Text(X_TURN_STR, key='textPlayerTurn', visible=self.full_gui, size=25)]], visible=self.full_gui),
            sg.Frame('Information', [[
                sg.Text(DEFAULT_TEXT_EXCEPTION, key='textException', visible=self.full_gui, size=53)]], visible=self.full_gui)
        ])

        layout.insert(0,
            [
                sg.Frame('', [[
                sg.Button('Human vs Human', visible=self.full_gui, focus=self.mode=='Human vs Human'),
                sg.Button('Human vs AI', visible=self.full_gui, focus=self.mode=='Human vs AI'),
                sg.Button('AI vs Human', visible=self.full_gui, focus=self.mode=='AI vs Human'),
                sg.Button('AI vs AI', visible=self.full_gui, focus=self.mode=='AI vs AI'),
                sg.Button('Open GitHub repository...', visible=self.full_gui),
                sg.Button('Exit', visible=self.full_gui),
            ]], border_width=0, element_justification='center', size=(670, 30)
        , visible=self.full_gui)])
        # a temporary fix for a bug where the first button of a layout is highlighted
        # no matter what button the user clicks
        layout.insert(0, [sg.Frame('', [[sg.Button()]], visible=False)])

        layout.insert(0, [
            sg.Frame(
                PROJECT_NAME, [[sg.Text(PROJECT_TEXT, visible=self.full_gui, size=(82, 3))]],
                title_location='n', visible=self.full_gui)
        ])

        return layout

    def create_window(self, window_name):
        return sg.Window(window_name, self.layout, finalize=True)

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
    
    def update_all_areas_colors(self):
        for x in range(3):
            for y in range(3):
                state_of_area = self.original_game.area[x, y]
                if state_of_area == 0:
                    self.update_area_color((x, y), None, BACKGROUND_COLOR)
                elif np.isnan(state_of_area):
                    self.update_area_color((x, y), None, DRAW_BACKGROUND_COLOR)
                else:
                    bkg_color_won = X_WON_BACKGROUND_COLOR if state_of_area == 1 else O_WON_BACKGROUND_COLOR
                    self.update_area_color((x, y), None, bkg_color_won)

        # change next area color
        if self.original_game.curr_area is not None:
            self.update_area_color(self.original_game.curr_area, None, NEXT_AREA_COLOR)
        else:
            for x in range(3):
                for y in range(3):
                    state_of_area = self.original_game.area[x, y]
                    if state_of_area == 0:
                        self.update_area_color((x, y), None, NEXT_AREA_COLOR)

    def play(self, xyij, update_window_elements=True):
        x, y, i, j = xyij 
        self.original_game.execute_move((x, y, i, j))

        if self.debug_printing:
            cell_state = self.original_game.cell_state
            print(ImplementationUtils().cell_state_4d_to_2d(cell_state).astype('int'))
            print(ImplementationUtils().cell_state_4d_to_2d(
                self.original_game._get_valid_moves(cell_state, self.original_game.curr_player, self.original_game.curr_area)).astype('int')
            )
            print()

        if update_window_elements:
            # update played cell
            self.update_button_text(
                xyij, X_CHAR if self.original_game.curr_player==-1 else O_CHAR)
            self.update_button_color(
                xyij, X_COLOR if self.original_game.curr_player==-1 else O_COLOR, None)
            self.update_all_areas_colors()
            # update texts
            self.window['textPlayerTurn'].update(X_TURN_STR if self.original_game.curr_player==1 else O_TURN_STR)
            self.window['textException'].update(DEFAULT_TEXT_EXCEPTION)
            

    def event_loop(self):
        # for AI only
        game = ImplementedGame()
        net = NNetWrapper(game)
        net.load_checkpoint(MODEL_FOLDER, MODEL_FILENAME)
        mtcs = MCTS(game=game, nnet=net, args=args)
        human_valid_move = True

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Exit':
                self.window.close()
                break

            elif event == 'Open GitHub repository...':
                webbrowser.open(r'https://github.com/htnminh/AlphaZero-Ultimate-TicTacToe')

            elif event == 'Human vs Human':
                self.window.close()
                self.__init__(mode='Human vs Human')

            elif event == 'Human vs AI':
                self.window.close()
                self.__init__(mode='Human vs AI')
            
            elif event == 'AI vs Human':
                self.window.close()
                self.__init__(mode='AI vs Human', start_event_loop=False)

                state = ImplementationUtils().cell_state_4d_to_2d(self.original_game.cell_state)
                if game.getGameEnded(state, 1, self.original_game.curr_area) == 0:
                    action = np.argmax(mtcs.getActionProb(
                        *game.getCanonicalForm(state, 1, self.original_game.curr_area),
                        temp=0
                    ))
                    self.play(LogicUtils().k_to_xyij(action))
                    
                self.event_loop()

            elif event == 'AI vs AI':
                self.window.close()
                self.__init__(mode='AI vs AI', start_window=True, start_event_loop=False)
                
                while True:
                    state = ImplementationUtils().cell_state_4d_to_2d(self.original_game.cell_state)
                    if game.getGameEnded(state, 1, self.original_game.curr_area) == 0:
                        action = np.argmax(mtcs.getActionProb(
                            *game.getCanonicalForm(state, 1, self.original_game.curr_area),
                            temp=0
                        ))
                        self.play(LogicUtils().k_to_xyij(action), update_window_elements=True)
                        self.window.refresh()
                    else:
                        try:
                            self.play((0,0,0,0))
                        except GameException as e:
                            self.window['textException'].update(e)
                        break

                    state = ImplementationUtils().cell_state_4d_to_2d(self.original_game.cell_state)
                    if game.getGameEnded(state, -1, self.original_game.curr_area) == 0:
                        action = np.argmax(mtcs.getActionProb(
                            *game.getCanonicalForm(state, -1, self.original_game.curr_area),
                            temp=0
                        ))
                        self.play(LogicUtils().k_to_xyij(action), update_window_elements=True)
                        self.window.refresh()
                    else:
                        try:
                            self.play((0,0,0,0))
                        except GameException as e:
                            self.window['textException'].update(e)
                        break

                self.event_loop()
                
            if self.mode == 'Human vs Human':
                if event.startswith('cell'):
                    xyij = tuple(map(int, event[-4:]))
                    try:
                        self.play(xyij)
                    except GameException as e:
                        self.window['textException'].update(e)

            elif self.mode == 'Human vs AI':
                
                if event.startswith('cell'):
                    xyij = tuple(map(int, event[-4:]))
                    try:
                        self.play(xyij)
                        human_valid_move = True
                    except GameException as e:
                        self.window['textException'].update(e)
                        human_valid_move = False
                    
                    if human_valid_move:
                        state = ImplementationUtils().cell_state_4d_to_2d(self.original_game.cell_state)
                        if game.getGameEnded(state, -1, self.original_game.curr_area) == 0:
                            action = np.argmax(mtcs.getActionProb(
                                *game.getCanonicalForm(state, -1, self.original_game.curr_area),
                                temp=0
                            ))
                            self.play(LogicUtils().k_to_xyij(action))
                        else:
                            try:
                                self.play((0,0,0,0))
                            except GameException as e:
                                self.window['textException'].update(e)
            
            elif self.mode == 'AI vs Human':
                
                if event.startswith('cell'):
                    xyij = tuple(map(int, event[-4:]))
                    try:
                        self.play(xyij)
                        human_valid_move = True
                    except GameException as e:
                        self.window['textException'].update(e)
                        human_valid_move = False
                    
                    if human_valid_move:
                        state = ImplementationUtils().cell_state_4d_to_2d(self.original_game.cell_state)
                        if game.getGameEnded(state, 1, self.original_game.curr_area) == 0:
                            action = np.argmax(mtcs.getActionProb(
                                *game.getCanonicalForm(state, 1, self.original_game.curr_area),
                                temp=0
                            ))
                            self.play(LogicUtils().k_to_xyij(action))
            
            elif self.mode == 'AI vs AI':

                if event.startswith('cell'):
                    xyij = tuple(map(int, event[-4:]))
                    try:
                        self.play(xyij)
                        human_valid_move = True
                    except GameException as e:
                        self.window['textException'].update(e)
            

if __name__ == '__main__':
    GraphicInterface()