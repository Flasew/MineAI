import sys
import os
import numpy as np
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Lock

from MinesweeperGame import *

# PIC Const
IMG_BORDER = {'tb': 'resources/images_16/bordertb.gif',
              'lr': 'resources/images_16/borderlr.gif', 
              'tlc': 'resources/images_16/bordertl.gif', 
              'trc': 'resources/images_16/bordertr.gif', 
              'blc': 'resources/images_16/borderbl.gif', 
              'brc': 'resources/images_16/borderbr.gif', 
              'jointl': 'resources/images_16/borderjointl.gif',
              'jointr': 'resources/images_16/borderjointr.gif'}

IMG_REV_GRID = {0: 'resources/images_16/open0.gif', 
                1: 'resources/images_16/open1.gif', 
                2: 'resources/images_16/open2.gif', 
                3: 'resources/images_16/open3.gif', 
                4: 'resources/images_16/open4.gif', 
                5: 'resources/images_16/open5.gif', 
                6: 'resources/images_16/open6.gif', 
                7: 'resources/images_16/open7.gif', 
                8: 'resources/images_16/open8.gif'}

IMG_HID_GRID ={'blank': 'resources/images_16/blank.gif', 
               'bdeath': 'resources/images_16/bombdeath.gif', 
               'bflag': 'resources/images_16/bombflagged.gif', 
               'bmflag': 'resources/images_16/bombmisflagged.gif', 
               'breveal': 'resources/images_16/bombrevealed.gif'}

class MinesweeperGUI(QMainWindow):

    _BACKGROUND = """
QMainWindow{
background-color: 0xC0C0C0;
}
"""

    def __init__(delf, difficulty):
        super(MinesweeperGUI, self).__init__()
        self.difficulty = difficulty
        self.mGame = None
        self.finished = False

        self.initUI()

    def initUI(self):
        self.init_menu()
        self.init_border()
        self.init_pic()
        
        self.setWindowTitle('Minesweeper')
        self.setFixedSize(self.difficulty['width'] * 16 + 20,
                          self.difficulty['height'] * 16 + 83)

        self.setStyleSheet(self._BACKGROUND)

        self.board = Board(self)
        # self.face = Face(self)
        # self.time_counter = Timecounter(self)
        # self.mine_counter = Minecounter(self)

        self.show()

    def init_menu(self):
        newGame = QAction('&New Game', self, 
            triggered=lambda: self.new_game(self.difficulty))
        newGame.setShortcut('F2')

        exit = QAction('&Exit', self, triggered=qApp.quit)
        exit.setShortcut('Alt+F4')

        beginner = QAction('&Beginner', 
            self, triggered=lambda: self.new_game(DIFF_BEGINNER))
        begAct.setShortcut('1')

        intermed = QAction('&Intermediate', 
            self, triggered=lambda: self.new_game(DIFF_INTERMED))
        intermed.setShortcut('2')

        expert = QAction('&Expert', 
            self, triggered=lambda: self.new_game(DIFF_EXPERT))
        expert.setShortcut('3')

        menubar = self.menuBar()
        gameMenu = menubar.addMenu('&Game')
        gameMenu.addAction(newGame)
        gameMenu.addSeparator()
        gameMenu.addAction(beginner)
        gameMenu.addAction(intermed)
        gameMenu.addAction(expert)
        gameMenu.addSeparator()
        gameMenu.addAction(exit)

    def init_border(self):
        self.setCentralWidget(QWidget(self))

        def place_Qlabel(image, x, y, w, h):
            label = QLabel(self.centralWidget())
            label.setPixmap(image)
            label.setGeometry(x, y, w, h)

        place_QLabel(IMG_BORDER['tlc'], 0, 0, 10, 10)
        place_QLabel(IMG_BORDER['blc'], 0, 52+self.difficulty['height']*16, 10, 10)
        place_QLabel(IMG_BORDER['trc'], 10+16*self.difficulty['width'], 0, 10, 10)
        place_QLabel(IMG_BORDER['brc'], 
            10+16*self.difficulty['width'], 52+self.difficulty['height']*16, 10, 10)

        # top and bottom
        image = IMG_BORDER['tb']
        for i in range(self.difficulty['width']*4):
            place_QLabel(image, 10+4*i, 0, 4, 10)
            place_QLabel(image, 10+4*i, 52+self.difficulty['height']*16, 4, 10)

        #left and right
        image = IMG_BORDER['lr']
        for i in range(8):
            place_QLabel(image, 0, 10 + 4 * i, 10, 4)
            place_QLabel(image, 10+16*self.difficulty['width'], 10+4*i, 10, 4)
        for i in range(self.difficulty['height'] * 4):
            place_QLabel(image, 0, 52+4*i, 10, 4)
            place_QLabel(image, 10+16*self.difficulty['width'], 52+4*i, 10, 4)
            place_QLabel(IMG_BORDER['tb'], 10+4*i, 42, 4, 10)

        # joints
        place_QLabel(IMG_BORDER['jointl'], 0, 42, 10, 10)
        place_QLabel(IMG_BORDER['jointr'], 
            10+16*self.difficulty['width'], 42, 10, 10)

    def init_pic(self):
        for pic in IMG_BORDER:
            IMG_BORDER[pic] = QPixmap(IMG_BORDER[pic])

        for pic in IMG_HID_GRID:
            IMG_HID_GRID[pic] = QPixmap(IMG_HID_GRID[pic])

        for pic in IMG_REV_GRID:
            IMG_REV_GRID[pic] = QPixmap(IMG_REV_GRID[pic])

    def new_game(self, difficulty):
        if self.difficulty == difficulty:
            self.board.reset()

        else:
            self.Board.setParent(None)
            # self.Face.setParent(None)
            # self.time_counter.setParent(None)
            # self.mine_counter.setParent(None)

            self.difficulty = difficulty
            self.setFixedSize(self.difficulty['width'] * 16 + 20,
                      self.difficulty['height'] * 16 + 62 + self.menuWidget().height())
            self.init_border()
            
            self.board = Board(self)
            # self.face = Face(self)
            # self.time_counter = Timecounter(self)
            # self.mine_counter = Minecounter(self)

        
class Grid(QLabel):
    def __init__(self, parrent):
        super.__init__(parrent)
        self.mine_state = HIDDEN

class Board(QWidget):

    def __init__(self, game):
        super.__init__(game.centralWidget())

        self.game = game

        self.setGeometry(10, 52, 
            self.game.difficulty['width']*16, self.game.difficulty['height']*16)
        self.setMouseTracking(True)

        self.l = False
        self.r = False

        self.flagged = []

        self.prev = [-1, -1]
        self.rl_lock = Lock()

        self.mousePressEvent = self.mouse_pressed
        self.mouseMoveEvent = self.mouse_moved
        self.mouseReleaseEvent = self.mouse_released

        # init grid
        self.grids = []
        for row in range(self.game.difficulty['height']):
            self.grids.append([])
            for col in range(self.game.difficulty['width']):
                grid = Grid(self)
                grid.setPixmap(IMG_HID_GRID['blank'])
                self.grids[row].append(grid)

    def reset(self):
        for grid_rows in self.grids:
            for grid in grid_rows:
                if grid.mine_state != HIDDEN:
                    grid.mine_state = HIDDEN
                    grid.setPixmap(IMG_HID_GRID['blank'])

    def l_press(self, row, col):
        if self.grids[row][col].mine_state == HIDDEN:
            self.grids[row][col].setPixmap(IMG_REV_GRID[0])

    def l_release(self, row, col):
        # start new game if is first click
        if self.game.mgame == None:
            self.game.mgame = mgame(self.game.difficulty, row, col)
            for pos in self.flagged:
                self.game.mgame.flag(pos[0], pos[1])
        changed_grids = self.game.mgame.click(row, col)
        if self.game.mgame.finished():
            self.game.finished = True
            print(self.game.mgame.get_time())
            self.update_all_grids()
        else:
            self.update(changed_grids)

    def r_press(self, row, col):
        changed_grid = []
        cur_grid = self.grids[row][col]
            if cur_grid.mine_state != OPEN:
                if self.game.mgame: 
                    changed_grid = self.game.mgame.flag(row, col)
                    self.update(changed_grid)
                else:
                    if cur_grid.mine_state == HIDDEN:
                        self.flagged.append((row, col))
                        cur_grid.mine_state = FLAGGED
                        cur_grid.show(IMG_HID_GRID['bflag'])
                    elif cur_grid.mine_state == FLAGGED:
                        try:
                            self.flagged.remove((cur_grid.row, cur_grid.col))
                            cur_grid.mine_state = HIDDEN
                            cur_grid.show(IMG_HID_GRID['blank'])
                        except:
                            pass

    def r_release(self, row, col):
        pass

    def m_press(self, row, col):
        nbh = self.neighbors(row, col)
        for i in nbh:
            if self.grids[i[0]][i[1]].mine_state == HIDDEN:
                self.grids[row][col].setPixmap(IMG_REV_GRID[0])


    def m_release(self, row, col):

        if self.game.mgame:
            changed_grids = self.game.mgame.chord(row, col)
            changed_grids.extand(self.neighbors(row, col))
            if self.game.mgame.finished():
                self.game.finished = True
                print(self.game.mgame.get_time())
                self.update_all_grids()
                
            else:
                self.update(changed_grids)

    def on_click(self, row, col):
        self.l_press(row, col)
        self.l_release(row, col)

    def on_flag(self, row, col):
        self.r_press(row, col)
        self.r_release(row, col)

    def on_chord(self, row, col):
        self.m_press(row, col)
        self.m_release(row, col)

    def mouse_pressed(self, e):

        if self.game.finished: 
            return 

        self.rl_lock.accquire()
        if event.button() == Qt.LeftButton:
            self.l = True
            if self.r:
                thisp = 'm'
            else:
                thisp = 'l'
        elif event.button() == Qt.RightButton:
            self.r = True
            if self.l:
                thisp = 'm'
            else:
                thisp = 'r'
        elif event.button == Qt.MiddleButton:
            thisp = 'm'

        self.rl_lock.release()

        x = event.x()
        y = event.y()

        if x < 0 or y < 0 or \
           x >= self.difficulty['width'] * 16 or y >= self.difficulty['height'] * 16:
            return

        row = y // 16
        col = x // 16
        self.prev_grid = grids[row,col]

        if thisp == 'l':
            self.l_press(row, col)
        elif thisp == 'r':
            self.r_press(row, col)
        elif thisp = 'm':
            self.m_press(row, col)

    def mouse_relased(self, e):
        if self.game.finished: 
            return 

        self.rl_lock.accquire()
        thisr = 'n'
        if event.button() == Qt.LeftButton:
            if self.l:
                self.l = False
                if self.r:
                    thisr = 'm'
                    self.r = False
                else:
                    thisr = 'l'
        elif event.button() == Qt.RightButton:
            if self.r:
                self.r = False
                if self.l:
                    thisr = 'm'
                    self.l = False
                else:
                    thisr = 'r'
        elif event.button() == Qt.MiddleButton():
            self.l = self.r = False
            thisr = 'm'
        self.rl_lock.release()

        x = event.x()
        y = event.y()

        if x < 0 or y < 0 or \
           x >= self.difficulty['width'] * 16 or y >= self.difficulty['height'] * 16:
            return

        row = y // 16
        col = x // 16

        if thisp == 'l':
            self.l_release(row, col)
        elif thisp == 'r':
            self.r_release(row, col)
        elif thisp == 'm':
            self.m_release(row, col)

    def mouse_move(self, e):
        if self.game.finished:
            return
        self.rl_lock.accquire()
        if self.l and self.r:
            thism = 'c'
        elif self.l:
            thism = 'l'
        elif self.r:
            thism = 'r'
        self.rl_lock.release()

        x = event.x()
        y = event.y()

        if x < 0 or y < 0 or \
           x >= self.difficulty['width'] * 16 or y >= self.difficulty['height'] * 16:
            return

        row = y // 16
        col = x // 16

        if row == self.prev_grid[0] and col == self.prev_grid[1]:
            return

        if thism == 'm':
            for points in self.neighbors(prev_grid[0], prev_grid[1]):
                if self.grids[points[0]][points[1]].mine_state == HIDDEN:
                    self.grids[points[0]][points[1]].setPixmap(IMG_HID_GRID['blank'])
            for points in self.neighbors(row, col):
                if self.grids[points[0]][points[1]].mine_state == HIDDEN:
                    self.grids[points[0]][points[1]].setPixmap(IMG_REV_GRID[0])

        elif thism == 'l':
            if self.grids[prev_grid[0]][prev_grid[1]].mine_state == HIDDEN:
                    self.grids[prev_grid[0]][prev_grid[1]].setPixmap(IMG_HID_GRID['blank'])
            if self.grids[row][col].mine_state == HIDDEN:
                self.grids[row][col].setPixmap(IMG_REV_GRID[0])

        self.prev_grid = [row, col]

    def update(self, changed_grids):
        """Update displayed board"""
        display_board = self.game.mgame.get_board()
        for grid in changed_grids:
            row = grid[0]
            col = grid[1]
            self.grids[row][col].mine_state = display_board[row][col]
            self.grids[row][col].show(DISP_BOARD_STATES[display_board[row][col]])

    def update_all_grids(self):
        """Update displayed board"""
        display_board = self.game.mgame.get_board()
        for row in range(self.difficulty['height']):
            for col in range(self.difficulty['width']):
                if self.grids[row][col].mine_state != display_board[row][col]:
                    self.grids[row][col].mine_state = display_board[row][col]
                    self.grids[row][col].show(DISP_BOARD_STATES[display_board[row][col]])

    def neighbors(self, row, col):
        """Return a list of neighboring locations specified by row and col"""
        row_i = (0, -1, 1) if 0 < row < self.game.difficulty['height'] - 1 else \
                ((0, -1) if row > 0 else (0, 1))
        col_i = (0, -1, 1) if 0 < col < self.game.difficulty['width'] - 1 else \
                ((0, -1) if col > 0 else (0, 1))
        return starmap((lambda a, b: [row + a, col + b]), product(row_i, col_i))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = MinesweeperGUI(DIFF_BEGINNER)
    sys.exit(app.exec_())






