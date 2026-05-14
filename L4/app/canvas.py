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

        self.scatterNode = None
        self.residualsData = None

        self.fig.canvas.mpl_connect("motion_notify_event", self.OnHover)

        self.InitStaticPlot()

    def InitStaticPlot(self):
        self.axes.clear()

        self.axes.set_title("Чудесні графіки, боже, я їх обожнюю", fontsize=12, fontweight="bold", color="#37474F")
        self.axes.set_xlabel("Координата X", fontsize=10, color="#546E7A")
        self.axes.set_ylabel("Координата Y", fontsize=10, color="#546E7A")
        self.axes.grid(True, linestyle="--", alpha=0.6, color="#B0BEC5")

        self.annot = self.axes.annotate(
            "", xy=(0, 0),
            xytext=(0, 0),
            textcoords="offset points",
            bbox=dict(
                boxstyle="round,pad=0.5",
                fc="#FFFFFF",
                ec="#AAAAAA",
                lw=1
            )
        )

        self.annot.set_visible(False)
        self.annot.set_zorder(10)

        self.draw()
        self.fig.tight_layout()

    def SetHoverData(self, nodes, residuals=None):
        self.scatterNodes = nodes if isinstance(nodes, list) else [nodes]
        self.residualsData = residuals

    def PlotBasePoints(self, xNodes, yNodes):
        self.InitStaticPlot()
        if not xNodes or not yNodes:
            return

        sc = self.axes.scatter(
            xNodes, yNodes,
            color="#FF5722",
            s=50,
            edgecolors="#BF360C",
            label="Експериментальні точки",
            zorder=5
        )

        self.SetHoverData(sc, None)
        self.axes.legend(loc='best', fontsize=10, facecolor='#F8F9FA', edgecolor='#CFD8DC')
        self.draw()

    def OnHover(self, event):
        if event.inaxes == self.axes and hasattr(self, 'scatterNodes'):
            for sc in self.scatterNodes:
                cont, ind = sc.contains(event)
                if cont:
                    self.UpdateTooltip(sc, ind, event)
                    self.annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                    return

            if self.annot.get_visible():
                self.annot.set_visible(False)
                self.fig.canvas.draw_idle()

    def UpdateTooltip(self, sc, ind, event):
        idx = ind["ind"][0]
        pos = sc.get_offsets()[idx]

        text = f"X: {pos[0]:.4f}\nY: {pos[1]:.4f}"

        if self.residualsData is not None and idx < len(self.residualsData):
            text += f"\nПохибка: {self.residualsData[idx]:.4f}"

        self.annot.xy = pos
        self.annot.set_text(text)

        xMin, xMax = self.axes.get_xlim()
        if pos[0] > (xMin + (xMax - xMin) * 0.75):
            self.annot.set_position((-90, 10)) 
        else:
            self.annot.set_position((10, 10))
