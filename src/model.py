# game_state.py

from constants import *
from rules import *

# classe qui encapsule tout l'état d'une partie a un instant T
class GameState:
    #constructeur
    def __init__(self):
        self.board = self.initial_board()
        self.scores = [0, 0]
        self.current_player = 0
        self.last_move = None
        self.moves_without_capture = 0
        self.deadlock_active = False
        self.captured_pieces = {0: [], 1: []}


    def initial_board(self):
        #compréhension de liste imbriquée
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

    # renvoi l'ID de l'autre joueur
    def opponent(self, player):
        return 1 - player

    def get_legal_moves(self, player):
        moves = []
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY and is_own_side(r, player):
                    # extend c'est comme append mais pour tout les élements d'une liste
                    moves.extend(get_piece_moves(self.board, r, c, player))
        if self.last_move is not None:
            if len(self.last_move) == 4:
                forbidden_move = self.reverse_move(self.last_move)
                if forbidden_move in moves :
                    moves.remove(forbidden_move)
        return moves

    def reverse_move(self, move):
        r1, c1, r2, c2 = move
        return (r2, c2, r1, c1)

    def apply_move(self, move):
        is_capture = False
        # len = 4 move normal, len = 6 fusion
        if len(move) == 4:
            r1, c1, r2, c2 = move
            moving_piece = self.board[r1][c1]
            captured = self.board[r2][c2]

            if captured != EMPTY:
                self.scores[self.current_player] += PIECE_VALUES[captured]
                self.captured_pieces[self.current_player].append(captured)
                is_capture = True

            self.board[r2][c2] = moving_piece
            self.board[r1][c1] = EMPTY

        else:  # fusion
            _, r1, c1, r2, c2, result_piece = move
            self.board[r2][c2] = result_piece
            self.board[r1][c1] = EMPTY

        #compteur pour le deadlock (7 moves sans capture = match nul)
        if is_capture : 
            self.moves_without_capture = 0
        else:
            self.moves_without_capture += 1
            
        self.last_move = move
        self.current_player = self.opponent(self.current_player)


    def has_pieces(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY and is_own_side(r, player):
                    return True
        return False

    def is_terminal(self):
        deadlock_reached = self.deadlock_active and self.moves_without_capture >= MAX_TURNS_WITHOUT_CAPTURE
        return (not self.has_pieces(0) or 
                not self.has_pieces(1) or
                deadlock_reached)
        
    def enable_deadlock(self):
        """Active le compte à rebours pour le match nul"""
        if not self.deadlock_active:
            self.deadlock_active = True
            self.moves_without_capture = 0
            
    def copy(self):
        """
        Crée une copie profonde (deep copy) de l'état du jeu actuel.
        C'est indispensable pour que le Minimax puisse simuler des coups 
        sans modifier le vrai plateau affiché à l'écran.
        """
        # On crée un nouvel objet GameState vierge
        new_state = GameState()
        
        # 1. Copie du plateau (Liste 2D)
        # On utilise une compréhension de liste pour copier chaque ligne indépendamment
        new_state.board = [row[:] for row in self.board]
        
        # 2. Copie des listes et dictionnaires
        new_state.scores = self.scores[:] # Le [:] clone la liste
        
        new_state.captured_pieces = {
            0: self.captured_pieces[0][:],
            1: self.captured_pieces[1][:]
        }
        
        # 3. Copie des variables simples (entiers, booléens, tuples)
        new_state.current_player = self.current_player
        new_state.last_move = self.last_move # C'est un tuple (immuable), on peut le copier tel quel
        new_state.moves_without_capture = self.moves_without_capture
        new_state.deadlock_active = self.deadlock_active
        
        return new_state
