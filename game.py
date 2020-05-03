"""
Konsolowa baza gry
"""

HUMAN, COMPUTER = range(2)


class Game:
    """
    Przeprowadza rozgrywkę w konsoli
    """

    def __init__(self):
        """
        Konstruktor, tworzy tablicę w konsoli i główne okno gry
        """
        self.board = [' ', ' ', ' ',
                      ' ', ' ', ' ',
                      ' ', ' ', ' ']
        self.current_player = COMPUTER  # podawać, kto jest pierwszym graczem

    def print_board(self):
        """
        Rysuje plansze w konsoli
        """
        for i in range(3):
            print(' ' + self.board[3 * i] + ' | '
                  + self.board[1 + 3 * i] + ' | '
                  + self.board[2 + 3 * i])
            if i < 2:
                print("---+---+---")

    def make_move(self):
        """
        Wykonanie ruchu przez aktualnego gracza
        """
        self.print_board()

        if self.current_player == COMPUTER:
            print("Ruch komputera!")
            self.computers_move()
            self.flip_player()

        else:
            print("Twój ruch!")
            self.humans_move()
            self.flip_player()

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
        self.flip_player()
        pass

    def humans_move(self):
        """
        Wykonuje ruch gracza
        :return:
        """
        print("Gracz")
        self.flip_player()
        pass
