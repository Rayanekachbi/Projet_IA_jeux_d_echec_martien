# main.py
import model
import view
import rules

def main():
    """
    Fonction principale du programme.
    1. Instancie le modèle (GameState) et la vue (ConsoleView).
    2. Initialise le plateau (initialize_board).
    3. Lance la boucle de jeu (While not game over):
        a. Affiche le plateau.
        b. Détermine qui joue (Humain ou IA).
        c. Si Humain : demande l'input via view.
        d. Si IA : demande le coup via l'algorithme (à implémenter plus tard).
        e. Vérifie si le coup est légal via RuleEngine.
        f. Applique le coup via RuleEngine.apply_move.
    4. Une fois la boucle finie, affiche le résultat final.
    """
    pass

if __name__ == "__main__":
    main()