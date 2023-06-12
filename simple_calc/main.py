import sys
from PySide2 import QtWidgets
from main_window import MainWindow

app = QtWidgets.QApplication()
window = MainWindow(app)
window.show()


sys.exit(app.exec_())