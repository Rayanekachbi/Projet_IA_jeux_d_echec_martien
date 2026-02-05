# game_state.py

from constants import *
from rules import *

class GameState:
    def __init__(self):
        self.board = self.initial_board()
        self.scores = [0, 0]
        self.current_player = 0
        self.last_move = None

    def initial_board(self):
        board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

        # Joueur 0 (haut)
        board[0] = [QUEEN, QUEEN, DRONE, EMPTY]
        board[1] = [QUEEN, DRONE, PAWN, EMPTY]
        board[2] = [DRONE, PAWN, PAWN, EMPTY]

        # Joueur 1 (bas)
        board[5] = [EMPTY, PAWN, PAWN, DRONE]
        board[6] = [EMPTY, PAWN, DRONE, QUEEN]
        board[7] = [EMPTY, DRONE, QUEEN, QUEEN]

        return board

    def opponent(self, player):
        return 1 - player

    def get_legal_moves(self, player):
        moves = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY and is_own_side(r, player):
                    moves.extend(get_piece_moves(self.board, r, c, player))
        return moves

    def reverse_move(self, move):
        r1, c1, r2, c2 = move
        return (r2, c2, r1, c1)

    def apply_move(self, move):
        if len(move) == 4:
            r1, c1, r2, c2 = move
            moving_piece = self.board[r1][c1]
            captured = self.board[r2][c2]

            if captured != EMPTY:
                self.scores[self.current_player] += PIECE_VALUES[captured]

            self.board[r2][c2] = moving_piece
            self.board[r1][c1] = EMPTY

        else:  # fusion
            _, r1, c1, r2, c2, result_piece = move
            self.board[r2][c2] = result_piece
            self.board[r1][c1] = EMPTY

        self.last_move = move
        self.current_player = self.opponent(self.current_player)

    def has_pieces(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY and is_own_side(r, player):
                    return True
        return False

    def is_terminal(self):
        return not self.has_pieces(0) or not self.has_pieces(1)
