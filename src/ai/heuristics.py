# src/ai/heuristics.py
import rules
from constants import *

"""
Contient les fonctions d'évaluation pour l'IA.
Chaque fonction prend un état (GameState) et un joueur, et retourne un score numérique.
"""
def eval_score_only(state, player_id, mobility=0, opp_mobility=0):
    """
    Niveau Facile.
    L'IA ne regarde que les points officiels déjà marqués.
    Elle ne prévoit rien à l'avance et joue purement à l'instinct.
    """
    opponent_id = 1 - player_id
    
    my_score = state.scores[player_id]
    opponent_score = state.scores[opponent_id]
    stall_penalty = state.moves_without_capture * 10
    return my_score - opponent_score - stall_penalty



def eval_material(state, player_id, mobility=0, opp_mobility=0):
    """
    Niveau Moyen.
    L'IA prend en compte le score officiel ET le "potentiel" sur le plateau.
    Elle préférera les coups qui amènent/gardent des pièces fortes sur son territoire.
    """
    opponent_id = 1 - player_id
    
    # Le score officiel (Priorité absolue : on multiplie par 100)
    # Ainsi, une vraie capture d'un pion (+100) vaudra toujours plus 
    # que juste déplacer une Reine sur son terrain (+3).
    score_diff = (state.scores[player_id] - state.scores[opponent_id]) * 100
    
    # Le calcul du matériel sur le plateau
    my_board_value = 0
    opp_board_value = 0
    
    # On scanne toutes les lignes et colonnes
    for r in range(ROWS):
        for c in range(COLS):
            piece = state.board[r][c]
            
            if piece != EMPTY:
                # À qui appartient la zone où se trouve la pièce ?
                owner = rules.piece_owner(r)
                piece_val = PIECE_VALUES[piece] # Vaut 1, 2 ou 3
                
                if owner == player_id:
                    my_board_value += piece_val
                else:
                    opp_board_value += piece_val
                    
    # La différence de force sur le plateau
    board_diff = my_board_value - opp_board_value


    # La note finale
    stall_penalty = state.moves_without_capture * 5
    return score_diff + board_diff - stall_penalty

def eval_positional(state, player_id, mobility=0, opp_mobility=0):
    """
    Niveau Difficile.
    Prend en compte le matériel, mais ajoute une compréhension stratégique du jeu :
    - Contrôle du canal (midline).
    - Gestion de la fin de partie (Vider sa zone si on gagne, fuir la fin si on perd).
    """
    opponent_id = 1 - player_id

    base_score = eval_material(state, player_id)
    
    positional_bonus = 0
    my_piece_count = 0
    
    # On analyse le placement et on compte nos pièces
    for r in range(ROWS):
        for c in range(COLS):
            piece = state.board[r][c]
            if piece != EMPTY:
                owner = rules.piece_owner(r)
                
                if owner == player_id:
                    my_piece_count += 1
                    # Bonus si la pièce est juste au bord du canal (lignes centrales)
                    if r == MIDLINE - 1 or r == MIDLINE:
                        positional_bonus += 5
                else:
                    # Malus si l'adversaire est collé au canal
                    if r == MIDLINE - 1 or r == MIDLINE:
                        positional_bonus -= 5 

    # Stratégie de fin de partie (Zone Vide)
    my_score = state.scores[player_id]
    opp_score = state.scores[opponent_id]
    
    if my_score > opp_score:
        # L'IA gagne ! Elle veut vider sa zone pour forcer la fin.
        # Plus elle a un nombre de pièces FAIBLE, plus le bonus est FORT.
        positional_bonus += (10 - my_piece_count) * 15 
        
    elif my_score < opp_score:
        # L'IA perd ! Elle veut garder des pièces pour ne pas perdre bêtement.
        if my_piece_count <= 2:
            positional_bonus -= 50 # Grosse pénalité si elle est sur le point de se vider



    mobility_score = (mobility - opp_mobility) * 2
    stall_penalty = state.moves_without_capture * 5

    return base_score + positional_bonus + mobility_score