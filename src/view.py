# gui.py

import pygame
from constants import *

class GUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT + UI_HEIGHT)
        )
        pygame.display.set_caption("Martian Chess")
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 28)
        self.selected = None

    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if (r + c) % 2 == 0 else GRAY
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
                        (WINDOW_WIDTH, r * CELL_SIZE),
                        3,
                    )

                piece = self.game.board[r][c]
                if piece != EMPTY:
                    self.draw_piece(piece, r, c)

        if self.selected:
            r, c = self.selected
            pygame.draw.rect(
                self.screen,
                BLUE,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                4,
            )

    def draw_piece(self, piece, r, c):
        color = BLACK if r < MIDLINE else RED
        text = self.font.render(piece, True, color)
        rect = text.get_rect(
            center=(c * CELL_SIZE + CELL_SIZE // 2,
                    r * CELL_SIZE + CELL_SIZE // 2)
        )
        self.screen.blit(text, rect)

    def draw_ui(self):
        pygame.draw.rect(
            self.screen, BLACK,
            (0, WINDOW_HEIGHT, WINDOW_WIDTH, UI_HEIGHT)
        )

        s0 = self.small_font.render(
            f"Joueur 0 : {self.game.scores[0]}", True, WHITE)
        s1 = self.small_font.render(
            f"Joueur 1 : {self.game.scores[1]}", True, WHITE)
        turn = self.small_font.render(
            f"Tour : Joueur {self.game.current_player}", True, WHITE)

        self.screen.blit(s0, (20, WINDOW_HEIGHT + 10))
        self.screen.blit(s1, (200, WINDOW_HEIGHT + 10))
        self.screen.blit(turn, (20, WINDOW_HEIGHT + 40))

    def get_cell_from_mouse(self, pos):
        x, y = pos
        if y >= WINDOW_HEIGHT:
            return None
        return y // CELL_SIZE, x // CELL_SIZE

    def update(self):
        self.screen.fill(BLACK)
        self.draw_board()
        self.draw_ui()
        pygame.display.flip()
