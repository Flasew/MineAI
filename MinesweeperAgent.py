import Minesweeper as MB

class Agent:

    def __init__(self, difficulty):
        self.game = MB.Minesweeper(difficulty, (0,0,))
        self.solveBoard = game.get_board()

        self.mousepos = (0,0,)

        self.known_opens
        self.known_mines
        self.boundaries

    def init_knowledge(self):
        for pos in range(self.height*self.width)

    def update_knowledge(self):
