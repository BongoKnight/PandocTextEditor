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

#PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
#PYQT5 QFileDialog, QColorDialog, QDialog

from PyQt5 import QtPrintSupport
#PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt


from ext import mdPreview, wordcount, datetime, find, table, markdownHighlight


class textEdit(QtWidgets.QMainWindow):

    def __init__(self,parent=None,filename=""):
        QtWidgets.QMainWindow.__init__(self,parent)

        self.filename = filename
        self.template = ""

        self.changesSaved = True

        self.initUI()

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

        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        self.toolbar.addAction(self.templateAction)
        self.toolbar.addAction(self.PDFExportAction)
        self.toolbar.addAction(self.HTMLExportAction)
        self.toolbar.addAction(self.EpubExportAction)
        self.toolbar.addAction(self.docxExportAction)
        self.toolbar.addAction(self.texExportAction)
        self.addToolBarBreak()

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
        self.view = mdPreview.MarkdownViewer(self)
        self.text = QtWidgets.QTextEdit(self) 
        self.highlighter = markdownHighlight.MarkdownHighlighter(self.text)      
        #self.view.render(pypandoc.convert_text(self.text, 'rst', format='html'))
        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.view)
        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        self.setCentralWidget(self.text)
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
        self.changesSaved = False

    def closeEvent(self,event):

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

    def context(self,pos):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QtGui.QMenu(self)

            appendRowAction = QtWidgets.QAction("Append row",self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QtWidgets.QAction("Append column",self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))


            removeRowAction = QtWidgets.QAction("Remove row",self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QtWidgets.QAction("Remove column",self)
            removeColAction.triggered.connect(self.removeCol)


            insertRowAction = QtWidgets.QAction("Insert row",self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QtWidgets.QAction("Insert column",self)
            insertColAction.triggered.connect(self.insertCol)


            mergeAction = QtWidgets.QAction("Merge cells",self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)


            splitAction = QtWidgets.QAction("Split cells",self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))

            else:
                splitAction.setEnabled(False)


            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)

            menu.addSeparator()

            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)

            menu.addSeparator()

            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)

            menu.addSeparator()

            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)

            if self.formatbar.isVisible():
                pos.setY(pos.y() + 45)
                
            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        else:

            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

            self.text.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(),1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(),1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(),1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(),1)


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

    def open(self,filename=""):
        if filename == "":
            # Get filename and show only .writer files
            #PYQT5 Returns a tuple in PyQt5, we only need the filename
            self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".md")[0]
        else:
            self.filename = filename
        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())
                self.setWindowTitle("Writter - " + self.filename)

    def load(self,filename=""):
        if filename:
            try:
                with open(filename,"rt") as file:
                    self.text.setText(file.read())
                    self.filename = filename
                    self.setWindowTitle("Writter - " + self.filename)      
            except:
                QtWidgets.QMessageBox.about(self,"Information!","Impossible to load last opened file.")
                self.text.setText("")
        self.changed = True
                
    def save(self):

        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

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
            

            if filename.endswith(".html"):
                with open(filename,"wt+") as file:
                    pdoc_args = ['-s']
                    file.write(pypandoc.convert_text(self.text.toPlainText(), 'html', format='md', extra_args=pdoc_args))
            elif filename.endswith(".tex"):
                with open(filename,"wt+") as file:
                    pdoc_args = ['-s']
                    file.write(pypandoc.convert_text(self.text.toPlainText(), 'tex', format='md', extra_args=pdoc_args))
            elif filename.endswith(".docx"):
                with open(filename,"wt+") as file:
                    pdoc_args = ['-s']
                    file.write(pypandoc.convert_file(self.text.toPlainText(), 'docx', format='md', outputfile=filename, extra_args=pdoc_args))           
            else :
                QtWidgets.QMessageBox.warning(self,"Warning!","Invalid file extension! Only HTML, docx and PDF are available.")




    def defineTemplate(self):
       self.template = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Template')[0]
       
     
    def exportPDF(self):
        pdoc_args = ['-s']
        filename = self.outputName()
        if self.template.endswith(".pdf") or self.template.endswith(".tex"):
            pdoc_args.append("--template={}".format(self.template))
            pypandoc.convert_text(self.text.toPlainText(), 'pdf', format='md', outputfile=filename, extra_args=pdoc_args)   
        else :
            pypandoc.convert_text(self.text.toPlainText(), 'pdf', format='md', outputfile=filename, extra_args=pdoc_args)   

    def exportHTML(self):
        pdoc_args = ['-s']
        filename = self.outputName()
        if self.template.endswith(".html"):
            pdoc_args.append("--template={}".format(self.template))
            pypandoc.convert_text(self.text.toPlainText(), 'html', format='md', outputfile=filename, extra_args=pdoc_args)   
        else :
            pypandoc.convert_text(self.text.toPlainText(), 'html', format='md', outputfile=filename, extra_args=pdoc_args)   
   
    def exportEpub(self):
        pdoc_args = ['-s']
        filename = self.outputName()
        if self.template.endswith(".epub"):
            pdoc_args.append("--template={}".format(self.template))
            pypandoc.convert_text(self.text.toPlainText(), 'epub', format='md', outputfile=filename, extra_args=pdoc_args)   
        else :
            pypandoc.convert_text(self.text.toPlainText(), 'epub', format='md', outputfile=filename, extra_args=pdoc_args)   

    def exportDocx(self):
        pdoc_args = ['-s']
        filename = self.outputName()
        if self.template.endswith(".html"):
            pdoc_args.append("--template={}".format(self.template))
            pypandoc.convert_text(self.text.toPlainText(), 'docx', format='md', outputfile=filename, extra_args=pdoc_args)   
        else :
            pypandoc.convert_text(self.text.toPlainText(), 'docx', format='md', outputfile=filename, extra_args=pdoc_args)   
            

    def exportTex(self):
        pdoc_args = ['-s']
        filename = self.outputName()
        if self.template.endswith(".tex"):
            pdoc_args.append("--template={}".format(self.template))
            pypandoc.convert_text(self.text.toPlainText(), 'tex', format='md', outputfile=filename, extra_args=pdoc_args)   
        else :
            pypandoc.convert_text(self.text.toPlainText(), 'tex', format='md', outputfile=filename, extra_args=pdoc_args)   
 


    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

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
            cursor = self.text.textCursor()
            cursor.insertText("[{}]({})".format(cursor.selectedText(),link))

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

def main():
    app = QtWidgets.QApplication(sys.argv)

    main = textEdit()
    main.show()
    main.load("README.md")


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
