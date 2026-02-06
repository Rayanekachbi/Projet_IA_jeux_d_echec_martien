# rules.py

from constants import *

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def is_own_side(r, player):
    return (r < MIDLINE and player == 0) or (r >= MIDLINE and player == 1)

def piece_owner(r):
    return 0 if r < MIDLINE else 1


def count_all(board):
    counts = {PAWN: 0, DRONE: 0, QUEEN: 0}
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != EMPTY:
                counts[board[r][c]] += 1
    return counts


def count_player(board, player):
    counts = {PAWN: 0, DRONE: 0, QUEEN: 0}
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != EMPTY and piece_owner(r) == player:
                counts[board[r][c]] += 1
    return counts


def piece_available(board, piece_type):
    counts_all = count_all(board)
    return counts_all[piece_type] < TOTAL_PIECES[piece_type]


def get_piece_moves(board, r, c, current_player):
    piece = board[r][c]
    moves = []

    # ---------- Déplacements normaux ----------

    if piece == PAWN:
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc):
                if board[nr][nc] == EMPTY or piece_owner(nr) != current_player:
                    moves.append((r, c, nr, nc))

    elif piece == DRONE:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for dist in [1, 2]:
                nr, nc = r + dr * dist, c + dc * dist
                if not in_bounds(nr, nc):
                    break
                if board[nr][nc] == EMPTY:
                    moves.append((r, c, nr, nc))
                else:
                    if piece_owner(nr) != current_player:
                        moves.append((r, c, nr, nc))
                    break

    elif piece == QUEEN:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            while in_bounds(nr, nc):
                if board[nr][nc] == EMPTY:
                    moves.append((r, c, nr, nc))
                else:
                    if piece_owner(nr) != current_player:
                        moves.append((r, c, nr, nc))
                    break
                nr += dr
                nc += dc

    # ----------- FIELD PROMOTIONS OFFICIELLES -----------

    player_counts = count_player(board, current_player)

    # Pawn + Pawn -> Drone
    if piece == PAWN and player_counts[DRONE] == 0 and piece_available(board, DRONE):
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and board[nr][nc] == PAWN and piece_owner(nr) == current_player:
                moves.append(("fusion", r, c, nr, nc, DRONE))

    # Pawn + Drone -> Queen
    if piece == PAWN and player_counts[QUEEN] == 0 and piece_available(board, QUEEN):
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and board[nr][nc] == DRONE and piece_owner(nr) == current_player:
                moves.append(("fusion", r, c, nr, nc, QUEEN))

    # Drone + Pawn -> Queen
    if piece == DRONE and player_counts[QUEEN] == 0 and piece_available(board, QUEEN):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for dist in [1, 2]:
                nr, nc = r + dr * dist, c + dc * dist
                if not in_bounds(nr, nc):
                    break
                if board[nr][nc] == EMPTY:
                    continue
                if piece_owner(nr) != current_player:
                    break
                if board[nr][nc] == PAWN:
                    moves.append(("fusion", r, c, nr, nc, QUEEN))
                break


    return moves

# determine le vainqueur, Renvoie: 0 ou 1 (ID du gagnant), None : Match nul (Tie)
def get_winner(scores, moves_without_capture, current_player):
    if scores[0] > scores[1]:
        return 0
    if scores[1] > scores[0]:
        return 1
    if moves_without_capture >= 7:
        return None
    # Si c'est une fin par "Zone Vide" (pas de deadlock), 
    # le joueur qui a provoqué la fin (celui qui vient de jouer) gagne le tie-breaker.
    # Dans model.apply_move, on change le current_player juste à la fin.
    # Donc le joueur qui a "fini" la partie est l'ADVERSAIRE du current_player actuel.
    winner_by_tie_break = 1 - current_player
    return winner_by_tie_break