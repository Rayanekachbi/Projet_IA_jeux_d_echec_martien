# model.py

class PieceType:
    """
    Enumération ou constantes pour les types de pièces.
    Valeurs : PAWN (1), DRONE (2), QUEEN (3).
    """
    PAWN = "Pawn"
    DRONE = "Drone"
    QUEEN = "Queen"

class Piece:
    def __init__(self, piece_type):
        """
        Initialise une pièce.
        :param piece_type: Le type de la pièce (Pawn, Drone, Queen).
        Note: Pas besoin de stocker la couleur/joueur ici car la propriété dépend de la zone (règle martienne).
        """
        self.type = piece_type

    def get_value(self):
        """
        Renvoie la valeur en points de la pièce (1, 2 ou 3).
        Utile pour le calcul du score.
        """
        pass

class GameState:
    def __init__(self):
        """
        Initialise l'état du jeu.
        - Crée un plateau vide (grille 4x8).
        - Initialise les scores des deux joueurs (J1 et J2).
        - Définit le joueur courant (celui qui doit jouer).
        - Initialise le compteur pour la règle du 'Deadlock' (tours sans capture).
        """
        self.board = [] # La grille 4x8
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.moves_without_capture = 0

    def initialize_board(self):
        """
        Place les 18 pièces initiales selon la configuration officielle.
        - Zone Bas (Joueur 1) : L de Reines, Diagonale Drones, Pions.
        - Zone Haut (Joueur 2) : Symétrie rotationnelle.
        """
        pass

    def get_piece_at(self, row, col):
        """
        Renvoie l'objet Piece situé aux coordonnées (row, col) ou None si vide.
        """
        pass

    def set_piece_at(self, row, col, piece):
        """
        Place une pièce manuellement à une coordonnée (utile pour apply_move).
        """
        pass

    def remove_piece_at(self, row, col):
        """
        Enlève une pièce du plateau (utile lors d'un déplacement ou capture).
        """
        pass

    def is_within_bounds(self, row, col):
        """
        Vérifie si les coordonnées sont bien dans la grille (0-7 lignes, 0-3 colonnes).
        """
        pass

    def switch_turn(self):
        """
        Passe la main à l'autre joueur (1 -> 2 ou 2 -> 1).
        """
        pass

    def copy(self):
        """
        Crée et renvoie une COPIE PROFONDE (Deep Copy) de l'état actuel.
        CRUCIAL pour l'IA Minimax : l'IA doit simuler des coups sur des copies 
        sans modifier le vrai plateau du jeu.
        """
        pass