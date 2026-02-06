# main.py

import pygame
import rules # Important pour get_winner
from model import GameState
from view import GUI

def main():
    game = GameState()
    gui = GUI(game)
    clock = pygame.time.Clock()
    
    running = True
    game_over = False # NOUVEAU : État pour savoir si la partie est finie
    winner = None     # Stockera l'ID du gagnant

    while running:
        clock.tick(60)
        
        # Si le jeu est en cours, on dessine le plateau normalement
        if not game_over:
            gui.update()
        else:
            # Si le jeu est fini, on dessine l'overlay de victoire
            gui.draw_game_over(winner)

        # --- GESTION DES ÉVÉNEMENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # GESTION DES CLICS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # CAS 1 : La partie est finie -> Le clic ferme le jeu
                if game_over:
                    running = False
                
                # CAS 2 : La partie est en cours -> On joue
                else:
                    cell = gui.get_cell_from_mouse(pygame.mouse.get_pos())
                    if not cell:
                        continue

                    r, c = cell

                    # Sélectionner une pièce
                    if gui.selected is None:
                        if game.board[r][c] != ".":
                            # Vérifie que la pièce appartient bien au joueur courant
                            if rules.is_own_side(r, game.current_player):
                                gui.selected = (r, c)
                    
                    # Déplacer une pièce
                    else:
                        r1, c1 = gui.selected
                        chosen_move = None
                        
                        # Si on reclique sur la même case, on désélectionne
                        if (r, c) == (r1, c1):
                            gui.selected = None
                            continue

                        # Chercher si le clic correspond à un coup légal
                        for m in game.get_legal_moves(game.current_player):
                            # Coup normal
                            if len(m) == 4 and m == (r1, c1, r, c):
                                chosen_move = m
                                break
                            # Fusion
                            elif len(m) == 6 and m[1] == r1 and m[2] == c1 and m[3] == r and m[4] == c:
                                chosen_move = m
                                break

                        if chosen_move:
                            game.apply_move(chosen_move)
                            gui.selected = None # On désélectionne après avoir joué
                            
                            # VÉRIFICATION DE FIN DE PARTIE APRÈS LE COUP
                            if game.is_terminal():
                                game_over = True
                                winner = rules.get_winner(
                                    game.scores, 
                                    game.moves_without_capture, 
                                    game.current_player
                                )
                                # On ne quitte pas la boucle, au prochain tour 'gui.draw_game_over' sera appelé
                                
                        else:
                            # Si le coup n'est pas valide, on change la sélection si c'est une de nos pièces
                            if game.board[r][c] != "." and rules.is_own_side(r, game.current_player):
                                gui.selected = (r, c)
                            else:
                                gui.selected = None

    pygame.quit()

if __name__ == "__main__":
    main()