# src/ai/minimax.py

"""
Implémentation des algorithmes de recherche.
"""

import rules


def move_priority(move):
    if isinstance(move, tuple) and move[0] == "fusion":
        return 3
    if len(move) == 4:
        return 2
    return 1



def minimax(state, depth, maximizing_player, player_id, eval_func):
    """
    Algorithme Minimax classique.
    Retourne un tuple : (meilleur_score, meilleur_coup)
    """
    # --- 1. CONDITION D'ARRÊT (La "photo" finale) ---
    if depth == 0 or state.is_terminal():
        if state.is_terminal():
            winner = rules.get_winner(state.scores, state.current_player, state.deadlock_active)
            if winner == player_id:
                return float('inf'), None  # Victoire absolue
            elif winner is None:
                return 0, None             # Match nul
            else:
                return float('-inf'), None # Défaite absolue
                
        return eval_func(state, player_id), None

    best_move = None

    # --- 2. TOUR DE L'IA (Cherche le score MAX) ---
    if maximizing_player:
        max_eval = float('-inf')
        moves = state.get_legal_moves(state.current_player)
        
        # Si aucun mouvement n'est possible (cas rare de blocage total)
        if not moves:
            return eval_func(state, player_id), None
            
        for move in moves:
            # On utilise TA méthode de copie rapide !
            simulated_state = state.copy()
            simulated_state.apply_move(move)
            
            # On descend d'un niveau et c'est au tour de l'adversaire (False)
            eval_score, _ = minimax(simulated_state, depth - 1, False, player_id, eval_func)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
        return max_eval, best_move

    # --- 3. TOUR DE L'ADVERSAIRE (Cherche le score MIN) ---
    else:
        min_eval = float('inf')
        moves = state.get_legal_moves(state.current_player)
        
        if not moves:
            return eval_func(state, player_id), None
            
        for move in moves:
            # On utilise TA méthode de copie rapide !
            simulated_state = state.copy()
            simulated_state.apply_move(move)
            
            # On descend d'un niveau et c'est au tour de l'IA (True)
            eval_score, _ = minimax(simulated_state, depth - 1, True, player_id, eval_func)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
        return min_eval, best_move

def alpha_beta(state, depth, alpha, beta, maximizing_player, player_id, eval_func):
    """
    Version optimisée du Minimax avec élagage Alpha-Bêta.
    Permet de chercher plus profondément en ignorant les mauvais coups évidents.
    """
    # --- 1. CONDITION D'ARRÊT ---
    if depth == 0 or state.is_terminal():

        if state.is_terminal():
            winner = rules.get_winner(state.scores, state.current_player, state.deadlock_active)
            if winner == player_id:
                return float('inf'), None  # Victoire
            elif winner is None:
                return 0, None             # Nul
            else:
                return float('-inf'), None # Défaite

        my_moves = state.get_legal_moves(player_id)
        opp_moves = state.get_legal_moves(1 - player_id)
        return eval_func(state, player_id, len(my_moves), len(opp_moves)), None

    best_move = None

    # --- 2. TOUR DE L'IA (Maximisant) ---
    if maximizing_player:
        max_eval = float('-inf')
        moves = state.get_legal_moves(state.current_player)

        moves.sort(key=move_priority, reverse=True)
        if not moves:
            return eval_func(state, player_id, 0, 0), None
            
        for move in moves:
            simulated_state = state.copy()
            simulated_state.apply_move(move)
            
            eval_score, _ = alpha_beta(simulated_state, depth - 1, alpha, beta, False, player_id, eval_func)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
            # --- L'ÉLAGAGE ALPHA-BÊTA ---
            # On met à jour alpha (le meilleur score garanti pour l'IA)
            alpha = max(alpha, eval_score)
            # Si le score garanti de l'adversaire (beta) est déjà pire ou égal à notre alpha,
            # on arrête de chercher dans cette branche : l'adversaire ne nous laissera jamais venir ici !
            if beta <= alpha:
                break 
                
        return max_eval, best_move

    # --- 3. TOUR DE L'ADVERSAIRE (Minimisant) ---
    else:
        min_eval = float('inf')
        moves = state.get_legal_moves(state.current_player)

        moves.sort(key=move_priority)
        if not moves:
            return eval_func(state, player_id, 0, 0), None
            
        for move in moves:
            simulated_state = state.copy()
            simulated_state.apply_move(move)
            
            eval_score, _ = alpha_beta(simulated_state, depth - 1, alpha, beta, True, player_id, eval_func)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
            # --- L'ÉLAGAGE ALPHA-BÊTA ---
            # On met à jour beta (le meilleur score garanti pour l'adversaire)
            beta = min(beta, eval_score)
            # Si l'adversaire voit qu'on a déjà un coup meilleur (alpha) ailleurs,
            # il sait qu'on ne choisira jamais cette branche. Il arrête de chercher.
            if beta <= alpha:
                break
                
        return min_eval, best_move

def iterative_deepening(state, time_limit, player_id, eval_func):
    """
    (Optionnel mais recommandé pour les tournois).
    Lance Alpha-Bêta à profondeur 1, puis 2, puis 3... tant qu'il reste du temps.
    Permet de toujours avoir une réponse prête si le temps est écoulé.
    """
    pass