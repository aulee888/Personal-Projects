class Validate:
    def __init__(self, board):
        self.board = board

    def col_check(self):
        for j in range(9):
            used = set()

            for i in range(9):
                if self.board[i][j] in used:
                    return False
                else:
                    used.add(self.board[i][j])

        return True

    def row_check(self):
        for i in range(9):
            used = set()

            for j in range(9):
                if self.board[i][j] in used:
                    return False
                else:
                    used.add(self.board[i][j])

        return True

    def box_check(self):
        for k in range(3):
            used = set()

            for i in range(3):
                for j in range(3):
                    if self.board[3*k + i][2*k + j] in used:
                        return False


