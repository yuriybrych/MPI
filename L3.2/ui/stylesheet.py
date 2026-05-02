QPUSHBUTTON_DEFAULT_STYLESHEET = """
    /* Default button */
    QPushButton {
        background-color: #eee;
        color: black;
        font-weight: bold;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #aaa;
    }
    QPushButton:hover {
        background-color: #fff;
    }
    QPushButton:pressed {
        background-color: #ddd;
    }
"""

QPUSHBUTTON_CALC_STYLESHEET = """
    /* Calc button */
    QPushButton[calcButton = "true"] {
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
    QPushButton[calcButton = "true"]:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4ed187, stop:1 #3fb572);
        border: 1px solid #36b36d;
    }
    QPushButton[calcButton = "true"]:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #329e61, stop:1 #2c8c56);
        border: 1px solid #26854b;
    }
"""

QPUSHBUTTON_STEP_STYLESHEET = """
    /* Step button */
    QPushButton[stepButton = "true"] {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #459fc2, stop:1 #367da6);
        color: white;
        padding: 12px;
        font-weight: bold;
        font-size: 12px;
        border: 1px solid #2e78a3;
        border-radius: 0px;
    }
    QPushButton[stepButton = "true"]:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4e98d1, stop:1 #3f8ab5);
        border: 1px solid #366cb3;
    }
    QPushButton[stepButton = "true"]:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #32769e, stop:1 #2c6e8c);
        border: 1px solid #265f85;
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

QLABEL_STYLESHEET = """
    /* Label */
    QLabel {
        background: transparent;
        border: none;
    }
"""

QLINEEDIT_STYLESHEET = """
    /* Line edit */
    QLineEdit {
        background: white;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 5px;
    }
    QLineEdit:focus {
        border: 1px solid #3CB371;
    }
"""

QSLIDER_STYLESHEET = """
    /* Slider */
    QSlider::groove:horizontal {
        border: none;
        height: 3px;
        background: #e0e0e0;
        border-radius: 3px;
    }
    QSlider::sub-page:horizontal {
        background: #4A90E2;
        border-radius: 3px;
    }
    QSlider::add-page:horizontal {
        background: #e0e0e0;
        border-radius: 3px;
    }
    QSlider::handle:horizontal {
        background: #ffffff;
        border: 1px solid #4A90E2;
        width: 12px;
        height: 16px;
        margin: -5px 0px;
        border-radius: 3px;
    }
    QSlider::handle:horizontal:hover {
        background: #4A90E2;
        border: 1px solid #357ABD;
    }
"""

AIO = (
    QPUSHBUTTON_CLEAR_STYLESHEET + QPUSHBUTTON_STEP_STYLESHEET +
    QPUSHBUTTON_CALC_STYLESHEET + QPUSHBUTTON_DEFAULT_STYLESHEET +
    QLABEL_STYLESHEET + QLINEEDIT_STYLESHEET + QSLIDER_STYLESHEET
)
