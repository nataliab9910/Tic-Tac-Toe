"""
Okno gry, część graficzna projektu
"""

import pygame
import game

BOARD_WIDTH = 450
BOARD_HEIGHT = 450
ERROR = -1
LINES = [((0, int(BOARD_WIDTH / 3)), (BOARD_WIDTH, int(BOARD_WIDTH / 3))),
         ((0, 2 * int(BOARD_WIDTH / 3)), (BOARD_WIDTH, 2 * int(BOARD_WIDTH / 3))),
         ((int(BOARD_WIDTH / 3), 0), (int(BOARD_WIDTH / 3), BOARD_WIDTH)),
         ((2 * int(BOARD_WIDTH / 3), 0), (2 * int(BOARD_WIDTH / 3), BOARD_WIDTH))]
WINDOW_COLOR = (200, 100, 100)
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 2


class Window:
    """
    Główne okno gry z planszą
    """

    def __init__(self):
        """
        Konstruktor głównego okna gry
        """
        self.window = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.game = game.Game()

    def events(self):
        """
        Obsługa kliknięć myszką
        :return: False gdy nastąpiło wyjście z gry, True w pozostałych przypadkach
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.return_current_player():
                    # jeśli tura komputera - zignoruj kliknięcie
                    continue
                # sprawdzenie pozycji, ustalenie jej przy pomocy numeru 0-8
                position = pygame.mouse.get_pos()
                num_position = Window.position_to_number(position)
                if num_position == ERROR:
                    continue
                self.game.humans_move(num_position)
                # prawdopodobnie do usunięcia
                # # Jeśli lewy przycisk - rysuj pionek
                # if pygame.mouse.get_pressed()[0]:
                #     Window.left_button(num_position)
                # # Jeśli prawy przycisk - usuń pionek
                # elif pygame.mouse.get_pressed()[2]:
                #     Window.right_button(num_position)
                print(position)
        return True

    def run(self):
        """
        Włączenie i działanie okna gry
        """
        running = True
        while running:
            if self.game.return_current_player():
                self.game.computers_move()
            running = self.events()

    def draw_lines(self):
        """
        Rysuje planszę do gry
        """

        self.window.fill(WINDOW_COLOR)

        for line in LINES:
            pygame.draw.line(self.window, LINE_COLOR, line[0], line[1], LINE_WIDTH)

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

        if ERROR in [pos_width, pos_height]:
            return ERROR

        num_pos = int(3 * pos_height + pos_width)
        print(num_pos)
        return num_pos

    @staticmethod
    def get_number(pos, size=BOARD_WIDTH):
        """
        Zmienia pozycję kliknięcia na liczbę od 0 do 2
        :param size: wymiar siatki
        :param pos: pozycja kliknięcia
        :return: liczba od 0 do 2
        """
        num = ERROR
        if 0 <= pos <= size / 3:
            num = 0
        elif size / 3 < pos <= (size * 2) / 3:
            num = 1
        elif (size * 2) / 3 < pos <= size:
            num = 2
        return num

    # prawdopodobnie do usunięcia
    # @staticmethod
    # def left_button(pos):
    #     """
    #     Umieszcza pionek w wybranym polu planszy
    #     :param pos: wybrane pole planszy do umieszczenia pionka
    #     """
    #     pass
    #
    # @staticmethod
    # def right_button(pos):
    #     """
    #     Usuwa pionek z wybranego pola planszy
    #     :param pos: wybrane pole planszy do usunięcia pionka
    #     """
    #     pass
