from PyQt6.QtCore import QTimer, QObject
import numpy as np

class AnimationEngine(QObject):
    def __init__(self, plotCanvas, mathCore):
        super().__init__()
        self.plotCanvas = plotCanvas
        self.mathCore = mathCore
        self.timer = QTimer()
        self.timer.timeout.connect(self.OnTimerTick)
        self.currentAnimMode = None

    def OnTimerTick(self):
        if self.currentAnimMode == "lagrange":
            self.NextLagrangeStep()
        elif self.currentAnimMode == "mnk":
            self.NextMnkStep()

    def StartLagrangeAnimation(self, xNodes, yNodes, paddingMultiplier=1.5, timerInterval=500):
        if not xNodes or len(xNodes) < 2:
            return
        self.currentAnimMode = "lagrange"
        self.xNodes, self.yNodes = np.array(xNodes), np.array(yNodes)

        minY, maxY = np.min(self.yNodes), np.max(self.yNodes)
        padding = (maxY - minY) * paddingMultiplier if (maxY - minY) != 0 else 1.0
        self.fixedYMin, self.fixedYMax = minY - padding, maxY + padding

        self.xEval = np.linspace(min(self.xNodes), max(self.xNodes), 500)
        self.currentIndex = 1

        self.plotCanvas.InitStaticPlot()
        self.timer.start(timerInterval)

    def NextLagrangeStep(self):
        if self.currentIndex > len(self.xNodes):
            self.timer.stop()
            return

        currentX = self.xNodes[:self.currentIndex]
        currentY = self.yNodes[:self.currentIndex]
        yEval = self.mathCore.CalculateLag(currentX, currentY, self.xEval)

        self.plotCanvas.axes.clear()
        self.plotCanvas.InitStaticPlot()
        self.plotCanvas.axes.set_ylim(self.fixedYMin, self.fixedYMax)

        scOld = None
        if self.currentIndex > 1:
            scOld = self.plotCanvas.axes.scatter(
                currentX[:-1], currentY[:-1],
                color='#FF5722',
                s=50,
                label='Вузли',
                zorder=5
            )

        scActive = self.plotCanvas.axes.scatter(
            currentX[-1], currentY[-1],
            color='#2196F3', s=100, edgecolors='black',
            label='Активний вузол', zorder=6
        )

        nodesToHover = [scActive]
        if scOld:
            nodesToHover.append(scOld)

        self.plotCanvas.SetHoverData(nodesToHover, None)

        self.plotCanvas.axes.scatter(
            currentX[-1], currentY[-1],
            color="#2196F3",
            s=100,
            edgecolors="black",
            label="Активний вузол",
            zorder=6
        )
        self.plotCanvas.axes.plot(
            self.xEval, yEval,
            color="#4CAF50",
            linewidth=2,
            label="Поліном Лагранжа",
            zorder=4
        )

        self.plotCanvas.axes.legend(loc="best")
        self.plotCanvas.draw()
        self.currentIndex += 1

    def StartMnkAnimation(self, xNodes, yNodes, degree, isLog, paddingMultiplier=1.5, timerInterval=50):
        if not xNodes or len(xNodes) < 2:
            return
        self.currentAnimMode = "mnk"
        self.xNodes, self.yNodes = np.array(xNodes), np.array(yNodes)

        self.xEval = np.linspace(min(self.xNodes), max(self.xNodes), 500)
        self.finalYEval, self.coefficients = self.mathCore.CalculateMnk(self.xNodes, self.yNodes, self.xEval, degree, isLog)
        self.yCalc, self.residuals = self.mathCore.CalculateResiduals(self.xNodes, self.yNodes, self.coefficients, degree, isLog)

        minY, maxY = np.min(self.yNodes), np.max(self.yNodes)
        padding = (maxY - minY) * paddingMultiplier if (maxY - minY) != 0 else 1.0
        self.fixedYMin, self.fixedYMax = minY - padding, maxY + padding

        self.totalFrames = 10
        self.currentFrame = 0
        self.residualIndex = 0

        self.plotCanvas.InitStaticPlot()
        self.timer.start(timerInterval)

        return self.residuals

    def NextMnkStep(self):
        self.plotCanvas.axes.clear()
        self.plotCanvas.InitStaticPlot()
        self.plotCanvas.axes.set_ylim(self.fixedYMin, self.fixedYMax)

        sc = self.plotCanvas.axes.scatter(
            self.xNodes, self.yNodes,
            color="#FF5722",
            s=50,
            label="Експериментальні точки",
            zorder=5
        )
        self.plotCanvas.SetHoverData([sc], self.residuals)

        if self.currentFrame <= self.totalFrames:
            t = self.currentFrame / self.totalFrames
            currentYEval = self.finalYEval * t

            self.plotCanvas.axes.plot(
                self.xEval, currentYEval,
                color="#9C27B0",
                linewidth=2,
                label="Тренд",
                zorder=4
            )
            self.currentFrame += 1
        else:
            self.plotCanvas.axes.plot(
                self.xEval, self.finalYEval,
                color="#9C27B0",
                linewidth=2,
                label="Тренд",
                zorder=4
            )

            for i in range(self.residualIndex):
                x = [self.xNodes[i], self.xNodes[i]]
                y = [self.yNodes[i], self.yCalc[i]]
                self.plotCanvas.axes.plot(
                    x, y,
                    color="#E53935",
                    linestyle="--",
                    linewidth=1.5,
                    zorder=3
                )

            if self.residualIndex > 0:
                self.plotCanvas.axes.plot(
                    [], [],
                    color="#E53935",
                    linestyle="--",
                    label="Залишки"
                )

            self.residualIndex += 1

            if self.residualIndex > len(self.xNodes):
                self.timer.stop()

        self.plotCanvas.axes.legend(loc="best")
        self.plotCanvas.draw()
