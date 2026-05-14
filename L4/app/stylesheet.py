QPUSHBUTTON_DEFAULT_STYLESHEET = """
    /* Default button */
    QPushButton {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #bfbfbf, stop:1 #a3a3a3);
        border: 1px solid #9e9e9e;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 6px;
        outline: none;
    }
    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #cccccc, stop:1 #b8b8b8);
        border: 1px solid #b0b0b0;
    }
    QPushButton:pressed {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9c9c9c, stop:1 #878787);
        border: 1px solid #828282;
    }
"""

QPUSHBUTTON_CALC_STYLESHEET = """
    /* Calc button */
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

    /* Calc button (active)*/
    QPushButton[buildButton = "true"][active = "true"] {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c2b645, stop:1 #a69336);
        border: 1px solid #a3972e;
    }
    QPushButton[buildButton = "true"][active = "true"]:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d1b94e, stop:1 #b5a33f);
        border: 1px solid #b3a436;
    }
    QPushButton[buildButton = "true"][active = "true"]:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #9e9132, stop:1 #8c812c);
        border: 1px solid #857d26;
    }
"""

QPUSHBUTTON_CLEAR_STYLESHEET = """
    /* Clear button */
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
"""

QPUSHBUTTON_ROWS_STYLESHEET = """
    QPushButton[addRow = "true"] {
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
        border-bottom-left-radius: 10px;
    }
    QPushButton[removeRow = "true"] {
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 10px;
        border-bottom-left-radius: 0px;
    }
"""

QCOMBOBOX_STYLESHEET = """
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
"""

AIO = (
    QPUSHBUTTON_CLEAR_STYLESHEET + QPUSHBUTTON_CALC_STYLESHEET + QPUSHBUTTON_DEFAULT_STYLESHEET + QCOMBOBOX_STYLESHEET + QPUSHBUTTON_ROWS_STYLESHEET
)
