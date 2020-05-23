"""Część graficzna projektu, określa działania na oknie gry."""

import os

import pygame

import game as g

# pygame.init()

BOARD_WIDTH = 450
BOARD_HEIGHT = 450

LINES = [((0, int(BOARD_WIDTH / 3)), (BOARD_WIDTH, int(BOARD_WIDTH / 3))),
         ((0, 2 * int(BOARD_WIDTH / 3)),
          (BOARD_WIDTH, 2 * int(BOARD_WIDTH / 3))),
         ((int(BOARD_WIDTH / 3), 0), (int(BOARD_WIDTH / 3), BOARD_WIDTH)),
         ((2 * int(BOARD_WIDTH / 3), 0),
          (2 * int(BOARD_WIDTH / 3), BOARD_WIDTH))]

WINDOW_COLOR = pygame.Color("salmon")
LINE_COLOR = pygame.Color("black")
LINE_WIDTH = 2
# FONT = pygame.font.Font('freesansbold.ttf', 32)
# FONT2 = pygame.font.Font('freesansbold.ttf', 16)

CHECKER_HUMAN = pygame.image.load(os.path.join('.', 'O.png'))
CHECKER_COMPUTER = pygame.image.load(os.path.join('.', 'X.png'))

ERROR = -1


class Window:
    """Implementuje główne okno gry z planszą."""

    def __init__(self):
        """Konstruktor głównego okna gry."""
        self.window = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT + 50))
        self.game = g.Game()

    def events(self):
        """Obsługuje kliknięcia myszką.

        :return: False - nastąpiło wyjście z gry, jeśli nie - True.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.current_player == g.COMPUTER:
                    # jeśli tura komputera - zignoruj kliknięcie
                    continue
                elif self.game.current_player == g.HUMAN:
                    # sprawdzenie pozycji, ustalenie jej przy pomocy numeru 0-8
                    position = pygame.mouse.get_pos()
                    num_position = Window.position_to_number(position)
                    if num_position == ERROR:
                        continue
                    self.game.humans_move(num_position)
                    self.draw_board()
                elif self.game.current_player not in (g.COMPUTER, g.HUMAN):
                    self.game.reset()
                    self.first_player()
                    self.draw_board()
                # prawdopodobnie do usunięcia
                # # Jeśli lewy przycisk - rysuj pionek
                # if pygame.mouse.get_pressed()[0]:
                #     Window.left_button(num_position)
                # # Jeśli prawy przycisk - usuń pionek
                # elif pygame.mouse.get_pressed()[2]:
                #     Window.right_button(num_position)
                # print(position)
        return True

    def run(self):
        """Określa działanie okna gry."""
        running = True
        while running:
            if self.game.current_player == g.COMPUTER:
                self.game.computers_move()
                self.draw_board()
            elif self.game.current_player == g.COMPUTER + 2:
                FONT = pygame.font.Font('freesansbold.ttf', 32)
                text = FONT.render('Wygrywa komputer!', True, WINDOW_COLOR,
                                   LINE_COLOR)
                textRect = text.get_rect()
                textRect.center = (int(BOARD_WIDTH // 2), int(BOARD_WIDTH // 2))
                self.window.blit(text, textRect)
                pygame.display.update()
            elif self.game.current_player == g.HUMAN + 2:
                FONT = pygame.font.Font('freesansbold.ttf', 32)
                text = FONT.render('Wygrywasz! Gratulacje!', True, WINDOW_COLOR,
                                   LINE_COLOR)
                textRect = text.get_rect()
                textRect.center = (int(BOARD_WIDTH // 2), int(BOARD_WIDTH // 2))
                self.window.blit(text, textRect)
                pygame.display.update()
            running = self.events()

    def draw_board(self):
        """Rysuje planszę do gry."""
        self.window.fill(WINDOW_COLOR)

        for line in LINES:
            pygame.draw.line(self.window, LINE_COLOR, line[0], line[1],
                             LINE_WIDTH)

        for pos in range(9):
            # print(self.game.board[pos])
            if self.game.board[pos] == g.HUMAN:
                col, row = Window.number_to_position(pos)
                # print('hum', row, col)
                self.window.blit(CHECKER_HUMAN, (col, row))
            elif self.game.board[pos] == g.COMPUTER:
                col, row = Window.number_to_position(pos)
                # print('com', row, col)
                self.window.blit(CHECKER_COMPUTER, (col, row))

        if self.game.current_player == g.COMPUTER:
            text = 'Ruch komputera'
        elif self.game.current_player == g.HUMAN:
            text = 'Twój ruch'
        else:
            text = 'Kliknij na planszę, aby zagrać ponownie.'
        FONT2 = pygame.font.Font('freesansbold.ttf', 16)
        text = FONT2.render(text, True, LINE_COLOR,
                            WINDOW_COLOR)
        textRect = text.get_rect()
        textRect.center = (BOARD_WIDTH // 2, BOARD_WIDTH + 25)
        self.window.blit(text, textRect)
        pygame.display.update()

        pygame.display.flip()

    def first_player(self):
        self.window.fill(WINDOW_COLOR)
        FONT = pygame.font.Font('freesansbold.ttf', 35)
        text = FONT.render('Kto zaczyna?', True, LINE_COLOR,
                            WINDOW_COLOR)
        textRect = text.get_rect()
        textRect.center = (BOARD_WIDTH/2, 100)
        self.window.blit(text, textRect)
        FONT = pygame.font.Font('freesansbold.ttf', 25)
        text1 = FONT.render('JA', True, LINE_COLOR,
                            WINDOW_COLOR)
        textRect = text1.get_rect()
        textRect.center = (125, 320)
        self.window.blit(text1, textRect)
        self.window.blit(CHECKER_HUMAN, (50, 150))
        text2 = FONT.render('KOMPUTER', True, LINE_COLOR,
                            WINDOW_COLOR)
        textRect2 = text2.get_rect()
        textRect2.center = (325, 320)
        self.window.blit(text2, textRect2)
        self.window.blit(CHECKER_COMPUTER,
                         (250, 150))
        pygame.display.update()

        pygame.display.flip()

        choosen = False
        while not choosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if position[0] < BOARD_WIDTH / 2:
                        self.game.current_player = g.HUMAN
                    else:
                        self.game.current_player = g.COMPUTER
                    choosen = True

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
        # print(num_pos)
        return num_pos

    @staticmethod
    def number_to_position(num):
        """Zamienia numer pozycji na planszy w konsoli na pozycję w oknie gry.

        :param num: pozycja na planszy w konsoli, od 0 do 8.
        :return: współrzędne lewego górnego rogu pola planszy w oknie gry.
        """
        pos_width = int(num % 3) * 150
        pos_height = int(num // 3) * 150

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
