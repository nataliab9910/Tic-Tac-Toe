"""
Okno gry, część graficzna projektu
"""

import pygame
from game import Game

SIZE = 450


class Window:
    """
    Główne okno gry z planszą
    """

    def __init__(self):
        """
        Konstruktor głównego okna gry
        """
        self.window = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("Tic-Tac-Toe Game!")
        self.game = Game()

    def events(self):
        """
        Obsługa kliknięć myszką
        :return: False gdy nastąpiło wyjście z gry, True w pozostałych przypadkach
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.return_actual_player():
                    # jeśli tura komputera - zignoruj kliknięcie
                    continue
                # sprawdzenie pozycji, ustalenie jej przy pomocy numeru 0-8
                position = pygame.mouse.get_pos()
                num_position = Window.position_to_number(position)
                self.game.humans_move(num_position)
                # # Jeśli lewy przycisk - rysuj pionek
                # if pygame.mouse.get_pressed()[0]:
                #     Window.left_button(num_position)
                # # Jeśli prawy przycisk - usuń pionek
                # elif pygame.mouse.get_pressed()[2]:
                #     Window.right_button(num_position)
                print(position)
        return True

    def run_window(self):
        """
        Włączenie i działanie okna gry
        """
        running = True
        while running:
            if self.game.return_actual_player():
                self.game.computers_move()
            running = self.events()

    def draw_lines(self):
        """
        Rysuje planszę do gry
        """
        window_color = (200, 100, 100)
        self.window.fill(window_color)

        lines = [((0, int(SIZE / 3)), (SIZE, int(SIZE / 3))),
                 ((0, 2 * int(SIZE / 3)), (SIZE, 2 * int(SIZE / 3))),
                 ((int(SIZE / 3), 0), (int(SIZE / 3), SIZE)),
                 ((2 * int(SIZE / 3), 0), (2 * int(SIZE / 3), SIZE))]

        line_color = (0, 0, 0)
        line_width = 2

        for line in lines:
            pygame.draw.line(self.window, line_color, line[0], line[1], line_width)

        pygame.display.flip()

    @staticmethod
    def position_to_number(pos):
        """
        Zamienia pozycję kliknięcia myszką na pole planszy numerowane od 0 do 8
        :param pos: miejsce, w które kliknęliśmy myszką w postaci (szerokość, wysokość)
        :return: liczba od 0 do 8 oznaczająca wybrane pole planszy
        """
        pos_width = Window.get_number(pos[0])
        pos_height = Window.get_number(pos[1])

        num_pos = int(3 * pos_height + pos_width)
        print(num_pos)
        return num_pos

    @staticmethod
    def get_number(pos):
        """
        Zmienia pozycję kliknięcia na liczbę od 0 do 2
        :param pos: pozycja kliknięcia
        :return: liczba od 0 do 2
        """
        num = -1
        if 0 <= pos <= SIZE / 3:
            num = 0
        elif SIZE / 3 < pos <= (SIZE * 2) / 3:
            num = 1
        elif (SIZE * 2) / 3 < pos <= SIZE:
            num = 2
        return num

    @staticmethod
    def left_button(pos):
        """
        Umieszcza pionek w wybranym polu planszy
        :param pos: wybrane pole planszy do umieszczenia pionka
        """
        pass

    @staticmethod
    def right_button(pos):
        """
        Usuwa pionek z wybranego pola planszy
        :param pos: wybrane pole planszy do usunięcia pionka
        """
        pass


def board_loop():
    """
    Główna pętla okna gry
    """
    print("1")
    board = Window()
    print("2")
    board.draw_lines()
    print(3)
    board.run_window()
