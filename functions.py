import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from classes import Point


def generate_noise(targets: list[Point], num_noise: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Генерирует шум вокруг заданных целей.

    :param targets: Список объектов Point, представляющих цели.
    :param num_noise: Общее количество шумовых точек для генерации.
    :return: Кортеж из двух массивов: координаты x и y шумовых точек.
    """
    noise_x = []
    noise_y = []

    # Генерация шума для каждой цели
    for target in targets:
        num = np.random.randint(1, num_noise)
        noise_x.extend(np.random.normal(loc=target.x, scale=5, size=num // len(targets)))
        noise_y.extend(np.random.normal(loc=target.y, scale=5, size=num // len(targets)))

    return np.array(noise_x), np.array(noise_y)


def generate_background_noise(num: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Генерирует фоновый шум в заданном диапазоне.

    :param num: Количество фоновых шумовых точек для генерации.
    :return: Кортеж из двух массивов: координаты x и y фонового шума.
    """
    return np.random.uniform(-range_max, range_max, num), np.random.uniform(-range_max, range_max, num)


# Создаем фигуру и оси
fig, ax = plt.subplots()
ax.set_xlim(-range_max, range_max)
ax.set_ylim(-range_max, range_max)
ax.set_aspect('equal')
ax.set_title('Симуляция радара')

# Генерация движущихся целей
targets: list[Point] = [
    Point(np.random.uniform(-range_max, range_max),
          np.random.uniform(-range_max, range_max),
          np.random.uniform(-5, 5),
          np.random.uniform(-5, 5)) for _ in range(num_targets)
]

# Начальная генерация шума
noise_x, noise_y = generate_noise(targets, num_noise)

# Начальная генерация фонового шума
background_x, background_y = generate_background_noise(background_num)
background_plot, = ax.plot(background_x, background_y, 'k.', markersize=1, alpha=0.2)

# Отображение движущихся целей
target_plot, = ax.plot([target.x for target in targets], [target.y for target in targets], 'ro', markersize=5)

# Отображение шумовых точек с прозрачностью
noise_plot, = ax.plot(noise_x, noise_y, 'ro', markersize=2, alpha=0.3)


def animate(i: int) -> tuple:
    """
    Обновляет состояние анимации на каждом кадре.

    :param i: Номер текущего кадра анимации.
    :return: Кортеж из обновленных графиков целей, шумов и фонового шума.
    """
    global targets, noise_x, noise_y, background_x, background_y

    # Обновление позиций целей
    for target in targets:
        target.x += target.vx
        target.y += target.vy

    # Удаление целей, вышедших за пределы диапазона
    targets = [target for target in targets if np.abs(target.x) <= range_max and np.abs(target.y) <= range_max]

    # Добавление новых целей, если их недостаточно
    while len(targets) < num_targets:
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
    background_x, background_y = generate_background_noise(background_num)
    background_plot.set_data(background_x, background_y)

    # Создание списка текущих объектов
    current_points = targets + [Point(x, y, 0, 0) for x, y in zip(background_x, background_y)] + \
                     [Point(x, y, 0, 0) for x, y in zip(noise_x, noise_y)]
    # Запись текущих позиций в файл
    with open("f2.txt", "a") as fe:  # Используем 'a' для добавления в файл
        for obj in current_points:
            fe.write(obj.to_string() + '\t')  # Запись координат и скоростей
        fe.write('\n')  # Переход на новую строку после записи всех объектов

    return target_plot, noise_plot, background_plot