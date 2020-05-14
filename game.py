"""
Konsolowa baza gry
"""

import time

HUMAN, COMPUTER = range(2)
NO_WINNER = -1
ERROR = -1
SUCCESS = 'SUCCESS'
EMPTY = ' '
BOARD = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']
MAX_WAITING_TIME = 5
WIN_SCORE = 100
LOSE_SCORE = -100
INFINITY = 10000


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
        :return: prawdopodobnie zwróci info o wygranej - do przemyślenia
        """

        print("Komputer")

        depth = 0
        best_score = -INFINITY
        best_remove_pos = best_add_pos = -1
        all_waiting = actual_waiting = previous_waiting = 0
        rate = 1

        # tablica do sprawdzania kolejnych ustwień pionków
        copy_board = self.board.copy()
        print("Zaczyna")
        if count_checkers(copy_board, COMPUTER) >= 3:
            # usuwa pionek, potem dodaje
            while all_waiting + actual_waiting * rate < MAX_WAITING_TIME and best_score < WIN_SCORE:
                start_timer = time.time()
                for remove_pos in [pos for pos in range(9) if copy_board[pos] == COMPUTER]:
                    copy_board[remove_pos] = EMPTY
                    for add_pos in [pos for pos in range(9) if
                                    copy_board[pos] == EMPTY and pos != remove_pos]:
                        copy_board[add_pos] = COMPUTER
                        score = minimax(depth, copy_board, HUMAN) + depth
                        if score > best_score:
                            best_score = score
                            best_remove_pos = remove_pos
                            best_add_pos = add_pos
                        copy_board[add_pos] = EMPTY
                    copy_board[remove_pos] = COMPUTER
                end_timer = time.time()
                previous_waiting = actual_waiting
                actual_waiting = end_timer - start_timer
                all_waiting += actual_waiting
                if previous_waiting > 0:
                    rate = actual_waiting / previous_waiting
                else:
                    rate = 1
                depth += 1
            self.board[best_remove_pos] = EMPTY
            self.board[best_add_pos] = COMPUTER
        else:
            # dodaje pionek
            while all_waiting + actual_waiting * rate < MAX_WAITING_TIME and best_score < WIN_SCORE:
                start_timer = time.time()
                for add_pos in [pos for pos in range(9) if copy_board[pos] == EMPTY]:
                    copy_board[add_pos] = COMPUTER
                    score = minimax(depth, copy_board, HUMAN) + depth
                    if score > best_score:
                        best_score = score
                        best_add_pos = add_pos
                    copy_board[add_pos] = EMPTY
                end_timer = time.time()
                previous_waiting = actual_waiting
                actual_waiting = end_timer - start_timer
                all_waiting += actual_waiting
                if previous_waiting > 0:
                    rate = actual_waiting / previous_waiting
                else:
                    rate = 1
                depth += 1
            self.board[best_add_pos] = COMPUTER
        ###
        print("Depth = ", depth, sep='')
        ###
        self.flip_player()
        self.print_board()

    def humans_move(self, position):
        """
        Wykonuje ruch gracza
        :return: prawdopodobnie będzie zwracać informację o wygranej - do przemyślenia
        """
        print("Gracz")

        # if count_checkers(self.board, HUMAN) >= 3:
        if len([i for i in self.board if i == HUMAN]) >= 3:
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


def minimax(depth, board, next_player):
    """
    Ocenia możliwe ruchy komputera tak, aby móc wyłonić ten najlepszy
    :param depth: maksymalna głębokość, na której będzie sprawdzał kombinacje
    :param board: plansza gry
    :param next_player: gracz, który będzie wykonywał następny ruch
    :return: ocena ruchu komputera
    """
    if depth == 0 or check_winner(board) != NO_WINNER:
        return evaluate(board)

    if next_player == COMPUTER:
        evaluation = -INFINITY
    else:
        evaluation = INFINITY

    if count_checkers(board, next_player) >= 3:
        for remove_pos in [pos for pos in range(9) if board[pos] == next_player]:
            board[remove_pos] = EMPTY
            evaluation = minimax_add(depth, board, next_player, evaluation, remove_pos)
            board[remove_pos] = next_player
    else:
        evaluation = minimax_add(depth, board, next_player, evaluation)
    return evaluation


def minimax_add(depth, board, next_player, evaluation, remove_pos=-1):
    """
    Szuka najlepszego miejsca na planszy na dodanie pionka komputera
    :param depth: maksymalna głębokość, na której będzie sprawdzał kombinacje
    :param board: plansza gry
    :param next_player: gracz, który będzie wykonywał następny ruch
    :param evaluation: aktualna ocena ruchu
    :param remove_pos: miejsce, z którego w tym samym ruchu został usunięty pionek
    :return: uaktualniona ocena ruchu
    """
    for add_pos in [pos for pos in range(9) if board[pos] == EMPTY and pos != remove_pos]:
        board[add_pos] = next_player
        if next_player == COMPUTER:
            score = minimax(depth - 1, board, HUMAN)
            if score > evaluation:
                evaluation = score
        else:
            score = minimax(depth - 1, board, COMPUTER)
            if score < evaluation:
                evaluation = score
        board[add_pos] = EMPTY
    return evaluation


def evaluate(board):
    """
    Ocenia aktualny stan planszy z punktu widzenia komputera
    :param board: plansza gry
    :return: WIN_SCORE jeśli wygra komputer, LOSE_SCORE - człowiek, NO_WINNER - nikt
    """
    if check_winner(board) == COMPUTER:
        score = WIN_SCORE
    elif check_winner(board) == HUMAN:
        score = LOSE_SCORE
    else:
        score = NO_WINNER
    return score


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
        return_val = ERROR
    elif board[position] == EMPTY:
        board[position] = HUMAN
        return_val = SUCCESS
    else:
        print("Nie możesz postawić pionka na zajętym miejscu.")
        return_val = ERROR
    return return_val


def check_winner(board):
    """
    Sprawdza czy ktoś ułożył zwycięską kombinację
    :param board: plansza gry
    :return: zwycięzca albo NO_WINNER
    """
    winner = check_columns(board)
    if winner == NO_WINNER:
        winner = check_rows(board)
        if winner == NO_WINNER:
            winner = check_diagonals(board)
    return winner


def check_columns(board):
    """
    Sprawdza czy w kolumnie została ułożona zwycięska kombinacja
    :param board: plansza gry
    :return: zwycięzca albo NO_WINNER
    """
    for i in range(0, 3):
        if board[i] == board[3 + i] == board[6 + i] != EMPTY:
            return board[i]
    return NO_WINNER


def check_rows(board):
    """
    Sprawdza czy w rzędie została ułożona zwycięska kombinacja
    :param board: plansza gry
    :return: zwycięzca albo NO_WINNER
    """
    for i in range(0, 3):
        if board[3 * i] == board[1 + 3 * i] == board[2 + 3 * i] != EMPTY:
            return board[3 * i]
    return NO_WINNER


def check_diagonals(board):
    """
    Sprawdza czy na przekątnej została ułożona zwycięska kombinacja
    :param board: plansza gry
    :return: zwycięzca albo NO_WINNER
    """
    if board[0] == board[4] == board[8] != EMPTY:
        return board[0]
    if board[2] == board[4] == board[6] != EMPTY:
        return board[2]
    return NO_WINNER
