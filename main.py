"""Uruchamia grę Tic-Tac-Toe."""

import pygame

import window


def main():
    """Wykonuje główną pętlę gry."""

    pygame.init()
    pygame.display.set_caption("TIC-TAC-TOE Game!")
    game_window = window.Window()
    game_window.first_player()
    game_window.draw_board()
    game_window.run()


if __name__ == "__main__":
    main()
