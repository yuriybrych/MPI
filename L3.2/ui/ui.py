from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QFormLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QSlider, QHeaderView, QStyle,
    QRadioButton, QButtonGroup, QMessageBox, QTableWidgetItem, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from .stylesheet import AIO

from algs import BruteForce
from algs import Recursive
from algs import Greedy
from algs import BranchAndBound
from algs import DynamicProgramming


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulator for loading parcels into a Nova Poshta vehicle 4000")
        self.resize(1600, 480)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
        self.setWindowIcon(icon)

        self.timer = QTimer()
        self.timer.timeout.connect(self.AnimateStep)
        self.animationLog = []
        self.currentStep = 0
        self.dpMatrix = []
        self.cellsToRestore = []

        self.InitUI()
        self.connectSignals()

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
        self.speedSlider.setRange(0, 1000)
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

    def connectSignals(self):
        self.calcButton.clicked.connect(self.RunAuto)
        self.stepButton.clicked.connect(self.RunStep)
        self.clearButton.clicked.connect(self.ClearTable)
        self.speedSlider.valueChanged.connect(self.UpdateSpeed)
        self.algoGroupButtons.buttonClicked.connect(self.OnAlgChange)

    def OnAlgChange(self, button):
        self.ClearTable()

    def UpdateSpeed(self):
        speed = self.speedSlider.value()
        interval = 1000 - speed
        if self.timer.isActive():
            self.timer.setInterval(interval)

    def parse_inputs(self):
        try:
            W = int(self.capacityInput.text().strip())
            w = [int(x.strip()) for x in self.weightsInput.text().split(',')]
            v = [int(x.strip()) for x in self.valuesInput.text().split(',')]
            if len(w) != len(v):
                raise ValueError("Кількість ваг та цінностей не співпадає!")
            return W, w, v
        except Exception as e:
            QMessageBox.critical(self, "Помилка вводу", f"Перевірте дані:\n{str(e)}")
            return None, None, None

    def RunAuto(self):
        if self.timer.isActive():
            self.timer.stop()
            self.calcButton.setText("Розрахувати")
            self.calcButton.setProperty("active", False)
            self.calcButton.style().unpolish(self.calcButton)
            self.calcButton.style().polish(self.calcButton)
            self.calcButton.update()
        else:
            algoIDx = self.algoGroupButtons.checkedId()

            if not self.animationLog or self.currentStep == 0:
                self.executeAlgorithm(autoAnimate = True)
            else:
                interval = 1000 - self.speedSlider.value()
                self.timer.start(interval)

            if algoIDx == 3:
                self.calcButton.setText("Стоп")
                self.calcButton.setProperty("active", True)
                self.calcButton.style().unpolish(self.calcButton)
                self.calcButton.style().polish(self.calcButton)
                self.calcButton.update()

    def RunStep(self):
        if not self.animationLog:
            self.executeAlgorithm(autoAnimate = False)
        else:
            self.timer.stop()
            self.AnimateStep()

    def executeAlgorithm(self, autoAnimate = True):
        W, w, v = self.parse_inputs()
        if W is None:
            return

        self.timer.stop()
        self.animationLog = []
        self.currentStep = 0
        self.ClearTable(keepLabels = True)

        algoIDx = self.algoGroupButtons.checkedId()
        maxValue, items = 0, []

        if algoIDx == 0:
            maxValue, items = BruteForce(W, w, v)
        elif algoIDx == 1:
            maxValue, items = Recursive(W, w, v)
        elif algoIDx == 2:
            maxValue, items = Greedy(W, w, v)
        elif algoIDx == 3:
            maxValue, items, self.dpMatrix, self.animationLog = DynamicProgramming(W, w, v)
            self.SetupTable(len(w), W)
        elif algoIDx == 4:
            maxValue, items = BranchAndBound(W, w, v)

        itemsDisplay = sorted([i + 1 for i in items])
        self.resultLabel.setText(f"Макс. цінність: <b>{maxValue}</b>")
        self.itemsLabel.setText(f"Оптимальний набір: <b>{itemsDisplay}</b>")

        if algoIDx == 3:
            if autoAnimate and self.animationLog:
                interval = 1000 - self.speedSlider.value()
                self.timer.start(interval)
        else:
            self.ShowNoAnimMessage()

    def SetupTable(self, n, W):
        self.table.setRowCount(n + 1)
        self.table.setColumnCount(W + 1)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.table.setHorizontalHeaderLabels([str(i) for i in range(W + 1)])
        self.table.setVerticalHeaderLabels([str(i) for i in range(n + 1)])

        for i in range(n + 1):
            self.table.setItem(i, 0, QTableWidgetItem("0"))
        for w in range(W + 1):
            self.table.setItem(0, w, QTableWidgetItem("0"))

        self.ResizeTable()

    def AnimateStep(self):
        if self.currentStep < len(self.animationLog):
            for r, c, color in self.cellsToRestore:
                if self.table.item(r, c):
                    self.table.item(r, c).setBackground(color)
            self.cellsToRestore = []

            stepData = self.animationLog[self.currentStep]
            i, w, val = stepData['i'], stepData['w'], stepData['val']
            action = stepData['action']
            source_w = stepData['source_w']

            weightsStr = self.weightsInput.text().split(',')
            itemWeight = int(weightsStr[i - 1].strip()) if i > 0 else 0

            if i > 0:
                c1w = w
                item1 = self.table.item(i - 1, c1w)
                if item1:
                    self.cellsToRestore.append((i - 1, c1w, item1.background()))
                    item1.setBackground(QColor(255, 200, 100))

                if w >= itemWeight:
                    c2w = w - itemWeight
                    item2 = self.table.item(i - 1, c2w)
                    if item2:
                        if c1w != c2w:
                            self.cellsToRestore.append((i - 1, c2w, item2.background()))
                            item2.setBackground(QColor(255, 200, 100))

                winnerItem = self.table.item(i - 1, source_w)
                if winnerItem:
                    winnerItem.setBackground(QColor(100, 200, 255))

            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if action == 'take':
                item.setBackground(QColor(144, 238, 144))
            elif action == 'skip':
                item.setBackground(QColor(255, 200, 200))
            else:
                item.setBackground(QColor(240, 240, 240))

            self.table.setItem(i, w, item)
            self.table.scrollToItem(item)

            self.currentStep += 1
        else:
            self.timer.stop()
            self.calcButton.setText("Розрахувати")
            self.calcButton.setProperty("active", False)
            self.calcButton.style().unpolish(self.calcButton)
            self.calcButton.style().polish(self.calcButton)
            self.calcButton.update()

            for r, c, color in self.cellsToRestore:
                if self.table.item(r, c):
                    self.table.item(r, c).setBackground(color)
            self.cellsToRestore = []

            if self.animationLog:
                lastStep = self.animationLog[-1]
                finalItem = self.table.item(lastStep['i'], lastStep['w'])
                if finalItem:
                    finalItem.setBackground(QColor(255, 215, 0))

    def ShowNoAnimMessage(self):
        self.table.setRowCount(1)
        self.table.setColumnCount(1)

        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()

        msg = (
            "УПС!\n"
            "Цей алгоритм НЕ підтримує візуалізацію :(\n"
            f"{'-' * 10} :sob: :sob: :sob: {'-' * 10}\n"
            "Дані, які вирахував алгоритм, можна подивитися в групі \"Результати\"\n"
            "Для візуалізації використовуйте алгоритм \"Динамічне програмування\""
        )

        item = QTableWidgetItem(msg)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = item.font()
        font.setPointSize(16)
        item.setFont(font)

        self.table.setItem(0, 0, item)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    def ClearTable(self, keepLabels=False):
        self.timer.stop()
        self.calcButton.setText("Розрахувати")
        self.animationLog = []
        self.currentStep = 0
        self.cellsToRestore = []

        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.horizontalHeader().show()
        self.table.verticalHeader().show()

        if not keepLabels:
            self.resultLabel.setText("Макс. цінність: -")
            self.itemsLabel.setText("Оптимальний набір: -")

        self.calcButton.setProperty("active", False)
        self.calcButton.style().unpolish(self.calcButton)
        self.calcButton.style().polish(self.calcButton)
        self.calcButton.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.ResizeTable()

    def ResizeTable(self):
        if self.table.columnCount() > 0:
            availableWidth = self.table.viewport().width()
            columnWidth = availableWidth // self.table.columnCount()

            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, columnWidth)

            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, columnWidth)
