"""
Created on Thu Apr 9 00:10:00 2020
@author: max

# Web preview for PandocTextEditor based on PyQt Web Engine
"""

import sys
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QApplication, QTextBrowser, QWidget, QMdiSubWindow, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDir, QUrl

# arg = text vs html; mInput = 'text'/'html'; mView = = 'textBrowser'/'webEngine'
class WebPrev(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        self.web = QWebEngineView()
        return(None)
    
    def browse(self,name, **kwargs): #**path or text
        print('path' in kwargs.keys())
        self.web.setWindowTitle("Html Preview - %s - WebEngine" % name)
        self.web.setWindowIcon(QtGui.QIcon("../PandocTextEditor/icons/icon.png"))
        #self.web.setGeometry(100,100,1000,800)
        self.web.load(QUrl.fromLocalFile(kwargs['path']))
        self.web.show()
        sys.exit(self.app.exec_())

# *********************************************************************
# *********************************************************************

class WebTextPrev(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        #self.app = QApplication(sys.argv)
        #QtWidgets.ChildWindows.__init__(self,parent)
        #QMdiSubWindow.__init__(self,parent)
        #super(WebTextPrev, self).__init__(parent)

        self.web = QWebEngineView()
        #self.setCentralWidget(self.web)
        return(None)
    
    def browse(self,name,textHTML):
        self.web.setWindowTitle("Html Preview - %s" % name)
        self.web.setWindowIcon(QtGui.QIcon("../PandocTextEditor/icons/icon.png"))
        #self.web.setGeometry(100,100,1000,800)
        self.web.setHtml(textHTML)
        self.web.show()
        #sys.exit(self.app.exec_())



# *********************************************************************
# *********************************************************************

class TextPrev():
    def __init__(self):
        #self.app = QApplication(sys.argv)
        self.web = QTextBrowser()
        return(None)
    
    def browse(self,path,name):
        self.web.setWindowTitle("Html Preview - %s - TextBrowser" % name)
        self.web.setWindowIcon(QtGui.QIcon("../PandocTextEditor/icons/icon.png"))
        #self.web.setGeometry(100,100,1000,800)
        self.web.setSource(QUrl.fromLocalFile(path))
        self.web.show()
        #sys.exit(self.app.exec_())


class TextTextPrev():
    def __init__(self):
        #self.app = QApplication(sys.argv)
        #QWidget.__init__(self)
        self.web = QTextBrowser()
        self.setWindowTitle('Window Two')
        return(None)
    
    def browse(self,name,textHTML):
        self.web.setWindowTitle("Html Preview - %s" % name)
        self.web.setWindowIcon(QtGui.QIcon("../PandocTextEditor/icons/icon.png"))
        #self.web.setGeometry(100,100,1000,800)
        self.web.setHtml(textHTML)
        self.web.show()
        #sys.exit(self.app.exec_())


#if __name__ == "__main__":
#    self.app = QApplication(sys.argv)
#
#
#
#    wp = WebPrev()
#    tp = TextPrev()
#    print(wp)
#    print(tp)
#    path = "D:\\Sciences\\2020_BongoKnight\\Blabla\\build\\README.html"
#    name = path.split("\\")[-1].split(".")[0]
#    
#    tp.browse(path,name)
#    wp.browse(name, path=path)

    # Toujours avec le même css ?
    # Comment on compile le fichir ?
    # Ici ou avec une autre fonction

    #QtGui.QTextBrowser(self)
    #self.html.setHtml(text)

class MainWindow(QtWidgets.QMainWindow):

    def __init(self, parent=None):
         QtWidgets.QMainWindow.__init__(self,parent)
         self.view = QtWidgets.QTextBrowser(self)
         self.show()
         return(None)


def main():
    app = QtWidgets.QApplication(sys.argv)
    #main = MainWindow()
    webPrev = WebPrev()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    