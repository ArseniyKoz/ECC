import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ECCVisualizer:

    def __init__(self):
        self.fig = None
        self.ax = None
        self.animations = []

    def _get_curve_points(self, a, b, p):
        points = []
        for x in range(p):
            y_squared = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y) % p == y_squared:
                    points.append((x, y))
        return points

    def _find_continuous_segments(self, x, y_squared, eps=1e-10):
        segments = []
        start = None

        for i in range(len(y_squared)):
            if y_squared[i] >= -eps:
                if start is None:
                    start = i
            else:
                if start is not None:
                    segments.append((start, i-1))
                    start = None

        if start is not None:
            segments.append((start, len(y_squared)-1))

        return segments

    def _find_x_axis_intersections(self, a, b, x_range):
        def equation(x):
            return x**3 + a * x + b

        roots = []
        x_test = np.linspace(x_range[0], x_range[1], 10000)
        y_test = equation(x_test)

        # Ищем смены знака
        for i in range(len(y_test) - 1):
            if y_test[i] * y_test[i + 1] < 0:
                try:
                    root = fsolve(equation, x_test[i])[0]
                    if abs(equation(root)) < 1e-10:
                        roots.append(root)
                except:
                    continue

        # Убираем дубликаты и сортируем
        roots = list(set([round(root, 8) for root in roots]))
        roots.sort()
        return roots

    def _setup_basic_plot_styling(self, ax, x_range=(-4, 4), y_range=(-4, 4)):
        ax.axhline(0, color='k', linewidth=1, alpha=0.7)
        ax.axvline(0, color='k', linewidth=1, alpha=0.7)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)

    def _draw_curve_segments(self, ax, x, y_squared, a, b, color='b', linewidth=2.5, add_label=True):
        segments = self._find_continuous_segments(x, y_squared)

        for i, (start, end) in enumerate(segments):
            x_seg = x[start:end+1]
            y_squared_seg = np.maximum(y_squared[start:end+1], 0)

            y_pos = np.sqrt(y_squared_seg)
            y_neg = -np.sqrt(y_squared_seg)

            if i == 0 and add_label:
                ax.plot(x_seg, y_pos, color=color, linewidth=linewidth,
                       label=f'y² = x³ + {a}x + {b}', alpha=0.8)
                ax.plot(x_seg, y_neg, color=color, linewidth=linewidth, alpha=0.8)
            else:
                ax.plot(x_seg, y_pos, color=color, linewidth=linewidth, alpha=0.8)
                ax.plot(x_seg, y_neg, color=color, linewidth=linewidth, alpha=0.8)


    def plot_elliptic_curve(self, a, b, x_range=(-4, 4), title=None,
                                   show_roots=False, save_path=None):
        x = np.linspace(x_range[0], x_range[1], 15000)
        y_squared = x**3 + a * x + b

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        self._draw_curve_segments(ax, x, y_squared, a, b)

        self._setup_basic_plot_styling(ax, x_range)

        if title is None:
            title = f'Эллиптическая кривая: y² = x³ + {a}x + {b}'
        ax.set_title(title, fontsize=16, weight='bold', pad=20)


        ax.legend(fontsize=12, loc='upper left')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.fig, self.ax = fig, ax
        return fig, ax

    def visualize_different_curve_types(self, save_png=True):

        curve_params = [
            (0, 7, "Кривая: y² = x³ + 7x + 10", "blue"),
            (-1, 1, "Кривая: y² = x³ - x + 1", "red"),
            (2, 3, "Кривая: y² = x³ + 2x + 3", "green"),
            (-1, 0, "Три корня: y² = x³ - x", "orange")
        ]

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()

        for i, (a, b, title, color) in enumerate(curve_params):
            ax = axes[i]

            x = np.linspace(-4, 4, 10000)
            y_squared = x**3 + a * x + b

            self._draw_curve_segments(ax, x, y_squared, a, b, color=color, add_label=False)

            x_intersections = self._find_x_axis_intersections(a, b, (-4, 4))
            for root in x_intersections:
                if -4 <= root <= 4:
                    ax.plot(root, 0, color=color, linewidth=2.5, alpha=0.8)

            self._setup_basic_plot_styling(ax)
            ax.set_title(title, fontsize=12, weight='bold')

        plt.suptitle("Эллиптические кривые с различными параметрами", fontsize=16, weight='bold')
        plt.tight_layout()

        if save_png:
            plt.savefig('static/curve_types_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

        return fig

    def visualize_singular_curves(self):

        singular_curves = [
            (0, 0, "y² = x³ (каспида)", "red"),
            (-3, 2, "y² = x³ - 3x + 2 (самопересечение)", "blue")
        ]

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        for i, (a, b, title, color) in enumerate(singular_curves):
            ax = axes[i]

            x = np.linspace(-3, 3, 15000)
            y_squared = x**3 + a * x + b

            self._draw_curve_segments(ax, x, y_squared, a, b, color=color, add_label=False)

            if a == 0 and b == 0:
                ax.plot(0, 0, 'ro', markersize=12, label='Особая точка (каспида)')
            elif a == -3 and b == 2:
                ax.plot(1, 0, 'bo', markersize=12, label='Особая точка (узел)')

            self._setup_basic_plot_styling(ax, (-3, 3), (-3, 3))
            ax.set_title(title, fontsize=14, weight='bold')
            ax.legend()

        plt.suptitle("Особые (сингулярные) эллиптические кривые", fontsize=16, weight='bold')
        plt.tight_layout()
        plt.savefig('static/singular_curves.png', dpi=300, bbox_inches='tight')
        plt.show()

        return fig

    def visualize_secp256k1(self):

        fig, ax = self.plot_elliptic_curve(
            0, 7,
            x_range=[-4, 4],
            title='Кривая secp256k1: y² = x³ + 7\n',
            show_roots=True
        )

        test_points = [(-1, None), (0, None), (1, None), (2, None)]

        for x_pt, _ in test_points:
            y_squared_val = x_pt**3 + 7
            if y_squared_val >= 0:
                y_vals = [math.sqrt(y_squared_val), -math.sqrt(y_squared_val)]
                for y_val in y_vals:
                    ax.plot(x_pt, y_val, 'go', markersize=8, alpha=0.8, zorder=8)
                    ax.annotate(f'({x_pt}, {y_val:.2f})', (x_pt, y_val),
                              xytext=(10, 10), textcoords='offset points',
                              fontsize=10, alpha=0.8)

        info_text = """
SECP256K1 - стандарт ECC
• Используется в Bitcoin, Etherium
        """

        ax.text(0.02, 0.2, info_text.strip(), transform=ax.transAxes,
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8),
               verticalalignment='top', fontsize=10, family='monospace')

        plt.savefig('static/secp256k1_curve.png', dpi=300, bbox_inches='tight')
        plt.show()

        return fig

    def visualize_point_doubling(self):

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        a, b = -1, 1
        x = np.linspace(-2.5, 2.5, 15000)
        y_squared = x**3 + a * x + b

        self._draw_curve_segments(ax, x, y_squared, a, b, add_label=False)

        x_p = 0.5
        y_p_squared = x_p**3 + a * x_p + b
        y_p = math.sqrt(y_p_squared)

        ax.plot(x_p, y_p, 'ro', markersize=12, label=f'P = ({x_p}, {y_p:.2f})')

        slope = (3 * x_p**2 + a) / (2 * y_p)

        x_tangent = np.linspace(-2.5, 2.5, 1000)
        y_tangent = y_p + slope * (x_tangent - x_p)
        ax.plot(x_tangent, y_tangent, 'g--', linewidth=2, alpha=0.8, label='Касательная')

        x_r = slope**2 - 2 * x_p
        y_r = y_p + slope * (x_r - x_p)
        y_2p = -y_r

        ax.plot(x_r, y_r, 'go', markersize=10, label=f'Промежуточная точка\n({x_r:.2f}, {y_r:.2f})')
        ax.plot(x_r, y_2p, 'yo', markersize=12, label=f'2P = ({x_r:.2f}, {y_2p:.2f})')

        ax.axvline(x=x_r, color='gray', linestyle=':', alpha=0.6, linewidth=2)

        ax.annotate('', xy=(x_r, y_2p), xytext=(x_r, y_r),
                   arrowprops=dict(arrowstyle='<->', color='black', lw=2))

        self._setup_basic_plot_styling(ax, (-2.5, 2.5), (-3, 3))
        ax.set_title('Удвоение точки P на эллиптической кривой\ny² = x³ - x + 1',
                    fontsize=16, weight='bold')

        ax.legend(fontsize=11, loc='upper left')

        explanation = f"""
Алгоритм удвоения точки P = (x, y):
1. Строим касательную в точке P.
2. Находим точку пересечения касательной
с прямой, отличную от P.
3. Берем обратную к этой точке.
        """

        ax.text(0.98, 0.02, explanation.strip(), transform=ax.transAxes,
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9),
               verticalalignment='bottom', horizontalalignment='right',
               fontsize=10, family='monospace')

        plt.tight_layout()
        plt.savefig('static/point_doubling.png', dpi=300, bbox_inches='tight')
        plt.show()

        return fig

    def visualize_finite_field_curves(self, p_values=[11, 17, 23]):

        fig, axes = plt.subplots(1, len(p_values), figsize=(6*len(p_values), 6))
        if len(p_values) == 1:
            axes = [axes]

        a, b = 2, 3

        for i, p in enumerate(p_values):
            ax = axes[i]
            points = []

            for x in range(p):
                y_squared = (x**3 + a * x + b) % p
                for y in range(p):
                    if (y * y) % p == y_squared:
                        points.append((x, y))

            if points:
                x_coords = [pt[0] for pt in points]
                y_coords = [pt[1] for pt in points]

                ax.scatter(x_coords, y_coords, c='red', s=10, alpha=0.7, zorder=5)


            ax.grid(True, alpha=0.3)
            ax.set_xlim(-0.5, p-0.5)
            ax.set_ylim(-0.5, p-0.5)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'y² ≡ x³ + 2x + 3 (mod {p})\n{len(points)} точек + O∞',
                        fontsize=12, weight='bold')

            if points:
                ax.legend(fontsize=10)

        plt.suptitle('Эллиптические кривые в конечных полях', fontsize=16, weight='bold')
        plt.tight_layout()
        plt.savefig('static/finite_field_curves.png', dpi=300, bbox_inches='tight')
        plt.show()

        return fig

def main():

    visualizer = ECCVisualizer()

    print("Доступные методы:")
    print("1. plot_elliptic_curve() - улучшенная отрисовка кривой")
    print("2. visualize_different_curve_types() - различные типы кривых")
    print("3. visualize_singular_curves() - особые кривые")
    print("4. visualize_secp256k1() - кривая Bitcoin")
    print("5. visualize_point_doubling() - удвоение точки")
    print("6. visualize_finite_field_curves() - кривые в конечных полях")


    fig, ax = visualizer.plot_elliptic_curve(
        -1, 0,
        title="y² = x³ - x",
        show_roots=True,
        save_path='static/test_function.png'
    )
    plt.show()

    print("\n" + "="*60)

    print("   a) Различные типы кривых")
    fig1 = visualizer.visualize_different_curve_types()

    print("   b) Особые кривые")
    fig2 = visualizer.visualize_singular_curves()

    print("   c) secp256k1")
    fig3 = visualizer.visualize_secp256k1()

    print("   d) Удвоение точки")
    fig4 = visualizer.visualize_point_doubling()

    print("   e) Конечные поля")
    fig5 = visualizer.visualize_finite_field_curves([11, 113, 9679])

if __name__ == "__main__":
    main()
