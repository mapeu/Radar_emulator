import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Установим количество движущихся целей и шумовых точек
num_targets = 10
num_noise = 300
background_num = 1000

# Установим параметры радара
range_max = 100

# Создаем фигуру и оси
fig, ax = plt.subplots()
ax.set_xlim(-range_max, range_max)
ax.set_ylim(-range_max, range_max)
ax.set_aspect('equal')
ax.set_title('Симуляция радара')

# Генерация движущихся целей
target_x = np.random.uniform(-range_max, range_max, num_targets)
target_y = np.random.uniform(-range_max, range_max, num_targets)
target_vx = np.random.uniform(-5, 5, num_targets)
target_vy = np.random.uniform(-5, 5, num_targets)

# Отображение движущихся целей
target_plot, = ax.plot(target_x, target_y, 'ro', markersize=5)

# Функция для генерации динамического шума вокруг целей
def generate_noise(target_x, target_y, num_noise):
    noise_x = []
    noise_y = []
    for x, y in zip(target_x, target_y):
        # Генерация шума вокруг каждой цели с использованием нормального распределения
        num = np.random.randint(1, num_noise)
        noise_x.extend(np.random.normal(loc=x, scale=5, size=num // len(target_x)))
        noise_y.extend(np.random.normal(loc=y, scale=5, size=num // len(target_y)))
    return np.array(noise_x), np.array(noise_y)

# Начальная генерация шума
noise_x, noise_y = generate_noise(target_x, target_y, num_noise)

# Отображение шумовых точек с прозрачностью
noise_plot, = ax.plot(noise_x, noise_y, 'ro', markersize=2, alpha=0.3)

# Параметры фона шума
background_x = np.random.uniform(-range_max, range_max, background_num)  # X координаты для фонового шума
background_y = np.random.uniform(-range_max, range_max, background_num)  # Y координаты для фонового шума
background_plot, = ax.plot(background_x, background_y, 'k.', markersize=1, alpha=0.2)

# Функция анимации
def animate(i):
    global target_x, target_y, target_vx, target_vy, noise_x, noise_y, background_x, background_y

    # Обновление движущихся целей
    target_x += target_vx
    target_y += target_vy

    # Проверка на выход за границы
    out_of_bounds = (np.abs(target_x) > range_max) | (np.abs(target_y) > range_max)

    # Удаление целей, вышедших за границы
    target_x = target_x[~out_of_bounds]
    target_y = target_y[~out_of_bounds]
    target_vx = target_vx[~out_of_bounds]
    target_vy = target_vy[~out_of_bounds]

    # Генерация новых целей, если это необходимо
    if len(target_x) < num_targets:
        new_targets = num_targets - len(target_x)
        new_x = np.random.uniform(-range_max, range_max, new_targets)
        new_y = np.random.uniform(-range_max, range_max, new_targets)
        new_vx = np.random.uniform(-5, 5, new_targets)
        new_vy = np.random.uniform(-5, 5, new_targets)

        target_x = np.concatenate((target_x, new_x))
        target_y = np.concatenate((target_y, new_y))
        target_vx = np.concatenate((target_vx, new_vx))
        target_vy = np.concatenate((target_vy, new_vy))

    # Обновление шумовых точек вокруг движущихся целей
    noise_x, noise_y = generate_noise(target_x, target_y, num_noise)

    # Обновление графиков
    target_plot.set_data(target_x, target_y)
    noise_plot.set_data(noise_x, noise_y)

    # Обновление фонового шума
    background_x += np.random.choice([1, -1]) * 0.1
    background_y += np.random.choice([1, -1]) * 0.1
    background_plot.set_data(background_x, background_y)

    return target_plot, noise_plot, background_plot

# Создание анимации
ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)

plt.show()