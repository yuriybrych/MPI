from typing import Callable
from bruteforce import BruteForce
from recursive import Recursive
from greedy import Greedy
from bnb import BranchAndBound
from dynprog import DynamicProgramming

class TestDataStruct:
    #
    #   Варіант із методички
    #
    W = 25
    w = [3, 2, 5, 7, 6, 4, 3, 1]
    v = [5, 3, 8, 13, 11, 6, 7, 2]

    def PrintValues():
        print(
            "Початкові дані:\n"
            f"\tМісткість: {TestDataStruct.W}\n" +
            f"\tВаги: {TestDataStruct.w}\n" +
            f"\tЦінності: {TestDataStruct.v}\n"
        )

def TestAlgorithm(algName, algorithm: Callable):
    algData_maxVal, algData_items = algorithm()
    algData_itemsDisplay = [i + 1 for i in algData_items]

    print(
        f"Алгоритм: {algName}\n" +
        f"\tМакс. цінність: {algData_maxVal}\n" +
        f"\tВибрані предмети: {algData_itemsDisplay}\n"
    )

    return [algData_maxVal, algData_itemsDisplay]

def TestDP():
    #
    #   Окремий тест метода динамічного програмування
    #
    maxVal, items, dpMatrix, animationLog = DynamicProgramming(TestDataStruct.W, TestDataStruct.w, TestDataStruct.v)
    itemsDisplay = [i + 1 for i in items]

    print(
        "Алгоритм: Динамічне програмування\n" +
        f"\tМакс. цінність: {maxVal}\n" +
        f"\tВибрані предмети: {itemsDisplay}\n" +
        f"\tКількість кроків для анімації: {len(animationLog)}\n"
    )

    return [maxVal, itemsDisplay]


if __name__ == "__main__":
    TestDataStruct.PrintValues()
    TestAlgorithm(
        "Повний перебір",
        lambda W = TestDataStruct.W, w = TestDataStruct.w, v = TestDataStruct.v:
        BruteForce(W, w, v)
    )

    TestAlgorithm(
        "Рекурсивний метод",
        lambda W = TestDataStruct.W, w = TestDataStruct.w, v = TestDataStruct.v:
        Recursive(W, w, v)
    )

    TestAlgorithm(
        "Жадібний алгоритм",
        lambda W = TestDataStruct.W, w = TestDataStruct.w, v = TestDataStruct.v:
        Greedy(W, w, v)
    )

    TestAlgorithm(
        "Метод гілок та меж",
        lambda W = TestDataStruct.W, w = TestDataStruct.w, v = TestDataStruct.v:
        BranchAndBound(W, w, v)
    )

    TestDP()
