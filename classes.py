class Point:
    def __init__(self, x: float, y: float, vx: float, vy: float):
        """
        :param x: Координата x точки
        :param y: Координата y точки
        :param vx: Скорость точки по x
        :param vy: Скорость точки по y
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def to_string(self) -> str:
        """
        Возвращает строковое представление объекта Point.

        :return: Строка с координатами и скоростями точки.
        """
        return f"x: {self.x}, y: {self.y}, vx: {self.vx}, vy: {self.vy}"