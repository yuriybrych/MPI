import itertools

def BruteForce(
    capacity: int,
    weights: list[int],
    values: list[int]
) -> tuple[
    int,
    list[int]
]:
    #
    #   Повний перебір
    #   Повертається кортеж: (макс. цінність, список індексів вибраних предметів)
    #
    n = len(weights)
    bestValue = 0
    bestCombination = []

    for r in range(1, n + 1):
        for combo in itertools.combinations(range(n), r):
            currentWeight = sum(weights[i] for i in combo)
            currentvalue = sum(values[i] for i in combo)

            if currentWeight <= capacity and currentvalue > bestValue:
                bestValue = currentvalue
                bestCombination = list(combo)

    return bestValue, bestCombination
