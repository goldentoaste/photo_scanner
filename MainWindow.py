# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(717, 586)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("padding:10px;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.printerSelect = QtWidgets.QComboBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printerSelect.sizePolicy().hasHeightForWidth())
        self.printerSelect.setSizePolicy(sizePolicy)
        self.printerSelect.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.printerSelect.setFont(font)
        self.printerSelect.setObjectName("printerSelect")
        self.horizontalLayout_2.addWidget(self.printerSelect)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.dpiSelect = QtWidgets.QComboBox(parent=self.centralwidget)
        self.dpiSelect.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dpiSelect.setFont(font)
        self.dpiSelect.setObjectName("dpiSelect")
        self.dpiSelect.addItem("")
        self.dpiSelect.addItem("")
        self.dpiSelect.addItem("")
        self.dpiSelect.addItem("")
        self.dpiSelect.addItem("")
        self.dpiSelect.addItem("")
        self.horizontalLayout_3.addWidget(self.dpiSelect)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.outpath = QtWidgets.QLineEdit(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outpath.setFont(font)
        self.outpath.setObjectName("outpath")
        self.horizontalLayout_4.addWidget(self.outpath)
        self.outpathButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.outpathButton.setObjectName("outpathButton")
        self.horizontalLayout_4.addWidget(self.outpathButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(parent=self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.consoleLog = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.consoleLog.setFont(font)
        self.consoleLog.setUndoRedoEnabled(False)
        self.consoleLog.setReadOnly(True)
        self.consoleLog.setObjectName("consoleLog")
        self.verticalLayout.addWidget(self.consoleLog)
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.scanBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scanBtn.setFont(font)
        self.scanBtn.setObjectName("scanBtn")
        self.verticalLayout.addWidget(self.scanBtn)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scanner"))
        self.label.setText(_translate("MainWindow", "Printer Select"))
        self.printerSelect.setPlaceholderText(_translate("MainWindow", "Loading..."))
        self.label_3.setText(_translate("MainWindow", "DPI"))
        self.dpiSelect.setItemText(0, _translate("MainWindow", "200"))
        self.dpiSelect.setItemText(1, _translate("MainWindow", "300"))
        self.dpiSelect.setItemText(2, _translate("MainWindow", "400"))
        self.dpiSelect.setItemText(3, _translate("MainWindow", "600"))
        self.dpiSelect.setItemText(4, _translate("MainWindow", "800"))
        self.dpiSelect.setItemText(5, _translate("MainWindow", "1200"))
        self.label_2.setText(_translate("MainWindow", "Output path"))
        self.outpathButton.setText(_translate("MainWindow", "..."))
        self.scanBtn.setText(_translate("MainWindow", "Scan"))