import re
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QMessageBox


def pulisci(self): # Pulisce il testo in input dai caratteri strani e rimpiazza gli accenti
    testo = re.sub(r'[^A-Za-z0-9.,\'\"\- ]+',"",self).replace("à", "a'").replace("è", "e'").replace("ì", "i'").replace("ò", "o'").replace("ù", "u'").replace('"',"''").upper()
    return testo

def conta_punt(n): # Funzione che serve per considerare SOLO la punteggiatura dal testo, senza creare dizionari
    n = re.sub(r'[^.,\'\"\-]', "", n)
    return n

def epigrafe(parola): # Crea il dizionario solo per lettere e numeri
    parola = parola.replace("'", ",")
    parola = re.sub(r'[^A-Za-z0-9]+',"",parola).replace("9", "6").upper()
    return dict([(carattere, parola.count(carattere)) for carattere in parola])


def elenco_punt(n): # Crea il dizionario solo per i caratteri di punteggiatura
    n = re.sub(r'[^.,\'\"\-]', "", n)
    return dict([(carattere, n.count(carattere)) for carattere in n])



class Ui_MainWindow(object):

    def showInfo(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Info")
        msgBox.setText("Calcola Epigrafe è stato creato interamente in Python3 usando le librerie Qt\nper l'interfaccia"
                       " grafica."
                       "\n \nScritto da Vecchio Federico."
                       "\nSi ringrazia Danilo Raineri per le consulenze.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def stampa(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textBrowser.print_(printer)


    def calcola(self):

        # Puliamo il textBrowser da eventuali precedenti output
        # e "puliamo" le scritte dai caratteri brutti
        self.textBrowser.clear()
        scritta4 = pulisci(self.lineEdit_4.text())
        scritta3 = pulisci(self.lineEdit_3.text())
        scritta25 = pulisci(self.lineEdit_25.text())
        scritta2 = pulisci(self.lineEdit_2.text())

        # Stampiamo nel riepilogo SOLO i campi di testo che non sono vuoti
        scritta_tot = ""
        for roba in (scritta4, scritta3, scritta25, scritta2):
            if roba != "":
                scritta_tot += roba + "\n"

        # Qui facciamo tutto quello che serve per avere un conteggio numerico complessivo
        # dei segni di punteggiatura, a prescindere dalla misura.
        punt4 = conta_punt(scritta4)
        punt3 = conta_punt(scritta3)
        punt25 = conta_punt(scritta25)
        punt2 = conta_punt(scritta2)
        puntTot = len(punt4+punt3+punt25+punt2)

        # Qui facciamo tutto quello che serve per generare le tabelle
        # contenenti solo i caratteri alfanumerici divisi per misura.
        risultato4 = epigrafe(scritta4)
        risultato3 = epigrafe(scritta3)
        risultato25 = epigrafe(scritta25)
        risultato2 = epigrafe(scritta2)

        # Qui invece generiamo SOLO la tabella per i segni di punteggiatura.
        # Rimpiazziamo gli apici con le virgole SOLO QUI perchè
        # a schermo, nel riepilogo della scritta da comporre,
        # risulterebbe di pessima lettura.
        elencopunt = elenco_punt(scritta_tot.replace("'", ","))

        self.textBrowser.append(
            "EPIGRAFE DA COMPORRE: \n" + scritta_tot + "\n")

        for carattere in sorted(risultato4):
            listaEpigrafe = ("[cm   4] {0}:  {1}".format(carattere, risultato4[carattere]))
            self.textBrowser.append(listaEpigrafe)
        info4 = len(scritta4) - len(punt4) - scritta4.count(" ")
        if info4 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTALE CM 4:          " + str(info4) + "pz.")
            self.textBrowser.append("\n")

        for carattere in sorted(risultato3):
            listaEpigrafe = ("[cm   3] {0}:  {1}".format(carattere, risultato3[carattere]))
            self.textBrowser.append(listaEpigrafe)
        info3 = len(scritta3) - len(punt3) - scritta3.count(" ")
        if info3 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTALE CM 3:          " + str(info3) + "pz.")
            self.textBrowser.append("\n")

        for carattere in sorted(risultato25):
            listaEpigrafe = ("[cm 2,5] {0}:  {1}".format(carattere, risultato25[carattere]))
            self.textBrowser.append(listaEpigrafe)
        info25 = len(scritta25) - len(punt25) - scritta25.count(" ")
        if info25 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTALE CM 2,5:        " + str(info25) + "pz.")
            self.textBrowser.append("\n")

        for carattere in sorted(risultato2):
            listaEpigrafe = ("[cm   2] {0}:  {1}".format(carattere, risultato2[carattere]))
            self.textBrowser.append(listaEpigrafe)
        info2 = len(scritta2) - len(punt2) - scritta2.count(" ")
        if info2 != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTALE CM 2:          " + str(info2) + "pz.")
            self.textBrowser.append("\n")

        for carattere in sorted(elencopunt):
            listaPunteggiatura = ("{0}:  {1}".format(carattere, elencopunt[carattere]))
            self.textBrowser.append(listaPunteggiatura)
        if puntTot != 0:
            self.textBrowser.append("__________________________")
            self.textBrowser.append("TOTALE PUNTEGGIATURA: {0}pz.".format(str(puntTot)))



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
        self.buttonCalcola = QtWidgets.QPushButton(self.frame)
        self.buttonCalcola.setGeometry(QtCore.QRect(10, 10, 80, 25))
        self.buttonCalcola.setFocusPolicy(QtCore.Qt.TabFocus)
        self.buttonCalcola.setAutoDefault(False)
        self.buttonCalcola.setObjectName("buttonCalcola")
        self.buttonCancella = QtWidgets.QPushButton(self.frame)
        self.buttonCancella.setGeometry(QtCore.QRect(10, 40, 80, 25))
        self.buttonCancella.setObjectName("buttonCancella")
        self.buttonEsci = QtWidgets.QPushButton(self.centralwidget)
        self.buttonEsci.setGeometry(QtCore.QRect(620, 620, 80, 41))
        self.buttonEsci.setFlat(False)
        self.buttonEsci.setObjectName("buttonEsci")
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
        self.buttonStampa = QtWidgets.QPushButton(self.frame_3)
        self.buttonStampa.setGeometry(QtCore.QRect(480, 10, 80, 25))
        self.buttonStampa.setObjectName("buttonStampa")
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
        self.actionStampa = QtWidgets.QAction(MainWindow)
        self.actionStampa.setObjectName("actionStampa")
        self.actionEsci = QtWidgets.QAction(MainWindow)
        self.actionEsci.setObjectName("actionEsci")
        self.actionCredits = QtWidgets.QAction(MainWindow)
        self.actionCredits.setEnabled(True)
        self.actionCredits.setWhatsThis("")
        self.actionCredits.setObjectName("actionCredits")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionStampa)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEsci)
        self.menu_Info.addAction(self.actionCredits)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Info.menuAction())

        self.retranslateUi(MainWindow)
        self.buttonCancella.clicked.connect(self.lineEdit_4.clear)
        self.buttonCancella.clicked.connect(self.lineEdit_3.clear)
        self.buttonCancella.clicked.connect(self.lineEdit_25.clear)
        self.buttonCancella.clicked.connect(self.lineEdit_2.clear)
        self.buttonCancella.clicked.connect(self.textBrowser.clear)
        self.buttonEsci.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.actionEsci.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.actionCredits.triggered.connect(self.showInfo)
        self.actionStampa.triggered.connect(self.stampa)
        self.buttonStampa.clicked.connect(self.stampa)
        self.buttonCalcola.clicked.connect(self.calcola)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESACROM - Calcola Epigrafi"))
        self.label.setText(_translate("MainWindow", "ESACROM FOTOCERAMICHE"))
        self.label_2.setText(_translate("MainWindow", "CALCOLA EPIGRAFI"))
        self.buttonCalcola.setText(_translate("MainWindow", "Calcola"))
        self.buttonCancella.setText(_translate("MainWindow", "Cancella"))
        self.buttonEsci.setText(_translate("MainWindow", "Esci"))
        self.label_5.setText(_translate("MainWindow", "← CM. 4"))
        self.label_6.setText(_translate("MainWindow", "← CM. 3"))
        self.label_7.setText(_translate("MainWindow", "← CM. 2,5"))
        self.label_8.setText(_translate("MainWindow", "← CM. 2"))
        self.buttonStampa.setText(_translate("MainWindow", "Stampa"))
        self.label_4.setText(_translate("MainWindow", "ANTEPRIMA:"))
        self.label_3.setText(_translate("MainWindow", "INSERISCI L\'EPIGRAFE DA CALCOLARE:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menu_Info.setTitle(_translate("MainWindow", "Info"))
        self.actionStampa.setText(_translate("MainWindow", "Stampa"))
        self.actionStampa.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionEsci.setText(_translate("MainWindow", "Esci"))
        self.actionEsci.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionCredits.setText(_translate("MainWindow", "Credits"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
