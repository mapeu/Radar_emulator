"""
Основная функция для загрузки данных, выполнения кластеризации
и визуализации результатов кластеризации с использованием алгоритма DBSCAN.

Данный модуль загружает данные из текстового файла, проверяет их наличие,
выполняет кластеризацию и отображает результаты на графике.
"""
import matplotlib.pyplot as plt

from functions import load_data_with_frames, animate_clustering

# Модуль для кластеризации данных с использованием DBSCAN

if __name__ == "__main__":
    # Загрузка данных с учетом кадров
    data, frames, target_count = load_data_with_frames('all_points_data.txt')

    # Проверка, есть ли загруженные данные
    if data.size == 0:
        print("Нет данных для кластеризации.")
    else:
        fig, ax = plt.subplots()
        animate_clustering(data, ax)
        plt.show()
