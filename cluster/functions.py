"""
Модуль для кластеризации данных с использованием алгоритма DBSCAN.

Этот модуль содержит функции для:
1. Загрузки данных из текстового файла с учетом информации о кадрах.
2. Выполнения кластеризации загруженных данных с использованием алгоритма DBSCAN.
3. Визуализации результатов кластеризации на графике.

Функции:
- load_data_with_frames: Загружает данные из файла и возвращает координаты,
кадры и количество целей.
- perform_clustering: Применяет алгоритм DBSCAN для кластеризации данных.
- plot_clusters: Визуализирует результаты кластеризации.
"""


import re
from typing import Tuple, List

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN  # type: ignore


def load_data_with_frames(filename: str) -> Tuple[np.ndarray, List[int], int]:
    """Загрузка данных из файла с учетом кадров."""
    points: List[List[float]] = []
    frames: List[int] = []  # Список для хранения информации о кадрах
    target_count: int = 0  # Счетчик целей

    with open(filename, 'r', encoding='utf-8') as file:  # Указан кодировщик
        for line in file:
            # Используем регулярные выражения для извлечения информации о кадре и координатах
            match = re.search(
                r'Frame:\s*(\d+),\s*(Target|Noise):\s*x:\s*(-?\d+\.\d+),\s*y:\s*(-?\d+\.\d+)',
                line
            )
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


def perform_clustering(data: np.ndarray, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
    """Применение алгоритма DBSCAN для кластеризации."""
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)
    return labels


def plot_clusters(data: np.ndarray, labels: np.ndarray) -> None:
    """Визуализация результатов кластеризации."""
    unique_labels = set(labels)
    colors = plt.cm.get_cmap('Spectral', len(unique_labels))

    for k in unique_labels:
        if k == -1:
            # Шум
            color = 'gray'
        else:
            color = colors(k)

        class_member_mask = labels == k
        plt.scatter(data[class_member_mask, 0], data[class_member_mask, 1],
                    c=color, label=f'Cluster {k}', edgecolor='k', s=50)

    plt.title('Кластеризация DBSCAN')
    plt.xlabel('Координата X')
    plt.ylabel('Координата Y')
    plt.legend()
    plt.show()
