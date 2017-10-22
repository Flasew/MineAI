import Minesweeper as MB

class Agent:

    def __init__(self, difficulty):
        self.game = MB.Minesweeper(difficulty, (0,0,))
        self.board = game.get_board()

        self.mousepos = (0,0,)

        self.known_opens=[]
        self.known_mines=[]
        self.boundary=[]
        self.init_knowledge()

        self.boundary_blocks = []

    def init_boundary(self):
        for pos in range(self.height*self.width):
            row = pos // self.width
            col = pos % self.width
            if self.board[row][col] == MB.HIDDEN:
                if self.is_boundary(row,col):
                    self.boundary.append((row,col,))
    def is_boundary(self,row,col):
        for nrow, ncol in game.neighbors(row, col):
            if row != nrow and col != nrol
                and self.board[nrow][ncol] != MB.HIDDEN:
                return True
        return False
    def boundary_split(self):
        for grid in self.boundary:
            self.boundary_blocks.append( blocks(grid[0], grid[1] ) )

    def blocks(self, row, col):
        block = []
        block.append(row,col,)
        self.boundary.remove( (row,col,) )
        for nrow, ncol in game.neighbors(row, col):
            if (nrow, ncol,) in self.boundary:
                block.extend( blocks(nrow, ncol) )
        return block
    def surr_flags(self,row,col):
        flags = 0
        for nrow, ncol in game.neighbors(row,col):
            if board[nrow][ncol] == MB.FLAGGED:
                flags += 1
        return hiddens
    def surr_hiddens(self,row,col):
        hiddens = 0
        for nrow, ncol in game.neighbors(row,col):
            if board[nrow][ncol] == MB.HIDDEN:
                hiddens += 1
        return hiddens
    def naive_flag(self):
        for grid in self.boundary:
            for nrow,ncol in game.neighbors(grid[0],grid[1]):
                if self.board[nrow][ncol] != MB.HIDDEN
                    and self.board[nrow]:
