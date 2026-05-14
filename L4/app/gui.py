import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QRadioButton, QTableWidgetItem,
    QPushButton, QComboBox, QLabel, QTabWidget, QSpinBox,
    QButtonGroup, QHeaderView, QGroupBox, QStyle, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from stylesheet import AIO
from randomfacts import RANDOM_FACTS
from canvas import PlotCanvas
from mathmodule import MathCore
from animengine import AnimationEngine
import random
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.mathCore = MathCore()
        self.animEngine = AnimationEngine(self.plotCanvas, self.mathCore)

    def InitUI(self):
        self.setWindowTitle(f"Рандомний факт: {random.choice(RANDOM_FACTS)}")
        self.resize(1200, 600)
        self.setStyleSheet(AIO)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        self.setWindowIcon(icon)

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QHBoxLayout(mainWidget)

        leftPanelWidget = QWidget()
        leftPanelWidget.setFixedWidth(320)
        leftPanel = QVBoxLayout(leftPanelWidget)
        leftPanel.setContentsMargins(0, 0, 0, 0)

        # I2.2
        self.settingsGroup = QGroupBox("Налаштування")
        settingsLayout = QVBoxLayout()

        settingsLayout.addWidget(QLabel("Ступінь полінома:"))
        self.comboDegree = QComboBox()
        self.comboDegree.addItems(["Лінійна", "Квадратична", "Кубічна", "Логарифмічна"])
        settingsLayout.addWidget(self.comboDegree)

        settingsLayout.addWidget(QLabel("Множник запасу осі Y:"))
        self.spinScale = QDoubleSpinBox()
        self.spinScale.setRange(0.1, 100.0)
        self.spinScale.setSingleStep(0.5)
        self.spinScale.setValue(1.5)
        settingsLayout.addWidget(self.spinScale)

        settingsLayout.addWidget(QLabel("Інтервал анімації:"))
        self.spinTimer = QSpinBox()
        self.spinTimer.setRange(10, 3000)
        self.spinTimer.setSingleStep(50)
        self.spinTimer.setValue(500)
        settingsLayout.addWidget(self.spinTimer)

        settingsLayout.addWidget(QLabel("Режим відображення:"))
        self.radioLagrange = QRadioButton("Інтерполяція")
        self.radioMnk = QRadioButton("Апроксимація")
        self.radioAll = QRadioButton("Усі графіки")
        self.radioAll.setChecked(True)

        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.radioLagrange)
        self.radioGroup.addButton(self.radioMnk)
        self.radioGroup.addButton(self.radioAll)

        settingsLayout.addWidget(self.radioLagrange)
        settingsLayout.addWidget(self.radioMnk)
        settingsLayout.addWidget(self.radioAll)
        self.settingsGroup.setLayout(settingsLayout)
        leftPanel.addWidget(self.settingsGroup)

        # I1.5
        self.metricsGroup = QGroupBox("Результати")
        metricsLayout = QVBoxLayout()
        self.lblMse = QLabel("MSE: -/-")
        metricsLayout.addWidget(self.lblMse)
        self.metricsGroup.setLayout(metricsLayout)
        leftPanel.addWidget(self.metricsGroup)

        leftPanel.addStretch()

        self.btnBuild = QPushButton("Зробити ✨уютненько✨")
        self.btnBuild.setProperty("buildButton", True)
        leftPanel.addWidget(self.btnBuild)

        self.btnClear = QPushButton("Очистити все")
        self.btnClear.setProperty("clearButton", True)
        leftPanel.addWidget(self.btnClear)

        copyrightLabel = QLabel("AbsoluteGarbage Corp.\nАвтор: Брич Юрій Михайлович\nВсі права не захищені.")
        copyrightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyrightLabel.setStyleSheet("color: gray; font-size: 10px; margin: 5px;")
        leftPanel.addWidget(copyrightLabel)

        self.mainTabs = QTabWidget()

        # I2.3
        self.tabPlot = QWidget()
        plotLayout = QVBoxLayout(self.tabPlot)
        self.plotCanvas = PlotCanvas(self.tabPlot)
        self.toolbar = NavigationToolbar(self.plotCanvas, self.tabPlot)
        plotLayout.addWidget(self.toolbar)
        plotLayout.addWidget(self.plotCanvas)
        self.mainTabs.addTab(self.tabPlot, "Візуалізація")

        # I2.1
        self.tabData = QWidget()
        dataLayout = QVBoxLayout(self.tabData)

        self.tableGroup = QGroupBox("Експериментальні точки")
        tableGroupLayout = QVBoxLayout()

        self.dataTable = QTableWidget(0, 2)
        self.dataTable.setHorizontalHeaderLabels(["Координата X", "Координата Y"])
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tableGroupLayout.addWidget(self.dataTable)

        tableBtnLayout = QHBoxLayout()
        self.btnAddRow = QPushButton("Додати рядок")
        self.btnAddRow.setProperty("addRow", True)
        self.btnRemoveRow = QPushButton("Видалити вибране")
        self.btnRemoveRow.setProperty("removeRow", True)

        self.btnImportString = QPushButton("Ввести RAW")
        self.btnImportString.setProperty("importButton", True)

        tableBtnLayout.addWidget(self.btnAddRow)
        tableBtnLayout.addWidget(self.btnImportString)
        tableBtnLayout.addWidget(self.btnRemoveRow)
        tableGroupLayout.addLayout(tableBtnLayout)

        self.tableGroup.setLayout(tableGroupLayout)
        dataLayout.addWidget(self.tableGroup)
        self.mainTabs.addTab(self.tabData, "Вхідні дані")

        mainLayout.addWidget(leftPanelWidget)
        mainLayout.addWidget(self.mainTabs)

        self.btnAddRow.clicked.connect(self.AddPoint)
        self.btnRemoveRow.clicked.connect(self.RemovePoint)
        self.btnClear.clicked.connect(self.ClearAll)
        self.btnBuild.clicked.connect(self.BuildAndPlot)
        self.btnImportString.clicked.connect(self.ImportString)

    # F2.1
    def AddPoint(self):
        currentRowCount = self.dataTable.rowCount()
        self.dataTable.insertRow(currentRowCount)
        self.dataTable.setItem(currentRowCount, 0, QTableWidgetItem(""))
        self.dataTable.setItem(currentRowCount, 1, QTableWidgetItem(""))

    def RemovePoint(self):
        currentRow = self.dataTable.currentRow()
        if currentRow >= 0:
            self.dataTable.removeRow(currentRow)
        else:
            rowCount = self.dataTable.rowCount()
            if rowCount > 0:
                self.dataTable.removeRow(rowCount - 1)

    def ClearAll(self):
        self.dataTable.setRowCount(0)
        self.lblMse.setText("MSE: -/-")
        self.plotCanvas.InitStaticPlot()

    def BuildAndPlot(self):
        xNodes, yNodes = self.GetTableData()
        if not xNodes or len(xNodes) < 2:
            return

        self.mainTabs.setCurrentIndex(0)
        self.lblMse.setText("MSE: ...")

        scaleVal = self.spinScale.value()
        timerVal = self.spinTimer.value()

        if self.radioLagrange.isChecked():
            self.animEngine.StartLagrangeAnimation(xNodes, yNodes, scaleVal, timerVal)
            self.lblMse.setText("MSE: Не застосовується для інтерполяції")

        elif self.radioMnk.isChecked():
            pass
        else:
            self.plotCanvas.PlotBasePoints(xNodes, yNodes)
            self.lblMse.setText("MSE: -/-")

    def GetTableData(self):
        xNodes = []
        yNodes = []
        for row in range(self.dataTable.rowCount()):
            itemX = self.dataTable.item(row, 0)
            itemY = self.dataTable.item(row, 1)

            if itemX and itemY and itemX.text().strip() and itemY.text().strip():
                try:
                    xVal = float(itemX.text().replace(',', '.'))
                    yVal = float(itemY.text().replace(',', '.'))
                    xNodes.append(xVal)
                    yNodes.append(yVal)
                except ValueError:
                    continue

        return xNodes, yNodes

    def ImportString(self):
        inputStr, ok = QInputDialog.getText(
            self,
            "Введення точок RAW виду",
            "Вставте рядок з точками:",
            text="(0, 1.2), (2, 3.5), (4, 4.1), (6, 5.8), (8, 9.2)"
        )

        if ok and inputStr:
            pairs = re.findall(r"\(([^,]+),\s*([^)]+)\)", inputStr)

            if not pairs:
                QMessageBox.warning(
                    self, "Ехххх, не фуриче сьогодні...",
                    "Не вдалося розпізнати формат.\nВикористовуйте: (x1, y1), (x2, y2)"
                )
                return

            self.dataTable.setRowCount(0)

            for xStr, yStr in pairs:
                try:
                    xVal = xStr.strip().replace(',', '.')
                    yVal = yStr.strip().replace(',', '.')

                    row = self.dataTable.rowCount()
                    self.dataTable.insertRow(row)
                    self.dataTable.setItem(row, 0, QTableWidgetItem(xVal))
                    self.dataTable.setItem(row, 1, QTableWidgetItem(yVal))
                except Exception as e:
                    print(f"Помилка при імпорті точки: {e}")

            QMessageBox.information(self, "Ecgsiyj svgjhnjdfyj!", f"Імпортовано точок: {len(pairs)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
