#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 21:15:37 2019

@author: BongoKnight


The MIT License (MIT)

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
import pypandoc
#PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
from spellchecker import SpellChecker

#PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
#PYQT5 QFileDialog, QColorDialog, QDialog

from PyQt5 import QtPrintSupport
#PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore


from ext import  wordcount, datetime, find, table, markdownHighlight, config, option, tools, spellcheckEditor


class textEdit(QtWidgets.QMainWindow):

    def __init__(self,parent=None,filename=""):
        QtWidgets.QMainWindow.__init__(self,parent)

        self.filename = filename
        self.template = ""


        self.changesSaved = True
        self.initConfig()
        self.initUI()
        self.initspellCheck()

    def initspellCheck(self):
        self.spell = spellcheckEditor.spellcheckEditor("",self)
        self.spell.spell.word_frequency.load_text_file("input/dict_fr.txt")

    def initConfig(self):
        config_path = "input/config.json"
        self.config_file = config.JSONPropertiesFile(config_path)
        self.config = self.config_file.get()

    def updateConf(self, key, value, immediateSave=True):
        self.config[key] = value
        if immediateSave:
            self.config_file.set(self.config)

    def saveConfig(self):
        self.config_file.set(self.config)


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                event.pos(),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                QtCore.Qt.NoModifier)
        if type(self) == QtWidgets.QTextEdit:
            QtWidgets.QTextEdit.mousePressEvent(self, event)


    def contextMenuEvent(self, event):
        if type(self) == QtWidgets.QTextEdit:
            self.popup_menu = self.createStandardContextMenu()
            first = self.popup_menu.actions()[0]

            # Select the word under the cursor.
            cursor = self.textCursor()
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
            self.setTextCursor(cursor)

            # Check if the selected word is misspelled and offer spelling
            # suggestions if it is.
            if self.textCursor().hasSelection():
                text = self.textCursor().selectedText()
                istitle = text.istitle()
                if len(self.spell.known([text, ])) < 1:
                    for word in self.spell.candidates(text):
                        if istitle:
                            newAct = QtWidgets.QAction(word.title(), self)
                        else:
                            newAct = QtWidgets.QAction(word, self)
                        newAct.triggered.connect(self.menuSelected)
                        self.popup_menu.insertAction(first, newAct)

            self.popup_menu.exec_(event.globalPos())




    def menuSelected(self):
        word = self.sender().text()
        self.correctWord(word)


    def correctWord(self, word):
        """
        Replaces the selected text with word.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()
        self.highlighter.rehighlight()






    def initToolbar(self):

        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon("icons/saveas.png"),"Save As",self)
        self.saveAsAction.setStatusTip("Save document as")
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.triggered.connect(self.saveAs)

        self.printAction = QtWidgets.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtWidgets.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        wordCountAction = QtWidgets.QAction(QtGui.QIcon("icons/count.png"),"See word/symbol count",self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        self.hortografAction = QtWidgets.QAction(QtGui.QIcon("icons/spellcheck.png"),"Correction",self)
        self.hortografAction.setStatusTip("Spellcheck of current document")
        self.hortografAction.setShortcut("Ctrl+Shift+P")
        self.hortografAction.triggered.connect(self.checkText)       

        self.findAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"),"Find and replace",self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        self.templateAction = QtWidgets.QAction(QtGui.QIcon("icons/template.png"),"Define template file",self)
        self.templateAction.setStatusTip("Define a template file before a quick export, extension must match the destination type")
        self.templateAction.triggered.connect(self.defineTemplate)

        self.optionAction = QtWidgets.QAction(QtGui.QIcon("icons/gear.png"),"Define export otions",self)
        self.optionAction.setStatusTip("Define the export options : self-contained, toc...")
        self.optionAction.triggered.connect(self.setOptions)


        self.PDFExportAction = QtWidgets.QAction(QtGui.QIcon("icons/pdf.png"),"Export as PDF file",self)
        self.PDFExportAction.setStatusTip("Export as PDF")
        self.PDFExportAction.triggered.connect(self.exportPDF)

        self.HTMLExportAction = QtWidgets.QAction(QtGui.QIcon("icons/html.png"),"Export as HTML file",self)
        self.HTMLExportAction.setStatusTip("Export as HTML")
        self.HTMLExportAction.triggered.connect(self.exportHTML)

        self.EpubExportAction = QtWidgets.QAction(QtGui.QIcon("icons/epub.png"),"Export as Epub file",self)
        self.EpubExportAction.setStatusTip("Export as Epub")
        self.EpubExportAction.triggered.connect(self.exportEpub)

        self.docxExportAction = QtWidgets.QAction(QtGui.QIcon("icons/word.png"),"Export as Docx file",self)
        self.docxExportAction.setStatusTip("Export as Docx")
        self.docxExportAction.triggered.connect(self.exportDocx)

        self.texExportAction = QtWidgets.QAction(QtGui.QIcon("icons/latex.png"),"Export as Tex file",self)
        self.texExportAction.setStatusTip("Export as Tex")
        self.texExportAction.triggered.connect(self.exportTex)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.saveAsAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(self.hortografAction)

        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        self.toolbar.addAction(self.templateAction)
        self.toolbar.addAction(self.optionAction)
        self.toolbar.addAction(self.PDFExportAction)
        self.toolbar.addAction(self.HTMLExportAction)
        self.toolbar.addAction(self.EpubExportAction)
        self.toolbar.addAction(self.docxExportAction)
        self.toolbar.addAction(self.texExportAction)
        self.addToolBarBreak()

    def checkText(self):
        self.spell.updateText(self.text.toPlainText())
        self.spell.show()

    def initFormatbar(self):

        fontSize = QtWidgets.QSpinBox(self)
        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(14)


        boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.setShortcut("Ctrl+B")
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.setShortcut("Ctrl+I")
        italicAction.triggered.connect(self.italic)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("icons/superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("icons/subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript)


        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/calender.png"),"Insert current date/time",self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)


        tableAction = QtWidgets.QAction(QtGui.QIcon("icons/table.png"),"Insert table",self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+Shift+T")
        tableAction.triggered.connect(table.Table(self).show)

        imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.png"),"Insert image",self)
        imageAction.setStatusTip("Insert image (Ctrl+Shift+I)")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        linkAction = QtWidgets.QAction(QtGui.QIcon("icons/link.png"),"Insert link",self)
        linkAction.setStatusTip("Insert link (Ctrl+K)")
        linkAction.setShortcut("Ctrl+K")
        linkAction.triggered.connect(self.insertLink)

        codeAction = QtWidgets.QAction(QtGui.QIcon("icons/code.png"),"Insert code block",self)
        codeAction.setStatusTip("Insert code block (Ctrl+Shift+C)")
        codeAction.setShortcut("Ctrl+Shift+C")
        codeAction.triggered.connect(self.insertCode)

        bulletAction = QtWidgets.QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtWidgets.QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(dateTimeAction)
        self.formatbar.addAction(tableAction)
        self.formatbar.addAction(imageAction)
        self.formatbar.addAction(linkAction)
        self.formatbar.addAction(codeAction)
        self.formatbar.addSeparator()

        self.formatbar.addAction(bulletAction)
        self.formatbar.addAction(numberedAction)


    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")
        export = menubar.addMenu("Export")

        # Add the most important actions to the menubar

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveAsAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        export.addAction(self.templateAction)
        export.addAction(self.optionAction)
        export.addAction(self.HTMLExportAction)
        export.addAction(self.PDFExportAction)
        export.addAction(self.EpubExportAction)
        export.addAction(self.docxExportAction)
        export.addAction(self.texExportAction)
        export.addAction(self.saveAsAction)


        # Toggling actions for the various bars
        toolbarAction = QtWidgets.QAction("Toggle Toolbar",self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Toggle Formatbar",self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Toggle Statusbar",self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)


    def initUI(self):
        self.view = QtWidgets.QTextBrowser(self)
        self.text = QtWidgets.QTextEdit(self)
        self.highlighter = markdownHighlight.MarkdownHighlighter(self.text)
        #self.view.render(pypandoc.convert_text(self.text, 'rst', format='html'))
        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)
        self.text.setFont(QtGui.QFont("Monospace"))
        self.text.cursorPositionChanged.connect(self.changed)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        #self.setCentralWidget(self.view)
        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)


        self.setGeometry(100,100,1000,800)
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        self.setCentralWidget(self.text)
        if  "filename" in self.config.keys():
            try:
                self.load(self.config["filename"])
            except Exception as e:
                print("No filemane was already created.")
                self.config.updateConf("filename","~/Desktop/tmp.md")
                self.load(self.config["filename"])
#        self.createGridLayout()
#
#        windowLayout = QtWidgets.QVBoxLayout()
#        windowLayout.addWidget(self.horizontalGroupBox)
#        self.setLayout(windowLayout)

    def createGridLayout(self):
        self.horizontalGroupBox = QtWidgets.QGroupBox()
        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.text,1,1)
        layout.addWidget(self.view,2,1)


        self.horizontalGroupBox.setLayout(layout)

    def changed(self):
        self.highlighter.rehighlight()
        self.changesSaved = False

    def closeEvent(self,event):
        self.config_file.set(self.config)
        if self.changesSaved:

            event.accept()

        else:

            popup = QtWidgets.QMessageBox(self)

            popup.setIcon(QtWidgets.QMessageBox.Warning)

            popup.setText("The document has been modified")

            popup.setInformativeText("Do you want to save your changes?")

            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()



    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):
        spawn = textEdit()
        spawn.show()

    def open(self):
        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".md")[0]
        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())
                self.setWindowTitle("Writter - " + self.filename)
                self.updateConf("filename",self.filename)


    def load(self,filename=""):
        if filename:
            try:
                with open(filename,"rb") as file:
                    self.text.setPlainText(str(file.read(),"utf-8"))
                    self.filename = filename
                    self.updateConf("filename",self.filename)
                    self.setWindowTitle("Writter - " + self.filename)
            except Exception as e:
                QtWidgets.QMessageBox.about(self,"Information!","Impossible to load last opened file.")
                self.text.setText("")
                print("Impossible to load last file : " + str(e))
        self.changesSaved = False

    def save(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]
          self.updateConf("filename",self.filename)
        if self.filename:

            # Append extension if not there yet
            if not self.filename.endswith(".md"):
                self.filename += ".md"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename,"wt") as file:
                file.write(self.text.toPlainText())
        self.changesSaved = True


    def saveAs(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if self.filename == "":
            buttonReply = QtWidgets.QMessageBox.question(self, 'Save your work first', "Markdown document need to be saved first with Ctrl+S. Do you want to save?", QtWidgets.QMessageBox.Yes |  QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                self.save()
            elif buttonReply == QtWidgets.QMessageBox.Cancel:
                return
            else:
                pass

        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File as')[0]

        if filename:
            with open(filename,"wt+") as file:
                    file.write(self.text.toPlainText())
                    self.filename = filename
                    self.setWindowTitle("Writter - " + self.filename)
                    self.updateConf("filename",self.filename)





    def defineTemplate(self):
       self.template = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Template')[0]
       self.updateConf("template",self.template)

    def setOptions(self):
        option.Parameters(self)

    def getOptions(self,exportType):
        pdoc_args=[]
        if "command" in self.config.keys() and self.config["command"] != "":
            pdoc_args=self.config["command"].split(" ")
        else:
            pdoc_args=["-s"]
            try:

                if self.config["toc"]:
                    pdoc_args.append("--toc")
                if exportType == "html":
                    if self.config["mathjax"]:
                        pdoc_args.append("--mathjax")
                    if self.config["selfContained"]:
                        pdoc_args.append("--self-contained")
                    #TODO Correct a bug when not self contained and local css
                    if self.config["css"]:
                        if self.config["css"].startswith("C:/") and not self.config["selfContained"]:
                            pdoc_args.append("-c file://{}".format(self.config["css"]))
                        else:
                            pdoc_args.append("-c {}".format(self.config["css"]))
                    if self.template.endswith("html"):
                        pdoc_args.append("--template {}".format(self.template))
                if exportType =="docx":
                    if self.template.endswith("docx"):
                        pdoc_args.append("--reference-doc={}".format(self.template))
                if exportType =="tex":
                    if self.template.endswith("tex"):
                        pdoc_args.append("--template {}".format(self.template))
            except Exception as e:
                print("Error getting options some may not have been set!")


        return pdoc_args


    def exportPDF(self):
        pdoc_args = self.getOptions("pdf")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as PDF',tools.clean_export_name(self.filename,".pdf"),filter="PDF files (*.pdf)")[0]
        pypandoc.convert_text(self.text.toPlainText(), 'pdf', format='md', outputfile=filename, extra_args=pdoc_args)


    def exportHTML(self):
        pdoc_args = self.getOptions("html")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as HTML',tools.clean_export_name(self.filename,".html"),filter="Web files (*.html *.htm)")[0]
        pypandoc.convert_text(self.text.toPlainText(), 'html', format='md', outputfile=filename, extra_args=pdoc_args)

    def exportEpub(self):
        pdoc_args = self.getOptions("epub")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Export as Epub',tools.clean_export_name(self.filename,".epub"),filter=".epub")[0]
        pypandoc.convert_text(self.text.toPlainText(), 'epub', format='md', outputfile=filename, extra_args=pdoc_args)

    def exportDocx(self):
        pdoc_args = self.getOptions("docx")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Export as OpenDocument',tools.clean_export_name(self.filename,".docx"),filter=".docx,*")[0]
        pypandoc.convert_text(self.text.toPlainText(), 'docx', format='md', outputfile=filename, extra_args=pdoc_args)


    def exportTex(self):
        pdoc_args = self.getOptions("tex")
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Export as tex',tools.clean_export_name(self.filename,".tex"),filter=".tex,*")[0]
        pypandoc.convert_text(self.text.toPlainText(), 'tex', format='md', outputfile=filename, extra_args=pdoc_args)




    def preview(self):

        if self.takeCentralWidget() == self.text:
            self.setCentralWidget(self.view)
            self.view.setHtml( pypandoc.convert_text(self.text.toPlainText(), 'html', format='md',extra_args=["-c input/github.css","-s"]))
        else:
            self.setCentralWidget(self.text)



    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def wordCount(self):

        wc = wordcount.WordCount(self)

        wc.getText()

        wc.show()

    def insertImage(self):

        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if not filename:

            popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                      "Image load error",
                                      "Could not load image file!",
                                      QtWidgets.QMessageBox.Ok,
                                      self)
            popup.show()
        cursor = self.text.textCursor()
        cursor.insertText("![{}]({})".format(cursor.selectedText(),filename))

    def insertLink(self):
            link= self.getLink()
            text = link if self.text.textCursor().selectedText() == "" else self.text.textCursor().selectedText()
            cursor = self.text.textCursor()
            cursor.insertText("[{}]({})".format(text,link))

    def insertCode(self):
            langage= self.getCodeLangage()
            cursor = self.text.textCursor()
            cursor.insertText("```{}\n{}\n```".format(langage,cursor.selectedText()))


    def getLink(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Create link","URL :", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

    def getCodeLangage(self):
        items = ("bash","C","C#","C++","python","md","java","js")
        item, okPressed = QtWidgets.QInputDialog.getItem(self, "Create code block","Langage :", items, 0, False)
        if okPressed and item != '':
            return item

    def outputName(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Export the md file","Name of exported document :", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

# Formatage functions
    def mdformat(self,formatChar):
        cursor = self.text.textCursor()
        text = cursor.selectedText()
        cursor.removeSelectedText()
        if text == "":
            cursor.insertText(formatChar*2)
            return
        elif text.startswith(formatChar) and text.endswith(formatChar) and len(text)>=2*len(formatChar) :
            if formatChar in ["^","~"]:
                text = text.replace("\\ "," ")
            text = text[len(formatChar):-len(formatChar)]
            cursor.insertText(text)
            return
        else:
            if formatChar in ["^","~"]:
                text = text.replace(" ","\\ ")
            text =  "{}{}{}".format(formatChar,text,formatChar)
            cursor.insertText(text)
            return

    def bold(self):
        self.mdformat("**")

    def italic(self):
        self.mdformat("*")

    def strike(self):
        self.mdformat("--")

    def superScript(self):
        self.mdformat("^")

    def subScript(self):
        self.mdformat("~")


    def bulletList(self):
        cursor = self.text.textCursor()
        cursor.insertText("- \n"*3)

    def numberList(self):
        cursor = self.text.textCursor()
        cursor.insertText("1. \n2. \n3. \n")



class SpellAction(QtWidgets.QAction):

    '''
    A special QAction that returns the text in a signal.
    '''

    correct = QtCore.pyqtSignal()

    def __init__(self, *args):
        QtWidgets.QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(self.text()))


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = textEdit()
    main.show()
    #main.showFullScreen()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
