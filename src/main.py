# main.py

import pygame
from model import GameState
from view import GUI

def main():
    game = GameState()
    gui = GUI(game)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        gui.update()

        if game.is_terminal():
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = gui.get_cell_from_mouse(pygame.mouse.get_pos())
                if not cell:
                    continue

                r, c = cell

                if gui.selected is None:
                    if game.board[r][c] != ".":
                        gui.selected = (r, c)
                else:
                    r1, c1 = gui.selected
                    chosen_move = None

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

                    gui.selected = None

    pygame.quit()

if __name__ == "__main__":
    main()
