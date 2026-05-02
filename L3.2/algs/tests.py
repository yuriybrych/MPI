from bruteforce import BruteForce

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

def TestBF():
    #
    #   Повний перебір
    #
    algBFData_maxVal, algBFData_items = BruteForce(TestDataStruct.W, TestDataStruct.w, TestDataStruct.v)
    algBFData_itemsDisplay = [i + 1 for i in algBFData_items]

    print(
        "Алгоритм: Повний перебір\n" +
        f"\tМакс. цінність: {algBFData_maxVal}\n" +
        f"\tВибрані предмети: {algBFData_itemsDisplay}\n"
    )

    return [algBFData_maxVal, algBFData_itemsDisplay]


if __name__ == "__main__":
    TestDataStruct.PrintValues()
    BFDataRAW = TestBF()
