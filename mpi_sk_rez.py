import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('mpi_results.csv', sep=';')

# Размеры матриц и количество процессов
sizes = df['size'].values
processes = [1, 2, 4, 6, 8, 10, 12]

# Цвета для каждого размера
colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))

# Преобразуем данные: строки - размеры, столбцы - количество процессов
time_matrix = df.iloc[:, 1:].values 
# Убедимся, что time_matrix в float
time_matrix = time_matrix.astype(float)

# ------------------------------------------------------------
# 1. Время выполнения
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for i, size in enumerate(sizes):
    plt.plot(processes, time_matrix[i, :], 'o-', label=f'Размер {size}', color=colors[i])
plt.xlabel('Количество процессов')
plt.ylabel('Время (секунды)')
plt.title('Время умножения матриц (MPI)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 2. Абсолютное ускорение (относительно 1 процесса)
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for i, size in enumerate(sizes):
    t1 = time_matrix[i, 0]  # время для 1 процесса
    speedup = t1 / time_matrix[i, :]
    plt.plot(processes, speedup, 's-', label=f'Размер {size}', color=colors[i])
# Идеальное ускорение
plt.plot([1, max(processes)], [1, max(processes)], 'k--', label='Идеальное ускорение', alpha=0.7)
plt.xlabel('Количество процессов')
plt.ylabel('Ускорение (T1 / Tn)')
plt.title('Абсолютное ускорение (MPI)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3. Эффективность (ускорение / число процессов * 100%)
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for i, size in enumerate(sizes):
    t1 = time_matrix[i, 0]
    speedup = t1 / time_matrix[i, :]
    efficiency = speedup / np.array(processes) * 100
    plt.plot(processes, efficiency, '^-', label=f'Размер {size}', color=colors[i])
plt.xlabel('Количество процессов')
plt.ylabel('Эффективность (%)')
plt.title('Эффективность использования процессов (MPI)')
plt.ylim(0, 105)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 4. Относительное ускорение (Tₙ₋₁ / Tₙ)
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
rel_proc = processes[1:]  # для отображения начиная со второго
for i, size in enumerate(sizes):
    times = time_matrix[i, :]
    rel_speedup = [1.0]  # для 1 процесса нет предыдущего
    for j in range(1, len(times)):
        rel_speedup.append(times[j-1] / times[j])
    plt.plot(rel_proc, rel_speedup[1:], 'd-', label=f'Размер {size}', color=colors[i])
plt.axhline(y=1, color='gray', linestyle=':', alpha=0.7, label='Нет ускорения')
plt.xlabel('Количество процессов')
plt.ylabel('Относительное ускорение (Tn-1 / Tn)')
plt.title('Относительное ускорение между соседними конфигурациями (MPI)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()