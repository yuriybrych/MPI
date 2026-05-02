def Recursive(
    capacity: int,
    weights: list[int],
    values: list[int],
    n: int = None
) -> tuple[
    int,
    list[int]
]:
    #
    #   Рекурсивний метод
    #   Повертається кортеж: (макс. цінність, список індексів вибраних предметів)
    #
    if n is None:
        n = len(weights)

    if n == 0 or capacity == 0:
        return 0, []

    currentItem = n - 1

    if weights[currentItem] > capacity:
        return Recursive(capacity, weights, values, n - 1)

    # Г1 | Не беремо предмет
    valueWithout, itemsWithout = Recursive(capacity, weights, values, n - 1)

    # Г2 | Беремо предмет
    valueWithSub, itemsWithSub = Recursive(capacity - weights[currentItem], weights, values, n - 1)
    valueWith = values[currentItem] + valueWithSub

    # Порівняння результатів двох гілок
    if valueWith > valueWithout:
        return valueWith, itemsWithSub + [currentItem]
    else:
        return valueWithout, itemsWithout
