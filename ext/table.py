import sys

#PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
#PYQT5 QSpinBox, QMessageBox, QDialog, QPushButton, QGridLayout, QLabel



from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

class Table(QtWidgets.QDialog):
    def __init__(self,parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
         
        self.initUI()
 
    def initUI(self):

        
        self.rows = 10
        
        self.cols = 10
        
        self.space = 30
        

        # Button
        insertButton = QtWidgets.QPushButton("Insert",self)
        insertButton.clicked.connect(self.insert)
        
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.cols)
        for col in range(self.cols):
            self.tableWidget.setColumnWidth(self.space,self.cols)
        
        
        # Layout
        layout = QtWidgets.QGridLayout()
        
        
        layout.addWidget(self.tableWidget,0,0,10,10)
        layout.addWidget(insertButton,11,0,1,10)

        self.setWindowTitle("Insert Table")
        self.setGeometry(300,300,1000,400)
        self.setLayout(layout)

    def insert(self):

        maxCol = 0
        maxRow = 0
        maxLength = [0]*self.tableWidget.columnCount()
        for col in range(self.tableWidget.columnCount()+1):
            for row in range(self.tableWidget.rowCount()+1):
                if self.tableWidget.item(row,col) is not None:
                    if row > maxRow:
                        maxRow = row
                    if col > maxCol:
                        maxCol = col
                    if self.tableWidget.item(row,col) is not None:
                        if len(self.tableWidget.item(row,col).text()) > maxLength[col]:
                            maxLength[col] = len(self.tableWidget.item(row,col).text())
                        
    
        textMd=""
        tabText=[]
        
        for row in range(maxRow+1):
        
            lineText = []
        
            for col in range(maxCol+1):
        
                if self.tableWidget.item(row,col) is not None:
        
                    lineText.append(self.standardString(self.tableWidget.item(row,col).text(), maxLength[col]))
        
                else :
        
                    lineText.append(self.standardString("", maxLength[col]))
        
            tabText.append( " | ".join(lineText))
        
            if row == 0 :

        
                tabText.append("-|-".join(["-"*maxLength[i] for i in range(maxCol+1)]))

        textMd="\n".join(tabText)
                
                
        if self.parent is not None:
            cursor = self.parent.text.textCursor()
            # Inser the new table
            cursor.insertText(textMd)
        
            self.close()
        print(textMd)
        
    def standardString(self,string, length,separator=" "):
        return string + separator*(length-len(string))
    
def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Table()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

