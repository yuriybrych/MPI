import numpy as np

class MathCore:
    @staticmethod
    def CalculateLag(xNodes, yNodes, xEval):
        xNodes = np.asarray(xNodes, dtype=float)
        yNodes = np.asarray(yNodes, dtype=float)
        xEval = np.asarray(xEval, dtype=float)

        n = len(xNodes)
        yEval = np.zeros_like(xEval, dtype=float)

        for i in range(n):
            L_i = np.ones_like(xEval, dtype=float)
            for j in range(n):
                if i != j:
                    if xNodes[i] == xNodes[j]:
                        continue
                    L_i *= (xEval - xNodes[j]) / (xNodes[i] - xNodes[j])

            yEval += yNodes[i] * L_i
        return yEval

    @staticmethod
    def GenerateDesignMatrix(xNodes, degree=2, isLog=False):
        xNodes = np.asarray(xNodes, dtype=float)

        if isLog:
            lnX = np.log(xNodes)
            return np.column_stack((np.ones_like(xNodes), lnX))
        else:
            return np.vander(xNodes, N=degree + 1, increasing=True)


if __name__ == "__main__":
    testX = [1, 2, 3]
    testY = [2, 4, 6]
    evalX = np.linspace(1, 3, 5)
    print(MathCore.CalculateLag(testX, testY, evalX))

    print(MathCore.GenerateDesignMatrix(testX))
