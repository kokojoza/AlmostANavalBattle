"""Морской бой с авто расстановкой кораблей"""


# Классы исключений
class BoardOutException(Exception):  # координаты мимо поля
    pass


class ReshootException(Exception):  # выстрел в точку в которую уже стреляли
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



        

