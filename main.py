import random


# Классы исключений
class BoardOutException(Exception):  # координаты мимо поля
    pass


class ReshootException(Exception):  # выстрел в точку в которую уже стреляли
    pass


class ShipAssignment(Exception):  # не удалось расставить корабли на доску
    pass


# Класс точек
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Метод проверяет равенство точек
        """
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False


# Клас кораблей
class Ship:
    def __init__(self, length, start_point, horizontal):
        self.length = length  # int 1-3
        self.start_point = start_point  # нос корабля (1, 1)
        self.horizontal = horizontal  # если горизонтально то True, нет False
        self.health = length  # кол-во жизней, изначально равно длине корабля


    def dots(self):
        """
        Метод возвращает список всех точек корабля.
        """
        dots = []
        for i in range(self.length):
            if self.horizontal:
                dot = Dot(self.start_point.x, self.start_point.y + i)
            else:
                dot = Dot(self.start_point.x + i, self.start_point.y)
            dots.append(dot)
        return dots


class Board:
    def __init__(self, size=6, hid=False):
        self.board = [["◯"] * size for _ in range(size)]
        self.list_ships = []
        self.size = size
        self.hid = hid
        self.live_ships = 0
        self.all_contour = []

    def add_ship(self, ship):
        """
        Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения)
        """
        for dot in ship.dots():
            if self.out(dot) or dot in self.all_contour:
                raise ShipAssignment("Не удалось поставить корабль на доску")
        for dot in ship.dots():
            self.board[dot.x][dot.y] = "■"
        self.list_ships.append(ship)
        self.live_ships += 1
        self.all_contour.extend(self.contour(ship))

    def contour(self, ship):
        """
        Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры,
        и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
        """
        contour = []
        for dot in ship.dots():
            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if self.out(Dot(i, j)) or Dot(i, j) in ship.dots():
                        continue

                    contour.append(Dot(i, j))
        return contour

    def show_board(self):
        """
        Метод, который выводит доску в консоль в зависимости от параметра hid
        """
        print("   | " + " | ".join(str(i + 1) for i in range(self.size)) + " |")
        for i in range(self.size):
            row = ""
            if i < self.size:
                row += " "
                row += str(i + 1) + " | "
                for j in range(self.size):
                    if self.hid and self.board[i][j] == "■":
                        row += "■ | "
                    else:
                        row += f"{self.board[i][j]} | "
                print(row)

    def out(self, dot):
        """
        Метод out, который для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит.
        """
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        """
        Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку,
        нужно выбрасывать исключения).
        """
        if self.out(dot):
            raise BoardOutException("Стреляете мимо доски!")

        if self.board[dot.x][dot.y] in ['T', 'X']:
            raise ReshootException("Вы уже стреляли сюда!")

        # self.board[dot.x][dot.y] = "T" if self.board[dot.x][dot.y] == '◯' else 'X'

        if self.board[dot.x][dot.y] == '◯':
            self.board[dot.x][dot.y] = "T"
            print('Мимо')
            return False
        else:
            self.board[dot.x][dot.y] = "X"
            for ship in self.list_ships:
                if dot in ship.dots():
                    ship.health -= 1
                    print('Ранил')
                    if ship.health == 0:
                        self.live_ships -= 1
                        print('Убил')
                        for d in self.contour(ship):
                            self.board[d.x][d.y] = 'T'
                    return True


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        """
        Метод, который «спрашивает» игрока, в какую клетку он делает выстрел.
        Пока мы делаем общий для AI и пользователя класс, этот метод мы описать не можем.
        Оставим этот метод пустым. Тем самым обозначим, что потомки должны реализовать этот метод.
        """
        pass

    def move(self):
        """
        Метод, который делает ход в игре.
        Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot),
        отлавливаем исключения, и если они есть, пытаемся повторить ход. Метод должен возвращать True,
        если этому игроку нужен повторный ход (например если он выстрелом подбил корабль).
        """
        while True:
            try:
                shot = self.enemy_board.shot(self.ask())
                return shot
            except (BoardOutException, ReshootException) as e:
                print(e)


class AI(Player):
    def ask(self):
        x = random.randint(0, self.own_board.size - 1)
        y = random.randint(0, self.own_board.size - 1)
        return Dot(x, y)


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Нужна 2 числа")
                continue

            x, y = cords

            if not (x.isdigit() and y.isdigit()):
                print("Только цифры")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        self.board_ai = self.random_board()
        self.board_user = self.random_board()
        self.board_ai.hid = True
        self.player_user = User(self.board_user, self.board_ai)
        self.player_ai = AI(self.board_ai, self.board_user)

    def random_board(self):
        board = Board()
        ships = [(1, 3), (2, 2), (4, 1)]
        for ship in ships:
            for _ in range(ship[0]):
                while True:
                    try:
                        start_point = Dot(random.randint(0, board.size), random.randint(0, board.size))
                        sh = Ship(ship[1], start_point, random.randint(0, 1))
                        board.add_ship(sh)
                        break
                    except ShipAssignment:
                        pass
            if board.live_ships == 0:
                break
        return board

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("Координаты задаются в формате 'x y', где x - цифра (1-6), y - цифра (1-6)")
        print("Например, '1 1' - координаты левой верхней клетки игрового поля")

    def loop(self):
        num = 0
        while True:
            print("-" * 25)
            print("Доска игрока:")
            print("-" * 25)
            self.board_user.show_board()
            print("-" * 25)
            print("Доска врага:")
            print("-" * 25)
            self.board_ai.show_board()
            print("-" * 25)

            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.player_user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.player_ai.move()
            if repeat:
                num -= 1

            if self.board_ai.live_ships == 0:
                print("Вы победили!")
                break

            if self.board_user.live_ships == 0:
                print("Компьютер победил!")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    g = Game()
    g.start()
