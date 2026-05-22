import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка русского шрифта
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# Чтение данных (разделитель ';')
df = pd.read_csv('results_mpi.csv', sep=';')

sizes = sorted(df['size'].unique())
processes = sorted(df['processes'].unique())

# Цвета для каждого размера
colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))

# ------------------------------------------------------------
# 1. Время выполнения
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('processes')
    plt.plot(sub['processes'], sub['time_sec'], 'o-', label=f'Размер {size}', color=colors[idx])

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
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('processes')
    t1 = sub[sub['processes'] == 1]['time_sec'].values[0]
    speedup = t1 / sub['time_sec'].values
    plt.plot(sub['processes'], speedup, 's-', label=f'Размер {size}', color=colors[idx])

# Идеальное ускорение
max_proc = max(processes)
plt.plot([1, max_proc], [1, max_proc], 'k--', label='Идеальное ускорение', alpha=0.7)
plt.xlabel('Количество процессов')
plt.ylabel('Ускорение (T1 / Tn)')
plt.title('Абсолютное ускорение (MPI)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3. Эффективность
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('processes')
    t1 = sub[sub['processes'] == 1]['time_sec'].values[0]
    speedup = t1 / sub['time_sec'].values
    efficiency = (speedup / sub['processes'].values) * 100
    plt.plot(sub['processes'], efficiency, '^-', label=f'Размер {size}', color=colors[idx])
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
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('processes')
    times = sub['time_sec'].values
    rel_speedup = [1.0] 
    for i in range(1, len(times)):
        rel_speedup.append(times[i-1] / times[i])
    plt.plot(sub['processes'][1:], rel_speedup[1:], 'd-', label=f'Размер {size}', color=colors[idx])

plt.axhline(y=1, color='gray', linestyle=':', alpha=0.7, label='Нет ускорения')
plt.xlabel('Количество процессов')
plt.ylabel('Относительное ускорение (Tn-1 / Tn)')
plt.title('Относительное ускорение между соседними конфигурациями (MPI)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

print("Все четыре графика отображены.")