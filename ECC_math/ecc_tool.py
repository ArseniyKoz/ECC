import math


class EllipticCurve:
    def __init__(self, a, b, p=None):
        """
        Инициализация эллиптической кривой y^2 = x^3 + ax + b
        p - модуль для конечного поля (None для действительных чисел)
        """
        self.a = a
        self.b = b
        self.p = p

        # Проверка дискриминанта
        discriminant = -16 * (4 * a**3 + 27 * b**2)
        if p:
            discriminant = discriminant % p

    def is_point_on_curve(self, x, y):
        if self.p:
            return (y**2) % self.p == (x**3 + self.a * x + self.b) % self.p
        else:
            return y**2 == x**3 + self.a * x + self.b

    def get_y(self, x):
        if self.p:
            # Для конечного поля

            y_squared = (x**3 + self.a * x + self.b) % self.p
            # Находим квадратные корни в конечном поле
            return self.sqrt_mod(y_squared, self.p) if y_squared >= 0 else []
        else:
            # Для действительных чисел

            y_squared = x**3 + self.a * x + self.b
            if y_squared >= 0:
                return [math.sqrt(y_squared), -math.sqrt(y_squared)]
            else:
                return []

    def sqrt_mod(self, a, p):
        """Находит квадратные корни в конечном поле"""
        if a == 0:
            return [0]

        # Простейший случай - используем алгоритм Тонелли-Шанкса
        # Для простоты используем только случай p ≡ 3 (mod 4)
        if p % 4 == 3:
            r = pow(a, (p + 1) // 4, p)
            if (r * r) % p == a % p:
                return [r, p - r] if r != p - r else [r]

        # Полный перебор для малых p
        if p < 1000:
            roots = []
            for i in range(p):
                if (i * i) % p == a % p:
                    roots.append(i)
            return roots

        return []

def point_add(curve, P, Q):
    """Сложение точек на эллиптической кривой"""
    # Случай с точкой в бесконечности
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if curve.p:
        # Арифметика в конечном поле
        if x1 == x2:
            if y1 == y2:
                # Удвоение точки
                if y1 == 0:
                    return None  # Результат - точка в бесконечности
                s = (3 * x1**2 + curve.a) * pow(2 * y1, -1, curve.p) % curve.p
            else:
                return None  # Результат - точка в бесконечности
        else:
            # Обычное сложение
            s = (y2 - y1) * pow(x2 - x1, -1, curve.p) % curve.p

        x3 = (s**2 - x1 - x2) % curve.p
        y3 = (s * (x1 - x3) - y1) % curve.p
    else:
        # Арифметика в действительных числах
        if x1 == x2:
            if y1 == y2:
                # Удвоение точки
                if y1 == 0:
                    return None  # Результат - точка в бесконечности
                s = (3 * x1**2 + curve.a) / (2 * y1)
            else:
                return None  # Результат - точка в бесконечности
        else:
            # Обычное сложение
            s = (y2 - y1) / (x2 - x1)

        x3 = s**2 - x1 - x2
        y3 = s * (x1 - x3) - y1

    return (x3, y3)

def point_multiply(curve, k, P):
    """Умножение точки на скаляр (k*P)"""
    if k == 0 or P is None:
        return None

    if k == 1:
        return P

    # Алгоритм двойного и сложения
    result = None
    addend = P

    while k:
        if k & 1:  # Если младший бит установлен
            result = point_add(curve, result, addend)
        addend = point_add(curve, addend, addend)  # Удвоение
        k >>= 1  # Сдвиг вправо

    return result
