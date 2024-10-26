import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Установим количество движущихся целей и шумовых точек
num_targets = 10
num_noise = 300
background_num = 1000

# Установим параметры радара
range_max = 100

# Класс для хранения координат и скорости точки
class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

# Создаем фигуру и оси
fig, ax = plt.subplots()
ax.set_xlim(-range_max, range_max)
ax.set_ylim(-range_max, range_max)
ax.set_aspect('equal')
ax.set_title('Симуляция радара')

# Генерация движущихся целей
targets = [Point(np.random.uniform(-range_max, range_max),
                 np.random.uniform(-range_max, range_max),
                 np.random.uniform(-5, 5),
                 np.random.uniform(-5, 5)) for _ in range(num_targets)]

# Отображение движущихся целей
target_plot, = ax.plot([target.x for target in targets], [target.y for target in targets], 'ro', markersize=5)

# Функция для генерации динамического шума вокруг целей
def generate_noise(targets, num_noise):
    noise_x = []
    noise_y = []
    for target in targets:
        # Генерация шума вокруг каждой цели с использованием нормального распределения
        num = np.random.randint(1, num_noise)
        noise_x.extend(np.random.normal(loc=target.x, scale=5, size=num // len(targets)))
        noise_y.extend(np.random.normal(loc=target.y, scale=5, size=num // len(targets)))
    return np.array(noise_x), np.array(noise_y)

# Начальная генерация шума
noise_x, noise_y = generate_noise(targets, num_noise)

# Отображение шумовых точек с прозрачностью
noise_plot, = ax.plot(noise_x, noise_y, 'ro', markersize=2, alpha=0.3)

# Функция для генерации фонового шума
def generate_background_noise(num):
    return np.random.uniform(-range_max, range_max, num), np.random.uniform(-range_max, range_max, num)

# Начальная генерация фонового шума
background_x, background_y = generate_background_noise(background_num)
background_plot, = ax.plot(background_x, background_y, 'k.', markersize=1, alpha=0.2)

# Функция анимации
def animate(i):
    global targets, noise_x, noise_y, background_x, background_y

    # Обновление движущихся целей
    for target in targets:
        target.x += target.vx
        target.y += target.vy

    # Проверка на выход за границы и удаление целей, вышедших за границы
    targets = [target for target in targets if np.abs(target.x) <= range_max and np.abs(target.y) <= range_max]

    # Генерация новых целей, если это необходимо
    while len(targets) < num_targets:
        new_target = Point(np.random.uniform(-range_max, range_max),
                           np.random.uniform(-range_max, range_max),
                           np.random.uniform(-5, 5),
                           np.random.uniform(-5, 5))
        targets.append(new_target)

    # Обновление шумовых точек вокруг движущихся целей
    noise_x, noise_y = generate_noise(targets, num_noise)

    # Обновление графиков
    target_plot.set_data([target.x for target in targets], [target.y for target in targets])
    noise_plot.set_data(noise_x, noise_y)

    # Генерация нового фонового шума
    background_x, background_y = generate_background_noise(background_num)
    background_plot.set_data(background_x, background_y)

    return target_plot, noise_plot, background_plot

# Создание анимации
ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)

plt.show()