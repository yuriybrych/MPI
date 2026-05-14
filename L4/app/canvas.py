import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use("QtAgg")

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(dpi=100, layout="tight")
        self.axes = self.fig.add_subplot(111)

        super().__init__(self.fig)
        self.setParent(parent)
        self.InitStaticPlot()

    def InitStaticPlot(self):
        self.axes.clear()

        self.axes.set_title("Чудесні графіки, боже, я їх обожнюю", fontsize=12, fontweight="bold", color="#37474F")
        self.axes.set_xlabel("Координата X", fontsize=10, color="#546E7A")
        self.axes.set_ylabel("Координата Y", fontsize=10, color="#546E7A")
        self.axes.grid(True, linestyle="--", alpha=0.6, color="#B0BEC5")

        self.draw()
        self.fig.tight_layout()

    def PlotBasePoints(self, xNodes, yNodes):
        self.InitStaticPlot()
        if not xNodes or not yNodes:
            return

        self.axes.scatter(
            xNodes, yNodes,
            color="#FF5722",
            s=50,
            edgecolors="#BF360C",
            label="Експериментальні точки",
            zorder=5
        )

        self.axes.legend(loc="best", fontsize=10, facecolor="#F8F9FA", edgecolor="#CFD8DC")

        self.draw()