import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
import xlrd
import FuzzyGW as fgw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class HasilDialog(QMainWindow):
    def __init__(self):
        super(HasilDialog, self).__init__()
        loadUi('UI/hasilpage.ui',self)

    def editLabel(self, TBB, TBA, TnBB, TnBA, Min, Max, nMin, nMax):
        #TnBB.setStyleSheet(" font-size: 8pt; qproperty-alignment: AlignHCenter;")
        TnBB.setText(str(nMin))
        #TnBA.setStyleSheet(" font-size: 8pt; qproperty-alignment: AlignHCenter;")
        TnBA.setText(str(nMax))
        #TBB.setStyleSheet(" font-size: 8pt; qproperty-alignment: AlignHCenter;")
        TBB.setText(str(Min))
        #TBA.setStyleSheet(" font-size: 8pt; qproperty-alignment: AlignHCenter;")
        TBA.setText(str(Max))
    
    def drawPlot(self, TPlot, LBB, LBA, LnBB, LnBA, LMin, LMax, LnMin, LnMax, nInput):
        if TPlot == 1:
            self.editLabel(LBB, LBA, LnBB, LnBA, LMin, LMax, LnMin, LnMax)
            bawah, atas = fgw.fuzifikasi(LnMin, LnMax, nInput)
            self.lbl_mBBx.setText('μ'+str(LMin))
            self.lbl_mBAx.setText('μ'+str(LMax))
            self.lbl_mnBBx.setText(str(FuzzyDialog().premise1_1.currentText()))
            self.lbl_mnBAx.setText(str(atas))
            print('Hasil',TPlot,bawah,atas,nInput)
            self.plotWidget1 = plt.figure()
            self.canvas1 = FigureCanvas(self.plotWidget1)
            self.plotWidget1.clear()
            ax = self.plotWidget1.add_subplot(111)
            ax.plot([0,0,0.25,0.5,0.75,1,1], color='b')
            ax.plot([1,1,0.75,0.5,0.25,0,0], color='r')
            plt.xticks([])
            self.canvas1.draw()
            self.plot_1.addWidget(self.canvas1)
        elif TPlot == 2:
            self.editLabel(LBB, LBA, LnBB, LnBA, LMin, LMax, LnMin, LnMax)
            bawah, atas = fgw.fuzifikasi(LnMin, LnMax, nInput)
            self.lbl_mBBy.setText('μ'+str(LMin))
            self.lbl_mBAy.setText('μ'+str(LMax))
            self.lbl_mnBBy.setText(str(bawah))
            self.lbl_mnBAy.setText(str(atas))
            print('Hasil',TPlot,bawah,atas,nInput)
            self.plotWidget2 = plt.figure()
            self.canvas2 = FigureCanvas(self.plotWidget2)
            self.plotWidget2.clear()
            ax = self.plotWidget2.add_subplot(111)
            plt.xticks([])
            ax.plot([0,0,0.25,0.5,0.75,1,1], color='b')
            ax.plot([1,1,0.75,0.5,0.25,0,0], color='r')
            self.canvas2.draw()
            self.plot_2.addWidget(self.canvas2)
        elif TPlot == 3:
            self.editLabel(LBB, LBA, LnBB, LnBA, LMin, LMax, LnMin, LnMax)
            self.plotWidget3= plt.figure()
            self.canvas3 = FigureCanvas(self.plotWidget3)
            self.plotWidget3.clear()
            ax = self.plotWidget3.add_subplot(111)
            ax.plot([0,0,0.25,0.5,0.75,1,1], color='b')
            ax.plot([1,1,0.75,0.5,0.25,0,0], color='r')
            plt.xticks([])
            self.canvas3.draw()
            self.plot_3.addWidget(self.canvas3)


class FuzzyDialog(QMainWindow):
    def __init__(self):
        super(FuzzyDialog, self).__init__()
        loadUi('UI/varpage.ui',self)
        self.btnPredict.clicked.connect(self.letsPredict)
        self.btnUpdate.clicked.connect(self.updateField)
        self.FormHasil = HasilDialog()

    def letsPredict(self):
        inputx = self.SBInput1.value()
        inputy = self.SBInput2.value()
        x=1
        for i in range (1,4):
            isInput = self.Tabel1.item(i,0).text() 
            if isInput.lower() == 'input' and x==1:
                nBB = int(self.Tabel1.item(i,3).text())
                nBA = int(self.Tabel1.item(i,5).text())
                BB = self.Tabel1.item(i,2).text()
                BA = self.Tabel1.item(i,4).text()
                self.FormHasil.drawPlot(1, self.FormHasil.lbl_BBx, self.FormHasil.lbl_BAx, self.FormHasil.lbl_Minx, self.FormHasil.lbl_Maxx, BB, BA, nBB, nBA, inputx)
                x+=1
            elif isInput.lower() == 'input' and x==2:
                nBB = int(self.Tabel1.item(i,3).text())
                nBA = int(self.Tabel1.item(i,5).text())
                BB = self.Tabel1.item(i,2).text()
                BA = self.Tabel1.item(i,4).text()
                self.FormHasil.drawPlot(2, self.FormHasil.lbl_BBy, self.FormHasil.lbl_BAy, self.FormHasil.lbl_Miny, self.FormHasil.lbl_Maxy, BB, BA, nBB, nBA, inputy)
            else:
                nBB = int(self.Tabel1.item(i,3).text())
                nBA = int(self.Tabel1.item(i,5).text())
                BB = self.Tabel1.item(i,2).text()
                BA = self.Tabel1.item(i,4).text()
                self.FormHasil.drawPlot(3, self.FormHasil.lbl_BBz, self.FormHasil.lbl_BAz, self.FormHasil.lbl_Minz, self.FormHasil.lbl_Maxz, BB, BA, nBB, nBA, 0)
        self.FormHasil.show()
        
    def updateField(self):
        prem1 = []
        prem2 = []
        conq = []
        x=1
        for i in range (1,4):
            isInput = self.Tabel1.item(i,0).text() 
            if isInput.lower() == 'input' and x==1:
                prem1.append(self.Tabel1.item(i,2).text())
                prem1.append(self.Tabel1.item(i,4).text())
                self.tambahitem(prem1,1)
                x+=1
            elif isInput.lower() == 'input' and x==2:
                prem2.append(self.Tabel1.item(i,2).text())
                prem2.append(self.Tabel1.item(i,4).text())
                self.tambahitem(prem2,2)
            else:
                conq.append(self.Tabel1.item(i,2).text())
                conq.append(self.Tabel1.item(i,4).text())
                self.tambahitem(conq,3)
    
    def tambahitem(self, arrinput, col):
        if col == 1:
            self.premise1_1.clear()
            self.premise1_2.clear()
            self.premise1_3.clear()
            self.premise1_4.clear()
        elif col == 2:
            self.premise2_1.clear()
            self.premise2_2.clear()
            self.premise2_3.clear()
            self.premise2_4.clear()
        elif col == 3:
            self.premise3_1.clear()
            self.premise3_2.clear()
            self.premise3_3.clear()
            self.premise3_4.clear()
        for i in range (len(arrinput)):
            if col == 1:
                self.premise1_1.addItem(str(arrinput[i]))
                self.premise1_2.addItem(str(arrinput[i]))
                self.premise1_3.addItem(str(arrinput[i]))
                self.premise1_4.addItem(str(arrinput[i]))
            elif col == 2:
                self.premise2_1.addItem(str(arrinput[i]))
                self.premise2_2.addItem(str(arrinput[i]))
                self.premise2_3.addItem(str(arrinput[i]))
                self.premise2_4.addItem(str(arrinput[i]))
            elif col == 3:
                self.premise3_1.addItem(str(arrinput[i]))
                self.premise3_2.addItem(str(arrinput[i]))
                self.premise3_3.addItem(str(arrinput[i]))
                self.premise3_4.addItem(str(arrinput[i]))
                                           
    def writeTabel(self,datanya):
        namavar = []
        #print(datanya)
        for i in range (3):
            if datanya[i] == "INPUT":
                namavar.append(datanya[i+3])
        #print(namavar)
        self.lblInput1.setStyleSheet(" font-size: 12pt; qproperty-alignment: AlignRight; font-weight:600;")
        self.lblInput1.setText(namavar[0])
        self.lblInput2.setStyleSheet(" font-size: 12pt; qproperty-alignment: AlignRight; font-weight:600;")
        self.lblInput2.setText(namavar[1])
        for i in range(6):
            for j in range(1,4):
                self.Tabel1.setItem(j,i,QTableWidgetItem(str(datanya[0])))
                datanya.pop(0)


class MainDialog(QMainWindow):
    def __init__(self):
        super(MainDialog, self).__init__()
        loadUi('UI/index.ui',self)
        self.btnOpen.clicked.connect(self.Open)
        self.btnNew.clicked.connect(self.change)
        self.hasil = None

    def Open(self):
        flname, filter = QFileDialog.getOpenFileName(self, 'Open File','C:\\',"Excel file(*.xls)")
        if flname:
            self.delimiter(flname)
        else:
            print('Invalid Excel File!')
        
    def delimiter(self, namafile):
        #global Hasilnya
        #Deelimiter File#
        tipe = []
        var = []
        batas = []
        natas = []
        bbawah = []
        nbawah = []
        masukan = []
        book = xlrd.open_workbook(namafile)
        sheet = book.sheet_by_name("Sheet1")
        for i in range (2,5):
            tipe.append(sheet.cell(i,0).value)
            var.append(sheet.cell(i,1).value)
            batas.append(sheet.cell(i,2).value)
            natas.append(int(sheet.cell(i,3).value))
            bbawah.append(sheet.cell(i,4).value)
            nbawah.append(int(sheet.cell(i,5).value))
        self.hasil = tipe + var + batas + natas + bbawah + nbawah
        #Hasilnya = self.hasil
        self.change()

    def change(self):
        #print('Dari index: ', self.hasil)
        self.editvar = FuzzyDialog()
        self.editvar.writeTabel(self.hasil)
        self.editvar.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainDialog()
    ex.setWindowTitle('')
    ex.show()
    sys.exit(app.exec_())