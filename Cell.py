class Cell():
    """Class for a cell of minesweeper"""

    def __init__(self, i: int, j: int, cell_size: int):
        """Init of cell size, index in the board, coordinates, state (revealed, mine, mines around)"""

        self.cell_size = cell_size
        self.i = i
        self.j = j
        self.x = j*cell_size
        self.y = i*cell_size

        self.revealed = False
        self.mine = False
        self.mine_clicked = False
        self.flaged = False
        self.mines_around = 0

    def coord(self) -> tuple:
        """Return the coordinates of itself"""

        return (self.x, self.y)

    def mines_around_count(self, board: list):
        """Count the number of mines around"""

        rows = len(board)
        cols = len(board[0])

        if self.mine:
            self.mines_around = -1
            return

        for i in range(-1, 2):
            i = self.i+i
            for j in range(-1, 2):
                j = self.j+j
                if not (i < 0 or i > rows-1 or j < 0 or j > cols-1):
                    cell = board[i][j]
                    if cell.mine:
                        self.mines_around += 1

    def reveal(self, board):
        """Reveal itself"""

        if not self.revealed and not self.flaged and not self.mine:
            # If it isn't revealed
            self.revealed = True

            if self.mines_around == 0:
                # Flood reveal
                rows = len(board)
                cols = len(board[0])

                for i in range(-1, 2):
                    i = self.i+i
                    for j in range(-1, 2):
                        j = self.j+j
                        if not (i < 0 or i > rows-1 or j < 0 or j > cols-1):
                            cell = board[i][j]
                            cell.reveal(board)

        elif self.revealed:
            # If already revealed
            self.reveal_around(board)

        elif self.mine and not self.flaged:
            # If it's a not flaged mine
            self.revealed = True
            self.mine_clicked = True
            self.reveal_all(board)

    def reveal_around(self, board):
        """Reveal the cells around itself"""

        if self.mines_around > 0:
            flags_around = 0
            rows = len(board)
            cols = len(board[0])

            # Count the flags around itself
            for i in range(-1, 2):
                i = self.i+i
                for j in range(-1, 2):
                    j = self.j+j
                    if not (i < 0 or i > rows-1 or j < 0 or j > cols-1):
                        cell = board[i][j]
                        if cell.flaged:
                            flags_around += 1

            if flags_around == self.mines_around:
                for i in range(-1, 2):
                    i = self.i+i
                    for j in range(-1, 2):
                        j = self.j+j
                        if not (i < 0 or i > rows-1 or j < 0 or j > cols-1):
                            cell = board[i][j]
                            if not cell.revealed:
                                cell.reveal(board)

    def reveal_all(self, board):
        """Reveal all the board"""
        rows = len(board)
        cols = len(board[0])

        for i in range(rows):
            for j in range(cols):
                cell = board[i][j]
                cell.revealed = True

    def flag(self):
        """Flag or unflag itself"""
        if not self.revealed:
            self.flaged = not self.flaged

