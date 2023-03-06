# Морской бой с авторастоновкой кораблей

# Классы исключений
class BoardOutException(Exception):  # координаты мимо поля
    pass


class ReshootException(Exception):  # выстрел в точку в которую уже стреляли
    pass


