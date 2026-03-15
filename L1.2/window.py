import sys
from PyQt6.QtWidgets import (
    QApplication, QFormLayout, QComboBox, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QStyle, QColorDialog
)
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtWidgets import QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from mathModule import MathModule
import time

# я це все коментувати не хочу :(

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Garbage Graph Maker 3500")
        self.resize(1280, 500)

        self.setStyleSheet("""
            QPushButton {
                background-color: #eee;
                color: black;
                font-weight: bold;
                padding-top: 2px;
                padding-bottom: 2px;
                padding-left: 30px;
                padding-right: 30px;
                border-radius: 6px;
                border: 1px solid #aaa;
            }

            QPushButton:hover {
                background-color: #fff;
            }

            QPushButton:pressed {
                background-color: #ddd;
            }

            QPushButton[buildButton = "true"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #45c27b, stop:1 #36a668);
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #2ea361;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton[buildButton = "true"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4ed187, stop:1 #3fb572);
                border: 1px solid #36b36d;
            }

            QPushButton[buildButton = "true"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #329e61, stop:1 #2c8c56);
                border: 1px solid #26854b;
            }

            QPushButton[clearButton = "true"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c24545, stop:1 #a63636);
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #a32e2e;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QPushButton[clearButton = "true"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d1554e, stop:1 #b53f3f);
                border: 1px solid #b33636;
            }

            QPushButton[clearButton = "true"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9e3732, stop:1 #8c2c2c);
                border: 1px solid #852626;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QLineEdit {
                background: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 5px;
            }

            QLineEdit:focus {
                border: 1px solid #3CB371;
            }

            QComboBox {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 5px;
            }

            QComboBox:focus {
                border: 1px solid #3CB371;
            }

            QComboBox::drop-down {
                background-color: #ddd;
                border: 1px solid #ddd;
                border-top-left-radius: 0px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 4px;
            }
        """)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.colors = {
            "Червоний": "red", "Синій": "blue", "Зелений": "green",
            "Чорний": "black", "Голубий": "cyan", "Пурпурний": "magenta",
            "Жовтий": "yellow"
        }

        self.customColor = "#000000"

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        self.setWindowIcon(icon)

        self.mainLayout = QHBoxLayout(centralWidget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.TimerTick)

        self.currentX = []
        self.currentY = []
        self.currentIndex = 0
        self.pointsPerFrame = 1
        self.currentLine = None

        self.CreateControlPanel()

        self.createGraphPanel()

    def CreateControlPanel(self):
        LeftLayout = QVBoxLayout()
        mainFormLayout = QVBoxLayout()

        controlGroup = QGroupBox("Параметри руху")
        controlGroup.setFixedWidth(300)

        form = QFormLayout()

        self.input_x0 = QLineEdit("0")
        self.input_y0 = QLineEdit("0")
        self.input_angle = QLineEdit("45")
        self.input_v0 = QLineEdit("1")
        self.input_a = QLineEdit("0")
        self.input_time = QLineEdit("5")
        self.input_fps = QLineEdit("30")

        self.graphColor = QComboBox()
        self.graphColor.addItems(["Червоний", "Синій", "Зелений", "Чорний", "Голубий", "Пурпурний", "Жовтий", "Свій"])
        self.graphColor.currentTextChanged.connect(self.ChooseCustomColor)

        form.addRow("Координата X0 (м):", self.input_x0)
        form.addRow("Координата Y0 (м):", self.input_y0)
        form.addRow("Кут (градуси):", self.input_angle)
        form.addRow("Поч. швидкість (м/с):", self.input_v0)
        form.addRow("Прискорення (м/с^2):", self.input_a)
        form.addRow("Час польоту (с):", self.input_time)
        form.addRow("FPS (кадри/с):", self.input_fps)
        form.addRow("Колір траєкторії:", self.graphColor)

        mainFormLayout.addLayout(form)

        mainFormLayout.addStretch()

        buttonLayout = QVBoxLayout()
        buttonLayout.setSpacing(0)

        self.buttonBuild = QPushButton("Побудувати графік")
        self.buttonBuild.setProperty("buildButton", True)
        self.buttonClear = QPushButton("Очистити")
        self.buttonClear.setProperty("clearButton", True)

        self.buttonBuild.clicked.connect(self.BuildGraph)
        self.buttonClear.clicked.connect(self.ClearGraph)

        buttonLayout.addWidget(self.buttonBuild)
        buttonLayout.addWidget(self.buttonClear)

        mainFormLayout.addLayout(buttonLayout)

        controlGroup.setLayout(mainFormLayout)
        LeftLayout.addWidget(controlGroup)

        copyright = QLabel("AbsoluteGarbage Corp.\nАвтор: Брич Юрій Михайлович\nВсі права не захищені.")
        copyright.setStyleSheet("margin: 5px;")
        LeftLayout.addWidget(copyright)

        self.mainLayout.addLayout(LeftLayout)

    def createGraphPanel(self):
        MPLlayout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, linestyle = '--')

        self.toolbar = NavigationToolbar(self.canvas, self)

        MPLlayout.addWidget(self.toolbar)
        MPLlayout.addWidget(self.canvas)

        self.mainLayout.addLayout(MPLlayout)

    def ClearGraph(self):
        self.timer.stop()
        self.axes.clear()
        self.axes.grid(True, linestyle='--')
        self.canvas.draw()

    def BuildGraph(self):
        try:
            x0 = float(self.input_x0.text())
            y0 = float(self.input_y0.text())
            v0 = float(self.input_v0.text())
            a = float(self.input_a.text())
            angleDeg = float(self.input_angle.text())
            totalTime = float(self.input_time.text())
            fps = int(self.input_fps.text())

        except ValueError:
            QMessageBox.critical(self, "We're in trouble!", "Схоже, в форму задано не всі параметри, або задано не числове значення")
            return

        mathModule = MathModule(x0, y0, v0, a, angleDeg, totalTime)
        t, x, y = mathModule.DoCalculations()

        selectedColorName = self.graphColor.currentText()
        if selectedColorName == "Свій":
            plotColor = self.customColor
        else:
            plotColor = self.colors.get(selectedColorName, "black")

        self.currentX = x
        self.currentY = y
        self.currentIndex = 0

        totalFrames = totalTime * fps
        if totalFrames == 0:
            totalFrames = 1
        self.pointsPerFrame = max(1, len(x) // int(totalFrames))

        self.axes.set_xlim(min(x) - 1, max(x) + 1)
        self.axes.set_ylim(min(y) - 1, max(y) + 1)

        if fps <= 0:
            self.axes.plot(
                x,
                y,
                color = plotColor,
                label = f"v₀ = {v0}, a = {a}, ∠ = {angleDeg}°"
            )
            self.axes.legend(loc = 'upper left')
            self.canvas.draw()
            return

        self.currentX = x
        self.currentY = y
        self.currentIndex = 0

        self.currentLine, = self.axes.plot(
            [],
            [],
            color = plotColor,
            label = f"v₀ = {v0}, a = {a}, ∠ = {angleDeg}°"
        )

        legend = self.axes.get_legend()
        if legend:
            legend.remove()

        self.canvas.draw()
        self.BGCache = self.canvas.copy_from_bbox(self.axes.bbox)

        self.animationStartTime = time.time()
        self.animationTotalTime = totalTime

        self.timer.start(int(1000 / fps))

    def ChooseCustomColor(self, text):
        if text == "Свій":
            color = QColorDialog.getColor()

            if color.isValid():
                self.customColor = color.name()
            else:
                self.graphColor.setCurrentText("Чорний")

    def TimerTick(self):
        elapsedTime = time.time() - self.animationStartTime
        progress = elapsedTime / self.animationTotalTime

        if progress >= 1.0:
            self.currentIndex = len(self.currentX)
            self.timer.stop()
            self.axes.legend(loc = "upper left")
            self.canvas.draw()
            return
        else:
            self.currentIndex = int(progress * len(self.currentX))

        self.currentLine.set_data(
            self.currentX[:self.currentIndex],
            self.currentY[:self.currentIndex]
        )

        self.canvas.restore_region(self.BGCache)

        self.axes.draw_artist(self.currentLine)

        self.canvas.blit(self.axes.bbox)

        self.canvas.flush_events()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
