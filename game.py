"""Część konsolowa projektu, określa logikę gry."""

import time

import random

BOARD = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']

HUMAN, COMPUTER, HUMAN_WIN, COMPUTER_WIN = range(4)
EMPTY = ' '

NO_WINNER = -1
ERROR = -1
SUCCESS = 'SUCCESS'

MAX_WAITING_SEC = 5
WIN_SCORE = 100
LOSE_SCORE = -100
INFINITY = 10000
FIELDS_IN_ROW = 3
FIELDS_IN_BOARD = 9


class Waiting:
    """Zapisuje czasy oczekiwania."""

    # pylint: disable=too-few-public-methods
    def __init__(self):
        """Inicjalizuje zerami wartości oczekiwania."""
        self.expected = 0  # oczekiwany przyszły czas oczekiwania
        self.all = 0  # sumaryczny czas oczekiwania
        self.current = 0  # aktualny (ostatni) czas oczekiwania
        self.previous = 0  # poprzedni czas oczekiwania


class Game:
    """Przeprowadza rozgrywkę w konsoli."""

    def __init__(self):
        """Tworzy tablicę rozgrywki w konsoli i główne okno gry."""

        self.board = BOARD[:]
        self.current_player = COMPUTER

    def print_board(self):
        """Rysuje planszę w konsoli."""

        for i in range(FIELDS_IN_ROW):
            print(f' {self.board[FIELDS_IN_ROW * i]} | '
                  f'{self.board[1 + FIELDS_IN_ROW * i]} | '
                  f'{self.board[2 + FIELDS_IN_ROW * i]}')
            if i < 2:
                print('---+---+---')

    def flip_player(self):
        """Zmienia gracza, który wykonuje ruch."""

        if self.current_player in (HUMAN, COMPUTER):
            self.current_player = {COMPUTER: HUMAN, HUMAN: COMPUTER}[
                self.current_player]

    def humans_move(self, position):
        """Wykonuje ruch gracza."""

        print('Gracz')

        if Game.count_checkers(self.board, HUMAN) >= FIELDS_IN_ROW:
            Game.remove_checker(self.board, position)
            return

        if Game.add_checker(self.board, position) == ERROR:
            return

        for i in range(0, FIELDS_IN_BOARD):
            if self.board[i] == 'r':
                self.board[i] = EMPTY
                break

        self.print_board()

        win = Game.check_winner(self.board)
        if win != NO_WINNER:
            self.current_player = HUMAN_WIN
            print('Wygrywasz!')
            return

        self.flip_player()

    @staticmethod
    def remove_checker(board, position):
        """Usuwa pionek gracza z wskazanej pozycji na planszy.

        Jeśli na danej pozycji planszy nie ma właściwego pionka, wypisuje
        informację o źle wybranej pozycji i nie zmienia stanu planszy.
        :param board: plansza gry,
        :param position: pozycja, z której chcemy usunąć pionek.
        """

        if board[position] == HUMAN:
            board[position] = 'r'
        else:
            print("Brak właściwego pionka do usunięcia na wybranej pozycji.")

    @staticmethod
    def add_checker(board, position):
        """Stawia pionek na pozycji na planszy wskazanej przez gracza.

        Jeśli wybrana pozycja nie jest pusta lub w tym samym ruchu gracz usunął
        z niej pionek, wypisuje informację o źle wybranej pozycji, zwraca błąd
        i nie zmienia stanu planszy.
        :param board: plansza gry,
        :param position: pozycja, na której chcemy ustawić pionek,
        :return: jeśli wybrano właściwą pozycję - SUCCESS, jeśli nie - ERROR.
        """

        if board[position] == 'r':
            print('Nie możesz postawić pionka w to samo miejsce, '
                  'z którego go usunąłęś.')
            return_val = ERROR
        elif board[position] == EMPTY:
            board[position] = HUMAN
            return_val = SUCCESS
        else:
            print("Nie możesz postawić pionka na zajętym miejscu.")
            return_val = ERROR

        return return_val

    def computers_move(self):
        """Wykonuje ruch komputera."""

        print('Komputer')

        depth = 0
        best_score = -INFINITY
        best_remove_pos = best_add_pos = -1
        waiting = Waiting()

        # tablica do sprawdzania kolejnych ustawień pionków
        copy_board = self.board[:]

        if Game.count_checkers(copy_board, COMPUTER) >= FIELDS_IN_ROW:
            # usuwa pionek i przestawia go w inne miejsce
            while (waiting.all + waiting.expected < MAX_WAITING_SEC
                   and best_score < WIN_SCORE):

                waiting.previous = waiting.current
                waiting.current = time.time()

                for remove_pos in [pos for pos in range(FIELDS_IN_BOARD) if
                                   copy_board[pos] == COMPUTER]:
                    copy_board[remove_pos] = EMPTY

                    empty_positions = [pos for pos in range(FIELDS_IN_BOARD) if
                                       (copy_board[pos] == EMPTY
                                        and pos != remove_pos)]
                    for add_pos in random.sample(empty_positions,
                                                 len(empty_positions)):
                        copy_board[add_pos] = COMPUTER
                        score = Game.minimax(depth, copy_board, HUMAN) + depth
                        if score > best_score:
                            best_score = score
                            best_remove_pos = remove_pos
                            best_add_pos = add_pos
                        copy_board[add_pos] = EMPTY
                    copy_board[remove_pos] = COMPUTER

                waiting.current = time.time() - waiting.current
                waiting.all += waiting.current
                waiting.expected = Game.waiting_evaluate(waiting.previous,
                                                         waiting.current)

                depth += 1
            self.board[best_remove_pos] = EMPTY
            self.board[best_add_pos] = COMPUTER

        else:
            # tylko dodaje pionek
            while (waiting.all + waiting.expected < MAX_WAITING_SEC
                   and best_score < WIN_SCORE):

                waiting.previous = waiting.current
                waiting.current = time.time()
                empty_positions = [pos for pos in range(FIELDS_IN_BOARD) if
                                   copy_board[pos] == EMPTY]
                for add_pos in random.sample(empty_positions,
                                             len(empty_positions)):
                    copy_board[add_pos] = COMPUTER
                    score = Game.minimax(depth, copy_board, HUMAN) + depth
                    if score > best_score:
                        best_score = score
                        best_add_pos = add_pos
                    copy_board[add_pos] = EMPTY

                waiting.current = time.time() - waiting.current
                waiting.all += waiting.current
                waiting.expected = Game.waiting_evaluate(waiting.previous,
                                                         waiting.current)

                depth += 1

            self.board[best_add_pos] = COMPUTER

        del waiting

        print(f'Głębokość = {depth}')
        self.print_board()

        win = Game.check_winner(self.board)
        if win != NO_WINNER:
            self.current_player = COMPUTER_WIN
            print('Wygrywa komputer!')
            return

        self.flip_player()

    @staticmethod
    def waiting_evaluate(previous, current):
        """Przybliża kolejnego wykonania pętli na podstawie dwóch poprzednich.

        :param previous: czas przedostatniego wykonania pętli,
        :param current: czas ostatniego wykonania pętli,
        :return:
        """

        if previous == 0:
            expected = current
        else:
            expected = current * (current / previous)

        return expected

    @staticmethod
    def minimax(depth, board, next_player):
        """Ocenia możliwe ruchy komputera tak, aby móc wyłonić ten najlepszy.

        :param depth: maksymalna głębokość przewidywania ruchów,
        :param board: plansza gry,
        :param next_player: gracz, który będzie wykonywał następny ruch,
        :return: ocena ruchu komputera.
        """

        if depth == 0 or Game.check_winner(board) != NO_WINNER:
            return Game.evaluate(board)

        if next_player == COMPUTER:
            evaluation = -INFINITY
        else:
            evaluation = INFINITY

        if Game.count_checkers(board, next_player) >= FIELDS_IN_ROW:
            for remove_pos in [pos for pos in range(FIELDS_IN_BOARD) if
                               board[pos] == next_player]:
                board[remove_pos] = EMPTY
                evaluation = Game.minimax_add(depth, board, next_player,
                                              evaluation, remove_pos)
                board[remove_pos] = next_player
        else:
            evaluation = Game.minimax_add(depth, board, next_player, evaluation)
        return evaluation

    @staticmethod
    def minimax_add(depth, board, next_player, evaluation, remove_pos=-1):
        """Szuka najlepszego miejsca na planszy na dodanie pionka komputera.

        :param depth: maksymalna głębokość przewidywania ruchów,
        :param board: plansza gry,
        :param next_player: gracz, który będzie wykonywał następny ruch,
        :param evaluation: aktualna ocena ruchu,
        :param remove_pos: miejsce, z którego w tym samym ruchu usunięto pionek,
        :return: uaktualniona ocena ruchu.
        """

        for add_pos in [pos for pos in range(FIELDS_IN_BOARD) if
                        board[pos] == EMPTY and pos != remove_pos]:
            board[add_pos] = next_player
            if next_player == COMPUTER:
                score = Game.minimax(depth - 1, board, HUMAN)
                if score > evaluation:
                    evaluation = score
            else:
                score = Game.minimax(depth - 1, board, COMPUTER)
                if score < evaluation:
                    evaluation = score
            board[add_pos] = EMPTY
        return evaluation

    @staticmethod
    def evaluate(board):
        """Ocenia aktualny stan gry z punktu widzenia komputera.

        :param board: plansza z aktualnym stanem gry,
        :return: informacja o wygranej: WIN_SCORE - komputer,
                                        LOSE_SCORE - człowiek,
                                        NO_WINNER - nikt.
        """

        if Game.check_winner(board) == COMPUTER:
            score = WIN_SCORE
        elif Game.check_winner(board) == HUMAN:
            score = LOSE_SCORE
        else:
            score = NO_WINNER
        return score

    @staticmethod
    def count_checkers(board, checker):
        """Liczy pionki danego gracza.

        :param board: plansza gry,
        :param checker: jakie pionki liczyć,
        :return: liczba pionków danego gracza.
        """

        number_of_checkers = 0
        for i in range(0, FIELDS_IN_BOARD):
            if board[i] == checker:
                number_of_checkers += 1
        return number_of_checkers

    @staticmethod
    def check_winner(board):
        """Sprawdza, czy ktoś ułożył zwycięską kombinację.

        :param board: plansza gry,
        :return: zwycięzca - ktoś wygrał, NO_WINNER - brak wygranej.
        """

        winner = Game.check_columns(board)
        if winner == NO_WINNER:
            winner = Game.check_rows(board)
            if winner == NO_WINNER:
                winner = Game.check_diagonals(board)
        return winner

    @staticmethod
    def check_columns(board):
        """Sprawdza, czy w kolumnie została ułożona zwycięska kombinacja.

        :param board: plansza gry,
        :return: zwycięzca - ktoś wygrał, NO_WINNER - brak wygranej.
        """

        for i in range(0, FIELDS_IN_ROW):
            if board[i] == board[FIELDS_IN_ROW + i] == board[6 + i] != EMPTY:
                return board[i]
        return NO_WINNER

    @staticmethod
    def check_rows(board):
        """Sprawdza, czy w rzędzie została ułożona zwycięska kombinacja.

        :param board: plansza gry,
        :return: zwycięzca - ktoś wygrał, NO_WINNER - brak wygranej.
        """

        for i in range(0, FIELDS_IN_ROW):
            if board[FIELDS_IN_ROW * i] == board[1 + FIELDS_IN_ROW * i] == \
                    board[2 + FIELDS_IN_ROW * i] != EMPTY:
                return board[FIELDS_IN_ROW * i]
        return NO_WINNER

    @staticmethod
    def check_diagonals(board):
        """Sprawdza czy na przekątnej została ułożona zwycięska kombinacja.

        :param board: plansza gry,
        :return: zwycięzca - ktoś wygrał, NO_WINNER - brak wygranej.
        """

        if board[0] == board[4] == board[8] != EMPTY:
            return board[0]
        if board[2] == board[4] == board[6] != EMPTY:
            return board[2]
        return NO_WINNER

    def reset(self):
        """Resetuje grę, aby rozgrywka mogła zacząć się od nowa."""

        self.board = BOARD[:]
        print('Nowa gra')
