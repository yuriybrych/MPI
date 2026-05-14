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

        if self.currentIndex > 1:
            self.plotCanvas.axes.scatter(
                currentX[:-1], currentY[:-1],
                color="#FF5722",
                s=50,
                label="Вузли",
                zorder=5
            )

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
