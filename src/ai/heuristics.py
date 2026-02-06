# src/ai/heuristics.py

"""
Contient les fonctions d'évaluation pour l'IA.
Chaque fonction prend un état (GameState) et un joueur, et retourne un score numérique.
"""

# gemini a genere random mais si je m'en rappel la prof a dit pas de randomisation des coups pour l'IA!!!!!
def eval_random(state, player):
    """
    Niveau Facile.
    Retourne une valeur totalement aléatoire, peu importe l'état du plateau.
    L'IA jouera n'importe comment.
    """
    pass

def eval_material(state, player):
    """
    Niveau Moyen.
    Calcule le score basé uniquement sur la différence de points matériel.
    Score = (Valeur de mes pièces capturées) - (Valeur des pièces capturées par l'adversaire).
    Ou bien (Valeur des pièces restantes sur le plateau).
    """
    pass

def eval_positional(state, player):
    """
    Niveau Difficile.
    Prend en compte le matériel MAIS AUSSI la position stratégique :
    - Contrôle du centre.
    - Menace de vider sa zone (pour finir la partie si on gagne).
    - Protection des pièces importantes (Reines).
    """
    pass