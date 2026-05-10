# main.py

import pygame
import sys
import rules
from constants import *
from model import GameState
from view import GUI
from player import HumanPlayer, AIPlayer

def show_menu(screen):
    """
    Affiche un menu de sélection des joueurs avant de lancer la partie.
    Retourne la configuration choisie pour les deux joueurs.
    """
    font_title = pygame.font.SysFont(None, 60, bold=True)
    font_btn = pygame.font.SysFont(None, 35)
    
    # Options possibles
    options = ["Humain", "IA Facile", "IA Moyenne", "IA Difficile"]
    
    # Sélections par défaut
    p0_selected = 0 # Index 0 = Humain
    p1_selected = 2 # Index 2 = IA Moyenne

    # Création des rectangles pour les boutons
    # Colonne 1 (Joueur 0)
    p0_rects = [pygame.Rect(WINDOW_WIDTH // 4 - 100, 150 + i * 60, 200, 40) for i in range(4)]
    # Colonne 2 (Joueur 1)
    p1_rects = [pygame.Rect(3 * WINDOW_WIDTH // 4 - 100, 150 + i * 60, 200, 40) for i in range(4)]
    
    # Bouton Jouer
    play_btn = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 60)

    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 40)) # Fond bleu nuit
        
        # Titre
        title = font_title.render("MARTIAN CHESS - MENU", True, WHITE)
        screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 60)))
        
        # Sous-titres
        screen.blit(font_btn.render("Joueur 0 (Haut)", True, GREEN), (WINDOW_WIDTH // 4 - 80, 110))
        screen.blit(font_btn.render("Joueur 1 (Bas)", True, RED), (3 * WINDOW_WIDTH // 4 - 80, 110))

        # Dessin des boutons Joueur 0
        for i, rect in enumerate(p0_rects):
            color = GREEN if i == p0_selected else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            text = font_btn.render(options[i], True, BLACK)
            screen.blit(text, text.get_rect(center=rect.center))

        # Dessin des boutons Joueur 1
        for i, rect in enumerate(p1_rects):
            color = RED if i == p1_selected else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            text = font_btn.render(options[i], True, BLACK)
            screen.blit(text, text.get_rect(center=rect.center))

        # Dessin du bouton Jouer
        pygame.draw.rect(screen, BLUE, play_btn)
        pygame.draw.rect(screen, WHITE, play_btn, 3)
        play_text = font_title.render("JOUER", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=play_btn.center))

        pygame.display.flip()

        # Gestion des clics du menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                for i, rect in enumerate(p0_rects):
                    if rect.collidepoint(pos): p0_selected = i
                        
                for i, rect in enumerate(p1_rects):
                    if rect.collidepoint(pos): p1_selected = i
                        
                if play_btn.collidepoint(pos):
                    return p0_selected, p1_selected
        
        clock.tick(30)

def create_player(player_id, selection):
    """Convertit l'index du menu en objet Player (Humain ou IA)"""
    if selection == 0:
        return HumanPlayer(player_id)
    else:
        # L'index 1 = Facile (Diff 1), 2 = Moyen (Diff 2), 3 = Difficile (Diff 3)
        return AIPlayer(player_id, difficulty=selection)

def main():
    total_moves = 0
    move_count = 0

    pygame.init()
    # On crée une fenêtre temporaire juste pour le menu
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Martian Chess - Menu")
    
    # 1. Afficher le menu et récupérer les choix
    p0_choice, p1_choice = show_menu(screen)
    
    # 2. Initialiser le vrai jeu
    game = GameState()
    gui = GUI(game)
    
    players = {
        0: create_player(0, p0_choice),
        1: create_player(1, p1_choice)
    }
    
    clock = pygame.time.Clock()
    running = True
    game_over = False
    winner = None
    
    while running:
        clock.tick(60)
        legal_moves = game.get_legal_moves(game.current_player)

        total_moves += len(legal_moves)
        move_count += 1
        # --- AFFICHAGE ---
        if not game_over:
            gui.update() 
        else:
            gui.screen.fill(BLACK) 
            gui.draw_board()
            gui.draw_ui()
            gui.draw_game_over(winner)

        # --- GESTION DU TOUR DE L'IA ---
        current_p = players[game.current_player]
        
        # Si c'est à l'IA de jouer et que le jeu n'est pas fini
        if isinstance(current_p, AIPlayer) and not game_over:
            # On force le dessin de l'écran avant que l'IA ne freeze le jeu en réfléchissant
            gui.update() 
            
            # L'IA réfléchit et trouve son coup
            ai_move = current_p.get_move(game)
            
            if ai_move:
                game.apply_move(ai_move)
                gui.selected = None
                
                if game.is_terminal():
                    game_over = True
                    winner = rules.get_winner(game.scores, game.current_player, game.deadlock_active)
            
            # On vide la file d'événements Pygame pour éviter que la fenêtre "ne réponde pas" 
            # pendant le temps de calcul de l'IA
            pygame.event.pump()
            continue # On passe directement à la prochaine frame, pas besoin de lire les clics souris

        # --- GESTION DES ÉVÉNEMENTS (SOURIS POUR L'HUMAIN) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    running = False
                
                # C'est ici qu'on gère le clic SEULEMENT si c'est un joueur humain
                elif isinstance(current_p, HumanPlayer):
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Clic sur le bouton Deadlock
                    if gui.deadlock_btn_rect.collidepoint(mouse_pos):
                        game.enable_deadlock()
                        continue

                    # Clic sur le plateau
                    cell = gui.get_cell_from_mouse(mouse_pos)
                    if not cell:
                        continue

                    r, c = cell

                    # Sélection
                    if gui.selected is None:
                        if game.board[r][c] != "." and rules.is_own_side(r, game.current_player):
                            gui.selected = (r, c)
                    # Déplacement
                    else:
                        r1, c1 = gui.selected
                        if (r, c) == (r1, c1):
                            gui.selected = None
                            continue

                        chosen_move = None
                        for m in game.get_legal_moves(game.current_player):
                            if len(m) == 4 and m == (r1, c1, r, c):
                                chosen_move = m
                                break
                            elif len(m) == 6 and m[1] == r1 and m[2] == c1 and m[3] == r and m[4] == c:
                                chosen_move = m
                                break

                        if chosen_move:
                            game.apply_move(chosen_move)
                            gui.selected = None
                            
                            if game.is_terminal():
                                game_over = True
                                winner = rules.get_winner(game.scores, game.current_player, game.deadlock_active)
                        else:
                            if game.board[r][c] != "." and rules.is_own_side(r, game.current_player):
                                gui.selected = (r, c)
                            else:
                                gui.selected = None

    print("Facteur de branchement moyen :", total_moves / move_count)
    pygame.quit()

if __name__ == "__main__":
    main()