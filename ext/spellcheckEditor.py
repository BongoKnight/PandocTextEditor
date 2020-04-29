#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:05:01 2019

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

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QListWidget, QListWidgetItem


from spellchecker import SpellChecker
import sys

class spellcheckEditor(QtWidgets.QMainWindow):
    def __init__(self,text,parent=None,spell=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        # Window attribute
        self.title = "Correction orthographique"
        self.width = 550
        self.height = 400
        self.parent = parent
        if parent :
            self.text = parent.text.toPlainText()
        else:
            # Content attributes
            self.text = text
        self.splitted_text = self.text.split()
        self.rank = 0
        if spell == None:
            self.spell = SpellChecker()
        else:
            self.spell = spell
        self.spell.word_frequency.load_text_file("./input/dict_fr.txt")
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon("icons/spellcheck.png"))
        self.setGeometry(200,200,self.width, self.height)

        validate_button = QPushButton('Valider',self)
        validate_button.setToolTip("Remplace le mot mal orthographié par le choix sélectionné.")
        validate_button.move(self.width-120, self.height - 50)
        validate_button.clicked.connect(self.validate)

        ignore_button = QPushButton('Ignorer',self)
        ignore_button.setToolTip("Ignore le mot mal orthographié.")
        ignore_button.move(self.width-230, self.height - 50)
        ignore_button.clicked.connect(self.ignore)

        add_button = QPushButton('Ajouter au dictionnaire',self)
        add_button.setToolTip('Ajoute au dictionnaire le mot courant.')
        add_button.move(self.width-390, self.height - 50)
        add_button.setMinimumWidth(150)
        add_button.clicked.connect(self.add_to_dict)

        # Current corrected word
        self.currentWordLabel = QtWidgets.QLabel("",self)
        self.currentWordLabel.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.currentWordLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.currentWordLabel.move(20,20)
        self.currentWordLabel.resize(self.width,self.currentWordLabel.height())
        # Current suggestion list
        self.currentCorrectionList = QtWidgets.QListWidget(self)
        self.currentCorrectionList.resize(460,250)
        self.currentCorrectionList.move(20,60)
        # Current context for the current corrected word
        self.context = QtWidgets.QLabel("",self)
        self.context.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.context.resize(self.width,self.currentWordLabel.height())
        self.context.move(20,self.height-80)
        
        self.update()

    
    def updateText(self, text):
        self.text = text
    

    def validate(self):
        try:
            self.splitted_text[self.rank] = self.currentCorrectionList.selectedItems()[0].text()
            print(self.splitted_text)
        except:
            pass
        self.rank+=1
        self.update(self.rank)
    
    def ignore(self):
        self.rank+=1
        self.update(self.rank)

    def add_to_dict(self):
        self.spell.word_frequency.add(self.splitted_text[self.rank])
        self.rank+=1
        self.update(self.rank)       

    def end(self):
        info = QtWidgets.QMessageBox
        info.information(self, "Correction", "Fin de la correction orthographique!", info.Ok)
        self.close()

    def update(self,rank=0):
        if self.text == "" or self.rank == len(self.splitted_text)-1:
            self.end()
        else:
            while self.rank < len(self.splitted_text)-1:
                if self.splitted_text[self.rank] not in self.spell:
                    self.currentWordLabel.setText(self.splitted_text[self.rank] + " :")
                    self.currentCorrectionList.clear()
                    minContext = max(0,self.rank-3)
                    maxContext = min(self.rank+3,len(self.splitted_text)-1)
                    self.context.setText(" ".join(self.splitted_text[minContext:maxContext]))
                    for word in self.spell.candidates(self.splitted_text[self.rank]):
                        QListWidgetItem(word, self.currentCorrectionList)
                    return
                else:
                    self.rank +=1
            self.end()

        


def main():

    app = QtWidgets.QApplication(sys.argv)
    main = spellcheckEditor("La table est désete et le ciel est bleu. L'immensité de ses yeux était telle un nuage.")
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
