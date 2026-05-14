import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QRadioButton,
    QPushButton, QComboBox, QLabel, QTabWidget,
    QButtonGroup, QHeaderView, QGroupBox, QStyle
)
from PyQt6.QtCore import Qt
from stylesheet import AIO
from randomfacts import RANDOM_FACTS
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

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
        self.canvasPlaceholder = QLabel("Matplotlib placeholder")
        self.canvasPlaceholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvasPlaceholder.setStyleSheet("background-color: #ECEFF1; border: 2px dashed #CFD8DC; color: #546E7A;")
        plotLayout.addWidget(self.canvasPlaceholder)
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
        tableBtnLayout.addWidget(self.btnAddRow)
        tableBtnLayout.addWidget(self.btnRemoveRow)
        tableGroupLayout.addLayout(tableBtnLayout)

        self.tableGroup.setLayout(tableGroupLayout)
        dataLayout.addWidget(self.tableGroup)
        self.mainTabs.addTab(self.tabData, "Вхідні дані")

        mainLayout.addWidget(leftPanelWidget)
        mainLayout.addWidget(self.mainTabs)

    # F2.1
    def AddPoint(self):
        pass

    def RemovePoint(self):
        pass

    def ClearAll(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
