def DynamicProgramming(
    capacity: int,
    weights: list[int],
    values: list[int]
) -> tuple[
    int,
    list[int],
    list[list[int]],
    list[dict]
]:
    #
    #   Метод динамічного програмування.
    #   Повертає:
    #      1. maxProfit: Максимальна цінність
    #      2. selectedItems: Список індексів вибраних предметів
    #      3. dp: Двовимірна матриця
    #      4. animationLog: Журнал кроків
    #
    n = len(weights)
    animationLog = []
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    #
    #   Заповнення таблиці AKA "Розрахунок"
    #
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            itemWeight = weights[i - 1]
            itemValue = values[i - 1]

            if itemWeight <= w:
                value_ifTaken = dp[i - 1][w - itemWeight] + itemValue
                value_ifSkipped = dp[i - 1][w]

                if value_ifTaken > value_ifSkipped:
                    dp[i][w] = value_ifTaken
                    animationLog.append(
                        {
                            'i': i,
                            'w': w,
                            'val': value_ifTaken,
                            'action': 'take',
                            'source_w': w - itemWeight
                        }
                    )
                else:
                    dp[i][w] = value_ifSkipped
                    animationLog.append(
                        {
                            'i': i,
                            'w': w,
                            'val': value_ifSkipped,
                            'action': 'skip',
                            'source_w': w
                        }
                    )
            else:
                dp[i][w] = dp[i - 1][w]
                animationLog.append(
                    {
                        'i': i,
                        'w': w,
                        'val': dp[i - 1][w],
                        'action': 'skip_full',
                        'source_w': w
                    }
                )

    maxProfit = dp[n][capacity]

    #
    #   Відновлення рішення
    #
    selectedItems = []
    current_w = capacity

    for i in range(n, 0, -1):
        if current_w <= 0:
            break

        if dp[i][current_w] != dp[i - 1][current_w]:
            selectedItems.append(i - 1)
            current_w -= weights[i - 1]

    selectedItems.reverse()

    return maxProfit, selectedItems, dp, animationLog
