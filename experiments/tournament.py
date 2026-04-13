# experiments/tournament.py

"""
Script pour lancer des tournois automatiques entre IAs sans interface graphique.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import time
import rules
from model import GameState
from player import AIPlayer

DIFFICULTY_NAMES = {
    1: "Facile",
    2: "Moyen",
    3: "Difficile"
}
def play_game(ai_0, ai_1, max_moves=500):
    game = GameState()
    players = {0: ai_0, 1: ai_1}

    start_time = time.time()
    winner = None

    move_count = 0

    while True:
        move_count += 1

        # ✅ Sécurité anti boucle infinie
        if move_count > max_moves:
            winner = None  # considéré comme nul
            break

        current_player = game.current_player
        current_ai = players[current_player]

        move = current_ai.get_move(game)

        if move is None:
            break

        game.apply_move(move)

        if game.is_terminal():
            winner = rules.get_winner(
                game.scores,
                game.moves_without_capture,
                game.current_player
            )
            break

    duration = time.time() - start_time
    return winner, duration

def play_match(ai_1, ai_2, games_count=50):
    results = {
        "ai1_wins": 0,
        "ai2_wins": 0,
        "draws": 0,
        "total_time": 0
    }

    for i in range(games_count):

        # Alternance : 25/25
        if i < games_count // 2:
            p0 = AIPlayer(0, difficulty=ai_1)
            p1 = AIPlayer(1, difficulty=ai_2)
            swapped = False
        else:
            p0 = AIPlayer(0, difficulty=ai_2)
            p1 = AIPlayer(1, difficulty=ai_1)
            swapped = True

        winner, duration = play_game(p0, p1)
        results["total_time"] += duration

        if winner is None:
            results["draws"] += 1
        else:
            # remettre dans le bon sens
            if swapped:
                winner = 1 - winner

            if winner == 0:
                results["ai1_wins"] += 1
            else:
                results["ai2_wins"] += 1

    results["avg_time"] = results["total_time"] / games_count
    return results

import csv

def save_results(results, filename="results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "IA 1", "IA 2",
            "Victoires IA1", "Victoires IA2",
            "Nuls", "Temps moyen"
        ])

        for r in results:
            writer.writerow([
                r["ai1_name"],
                r["ai2_name"],
                r["ai1_wins"],
                r["ai2_wins"],
                r["draws"],
                round(r["avg_time"], 4)
            ])

if __name__ == "__main__":

    # Difficultés comme dans ton menu :
    # 1 = Facile, 2 = Moyen, 3 = Difficile
    difficulties = [1, 2, 3]

    all_results = []

    for i in range(len(difficulties)):
        for j in range(i + 1, len(difficulties)):

            d1 = difficulties[i]
            d2 = difficulties[j]

            print(f"Match IA {d1} vs IA {d2}...")

            result = play_match(d1, d2, games_count=50)

            result["ai1_name"] = DIFFICULTY_NAMES[d1]
            result["ai2_name"] = DIFFICULTY_NAMES[d2]

            all_results.append(result)

    save_results(all_results)

    print("Tournoi terminé")