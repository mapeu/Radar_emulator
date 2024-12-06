"""
Модуль для загрузки данных, выполнения кластеризации и визуализации результатов кластеризации
с использованием алгоритма DBSCAN.

Данный модуль загружает данные из текстового файла, проверяет их наличие,
выполняет кластеризацию и отображает результаты на графике.
"""

import re
import time
from typing import Tuple, List
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore

def load_data_with_frames(filename: str) -> Tuple[np.ndarray, List[int], int]:
    """
    Загрузка данных из файла с учетом кадров.

    Args:
        filename (str): Путь к файлу, содержащему данные.

    Returns:
        Tuple[np.ndarray, List[int], int]: 
            - Массив координат точек (n, 2).
            - Список кадров, к которым принадлежат точки.
            - Количество целей (Target) в данных.
    """
    points: List[List[float]] = []
    frames: List[int] = []  # Список для хранения информации о кадрах
    target_count: int = 0  # Счетчик целей

    try:
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
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return np.array([]), [], 0

    return np.array(points), frames, target_count  # Возвращаем данные, кадры и количество целей

def perform_clustering(data: np.ndarray, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
    """
    Применение алгоритма DBSCAN для кластеризации.

    Args:
        data (np.ndarray): Массив координат точек для кластеризации.
        eps (float): Максимальное расстояние между двумя образцами для их объединения в кластер.
        min_samples (int): Минимальное количество образцов в кластере.

    Returns:
        np.ndarray: Метки кластеров для каждой точки.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)
    return labels


def plot_clusters(data: np.ndarray, labels: np.ndarray, ax) -> None:
    """
    Визуализация результатов кластеризации.

    Args:
        data (np.ndarray): Массив координат точек.
        labels (np.ndarray): Метки кластеров для каждой точки.
        ax: Объект осей для визуализации.
    """
    ax.clear()  # Очищаем оси перед новым отображением
    unique_labels = set(labels)
    colors = plt.cm.get_cmap('Spectral', len(unique_labels))  # Получаем цветовую карту

    for k in unique_labels:
        if k == -1:
            # Шум
            color = 'gray'
        else:
            color = colors(k)

        class_member_mask = labels == k
        ax.scatter(data[class_member_mask, 0], data[class_member_mask, 1],
                   c=color, label=f'Cluster {k}', edgecolor='k', s=20)  # Уменьшили размер точек

    ax.set_title('Кластеризация DBSCAN')
    ax.set_xlabel('Координата X')
    ax.set_ylabel('Координата Y')
    ax.legend()


def animate_clustering(data: np.ndarray, ax, step: int = 10) -> None:
    """
    Анимация кластеризации.

    Args:
        data (np.ndarray): Массив координат точек для кластеризации.
        ax: Объект осей для визуализации.
        step (int): Количество кадров, обрабатываемых за один шаг анимации.
    """
    for i in range(0, len(data), step):
        if i + step <= len(data):
            current_data = data[i:i + step]
            # Нормализация данных
            current_data = StandardScaler().fit_transform(current_data)
            start_time = time.time()  # Начало отсчета времени обработки
            labels = perform_clustering(current_data, eps=0.3, min_samples=2)
            end_time = time.time()  # Конец отсчета времени обработки
            # Вывод времени обработки
            print(
                f"Время обработки кадров {i} - {i + step - 1}: {end_time - start_time:.2f} секунд")
            plot_clusters(current_data, labels, ax)
            plt.pause(0.5)  # Пауза для визуализации
