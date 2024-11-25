import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import re

# Шаг 1: Загрузка данных из файла с учетом кадров
def load_data_with_frames(filename):
    points = []
    frames = []  # Список для хранения информации о кадрах
    target_count = 0  # Счетчик целей
    with open(filename, 'r') as file:
        for line in file:
            # Используем регулярные выражения для извлечения информации о кадре и координатах
            match = re.search(r'Frame:\s*(\d+),\s*(Target|Noise):\s*x:\s*(-?\d+\.\d+),\s*y:\s*(-?\d+\.\d+)', line)
            if match:
                try:
                    frame = int(match.group(1))  # Извлекаем номер кадра
                    x = float(match.group(3))
                    y = float(match.group(4))
                    points.append([x, y])  # Добавляем только координаты
                    frames.append(frame)  # Сохраняем информацию о кадре
                    if match.group(2) == "Target":
                        target_count += 1  # Увеличиваем счетчик, если это цель
                except ValueError as e:
                    print(f"Ошибка при преобразовании данных: {e}")
            else:
                print(f"Не удалось извлечь данные из строки: {line.strip()}")
    return np.array(points), frames, target_count  # Возвращаем данные, кадры и количество целей

# Шаг 2: Применение алгоритма DBSCAN
def perform_clustering(data, eps=0.5, min_samples=5):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)
    return labels

# Шаг 3: Визуализация результатов с учетом кадров
def plot_clusters(data, labels):
    unique_labels = set(labels)
    colors = plt.cm.get_cmap('Spectral', len(unique_labels))

    for k in unique_labels:
        if k == -1:
            # Шум
            color = 'gray'
        else:
            color = colors(k)

        class_member_mask = (labels == k)
        plt.scatter(data[class_member_mask, 0], data[class_member_mask, 1], c=color, label=f'Cluster {k}', edgecolor='k', s=50)

    plt.title('Кластеризация DBSCAN')
    plt.xlabel('Координата X')
    plt.ylabel('Координата Y')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Загрузка данных с учетом кадров
    data, frames, target_count = load_data_with_frames('all_points_data.txt')

    # Проверка, есть ли загруженные данные
    if data.size == 0:
        print("Нет данных для кластеризации.")
    else:
        # Выполнение кластеризации
        labels = perform_clustering(data, eps=0.5, min_samples=5)

        # Визуализация результатов
        plot_clusters(data, labels)