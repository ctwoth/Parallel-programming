import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# Чтение данных
df = pd.read_csv('results.csv')
sizes = sorted(df['size'].unique())
threads = sorted(df['threads'].unique())
colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))

# ------------------------------------------------------------
# 1. Время выполнения
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('threads')
    plt.plot(sub['threads'], sub['time_sec'], 'o-', label=f'Размер {size}', color=colors[idx])

plt.xlabel('Количество потоков')
plt.ylabel('Время (секунды)')
plt.title('Время выполнения умножения матриц')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 2. Абсолютное ускорение (относительно 1 потока)
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('threads')
    t1 = sub[sub['threads'] == 1]['time_sec'].values[0]
    speedup = t1 / sub['time_sec'].values
    plt.plot(sub['threads'], speedup, 's-', label=f'Размер {size}', color=colors[idx])

# Идеальное ускорение
max_thread = max(threads)
plt.plot([1, max_thread], [1, max_thread], 'k--', label='Идеальное ускорение', alpha=0.7)
plt.xlabel('Количество потоков')
plt.ylabel('Ускорение (T1 / Tn)')
plt.title('Абсолютное ускорение')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3. Эффективность
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('threads')
    t1 = sub[sub['threads'] == 1]['time_sec'].values[0]
    speedup = t1 / sub['time_sec'].values
    efficiency = (speedup / sub['threads'].values) * 100
    plt.plot(sub['threads'], efficiency, '^-', label=f'Размер {size}', color=colors[idx])

plt.xlabel('Количество потоков')
plt.ylabel('Эффективность (%)')
plt.title('Эффективность использования потоков')
plt.ylim(0, 115)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    sub = df[df['size'] == size].sort_values('threads')
    times = sub['time_sec'].values
    # Вычисляем ускорение относительно предыдущего колва потоков
    rel_speedup = [1.0]

    for i in range(1, len(times)):
        rel_speedup.append(times[i-1] / times[i])

    plt.plot(sub['threads'][1:], rel_speedup[1:], 'd-', label=f'Размер {size}', color=colors[idx])

plt.axhline(y=1, color='gray', linestyle=':', alpha=0.7, label='Нет ускорения')
plt.xlabel('Количество потоков')
plt.ylabel('Относительное ускорение (Tn-1 / Tn)')
plt.title('Относительное ускорение между соседними конфигурациями')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
