"""
Uruchomienie gry
"""

import window
import pygame


def main():
    """
    Główna pętla gry
    """
    pygame.init()
    pygame.display.set_caption("TIC-TAC-TOE Game!")
    game_window = window.Window()
    game_window.draw_lines()
    game_window.run()


if __name__ == "__main__":
    main()
