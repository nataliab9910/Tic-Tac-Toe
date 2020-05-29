"""Część graficzna projektu, określa działania na oknie gry."""

import os
import sys

import pygame

import game as g

BOARD_WIDTH = 450
BOARD_HEIGHT = 450
TEXT_AREA_HEIGHT = 50

LINES = [((0, int(BOARD_WIDTH / 3)), (BOARD_WIDTH, int(BOARD_WIDTH / 3))),
         ((0, 2 * int(BOARD_WIDTH / 3)),
          (BOARD_WIDTH, 2 * int(BOARD_WIDTH / 3))),
         ((int(BOARD_WIDTH / 3), 0), (int(BOARD_WIDTH / 3), BOARD_WIDTH)),
         ((2 * int(BOARD_WIDTH / 3), 0),
          (2 * int(BOARD_WIDTH / 3), BOARD_WIDTH))]
LINE_WIDTH = 2

COLORS = {'SALMON': pygame.Color("salmon"), 'BLACK': pygame.Color("black")}
CHECKERS = {'HUMAN': pygame.image.load(os.path.join('.', 'O.png')),
            'COMPUTER': pygame.image.load(os.path.join('.', 'X.png'))}
CHECKER_WIDTH = 150
CHECKER_HEIGHT = 150

FONT_STYLE = 'freesansbold.ttf'
FONT_SIZES = {'SMALL': 21, 'MEDIUM': 25, 'BIG': 31, 'LARGE': 35}

ERROR = -1


class Window:
    """Implementuje główne okno gry z planszą."""

    def __init__(self):
        """Konstruktor głównego okna gry."""

        self.window = pygame.display.set_mode(
            (BOARD_WIDTH, BOARD_HEIGHT + TEXT_AREA_HEIGHT))
        self.game = g.Game()

    def run(self):
        """Określa działanie okna gry."""

        while True:
            if self.game.current_player == g.COMPUTER:
                self.game.computers_move()
            elif self.game.current_player == g.HUMAN:
                # sprawdzenie pozycji, ustalenie jej przy pomocy numeru 0-8
                position = Window.event()
                position_number = Window.position_to_number(position)
                if position_number == ERROR:
                    continue
                self.game.humans_move(position_number)
            self.draw_board()

            if self.game.current_player == g.COMPUTER_WIN:
                self.show_text(' Wygrywa komputer! ', FONT_SIZES['BIG'],
                               (int(BOARD_WIDTH // 2), int(BOARD_WIDTH // 2)),
                               (COLORS['SALMON'], COLORS['BLACK']))
            elif self.game.current_player == g.HUMAN_WIN:
                self.show_text(' Wygrywasz! Gratulacje! ', FONT_SIZES['BIG'],
                               (int(BOARD_WIDTH // 2), int(BOARD_WIDTH // 2)),
                               (COLORS['SALMON'], COLORS['BLACK']))
            pygame.display.update()

            if self.game.current_player not in (g.COMPUTER, g.HUMAN):
                Window.event()
                self.game.reset()
                self.first_player()
                self.draw_board()

    def draw_board(self):
        """Rysuje planszę do gry."""

        self.window.fill(COLORS['SALMON'])

        for line in LINES:
            pygame.draw.line(self.window, COLORS['BLACK'], line[0], line[1],
                             LINE_WIDTH)

        for pos in range(9):
            if self.game.board[pos] == g.HUMAN:
                column, row = Window.number_to_position(pos)
                self.window.blit(CHECKERS['HUMAN'], (column, row))
            elif self.game.board[pos] == g.COMPUTER:
                column, row = Window.number_to_position(pos)
                self.window.blit(CHECKERS['COMPUTER'], (column, row))

        if self.game.current_player == g.COMPUTER:
            text = 'Ruch komputera'
        elif self.game.current_player == g.HUMAN:
            text = 'Twój ruch'
        else:
            text = 'Kliknij na planszę, aby zagrać ponownie.'
        self.show_text(text, FONT_SIZES['SMALL'],
                       (BOARD_WIDTH // 2, BOARD_WIDTH + 25))

        pygame.display.flip()

    def first_player(self):
        """Tworzy widok wyboru, kto zaczyna grę i ustawia pierwszego gracza."""

        self.window.fill(COLORS['SALMON'])

        self.show_text('Kto zaczyna?', FONT_SIZES['LARGE'],
                       (BOARD_WIDTH / 2, (BOARD_HEIGHT + TEXT_AREA_HEIGHT) / 5))
        self.show_text('JA', FONT_SIZES['MEDIUM'], (
            (BOARD_WIDTH / 4), BOARD_HEIGHT / 3 + CHECKER_HEIGHT + 20))
        self.show_text('KOMPUTER', FONT_SIZES['MEDIUM'], (
            (BOARD_WIDTH / 4) * 3, BOARD_HEIGHT / 3 + CHECKER_HEIGHT + 20))

        self.window.blit(CHECKERS['HUMAN'], (
            BOARD_WIDTH / 4 - CHECKER_WIDTH / 2, BOARD_HEIGHT / 3))
        self.window.blit(CHECKERS['COMPUTER'], (
            (BOARD_WIDTH / 4) * 3 - CHECKER_WIDTH / 2, BOARD_HEIGHT / 3))
        pygame.display.update()

        position = Window.event()
        if position[0] < BOARD_WIDTH / 2:
            self.game.current_player = g.HUMAN
        else:
            self.game.current_player = g.COMPUTER

    def show_text(self, text, size, position,
                  colors=(COLORS['BLACK'], COLORS['SALMON'])):
        """Wypisuje tekst w oknie gry.

        :param text: tekst do wypisania,
        :param size: rozmiar czcionki
        :param position: pozycja w oknie gry postaci (szerokość, wysokość),
        :param colors: kolor tekstu i tła, domyślnie (BLACK, SALMON).
        """

        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(text, True, colors[0], colors[1])
        text_rect = text.get_rect()
        text_rect.center = position
        self.window.blit(text, text_rect)

    @staticmethod
    def event():
        """Obsługuje kliknięcia myszką.

        :return: pozycja kliknięcia, jeśli nie nastąpiło wyjście z gry.
        """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return pygame.mouse.get_pos()

    @staticmethod
    def position_to_number(pos):
        """Zamienia pozycję kliknięcia na pole planszy numerowane od 0 do 8.

        :param pos: pozycja kliknięcia w postaci (szerokość, wysokość).
        :return: liczba od 0 do 8, oznaczająca wybrane pole planszy.
        """

        pos_width = Window.get_number(pos[0])
        pos_height = Window.get_number(pos[1])

        if ERROR in [pos_width, pos_height]:
            return ERROR

        num_pos = int(3 * pos_height + pos_width)

        return num_pos

    @staticmethod
    def number_to_position(num):
        """Zamienia numer pozycji na planszy w konsoli na pozycję w oknie gry.

        :param num: pozycja na planszy w konsoli, od 0 do 8.
        :return: współrzędne lewego górnego rogu pola planszy w oknie gry.
        """

        pos_width = int(num % 3) * int(BOARD_HEIGHT // 3)
        pos_height = int(num // 3) * int(BOARD_HEIGHT // 3)

        return pos_width, pos_height

    @staticmethod
    def get_number(pos, size=BOARD_WIDTH):
        """Zmienia pozycję kliknięcia na liczbę od 0 do 2.

        :param size: wymiar siatki.
        :param pos: pozycja kliknięcia.
        :return: liczba od 0 do 2.
        """

        num = ERROR
        if 0 <= pos <= size / 3:
            num = 0
        elif size / 3 < pos <= (size * 2) / 3:
            num = 1
        elif (size * 2) / 3 < pos <= size:
            num = 2
        return num
