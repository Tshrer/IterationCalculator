import Calu_ui
import logic
from PyQt6 import QtWidgets, QtCore, QtGui
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = QtWidgets.QWidget()
    ui = Calu_ui.Ui_Form()
    ui.setupUi(mainWin)
    mainWin.setWindowTitle("迭代法解方程组计算器")
    #加减阶数
    logic.setLineEdit(ui,1)
    ui.pushButton.clicked.connect(lambda: logic.Ladd(ui,ui.lineEdit_43,1))
    ui.pushButton_2.clicked.connect(lambda: logic.Lsub(ui,ui.lineEdit_43,1))

    ui.pushButton_3.clicked.connect(lambda: logic.start(ui))

    mainWin.show()

    sys.exit(app.exec())