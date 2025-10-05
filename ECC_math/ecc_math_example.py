import ecc_tool as ecc


# Создаем демонстрационные функции для лекции
def demonstrate_ecc_operations():
    """Демонстрирует основные операции на эллиптических кривых"""
    
    print("=== ДЕМОНСТРАЦИЯ ОПЕРАЦИЙ НА ЭЛЛИПТИЧЕСКИХ КРИВЫХ ===\n")
    
    # Пример 1: Кривая secp256k1 (Bitcoin)
    print("1. Кривая secp256k1 (используется в Bitcoin)")
    print("   y² = x³ + 7")
    secp256k1 = ecc.EllipticCurve(0, 7, None)  # Для демонстрации используем без модуля
    
    # Пример 2: Кривая в конечном поле
    print("\n2. Кривая в конечном поле F₂₃")
    print("   y² ≡ x³ + 2x + 3 (mod 23)")
    curve_f23 = ecc.EllipticCurve(2, 3, 23)
    
    # Найдем все точки кривой в F₂₃
    points = []
    for x in range(23):
        y_values = curve_f23.get_y(x)
        for y in y_values:
            points.append((x, y))
    
    print(f"   Кривая содержит {len(points)} точек (плюс точка в бесконечности)")
    print(f"   Первые 10 точек: {points[:10]}")
    
    # Пример 3: Сложение точек
    if len(points) >= 2:
        P = points[0]
        Q = points[1]
        R = ecc.point_add(curve_f23, P, Q)
        
        print(f"\n3. Сложение точек на кривой:")
        print(f"   P = {P}")
        print(f"   Q = {Q}")
        print(f"   P + Q = {R}")

        P_doubled = ecc.point_add(curve_f23, P, P)
        print(f"   2P = {P_doubled}")

    if len(points) >= 1:
        P = points[0]
        print(f"\n4. Скалярное умножение:")
        print(f"   Базовая точка P = {P}")
        
        for k in range(2, 9):
            kP = ecc.point_multiply(curve_f23, k, P)
            if kP == None:
                print(f"   {k}P = O - точка в бесконечности")
            else:
                print(f"   {k}P = {kP}")
    
    return curve_f23, points

def demonstrate_ecdh():
    
    # Используем кривую y² ≡ x³ + 2x + 3 (mod 23)
    curve = ecc.EllipticCurve(2, 3, 23)
    
    # Найдем базовую точку G
    for x in range(23):
        y_values = curve.get_y(x)
        if y_values:
            G = (x, y_values[0])
            break
    
    print(f"Выбранная базовая точка G = {G}")
    
    # Алиса и Боб генерируют приватные ключи
    import random
    random.seed(42)
    
    alice_private = random.randint(2, 22)
    bob_private = random.randint(2, 22)
    
    print(f"\nАлиса выбирает приватный ключ: dₐ = {alice_private}")
    print(f"Боб выбирает приватный ключ: dᵦ = {bob_private}")
    
    # Вычисляют публичные ключи
    alice_public = ecc.point_multiply(curve, alice_private, G)
    bob_public = ecc.point_multiply(curve, bob_private, G)
    
    print(f"\nАлиса вычисляет публичный ключ: Hₐ = {alice_private}×G = {alice_public}")
    print(f"Боб вычисляет публичный ключ: Hᵦ = {bob_private}×G = {bob_public}")
    
    print("\n Алиса и Боб обмениваются публичными ключами по открытому каналу")
    
    # Вычисляют общий секрет
    alice_secret = ecc.point_multiply(curve, alice_private, bob_public)
    bob_secret = ecc.point_multiply(curve, bob_private, alice_public)
    
    print(f"\nАлиса вычисляет: S = dₐ×Hᵦ = {alice_private}×{bob_public} = {alice_secret}")
    print(f"Боб вычисляет: S = dᵦ×Hₐ = {bob_private}×{alice_public} = {bob_secret}")

    print("\nАлиса и Боб получили одинаковый общий секрет")
    print(f"   Общий секрет: S = {alice_secret}")

    print(f"\n Математическое обоснование:")
    print(f"   S = dₐ×(dᵦ×G) = dₐ×dᵦ×G = {alice_private}×{bob_private}×G")
    print(f"   S = dᵦ×(dₐ×G) = dᵦ×dₐ×G = {bob_private}×{alice_private}×G")
    print(f"   Оба выражения равны {(alice_private * bob_private) % 23}×G")
    
    return alice_secret, bob_secret

def demonstrate_discrete_log_problem():
    """Демонстрирует проблему дискретного логарифма"""

    curve = ecc.EllipticCurve(2, 3, 23)
    
    # Найдем базовую точку
    for x in range(23):
        y_values = curve.get_y(x)
        if y_values:
            G = (x, y_values[0])
            break
    
    # Выберем случайное k
    k = 7
    P = ecc.point_multiply(curve, k, G)
    
    print(f"Дано: G = {G} (базовая точка)")
    print(f"Дано: P = {P} (результат k×G)")
    print(f"Найти: k = ? (приватный ключ)")
    
    print(f"\n Решение методом полного перебора:")
    
    # Перебираем все возможные значения k
    for test_k in range(1, 24):
        test_P = ecc.point_multiply(curve, test_k, G)
        if test_P == P:
            print(f"   Найдено: k = {test_k}")
            print(f"   Проверка: {test_k}×{G} = {test_P}")
            break
        else:
            print(f"   k = {test_k}: {test_k}×G = {test_P} ≠ P")
    
    print(f"\n Для малого поля (p = 23) задача решается за {23} операций")
    print(f"   Для Bitcoin (p ≈ 2²⁵⁶) потребовалось бы ~2²⁵⁶ операций!")
    print(f"   Это примерно 10⁷⁷ операций")

if __name__ == "__main__":
    curve, points = demonstrate_ecc_operations()
    
    alice_secret, bob_secret = demonstrate_ecdh()
    
    demonstrate_discrete_log_problem()

