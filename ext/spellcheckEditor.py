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
from spellchecker import spellchecker
import sys

class spellcheckEditor(QtWidgets.QMainWindow):
    def __init__(self,text,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.text = text
        self.parent = parent
        self.dict = spellchecker.load_file("../input/dict_fr.txt","utf-8")
        
    def initUI(self):
        for word in self.text:
            
        
def main():

    app = QtWidgets.QApplication(sys.argv)
    main = spellcheckEditor("Toto est beau")
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
