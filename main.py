"""Морской бой с авто расстановкой кораблей"""


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
                dot = (self.start_point[0], self.start_point[1] + i)
            else:
                dot = (self.start_point[0] + i, self.start_point[1])
            dots.append(dot)
        return dots


class Board:
    def __init__(self, size=6, hid=False):
        self.board = [["◯"] * size for _ in range(size)]
        self.list_ships = []
        self.size = size
        self.hid = hid
        self.live_ships = 0

    def add_ship(self, ship):
        """
        Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения)
        """
        for dot in ship.dots():
            if self.out(dot) or dot in self.contour(ship):
                raise ShipAssignment("Не удалось поставить корабль на доску")
        for dot in ship.dots():
            x, y = dot.x, dot.y
            self.board[x][y] = "■"
        self.list_ships.append(ship)
        self.live_ships += 1

    def contour(self, ship, hide=False):
        """
        Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры,
        и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
        """
        contour = []
        for dot in ship.dots():
            for i in range(dot.x-1, dot.x+2):
                for j in range(dot.y-1, dot.y+2):
                    if self.out(Dot(i, j)):
                        continue
                    if hide and self.board[i][j] == "■":
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

        if self.board[dot.x][dot.y] != "◯":
            raise ReshootException("Вы уже стреляли сюда!")

        self.board[dot.x][dot.y] = "T" if self.board[dot.x][dot.y] == '◯' else 'X'

        for ship in self.list_ships:
            if dot in ship.dots():
                ship.lives -= 1
                if ship.lives == 0:
                    self.live_ships -= 1
                    for d in self.contour(ship, hide=True):
                        x, y = d.x, d.y
                        self.board[x][y] = 'T'
                    return False
                return True
        return False




a = Board()
print(a.out(Dot(1, 5)))