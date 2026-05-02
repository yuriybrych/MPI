def Greedy(
    capacity: int,
    weights: list[int],
    values: list[int]
) -> tuple[
    int,
    list[int]
]:
    #
    #   Жадібний алгоритм
    #   Повертається кортеж: (макс. цінність, список індексів вибраних предметів)
    #
    n = len(weights)
    items = []

    for i in range(n):
        items.append({
            'index': i,
            'weight': weights[i],
            'value': values[i],
            'ratio': values[i] / weights[i]
        })

    items.sort(key = lambda x: x['ratio'], reverse = True)

    totalValue = 0
    currentWeight = 0
    selectedItems = []

    for item in items:
        if currentWeight + item['weight'] <= capacity:
            currentWeight += item['weight']
            totalValue += item['value']
            selectedItems.append(item['index'])

    return totalValue, selectedItems
