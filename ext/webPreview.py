import os
import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDir, QUrl


# mode = 'text'/'html'; name = window name; content = link to html file
class WebPreview(QtWidgets.QMainWindow):

    def __init__(self, mode, name, path):
        QtWidgets.QMainWindow.__init__(self, parent=None)
        if mode == "text":
            self.web = QtWidgets.QTextBrowser()
            self.setWindowTitle("Html Preview - %s - TextBrowser" % name)
        elif mode == "web":
            self.web = QWebEngineView()
            self.setWindowTitle("Html Preview - %s - WebEngine" % name)
        
        self.setCentralWidget(self.web)
        self.setWindowIcon(QtGui.QIcon("../icons/icon.png"))
        #self.web.setGeometry(100,100,1000,800)

        self.browse(mode, path)
        return(None)
    
    def browse(self, mode, path):
        if mode == "text":
            self.web.setSource(QUrl.fromLocalFile(path))
        elif mode == "web":
            path = os.path.abspath(path)
            self.web.load(QUrl.fromLocalFile(path))
        return(None)


# ************************************ Main *********************************
def main():
    path = "../preview.html"
    app = QtWidgets.QApplication(sys.argv)
    webPrev = WebPreview("web", "Test", path, None)
    webPrev.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 