# experiments/tournament.py

"""
Script pour lancer des tournois automatiques entre IAs sans interface graphique.
"""

def play_game(ai_1, ai_2):
    """
    Simule une seule partie complète entre deux IAs.
    Ne doit PAS utiliser d'affichage graphique (pas de pygame.display).
    Retourne le vainqueur (0, 1 ou None pour nul) et la durée de la partie.
    """
    pass

def play_match(ai_1, ai_2, games_count=50):
    """
    Lance une série de X parties (ex: 50) entre deux IAs.
    Alterne qui commence (J0 ou J1) pour l'équité.
    :param games_count: Nombre de parties à jouer[cite: 368].
    :return: Un dictionnaire avec les stats (Victoires J0, Victoires J1, Nuls, Temps moyen).
    """
    pass

def save_results(results, filename="results.csv"):
    """
    Exporte les résultats du tournoi dans un fichier CSV ou Texte
    pour pouvoir les analyser dans le rapport (tableaux, graphiques).
    """
    pass

if __name__ == "__main__":
    # Zone pour lancer le tournoi quand on exécute ce fichier
    pass