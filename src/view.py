# gui.py

import pygame
import os
from constants import *

class GUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Martian Chess")
        self.title_font = pygame.font.SysFont(None, 40, bold=True)
        self.info_font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.selected = None
        
        #chargement images
        self.piece_images = {}
        target_size = int(CELL_SIZE * 0.9)
        piece_types = [PAWN, DRONE, QUEEN]
        
        for p_type in piece_types:
            path = os.path.join("img", f"{p_type}.png")
            try:
                raw_image = pygame.image.load(path)
                scaled_image = pygame.transform.smoothscale(raw_image, (target_size, target_size))
                self.piece_images[p_type] = scaled_image
            except pygame.error as e:
                print(f"ERREUR : Impossible de charger l'image {path}")
                pygame.quit()
                exit()
                
    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = BOARD_LIGHT if (r + c) % 2 == 0 else BOARD_DARK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

                # Ligne centrale
                if r == MIDLINE:
                    pygame.draw.line(
                        self.screen,
                        BLACK,
                        (0, r * CELL_SIZE),
                        (BOARD_WIDTH, r * CELL_SIZE),
                        5,
                    )

                piece = self.game.board[r][c]
                if piece != EMPTY:
                    self.draw_piece(piece, r, c)

        if self.selected:
            r_start, c_start = self.selected
            valid_moves = self.game.get_legal_moves(self.game.current_player)
            
            for move in valid_moves:
                if len(move) == 4:
                    r1, c1, r2, c2 = move
                else:
                    _, r1, c1, r2, c2, _ = move
                
                # Si le coup part bien de la pièce qu'on a sélectionnée
                if r1 == r_start and c1 == c_start:
                    #centre de la case d'arrivée
                    center_x = c2 * CELL_SIZE + CELL_SIZE // 2
                    center_y = r2 * CELL_SIZE + CELL_SIZE // 2
                    
                    # Dessin du point
                    pygame.draw.circle(
                        self.screen,
                        BLUE,
                        (center_x, center_y),
                        # Rayon du point
                        CELL_SIZE // 12
                    )
            #carré qui encadre la case sélectionnée
            r, c = self.selected
            pygame.draw.rect(
                self.screen,
                BLUE,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                4,
            )

    def draw_piece(self, piece_type, r, c):
        """Affiche l'image de la pièce centrée sur la case"""
        #Récupérer l'image correspondante dans le dictionnaire chargé au début
        image = self.piece_images[piece_type]
        #Obtenir le rectangle de l'image
        rect = image.get_rect()
        #Positionner le centre de ce rectangle au centre de la case cible
        rect.center = (c * CELL_SIZE + CELL_SIZE // 2,
                       r * CELL_SIZE + CELL_SIZE // 2)
        
        #Blit (dessiner) l'image sur l'écran
        self.screen.blit(image, rect)
        
    def draw_ui(self):
        pygame.draw.rect(
            self.screen, (40, 40, 40), # Gris foncé
            (BOARD_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        )

        # séparer le jeu du tableau des scores
        pygame.draw.line(
            self.screen, WHITE,
            (BOARD_WIDTH, 0), (BOARD_WIDTH, WINDOW_HEIGHT), 2
        )
        
        # --- CONTENU DU TEXTE ---
        margin_x = BOARD_WIDTH + 20
        y = 30 

        # Titre
        title = self.title_font.render("Martian Chess", True, WHITE)
        self.screen.blit(title, (margin_x, y))
        y += 60

        # Info Joueur Courant
        turn_text = f"Tour : Joueur {self.game.current_player}"
        color_turn = GREEN if self.game.current_player == 0 else RED 
        
        label_turn = self.info_font.render(turn_text, True, color_turn)
        self.screen.blit(label_turn, (margin_x, y))
        y += 50

        # Scores
        self.screen.blit(self.info_font.render("Scores :", True, WHITE), (margin_x, y))
        y += 35
        
        s0 = self.info_font.render(f"Joueur 0 (Haut) : {self.game.scores[0]}", True, WHITE)
        self.screen.blit(s0, (margin_x, y))
        y += 30
        
        s1 = self.info_font.render(f"Joueur 1 (Bas)  : {self.game.scores[1]}", True, WHITE)
        self.screen.blit(s1, (margin_x, y))
        
        # --- BANQUE DE PIÈCES (CAPTURES) ---
        y += 60
        self.screen.blit(self.info_font.render("Captures :", True, GRAY), (margin_x, y))
        y += 35

        # Fonction interne pour formater le texte (ex: "Queen x1, Pawn x2")
        def get_inventory_text(player_id):
            pieces = self.game.captured_pieces[player_id]
            nb_q = pieces.count(QUEEN)
            nb_d = pieces.count(DRONE)
            nb_p = pieces.count(PAWN)
            
            items = []
            if nb_q > 0: items.append(f"Queen x{nb_q}")
            if nb_d > 0: items.append(f"Drone x{nb_d}")
            if nb_p > 0: items.append(f"Pawn x{nb_p}")
            
            if not items:
                return "Vide"
            return ", ".join(items)

        # Affichage Inventaire Joueur 0
        self.screen.blit(self.small_font.render("J0 a capturé :", True, WHITE), (margin_x, y))
        y += 25
        inv_j0 = get_inventory_text(0)
        self.screen.blit(self.small_font.render(inv_j0, True, GREEN), (margin_x, y))
        
        y += 40 # Espace
        
        # Affichage Inventaire Joueur 1
        self.screen.blit(self.small_font.render("J1 a capturé :", True, WHITE), (margin_x, y))
        y += 25
        inv_j1 = get_inventory_text(1)
        self.screen.blit(self.small_font.render(inv_j1, True, RED), (margin_x, y))

    def get_cell_from_mouse(self, pos):
        x, y = pos
        if x >= BOARD_WIDTH:
            return None
        if y >= BOARD_HEIGHT:
            return None
            
        return y // CELL_SIZE, x // CELL_SIZE

    def update(self):
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_ui()
        pygame.display.flip()


    # À ajouter à la fin de la classe GUI dans view.py

    def draw_game_over(self, winner):
        """Affiche un écran de fin de partie par-dessus le jeu"""
        # 1. Créer un fond noir semi-transparent (Overlay)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200) # Transparence (0-255)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 2. Préparer le message
        if winner is None:
            msg = "MATCH NUL !"
            color = WHITE
            sub_msg = "(Deadlock : 7 tours sans capture)"
        else:
            msg = f"VICTOIRE JOUEUR {winner} !"
            # Vert pour J0, Rouge pour J1
            color = GREEN if winner == 0 else RED
            sub_msg = "Bravo !"

        # 3. Rendu du Texte Principal
        text_surf = self.title_font.render(msg, True, color)
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        
        # Dessiner un cadre autour du texte
        box_rect = text_rect.inflate(60, 60) # Un peu plus grand que le texte
        pygame.draw.rect(self.screen, (60, 60, 60), box_rect) # Fond du cadre gris
        pygame.draw.rect(self.screen, color, box_rect, 4)     # Bordure colorée
        
        self.screen.blit(text_surf, text_rect)

        # 4. Rendu du Sous-titre
        sub_surf = self.small_font.render(sub_msg, True, WHITE)
        sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(sub_surf, sub_rect)
        
        # 5. Message pour quitter
        quit_msg = self.small_font.render("Cliquez pour fermer le jeu", True, GRAY)
        quit_rect = quit_msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(quit_msg, quit_rect)

        # Mettre à jour l'écran
        pygame.display.flip()