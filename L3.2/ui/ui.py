from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QFormLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QSlider,
    QRadioButton, QButtonGroup
)
from .stylesheet import AIO
from PyQt6.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulator for loading parcels into a Nova Poshta vehicle 4000")
        self.resize(1600, 480)
        self.InitUI()

    def InitUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.setStyleSheet(AIO)

        # Main
        mainLayout = QHBoxLayout(centralWidget)

        # Left
        leftPanelWidget = QWidget()
        leftPanelWidget.setFixedWidth(320)
        leftPanel = QVBoxLayout(leftPanelWidget)
        leftPanel.setContentsMargins(0, 0, 0, 0)

        inputGroup = QGroupBox("Дані")
        inputLayout = QFormLayout()

        self.capacityInput = QLineEdit("25")
        inputLayout.addRow("Місткість [W]:", self.capacityInput)

        self.weightsInput = QLineEdit("3, 2, 5, 7, 6, 4, 3, 1")
        inputLayout.addRow("Ваги [w]:", self.weightsInput)

        self.valuesInput = QLineEdit("5, 3, 8, 13, 11, 6, 7, 2")
        inputLayout.addRow("Цінності [v]:", self.valuesInput)

        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setRange(100, 2000)
        self.speedSlider.setValue(500)
        inputLayout.addRow("Швидкість:", self.speedSlider)

        inputGroup.setLayout(inputLayout)
        leftPanel.addWidget(inputGroup)

        algoGroup = QGroupBox("Алгоритм")
        algoLayout = QVBoxLayout()

        self.algoGroupButtons = QButtonGroup(self)
        algos = [
            "Метод повного перебору",
            "Рекурсивний метод",
            "Жадібний алгоритм",
            "Динамічне програмування",
            "Метод гілок та меж"
        ]

        for i, text in enumerate(algos):
            btn = QRadioButton(text)
            if i == 3:
                btn.setChecked(True)
            self.algoGroupButtons.addButton(btn, i)
            algoLayout.addWidget(btn)

        algoGroup.setLayout(algoLayout)
        leftPanel.addWidget(algoGroup)

        infoGroup = QGroupBox("Результати")
        infoLayout = QVBoxLayout()

        self.resultLabel = QLabel("Макс. цінність: -")
        self.itemsLabel = QLabel("Оптимальний набір: -")
        self.itemsLabel.setWordWrap(True)

        infoLayout.addWidget(self.resultLabel)
        infoLayout.addWidget(self.itemsLabel)

        infoGroup.setLayout(infoLayout)
        leftPanel.addWidget(infoGroup)
        leftPanel.addStretch()

        buttonGroup = QGroupBox("Керування")
        buttonLayout = QVBoxLayout()

        self.calcButton = QPushButton("Розрахувати")
        self.calcButton.setProperty("calcButton", True)
        self.stepButton = QPushButton("Покроково")
        self.stepButton.setProperty("stepButton", True)
        self.clearButton = QPushButton("Очистити")
        self.clearButton.setProperty("clearButton", True)

        buttonLayout.addWidget(self.calcButton)
        buttonLayout.addWidget(self.stepButton)
        buttonLayout.addWidget(self.clearButton)

        buttonGroup.setLayout(buttonLayout)
        leftPanel.addWidget(buttonGroup)

        copyrightLabel = QLabel("AbsoluteGarbage Corp.\nАвтор: Брич Юрій Михайлович\nВсі права не захищені.")
        copyrightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyrightLabel.setStyleSheet("color: gray; font-size: 10px; margin: 5px;")
        leftPanel.addWidget(copyrightLabel)

        mainLayout.addWidget(leftPanelWidget)

        # Right
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        mainLayout.addWidget(self.table)
