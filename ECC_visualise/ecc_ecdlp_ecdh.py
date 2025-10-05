import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def visualize_ecdlp_demonstration(p=11):
    # y² = x³ - 7x + 10 в F_11
    a, b = -7, 10

    # Находим все точки
    points = []
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))

    G = (9, 4)  # Генераторная точка
    target = (8, 2)  # nG

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    # Все точки кривой
    if points:
        x_all = [pt[0] for pt in points]
        y_all = [pt[1] for pt in points]
        ax.scatter(x_all, y_all, c='lightblue', s=100, alpha=0.6, zorder=3, label='Точки кривой')

    # Генераторная точка
    ax.scatter([G[0]], [G[1]], c='red', s=300, marker='*',
              edgecolor='black', linewidth=2, zorder=6, label=f'G = {G}')

    # Целевая точка
    ax.scatter([target[0]], [target[1]], c='gold', s=250, marker='D',
              edgecolor='black', linewidth=2, zorder=6, label=f'nG = {target}')

    # Настройка осей
    ax.set_xticks(range(p))
    ax.set_yticks(range(p))
    ax.set_xlim(-0.5, p-0.5)
    ax.set_ylim(-0.5, p-0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title(f'ECDLP Демонстрация в F_{p}\ny² ≡ x³ - 7x + 10 (mod {p})',
                fontsize=16, weight='bold')

    # Информационный блок
    info_text = f"""
ЗАДАЧА ECDLP:
Дано: G = {G}, nG = {target}
Найти: n = ?

Кривая: y² ≡ x³ - 7x + 10 (mod {p})
Всего точек на кривой: {len(points)}

Метод: Полный перебор
Для F_{p}: максимум {p} проверок
Для реальных кривых: ~2^128 проверок!
    """

    ax.text(0.02, 0.98, info_text.strip(), transform=ax.transAxes,
           bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9),
           verticalalignment='top', fontsize=11, family='monospace')

    ax.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('static/ecdlp_demonstration.png', dpi=300, bbox_inches='tight')
    plt.show()

    return fig

def visualize_diffie_hellman_steps():

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Параметры
    p = 23
    a, b = 2, 3

    # Находим точки кривой
    points = []
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))

    G = points[0] if points else (0, 1)  # Базовая точка

    # Случайные приватные ключи
    d_A = 7   # Приватный ключ Алисы
    d_B = 13  # Приватный ключ Боба

    # Публичные ключи
    H_A = points[d_A % len(points)] if points else (1, 1)
    H_B = points[d_B % len(points)] if points else (2, 2)

    # Общий секрет
    S = points[(d_A * d_B) % len(points)] if points else (3, 3)

    steps = [
        ("Шаг 1: Инициализация", f"Базовая точка G = {G}\nКривая в F_{p}"),
        ("Шаг 2: Генерация ключей", f"Алиса: d_A = {d_A}, H_A = {H_A}\nБоб: d_B = {d_B}, H_B = {H_B}"),
        ("Шаг 3: Обмен публичными ключами", f"Алиса → Боб: H_A = {H_A}\nБоб → Алиса: H_B = {H_B}"),
        ("Шаг 4: Вычисление общего секрета", f"Алиса: S = d_A × H_B = {S}\nБоб: S = d_B × H_A = {S}")
    ]

    for i, (title, description) in enumerate(steps):
        ax = axes[i // 2, i % 2]

        if points:
            x_all = [pt[0] for pt in points]
            y_all = [pt[1] for pt in points]
            ax.scatter(x_all, y_all, c='lightgray', s=60, alpha=0.4, zorder=2)

        if i == 0:  # Инициализация
            ax.scatter([G[0]], [G[1]], c='black', s=300, marker='*',
                      edgecolor='white', linewidth=2, zorder=6, label=f'G = {G}')
        elif i == 1:  # Генерация ключей
            ax.scatter([G[0]], [G[1]], c='black', s=200, marker='*', zorder=5, label=f'G = {G}')
            ax.scatter([H_A[0]], [H_A[1]], c='red', s=200, marker='o', zorder=5, label=f'H_A = {H_A}')
            ax.scatter([H_B[0]], [H_B[1]], c='blue', s=200, marker='s', zorder=5, label=f'H_B = {H_B}')
        elif i == 2:  # Обмен ключами
            ax.scatter([H_A[0]], [H_A[1]], c='red', s=200, marker='o', zorder=5, label=f'H_A = {H_A}')
            ax.scatter([H_B[0]], [H_B[1]], c='blue', s=200, marker='s', zorder=5, label=f'H_B = {H_B}')
            # Стрелки обмена
            ax.annotate('', xy=(H_B[0], H_B[1]-0.3), xytext=(H_A[0], H_A[1]+0.3),
                       arrowprops=dict(arrowstyle='Wedge', color='green', lw=2))
        elif i == 3:  # Общий секрет
            ax.scatter([S[0]], [S[1]], c='gold', s=300, marker='D',
                      edgecolor='black', linewidth=2, zorder=6, label=f'S = {S}')

        ax.set_xticks(range(0, p, 2))
        ax.set_yticks(range(0, p, 2))
        ax.set_xlim(-1, p)
        ax.set_ylim(-1, p)
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontsize=14, weight='bold')

        # Описание
        ax.text(0.02, 0.02, description, transform=ax.transAxes,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
               verticalalignment='bottom', fontsize=10, family='monospace')

        if i <= 3:
            ax.legend(fontsize=9)

    plt.suptitle('Алгоритм Диффи-Хеллмана на эллиптических кривых', fontsize=18, weight='bold')
    plt.tight_layout()
    plt.savefig('static/diffie_hellman_steps.png', dpi=300, bbox_inches='tight')
    plt.show()

    return fig

# Создание дополнительных визуализаций
fig1 = visualize_ecdlp_demonstration()

fig2 = visualize_diffie_hellman_steps()
