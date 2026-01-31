# view.py

class ConsoleView:
    def display_board(self, gamestate):
        """
        Affiche le plateau dans la console.
        - Utilise des caractères pour les pièces (P, D, Q).
        - Affiche les coordonnées (A-D, 1-8) pour aider le joueur.
        - Affiche les scores actuels et le joueur dont c'est le tour.
        """
        pass

    def get_human_input(self):
        """
        Demande au joueur de saisir son coup (ex: "A2 B3").
        Lit l'entrée clavier et la transforme en coordonnées (row, col).
        Gère les erreurs de saisie (format invalide).
        """
        pass

    def show_message(self, message):
        """
        Affiche un message informatif (ex: "Coup invalide", "Joueur 1 gagne !").
        """
        pass