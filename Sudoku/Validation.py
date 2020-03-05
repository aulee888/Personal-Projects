class Validate:
    def col_check(self, board):
        for j in range(9):
            used = set()

            for i in range(9):
                if board[i][j] in used:
                    return False
                else:
                    used.add(board[i][j])

        return True

    def row_check(self, board):
        for i in range(9):
            used = set()

            for j in range(9):
                if board[i][j] in used:
                    return False
                else:
                    used.add(board[i][j])

        return True

    def box_check(self, board):
        for p in range(3):
            for q in range(3):
                used = set()

                for i in range(3):
                    for j in range(3):
                        value = board[3*p + i][3*q + j]

                        if value in used:
                            return False
                        else:
                            used.add(value)

        return True


test = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
        [9, 6, 5, 3, 2, 7, 1, 4, 8],
        [3, 4, 1, 6, 8, 9, 7, 5, 2],
        [5, 9, 3, 4, 6, 8, 2, 7, 1],
        [4, 7, 2, 5, 1, 3, 6, 8, 9],
        [6, 1, 8, 9, 7, 2, 4, 3, 5],
        [7, 8, 6, 2, 3, 5, 9, 1, 4],
        [1, 5, 4, 7, 9, 6, 8, 2, 3],
        [2, 3, 9, 8, 4, 1, 5, 6, 7]]

print(Validate().col_check(test))
print(Validate().row_check(test))
print(Validate().box_check(test))