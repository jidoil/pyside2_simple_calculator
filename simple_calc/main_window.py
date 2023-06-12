from PySide2.QtCore import QSize, Slot
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import QMainWindow, QToolBar, QAction, QStatusBar, QLineEdit, QToolButton, QSizePolicy, \
    QGridLayout, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("Simple Calculator")

        # 중요 변수들
        self.digit_buttons = []
        self.is_waiting_for_operand = False
        self.sum_memory = 0
        self.sum_so_far = 0


        # 메뉴바와 메뉴들
        toolbar = QToolBar("Main Tool Bar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        quit_action = QAction(QIcon("quit.png"), "Quit Action", self)
        quit_action.setStatusTip("Quit simple calculator")
        quit_action.triggered.connect(self.toolbar_button_click)

        toolbar.addAction(quit_action)
        toolbar.addSeparator()

        # status bar
        self.setStatusBar(QStatusBar(self))

        # current input display
        self.display = QLineEdit('0', self)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)
        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        # operated display
        self.result_display = QLineEdit('0', self)
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setMaxLength(15)
        font = self.result_display.font()
        self.result_display.setFont(font)

        # display layout
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.result_display)
        display_layout.addWidget(self.display)

        # button
        for i in range(10):
            button = self.create_digit_button(i, self.digit_clicked)
            self.digit_buttons.append(button)

        self.clear_button = self.create_clear_button("c", self.clear_button_clicked)
        self.delete_button = self.create_delete_button("<", self.delete_button_clicked)
        self.add_operator_button = self.create_add_button("+", self.add_button_clicked)
        self.equal_operator_button = self.create_equal_button("=", self.equal_button_clicked)
        # grid layout
        self.layout = QGridLayout()
        self.layout.setSizeConstraint(QGridLayout.SetFixedSize)
        self.setLayout(self.layout)

        # put buttons into the layout

        # central widget
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.layout.addLayout(display_layout, 0, 0, 1, 3)
        self.layout.addWidget(self.digit_buttons[0], 1, 0)
        self.layout.addWidget(self.digit_buttons[1], 1, 1)
        self.layout.addWidget(self.digit_buttons[2], 1, 2)
        self.layout.addWidget(self.digit_buttons[3], 2, 0)
        self.layout.addWidget(self.digit_buttons[4], 2, 1)
        self.layout.addWidget(self.digit_buttons[5], 2, 2)
        self.layout.addWidget(self.digit_buttons[6], 3, 0)
        self.layout.addWidget(self.digit_buttons[7], 3, 1)
        self.layout.addWidget(self.digit_buttons[8], 3, 2)
        self.layout.addWidget(self.add_operator_button, 3, 3)
        self.layout.addWidget(self.clear_button, 4, 0)
        self.layout.addWidget(self.digit_buttons[9], 4, 1)
        self.layout.addWidget(self.delete_button, 4, 2)
        self.layout.addWidget(self.equal_operator_button, 4, 3)


    @Slot()
    def toolbar_button_click(self):
        self.statusBar().showMessage("Message from my app", 3000)
        self.app.quit()
    @Slot()
    def digit_clicked(self):
        number_to_display = int(self.sender().text())
        current_text = self.display.text()
        if self.display.text() == 0 and number_to_display == 0:
            return
        if self.is_waiting_for_operand:
            self.display.clear()
            self.is_waiting_for_operand = False
        if current_text == "0":
            self.display.setText(str(number_to_display))
        else:
            self.display.setText(self.display.text() + str(number_to_display))

    @Slot()
    def create_digit_button(self, button_number, digit_clicked):
        button = QToolButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setText(str(button_number))
        button.setShortcut(str(button_number))
        button.clicked.connect(digit_clicked)
        return button

    @Slot()
    def create_clear_button(self, button_name, clear_button_clicked):
        button = QToolButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setText(button_name)
        button.setShortcut("c")
        button.clicked.connect(clear_button_clicked)
        return button

    @Slot()
    def create_delete_button(self, button_name, delete_button_clicked):
        button = QToolButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setText(button_name)
        button.setShortcut("backspace")
        button.clicked.connect(delete_button_clicked)
        return button

    @Slot()
    def create_add_button(self, button_name, add_button_clicked):
        button = QToolButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setText(button_name)
        button.setShortcut("+")
        button.clicked.connect(add_button_clicked)
        return button

    @Slot()
    def create_equal_button(self, button_name, equal_button_clicked):
        button = QToolButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setText(button_name)
        button.setShortcut("=")
        button.clicked.connect(equal_button_clicked)
        return button


    @Slot()
    def clear_button_clicked(self):
        self.display.clear()
        self.result_display.clear()
        self.sum_memory = 0
        self.sum_so_far = 0

    @Slot()
    def delete_button_clicked(self):
        pass

    @Slot()
    def add_button_clicked(self):
        current_number = int(self.display.text())
        if self.is_waiting_for_operand:
            print("cannot input operand twice")
            return
        self.is_waiting_for_operand = False
        self.display.clear()
        self.sum_memory = current_number
        if self.sum_so_far == 0:
            self.result_display.setText(str(current_number) + " + ")
        else:
            self.result_display.setText(str(self.sum_so_far) + " + " + str(current_number))
        self.sum_so_far += self.sum_memory
    @Slot()
    def equal_button_clicked(self):
        current_number = self.display.text()
        if self.is_waiting_for_operand:
            print("cannot input operand twice")
            return
        self.is_waiting_for_operand = False
        self.display.clear()
        self.result_display.setText(str(self.sum_so_far + int(current_number)))
        pass
