import re
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QMessageBox


def cleanText(self): # Clear input text from strange char
    testo = re.sub(r'[^A-Za-z0-9.,\'\"\- ]+',"",self).replace("à", "a'").replace("è", "e'").replace("ì", "i'").replace("ò", "o'").replace("ù", "u'").replace('"',"''").upper()
    return testo

def countPunct(n): # Function needed to underline punctuaction symbol ONLY, without creating dictionary
    n = re.sub(r'[^.,\'\"\-]', "", n)
    return n

def epigraph(word): # Create dictionary for numbers and letters
    word = word.replace("'", ",")
    word = re.sub(r'[^A-Za-z0-9]+', "", word).replace("9", "6").upper()
    return dict([(character, word.count(character)) for character in word])


def puntuaction(n): # Create dictionary for punctuaction
    n = re.sub(r'[^.,\'\"\-]', "", n)
    return dict([(character, n.count(character)) for character in n])



class Ui_MainWindow(object):

    def showInfo(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Info")
        msgBox.setText("Epigraph List Calculator is written in Python3 using Qt\nlybraries fo the graphic interface."
                       "\n \nCode written by Vecchio Federico."
                       "\nThanks to Danilo Raineri for all the help given.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def printSheet(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textBrowser.print_(printer)


    def createSheet(self):

        # Clean the text browser from previous inputs
        # and "clean" the text fields from "bad" characters
        self.textBrowser.clear()
        text4cm = cleanText(self.lineEdit_4.text())
        text3cm = cleanText(self.lineEdit_3.text())
        text25cm = cleanText(self.lineEdit_25.text())
        text2cm = cleanText(self.lineEdit_2.text())

        # Print in the preview list ONLY non-empy fields
        whole_text = ""
        for smth in (text4cm, text3cm, text25cm, text2cm):
            if smth != "":
                whole_text += smth + "\n"

        # Calculate the total amount of punctuaction symbol
        # regardless size.
        punct4 = countPunct(text4cm)
        punct3 = countPunct(text3cm)
        punct25 = countPunct(text25cm)
        punct2 = countPunct(text2cm)
        punctTot = len(punct4 + punct3 + punct25 + punct2)

        # Generate lists for numbers and letters,
        # separated according sizes.
        epigraph4cm = epigraph(text4cm)
        epigraph3cm = epigraph(text3cm)
        epigraph25cm = epigraph(text25cm)
        epigraph2cm = epigraph(text2cm)

        # Generate list for punctuaction symbols ONLY.
        # We are replacing ' with , here because
        # otherwise it would be very bad reading
        # while printed in the preview field.
        punctList = puntuaction(whole_text.replace("'", ","))

        self.textBrowser.append(
            "EPIGRAPH TO COMPOSE: \n" + whole_text + "\n")

        for character in sorted(epigraph4cm):
            epigraphList = ("[cm   4] {0}:  {1}".format(character, epigraph4cm[character]))
            self.textBrowser.append(epigraphList)
        info4 = len(text4cm) - len(punct4)
        if info4 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTAL CM 4:          " + str(info4) + "pz.")
            self.textBrowser.append("\n")

        for character in sorted(epigraph3cm):
            epigraphList = ("[cm   3] {0}:  {1}".format(character, epigraph3cm[character]))
            self.textBrowser.append(epigraphList)
        info3 = len(text3cm) - len(punct3)
        if info3 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTAL CM 3:          " + str(info3) + "pz.")
            self.textBrowser.append("\n")

        for character in sorted(epigraph25cm):
            epigraphList = ("[cm 2,5] {0}:  {1}".format(character, epigraph25cm[character]))
            self.textBrowser.append(epigraphList)
        info25 = len(text25cm) - len(punct25)
        if info25 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTAL CM 2,5:        " + str(info25) + "pz.")
            self.textBrowser.append("\n")

        for character in sorted(epigraph2cm):
            epigraphList = ("[cm   2] {0}:  {1}".format(character, epigraph2cm[character]))
            self.textBrowser.append(epigraphList)
        info2 = len(text2cm) - len(punct2)
        if info2 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTAL CM 2:          " + str(info2) + "pz.")
            self.textBrowser.append("\n")

        for character in sorted(punctList):
            punctuactionList = ("{0}:  {1}".format(character, punctList[character]))
            self.textBrowser.append(punctuactionList)
        if punctTot != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTAL PUNCTUACTION:  {0}pz.".format(str(punctTot)))



    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 729)
        MainWindow.setMinimumSize(QtCore.QSize(730, 729))
        MainWindow.setMaximumSize(QtCore.QSize(730, 729))
        MainWindow.setWindowIcon(QtGui.QIcon("app.ico"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 491, 41))
        font = QtGui.QFont()
        font.setFamily("Unsteady Oversteer")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 351, 17))
        font = QtGui.QFont()
        font.setFamily("Unsteady Oversteer")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 60, 981, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(610, 100, 101, 71))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.buttonCreateList = QtWidgets.QPushButton(self.frame)
        self.buttonCreateList.setGeometry(QtCore.QRect(10, 10, 80, 25))
        self.buttonCreateList.setFocusPolicy(QtCore.Qt.TabFocus)
        self.buttonCreateList.setAutoDefault(False)
        self.buttonCreateList.setObjectName("buttonCreateList")
        self.buttonClearAll = QtWidgets.QPushButton(self.frame)
        self.buttonClearAll.setGeometry(QtCore.QRect(10, 40, 80, 25))
        self.buttonClearAll.setObjectName("buttonClearAll")
        self.buttonExit = QtWidgets.QPushButton(self.centralwidget)
        self.buttonExit.setGeometry(QtCore.QRect(620, 620, 80, 41))
        self.buttonExit.setFlat(False)
        self.buttonExit.setObjectName("buttonExit")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 100, 571, 201))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(460, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(False)
        self.label_5.setObjectName("label_5")
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(10, 40, 551, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setGeometry(QtCore.QRect(10, 90, 551, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(460, 60, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setScaledContents(False)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(460, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setScaledContents(False)
        self.label_7.setObjectName("label_7")
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setGeometry(QtCore.QRect(10, 140, 551, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(460, 160, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setScaledContents(False)
        self.label_8.setObjectName("label_8")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 10, 441, 33))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 60, 441, 33))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_25.setGeometry(QtCore.QRect(10, 110, 441, 33))
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 160, 441, 33))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(10, 310, 571, 361))
        self.frame_3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_3)
        self.textBrowser.setGeometry(QtCore.QRect(10, 40, 551, 311))
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.Box)
        self.textBrowser.setObjectName("textBrowser")
        self.buttonPrint = QtWidgets.QPushButton(self.frame_3)
        self.buttonPrint.setGeometry(QtCore.QRect(480, 10, 80, 25))
        self.buttonPrint.setObjectName("buttonPrint")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 91, 17))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 321, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Info = QtWidgets.QMenu(self.menubar)
        self.menu_Info.setObjectName("menu_Info")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCredits = QtWidgets.QAction(MainWindow)
        self.actionCredits.setEnabled(True)
        self.actionCredits.setWhatsThis("")
        self.actionCredits.setObjectName("actionCredits")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menu_Info.addAction(self.actionCredits)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Info.menuAction())

        self.retranslateUi(MainWindow)
        self.buttonClearAll.clicked.connect(self.lineEdit_4.clear)
        self.buttonClearAll.clicked.connect(self.lineEdit_3.clear)
        self.buttonClearAll.clicked.connect(self.lineEdit_25.clear)
        self.buttonClearAll.clicked.connect(self.lineEdit_2.clear)
        self.buttonClearAll.clicked.connect(self.textBrowser.clear)
        self.buttonExit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.actionCredits.triggered.connect(self.showInfo)
        self.actionPrint.triggered.connect(self.printSheet)
        self.buttonPrint.clicked.connect(self.printSheet)
        self.buttonCreateList.clicked.connect(self.createSheet)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESACROM - Epigraph List"))
        self.label.setText(_translate("MainWindow", "EPIGRAPH LIST CALCULATOR"))
        self.label_2.setText(_translate("MainWindow", ""))
        self.buttonCreateList.setText(_translate("MainWindow", "Create List"))
        self.buttonClearAll.setText(_translate("MainWindow", "Clear All"))
        self.buttonExit.setText(_translate("MainWindow", "Exit"))
        self.label_5.setText(_translate("MainWindow", "← CM. 4"))
        self.label_6.setText(_translate("MainWindow", "← CM. 3"))
        self.label_7.setText(_translate("MainWindow", "← CM. 2,5"))
        self.label_8.setText(_translate("MainWindow", "← CM. 2"))
        self.buttonPrint.setText(_translate("MainWindow", "Print"))
        self.label_4.setText(_translate("MainWindow", "PREVIEW:"))
        self.label_3.setText(_translate("MainWindow", "WRITE DOWN THE EPIGRAPH YOU NEED TO COMPOSE:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menu_Info.setTitle(_translate("MainWindow", "Info"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionPrint.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionCredits.setText(_translate("MainWindow", "Credits"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())