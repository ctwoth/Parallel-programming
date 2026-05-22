import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка шрифта (английские подписи, но можно оставить русские)
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# Чтение CSV
df = pd.read_csv('results_cuda.csv', sep=';')

# Сопоставление названий блоков с количеством потоков
block_threads = {
    '8x8': 64,
    '16x16': 256,
    '16x32': 512,
    '32x16': 512,
    '32x32': 1024
}
df['threads'] = df['block'].map(block_threads)

# Уникальные размеры матриц
sizes = sorted(df['size'].unique())
# Уникальные конфигурации блоков в порядке возрастания потоков (для читаемости)
block_order = ['8x8', '16x16', '16x32', '32x16', '32x32']

colors = plt.cm.viridis(np.linspace(0, 1, len(sizes)))

# ------------------------------------------------------------
# 1. Время выполнения (от конфигурации блока)
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    subset = df[df['size'] == size].set_index('block').loc[block_order]
    plt.plot(subset.index, subset['time_sec'], 'o-', label=f'Size {size}', color=colors[idx])

plt.xlabel('Конфигурация блока')
plt.ylabel('Время (секунды)')
plt.title('Время перемножения CUDA')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 2. Ускорение относительно конфигурации 8x8
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    subset = df[df['size'] == size].set_index('block').loc[block_order]
    t_base = subset.loc['8x8', 'time_sec']
    speedup = t_base / subset['time_sec']
    plt.plot(subset.index, speedup, 's-', label=f'Size {size}', color=colors[idx])

plt.xlabel('Конфигурация блока')
plt.ylabel('Ускорение (T_8x8 / T_блок)')
plt.title('ускореение относительно 8x8')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3. Эффективность (ускорение / (потоки_блока / потоки_базы) )
# База 8x8 имеет 64 потока
# ------------------------------------------------------------
base_threads = 64
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    subset = df[df['size'] == size].set_index('block').loc[block_order]
    t_base = subset.loc['8x8', 'time_sec']
    speedup = t_base / subset['time_sec']
    # Эффективность = (speedup) / (threads_block / base_threads) * 100%
    threads_block = subset['threads']
    efficiency = (speedup / (threads_block / base_threads)) * 100
    plt.plot(subset.index, efficiency, '^-', label=f'Size {size}', color=colors[idx])

plt.xlabel('Конфигурация блока')
plt.ylabel('Эффективность блока (%)')
plt.title('Эффективность относительно 8x8')
plt.ylim(0, 110)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 4. Относительное ускорение (соседние конфигурации) – опционально
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
for idx, size in enumerate(sizes):
    subset = df[df['size'] == size].set_index('block').loc[block_order]
    times = subset['time_sec'].values
    rel_speedup = [1.0]
    
    for i in range(1, len(times)):
        rel_speedup.append(times[i-1] / times[i])
    
    plt.plot(block_order[1:], rel_speedup[1:], 'd-', label=f'Size {size}', color=colors[idx])

plt.axhline(y=1, color='gray', linestyle=':', alpha=0.7, label='No speedup')
plt.xlabel('Конфигурация блока')
plt.ylabel('Относительное ускорение (T_пред / T_тек)')
plt.title('Ускорение блока относительно предыдущего')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()