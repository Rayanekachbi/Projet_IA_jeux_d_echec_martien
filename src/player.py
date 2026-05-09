# src/player.py

import ai.heuristics as heur
from ai.minimax import alpha_beta

class Player:
    """Classe abstraite représentant un joueur."""
    def __init__(self, player_id):
        self.player_id = player_id

    def get_move(self, state, gui=None):
        """Retourne le coup choisi par le joueur."""
        pass


class HumanPlayer(Player):
    """
    Représente un joueur humain.
    Dans notre architecture avec Pygame, l'humain joue via les événements
    de la souris gérés dans main.py. Cette classe sert surtout d'étiquette 
    pour dire au jeu : "Attends que l'utilisateur clique".
    """
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_move(self, state, gui=None):
        # Pour l'humain, la gestion de la souris se fera dans main.py
        # Donc cette fonction renvoie None par défaut.
        return None


class AIPlayer(Player):
    """
    Représente l'ordinateur.
    Il utilise l'algorithme Alpha-Bêta et une heuristique selon sa difficulté.
    """
    def __init__(self, player_id, difficulty=2):
        super().__init__(player_id)
        self.difficulty = difficulty
        
        # --- CONFIGURATION DE LA DIFFICULTÉ ---
        if difficulty == 1:
            self.depth = 2
            self.eval_func = heur.eval_score_only
            print(f"Joueur {player_id} initialisé : IA Facile")
            
        elif difficulty == 2:
            self.depth = 3
            self.eval_func = heur.eval_positional
            print(f"Joueur {player_id} initialisé : IA Moyenne")
        elif difficulty == 3:
            self.depth = 4
            self.eval_func = heur.eval_pression
            print(f"Joueur {player_id} initialisé : IA Difficile")


    def get_move(self, state, gui=None):
        """
        Calcule et retourne le meilleur coup pour l'IA.
        """
        print(f"IA {self.player_id} réfléchit...")

        # 1. GESTION STRATÉGIQUE DU DEADLOCK
        # Si l'IA mène au score et que le deadlock n'est pas actif,
        # elle appuie "virtuellement" sur le bouton Deadlock pour presser l'adversaire !
        opponent_id = 1 - self.player_id
        if state.moves_without_capture >= 10:
            if state.scores[self.player_id] > state.scores[opponent_id]:
                if not state.deadlock_active:
                    print(f"L'IA {self.player_id} réclame le Deadlock !")
                    state.enable_deadlock()


        if state.moves_without_capture >= 30:
                if not state.deadlock_active:
                    print(f"L'IA {self.player_id} réclame le Deadlock !")
                    state.enable_deadlock()
        # 2. APPEL DE L'ALGORITHME DE RECHERCHE
        # On utilise l'Alpha-Bêta pour aller vite
        # alpha = -infini, beta = +infini, maximizing_player = True
        meilleur_score, meilleur_coup = alpha_beta(
            state, 
            self.depth, 
            float('-inf'), 
            float('inf'), 
            True, 
            self.player_id, 
            self.eval_func
        )
        
        # S'il y a un coup légal, on le retourne
        if meilleur_coup:
            return meilleur_coup
            
        # Sécurité : Si l'IA est complètement bloquée (aucun coup possible),
        # elle passe son tour (bien que ce soit très rare dans ce jeu).
        moves = state.get_legal_moves(self.player_id)
        if moves:
            return moves[0]
            
        return None