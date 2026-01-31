# rules.py
import model

class RuleEngine:
    
    @staticmethod
    def get_player_zone(player_id):
        """
        Renvoie l'intervalle des lignes appartenant au joueur.
        - Joueur 1 (Bas) : lignes 0 à 3.
        - Joueur 2 (Haut) : lignes 4 à 7.
        Sert à déterminer quelles pièces le joueur a le droit de bouger.
        """
        pass

    @staticmethod
    def get_legal_moves(gamestate):
        """
        LA fonction la plus importante pour l'IA.
        1. Identifie la zone du joueur courant via gamestate.current_player.
        2. Parcourt toutes les cases de cette zone.
        3. Pour chaque pièce trouvée, appelle les fonctions de mouvement spécifiques (_get_pawn_moves, etc.).
        4. Renvoie une liste de tous les coups possibles [(start_pos, end_pos), ...].
        """
        pass

    @staticmethod
    def _get_pawn_moves(gamestate, row, col):
        """
        Logique spécifique au Pion :
        - Déplacement d'1 case en diagonale (4 directions possibles).
        - Vérifie si la case cible est libre ou contient un ennemi.
        """
        pass

    @staticmethod
    def _get_drone_moves(gamestate, row, col):
        """
        Logique spécifique au Drone :
        - 1 ou 2 cases orthogonalement (Hori/Vert).
        - Vérifie qu'on ne saute pas par-dessus une pièce.
        """
        pass

    @staticmethod
    def _get_queen_moves(gamestate, row, col):
        """
        Logique spécifique à la Reine :
        - Distance illimitée dans les 8 directions.
        - S'arrête avant un obstacle (ou capture l'obstacle ennemi).
        """
        pass

    @staticmethod
    def apply_move(gamestate, move):
        """
        Exécute un coup sur l'état du jeu.
        1. Déplace la pièce de départ à arrivée.
        2. Gère la capture : si arrivée occupée, ajoute les points au score du joueur courant.
        3. Gère le compteur de Deadlock (reset si capture, +1 sinon).
        4. Vérifie la promotion éventuelle (fusion).
        5. Change le tour (switch_turn).
        """
        pass

    @staticmethod
    def check_promotion(gamestate, move):
        """
        Vérifie si le coup est une fusion (ex: Drone sur Pion).
        Si oui, remplace les deux pièces par la pièce supérieure.
        """
        pass

    @staticmethod
    def is_game_over(gamestate):
        """
        Vérifie les conditions de fin :
        1. Une zone est-elle totalement vide ? 
        2. Le compteur de Deadlock a-t-il atteint 7 tours ? 
        Renvoie True ou False.
        """
        pass

    @staticmethod
    def get_winner(gamestate):
        """
        Compare les scores.
        Gère les égalités selon la règle : si fin par zone vide, le joueur courant gagne l'égalité.
        Renvoie l'ID du gagnant ou None si match nul strict.
        """
        pass