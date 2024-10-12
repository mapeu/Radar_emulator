import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Задаём количество шума и двигающихся целей
num_targets = 10
num_noise = 500

# Задаём параметры радара
range_max = 100
azimuth_max = 360

# Создаём окошко
fig, ax = plt.subplots()
ax.set_xlim(-range_max, range_max)
ax.set_ylim(-range_max, range_max)
ax.set_aspect('equal')
ax.set_title('Radar Simulation')

# Генерируем шум
noise_x = np.random.uniform(-range_max, range_max, num_noise)
noise_y = np.random.uniform(-range_max, range_max, num_noise)

# Генерируем двигающиеся цели
target_x = np.random.uniform(-range_max, range_max, num_targets)
target_y = np.random.uniform(-range_max, range_max, num_targets)
target_vx = np.random.uniform(-5, 5, num_targets)
target_vy = np.random.uniform(-5, 5, num_targets)

# Рисуем шум
noise_plot, = ax.plot(noise_x, noise_y, 'bo', markersize=2)

# Рисуем двигающихся
target_plot, = ax.plot(target_x, target_y, 'ro', markersize=5)


# Анимируем
def animate(i):
    global target_x, target_y, target_vx, target_vy

    # Обновляем точки
    target_x += target_vx
    target_y += target_vy

    # ПРоверка на сталкивание с границей
    out_of_bounds = (np.abs(target_x) > range_max) | (np.abs(target_y) > range_max)

    # Удаляем точки за границей
    target_x = target_x[~out_of_bounds]
    target_y = target_y[~out_of_bounds]
    target_vx = target_vx[~out_of_bounds]
    target_vy = target_vy[~out_of_bounds]
    #TO DO - добавить ускорение и различные траектории, типо круговых. Добавить шуму небольшое движение, при этом различное, чтобы сделать второй пункт задания.

    # Генерируем новые точки, раз удалили прошлые
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

    target_plot.set_data(target_x, target_y)
    return target_plot,


# Создаём анимацию
ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)

plt.show()