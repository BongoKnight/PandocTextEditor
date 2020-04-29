#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 22:19:23 2019

@author: BongoKnight


The MIT License (MIT)

Copyright (c) 2014 Peter Goldsborough

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import sys

#PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets, QtGui
#PYQT5 QSpinBox, QMessageBox, QDialog, QPushButton, QGridLayout, QLabel



class Parameters(QtWidgets.QDialog):
    def __init__(self,parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
        self.initUI()
 
    def initUI(self):
        self.setWindowIcon(QtGui.QIcon("icons/gear.png"))
        # Button
        cancelButton = QtWidgets.QPushButton("Cancel",self)
        cancelButton.clicked.connect(self.cancel)
        saveButton = QtWidgets.QPushButton("Save",self)
        saveButton.clicked.connect(self.save)
        
        
        # Check Box for options
        self.tocLabel = QtWidgets.QLabel("Table des matières : ",self)
        self.tocBox = QtWidgets.QCheckBox(self)
        self.tocBox.setTristate(False)

        self.selfContainedLabel = QtWidgets.QLabel("HTML auto-suffisant : ",self)
        self.selfContainedBox = QtWidgets.QCheckBox(self)
        self.selfContainedBox.setTristate(False)
        
        self.mathjaxLabel = QtWidgets.QLabel("Utiliser mathjax : ",self)
        self.mathjaxBox = QtWidgets.QCheckBox(self)
        self.mathjaxBox.setTristate(False)

        # Custom compilation command
        compileLabel = QtWidgets.QLabel("Utiliser une commande pour la compilation :",self)
        self.compileCommand = QtWidgets.QLineEdit(self)
        self.compileCommand.setPlaceholderText("Entrer une commande à utiliser lors de l'export.")

        # Pdf engine


        # file selction
        self.cssBox = QtWidgets.QLabel("Utiliser un CSS pour l'HTML: ",self)
        self.cssButton= QtWidgets.QPushButton("Choisir un fichier",self)
        self.cssButton.clicked.connect(self.selectCSS)
        self.cssSelected = QtWidgets.QLabel("",self)
    


        if str(type(self.parent))== "<class '__main__.textEdit'>":
        # Try to load preceding conf
            if self.parent.config["css"]:
                self.cssSelected = QtWidgets.QLabel(self.parent.config["css"],self)
            else:
                self.cssSelected = QtWidgets.QLabel("",self)
            if self.parent.config["selfContained"]:
                self.selfContainedBox.setChecked(True)
            if self.parent.config["mathjax"]:
                self.mathjaxBox.setChecked(True)
            if self.parent.config["toc"]:
                self.tocBox.setChecked(True)
            if self.parent.config["command"]:
                self.compileCommand.setText(self.parent.config["command"])

        # Layout
        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self.tocLabel,0,0)
        layout.addWidget(self.tocBox,0,1)
        layout.addWidget(self.selfContainedLabel,1,0)
        layout.addWidget(self.selfContainedBox,1,1)
        layout.addWidget(self.mathjaxLabel,2,0)
        layout.addWidget(self.mathjaxBox,2,1)        
        
        layout.addWidget(self.cssBox,3,0)
        layout.addWidget(self.cssButton,3,1)
        layout.addWidget(self.cssSelected,3,2)
        layout.addWidget(compileLabel,4,0)
        layout.addWidget(self.compileCommand,4,1)
        #layout.addWidget()
        
        
        
        layout.addWidget(saveButton,11,0,11,1)
        layout.addWidget(cancelButton,11,6,11,1)

        self.setWindowTitle("Choix des paramètres d'export")
        self.setGeometry(300,300,1000,400)
        self.setLayout(layout)
        self.show()

    def save(self):
        if self.parent !=None:
            self.parent.updateConf("css",self.cssSelected.text())
            if self.tocBox.checkState():
                self.parent.updateConf("toc",True,False)
            else:
                self.parent.updateConf("toc",False,False)
                
            if self.selfContainedBox.checkState():
                self.parent.updateConf("selfContained",True,False)
            else :
                self.parent.updateConf("selfContained",False,False)
                
            if self.mathjaxBox.checkState():
                self.parent.updateConf("mathjax",True,False)
            else:
                self.parent.updateConf("mathjax",False,False)

            if self.selfContainedBox.checkState():
                self.parent.updateConf("selfContained",True,False)
            else:
                self.parent.updateConf("selfContained",False,False)

            self.parent.updateConf("command",self.compileCommand.text(),True)            
            
            self.parent.saveConfig()
        
        self.close()
        
    def selectCSS(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Fichier CSS')[0]
        self.cssSelected.setText(filename)
        
        
    def cancel(self):
        self.close()


    
def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Parameters()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

