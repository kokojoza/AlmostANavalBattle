"""Морской бой с авторасстановкой кораблей"""


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

    def __eq__(self, other):  # метод проверяет равенство точек
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False
