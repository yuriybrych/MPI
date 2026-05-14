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

    @staticmethod
    def CalculateMnk(xNodes, yNodes, xEval, degree=2, isLog=False):
        yNodes = np.asarray(yNodes, dtype=float)

        matrixX = MathCore.GenerateDesignMatrix(xNodes, degree, isLog)

        B, residuals, rank, s = np.linalg.lstsq(matrixX, yNodes, rcond=None)

        evalMatrix = MathCore.GenerateDesignMatrix(xEval, degree, isLog)
        yEval = evalMatrix @ B

        return yEval, B

    @staticmethod
    def CalculateResiduals(xNodes, yNodes, B, degree=2, isLog=False):
        yNodes = np.asarray(yNodes, dtype=float)

        matrixX = MathCore.GenerateDesignMatrix(xNodes, degree, isLog)
        yCalc = matrixX @ B

        residuals = yNodes - yCalc

        return yCalc, residuals

    @staticmethod
    def CalculateMetrics(residuals):
        residuals = np.asarray(residuals, dtype=float)
        mse = np.mean(residuals ** 2)
        return mse


if __name__ == "__main__":
    testX = [1, 2, 3]
    testY = [2, 4, 6]
    evalX = np.linspace(1, 3, 5)
    print("Інтерполяція:\n", MathCore.CalculateLag(testX, testY, evalX))

    print("\nМатриця:\n", MathCore.GenerateDesignMatrix(testX))

    yEvalMnk, coefficients = MathCore.CalculateMnk(testX, testY, evalX, degree=1, isLog=False)
    print("\nМНК:\n", yEvalMnk)
    print("b0, b1:\n", coefficients)

    yCalc, res = MathCore.CalculateResiduals(testX, testY, coefficients, degree=1, isLog=False)
    print("\nРозрахункові Y у вузлах:\n", yCalc)
    print("Залишки:\n", res)

    print(MathCore.CalculateMetrics(res))