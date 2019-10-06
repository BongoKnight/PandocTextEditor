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

from PyQt5 import QtGui, QtCore
import re

class SpellHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, *args):
        super(SpellHighlighter, self).__init__(*args)
        self.spell = None
        self.regExp = re.compile('^[-+]?([0-9,.]*)$')

    def setDict(self, spell):
        self.spell = spell

    def highlightBlock(self, text):
        if not self.spell:
            return
        text = text
        textFormat = QtGui.QTextCharFormat()
        textFormat.setUnderlineColor(QtCore.Qt.red)
        textFormat.setUnderlineStyle(QtGui.QTextCharFormat.WaveUnderline)
        for word_object in re.finditer(r'\w+', text, re.UNICODE):
            if self.regExp.match(word_object.group()) == None:
                if len(self.spell.known([word_object.group().lower(), ])) < 1:
                    self.setFormat(
                        word_object.start(), 
                        word_object.end() - word_object.start(), 
                        textFormat)