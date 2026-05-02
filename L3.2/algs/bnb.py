class BranchAndBoundSolver:
    #
    #   Метод гілок та меж
    #   Повертається кортеж: (макс. цінність, список індексів вибраних предметів)
    #
    def __init__(self, capacity: int, weights: list[int], values: list[int]):
        self.capacity = capacity
        self.n = len(weights)
        self.maxProfit = 0
        self.bestItems = []
        self.items = []

        for i in range(self.n):
            self.items.append(
                {
                    'index': i,
                    'weight': weights[i],
                    'value': values[i],
                    'ratio': values[i] / weights[i] if weights[i] > 0 else 0
                }
            )

        self.items.sort(key = lambda x: x['ratio'], reverse = True)

    def Bound(self, level, currentWeight, currentProfit):
        if currentWeight == self.capacity:
            return currentProfit

        if currentWeight >= self.capacity:
            return 0

        profitBound = currentProfit
        j = level + 1
        totweight = currentWeight

        while j < self.n and totweight + self.items[j]['weight'] <= self.capacity:
            totweight += self.items[j]['weight']
            profitBound += self.items[j]['value']
            j += 1

        if j < self.n:
            profitBound += (self.capacity - totweight) * self.items[j]['ratio']

        return profitBound

    def DepthFirstSearch(self, level, currentWeight, currentProfit, selected):
        if currentWeight <= self.capacity and currentProfit > self.maxProfit:
            self.maxProfit = currentProfit
            self.bestItems = selected[:]

        if level == self.n - 1:
            return

        nextLevel = level + 1
        nextItem = self.items[nextLevel]

        # Г1: Беремо предмет
        if currentWeight + nextItem['weight'] <= self.capacity:
            nextProfit = currentProfit + nextItem['value']
            nextWeight = currentWeight + nextItem['weight']

            if self.Bound(nextLevel, nextWeight, nextProfit) > self.maxProfit:
                self.DepthFirstSearch(nextLevel, nextWeight, nextProfit, selected + [nextItem['index']])

        # Г2: Не беремо предмет
        if self.Bound(nextLevel, currentWeight, currentProfit) > self.maxProfit:
            self.DepthFirstSearch(nextLevel, currentWeight, currentProfit, selected)

    def Solve(self):
        self.DepthFirstSearch(-1, 0, 0, [])
        return self.maxProfit, self.bestItems


def BranchAndBound(
    capacity: int,
    weights: list[int],
    values: list[int]
) -> tuple[
    int,
    list[int]
]:
    #
    #   Метод гілок та меж (Хелпер)
    #   ВСЕ ЩЕ повертається кортеж: (макс. цінність, список індексів вибраних предметів)
    #
    solver = BranchAndBoundSolver(capacity, weights, values)
    return solver.Solve()
