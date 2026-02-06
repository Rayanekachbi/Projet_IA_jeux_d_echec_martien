# src/player.py

"""
=============================================================================
A LIRE POUR LA PROCHAINE FOIS (MODIFICATIONS MAIN.PY)
=============================================================================
Quand vous serez prêt à intégrer ce fichier dans main.py, voici ce qu'il faudra changer :

1. Instanciation : Au début de main(), il faudra créer deux joueurs :
   player1 = HumanPlayer()
   player2 = AIPlayer(difficulty=2) (par exemple)

2. Boucle de jeu : Au lieu de gérer pygame.MOUSEBUTTONDOWN directement dans la boucle,
   il faudra demander au joueur courant de jouer :
   
   current_p_obj = player1 if game.current_player == 0 else player2
   move = current_p_obj.get_move(game, gui) # gui est nécessaire pour l'humain

   Si move n'est pas None (l'humain a cliqué ou l'IA a fini de calculer) :
       game.apply_move(move)
=============================================================================
"""

class Player:
    """
    Classe abstraite représentant un joueur (Humain ou IA).
    """
    def __init__(self, player_id):
        self.player_id = player_id

    def get_move(self, state, gui=None):
        """
        Détermine le prochain coup à jouer.
        :param state: L'objet GameState actuel.
        :param gui: L'interface graphique (nécessaire pour l'humain pour récupérer les clics).
        :return: Un tuple représentant le coup (r1, c1, r2, c2) ou None si pas encore choisi.
        """
        pass

class HumanPlayer(Player):
    """
    Représente un joueur humain qui utilise l'interface graphique.
    """
    def get_move(self, state, gui=None):
        """
        Logique pour l'humain :
        - Doit vérifier les événements Pygame (clics souris) via l'objet gui.
        - Retourne le coup si un mouvement valide est sélectionné à la souris.
        - Retourne None tant que le joueur réfléchit.
        """
        pass

class AIPlayer(Player):
    """
    Représente une Intelligence Artificielle.
    """
    def __init__(self, player_id, depth=3, heuristic_func=None):
        super().__init__(player_id)
        # depth : Profondeur de recherche pour Minimax
        # heuristic_func : La fonction d'évaluation à utiliser
        pass

    def get_move(self, state, gui=None):
        """
        Logique pour l'IA :
        - Appelle l'algorithme Minimax ou Alpha-Bêta situé dans src/ai/minimax.py.
        - Retourne le meilleur coup trouvé.
        """
        pass