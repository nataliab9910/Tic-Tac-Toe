"""
Konsolowa baza gry
"""

HUMAN, COMPUTER = range(2)
ERROR = -1
SUCCESS = 'SUCCESS'
EMPTY = ' '
BOARD = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']


class Game:
    """
    Przeprowadza rozgrywkę w konsoli
    """

    def __init__(self):
        """
        Konstruktor, tworzy tablicę w konsoli i główne okno gry
        """
        self.board = BOARD
        self.current_player = COMPUTER  # podawać, kto jest pierwszym graczem

    def print_board(self):
        """
        Rysuje plansze w konsoli
        """
        for i in range(3):
            print(' ', self.board[3 * i], ' | ',
                  self.board[1 + 3 * i], ' | ',
                  self.board[2 + 3 * i], sep='')
            if i < 2:
                print("---+---+---")

    # prawdopodobnie do usunięcia
    # def make_move(self):
    #     """
    #     Wykonanie ruchu przez aktualnego gracza
    #     """
    #     self.print_board()
    #
    #     if self.current_player == COMPUTER:
    #         print("Ruch komputera!")
    #         self.computers_move()
    #         self.flip_player()
    #
    #     else:
    #         print("Twój ruch!")
    #         self.humans_move()
    #         self.flip_player()

    def flip_player(self):
        """
        Zmienia gracza, który wykonuje ruch
        """
        self.current_player = {COMPUTER: HUMAN, HUMAN: COMPUTER}[self.current_player]

    def return_current_player(self):
        """
        Zwraca aktualnego gracza
        :return: HUMAN/COMPUTER (0/1)
        """
        return self.current_player == COMPUTER

    def computers_move(self):
        """
        Wykonuje ruch komputera
        :return:
        """
        print("Komputer")
        self.print_board()
        self.flip_player()

    def humans_move(self, position):
        """
        Wykonuje ruch gracza
        :return: prawdopodobnie będzie zwracać informację o wygranej - do przemyślenia
        """
        print("Gracz")

        if count_checkers(self.board, HUMAN) >= 3:
            remove_checker(self.board, position)
            return

        if add_checker(self.board, position) == ERROR:
            return

        for i in range(0, 9):
            if self.board[i] == 'r':
                self.board[i] = EMPTY
                break

        self.print_board()
        self.flip_player()


def count_checkers(board, checker):
    """
    Liczy pionki danego gracza
    :param board: plansza gry
    :param checker: jakie pionki liczyć
    :return: liczba pionków
    """
    number_of_checkers = 0
    for i in range(0, 9):
        if board[i] == checker:
            number_of_checkers += 1
    return number_of_checkers


def remove_checker(board, position):
    """
    Usuwa wskazany pionek gracza
    :param board: plansza gry
    :param position: pozycja, z której pionek chcemy usunąć
    :return:
    """
    if board[position] == HUMAN:
        board[position] = 'r'
    else:
        print("Brak właściwego pionka do usunięcia na wybranej pozycji.")


def add_checker(board, position):
    """
    Stawia pionek na pozycji wskazanej przez gracza
    :param board: plansza gry
    :param position: pozycja, na której chcemy ustawić pionek
    :return: ERROR gdy pozycja jest już zajęta bądź przed chwilą usunęliśmy z niej pionek
    """
    if board[position] == 'r':
        print("Nie możesz postawić pionka w to samo miejsce, z którego go usunąłęś.")
        return ERROR
    elif board[position] == EMPTY:
        board[position] = HUMAN
        return SUCCESS
    else:
        print("Nie możesz postawić pionka na zajętym miejscu.")
        return ERROR
