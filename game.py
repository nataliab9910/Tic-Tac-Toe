"""
Konsolowa baza gry
"""


class Game:
    """
    Przeprowadza rozgrywkę w konsoli
    """

    actual_player = True  # True - komputer, False - człowiek

    def __init__(self):
        """
        Konstruktor, tworzy tablicę w konsoli i główne okno gry
        """
        self.board = [' ', ' ', ' ',
                      ' ', ' ', ' ',
                      ' ', ' ', ' ']

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

        if Game.actual_player:
            print("Ruch komputera!")
            self.computers_move()
            self.flip_player()

        else:
            print("Twój ruch!")
            self.humans_move()
            self.flip_player()

    @classmethod
    def flip_player(cls):
        """
        Zmienia gracza, który wykonuje ruch
        """
        cls.actual_player = not cls.actual_player

    @classmethod
    def return_actual_player(cls):
        return cls.actual_player

    def computers_move(self):
        """
        Wykonuje ruch komputera
        :return:
        """
        print("Komputer")
        Game.flip_player()
        pass

    def humans_move(self, pos):
        """
        Wykonuje ruch gracza
        :return:
        """
        print("Gracz")
        Game.flip_player()
        pass


# def get_mouse_click(position):
#     if

