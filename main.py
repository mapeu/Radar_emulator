import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from parameters import *
from point import Point
from functions import generate_noise, generate_background_noise, animate

# Создаем фигуру и оси
fig, ax = plt.subplots()
ax.set_xlim(-RANGE_MAX, RANGE_MAX)
ax.set_ylim(-RANGE_MAX, RANGE_MAX)
ax.set_aspect('equal')
ax.set_title('Симуляция радара')

# Генерация движущихся целей
targets: list[Point] = [
    Point(np.random.uniform(-RANGE_MAX, RANGE_MAX),
          np.random.uniform(-RANGE_MAX, RANGE_MAX),
          np.random.uniform(-5, 5),
          np.random.uniform(-5, 5)) for _ in range(NUM_TARGETS)
]

# Начальная генерация шума
noise_x: list[float] = []
noise_y: list[float] = []
noise_x, noise_y = generate_noise(targets, NUM_NOISE)

# Начальная генерация фонового шума
background_x, background_y = generate_background_noise(BACKGROUND_NUM, RANGE_MAX)
background_plot, = ax.plot(background_x, background_y, 'k.', markersize=1, alpha=0.2)

# Отображение движущихся целей
target_plot, = ax.plot([target.x for target in targets], [target.y for target in targets], 'ro', markersize=5)

# Отображение шумовых точек с прозрачностью
noise_plot, = ax.plot(noise_x, noise_y, 'ro', markersize=2, alpha=0.3)

if __name__ == "__main__":
    # Создание анимации
    ani = animation.FuncAnimation(fig, animate, fargs=(targets, target_plot, noise_plot, background_plot,
                                                       NUM_NOISE, BACKGROUND_NUM, RANGE_MAX),
                                  frames=FRAMES, interval=50)

    # Отображение графика
    plt.show()