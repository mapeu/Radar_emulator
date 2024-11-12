import numpy as np
from point import Point

from parameters import *
def generate_noise(targets: list[Point], num_noise: int) -> tuple[list[float], list[float]]:
    """
    Генерирует шум вокруг заданных целей.

    :param targets: Список объектов Point, представляющих цели.
    :param num_noise: Общее количество шумовых точек для генерации.
    :return: Кортеж из двух массивов: координаты x и y шумовых точек.
    """
    noise_x: list[float] = []
    noise_y: list[float] = []

    # Генерация шума для каждой цели
    for target in targets:
        num = np.random.randint(1, num_noise)
        noise_x.extend(np.random.normal(loc=target.x, scale=5, size=num // len(targets)))
        noise_y.extend(np.random.normal(loc=target.y, scale=5, size=num // len(targets)))

    return noise_x, noise_y

def generate_background_noise(num: int, range_max: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Генерирует фоновый шум в заданном диапазоне.

    :param num: Количество фоновых шумовых точек для генерации.
    :param range_max: Максимальное значение диапазона.
    :return: Кортеж из двух массивов: координаты x и y фонового шума.
    """
    return np.random.uniform(-range_max, range_max, num), np.random.uniform(-range_max, range_max, num)

def animate(i: int, targets: list[Point], target_plot, noise_plot, background_plot, num_noise: int, background_num: int, range_max: float) -> tuple:
    """
    Обновляет состояние анимации на каждом кадре.

    :param i: Номер текущего кадра анимации.
    :param targets: Список объектов Point, представляющих цели.
    :param target_plot: График целей.
    :param noise_plot: График шумовых точек.
    :param background_plot: График фонового шума.
    :param num_noise: Общее количество шумовых точек для генерации.
    :param background_num: Количество фоновых шумовых точек для генерации.
    :param range_max: Максимальное значение диапазона.
    :return: Кортеж из обновленных графиков целей, шумов и фонового шума.
    """
    # Обновление позиций целей
    for target in targets:
        target.x += target.vx
        target.y += target.vy

    # Удаление целей, вышедших за пределы диапазона
    targets = [target for target in targets if np.abs(target.x) <= range_max and np.abs(target.y) <= range_max]

    # Добавление новых целей, если их недостаточно
    while len(targets) < NUM_TARGETS:
        new_target = Point(np.random.uniform(-range_max, range_max),
                           np.random.uniform(-range_max, range_max),
                           np.random.uniform(-5, 5),
                           np.random.uniform(-5, 5))
        targets.append(new_target)

    # Генерация шума
    noise_x, noise_y = generate_noise(targets, num_noise)

    # Обновление данных для графиков
    target_plot.set_data([target.x for target in targets], [target.y for target in targets])
    noise_plot.set_data(noise_x, noise_y)

    # Генерация фонового шума
    background_x, background_y = generate_background_noise(background_num, range_max)
    background_plot.set_data(background_x, background_y)

    return target_plot, noise_plot, background_plot