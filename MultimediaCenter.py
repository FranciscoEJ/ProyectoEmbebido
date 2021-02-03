from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys

from photo import AppPhoto
from music import MusicWindow
from video import VideoWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #progress bar
        self.pbar = QProgressBar()
        self.pbar.setMaximumWidth(100)

        #creating mainwindow page
        self.browser=QWebEngineView(loadProgress=self.pbar.setValue, loadFinished=self.pbar.hide,
                                  loadStarted=self.pbar.show, titleChanged=self.setWindowTitle)
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.setCentralWidget(self.browser)

        #when mouse is hovered over any link
        self.browser.page().linkHovered.connect(self.if_link_hover)

        #creating statusbar
        self.browser.setMinimumSize(1200, 600)
        self.status = self.statusBar()
        self.status.addPermanentWidget(self.pbar)

        self.show()
        self.setWindowTitle("Multimedia Center")
        self.setWindowIcon(QIcon("iconos/cosmo.png"))

        #adding toolbar
        tb2 = QToolBar("Shortcuts")
        tb2.setIconSize(QSize(45,45))
        self.addToolBar(Qt.LeftToolBarArea,tb2)

        #adding shortcut links of popular websites

        nx_btn = QAction(QIcon("iconos/netflix.png"), "Netflix", self)
        nx_btn.setStatusTip("Go to Netflix")
        nx_btn.triggered.connect(lambda: self.conn("http://www.netflix.com/mx-en/"))
        tb2.addAction(nx_btn)

        ib_btn = QAction(QIcon("iconos/hbo.png"), "HBO GO", self)
        ib_btn.setStatusTip("Go to HBO")
        ib_btn.triggered.connect(lambda: self.conn("https://www.hbogola.com/landing"))
        tb2.addAction(ib_btn)
        
        ib_btn = QAction(QIcon("iconos/disney.png"), "Disney Plus", self)
        ib_btn.setStatusTip("Go to Disne+")
        ib_btn.triggered.connect(lambda: self.conn("https://www.disneyplus.com/es-mx/"))
        tb2.addAction(ib_btn)

        ib_btn = QAction(QIcon("iconos/primevideo.png"), "Amazon Prime Video", self)
        ib_btn.setStatusTip("Go to Amazon Prime Video")
        ib_btn.triggered.connect(lambda: self.conn("https://www.primevideo.com/"))
        tb2.addAction(ib_btn)

        msn_btn = QAction(QIcon("iconos/blim.png"), "Bim", self)
        msn_btn.setStatusTip("Go to Blim")
        msn_btn.triggered.connect(lambda: self.conn("https://www.blim.com/cuenta/ingresar"))
        tb2.addAction(msn_btn)

        msn_btn = QAction(QIcon("iconos/spoti.png"), "Spotify", self)
        msn_btn.setStatusTip("Go to Spotify")
        msn_btn.triggered.connect(lambda: self.conn("https://open.spotify.com/"))
        tb2.addAction(msn_btn)

        msn_btn = QAction(QIcon("iconos/deezer.png"), "Deezer", self)
        msn_btn.setStatusTip("Go to Deezer")
        msn_btn.triggered.connect(lambda: self.conn("https://www.deezer.com/mx/"))
        tb2.addAction(msn_btn)

        msn_btn = QAction(QIcon("iconos/itunes.png"), "iTunes", self)
        msn_btn.setStatusTip("Go to iTunes")
        msn_btn.triggered.connect(lambda: self.conn("https://www.apple.com/mx/itunes/"))
        tb2.addAction(msn_btn)

        msn_btn = QAction(QIcon("iconos/youtube.png"), "Youtube", self)
        msn_btn.setStatusTip("Go to Youtube")
        msn_btn.triggered.connect(lambda: self.conn("https://music.youtube.com/"))
        tb2.addAction(msn_btn)

        msn_btn = QAction(QIcon("iconos/cloudflare.png"), "Cloudflare", self)
        msn_btn.setStatusTip("Go to Cloudflare")
        msn_btn.triggered.connect(lambda: self.conn("https://www.cloudflare.com/es-es/"))
        tb2.addAction(msn_btn)

        #another toolbar
        tb=QToolBar("Navigation")
        tb.setIconSize(QSize(40,40))
        self.addToolBar(tb)

        win_btn = QAction(QIcon("iconos/gallery.png"), "Open Gallery", self)
        win_btn.setStatusTip("Open Gallery")
        win_btn.triggered.connect(self.new_winPhoto)
        tb.addAction(win_btn)

        win_btn = QAction(QIcon("iconos/videoplay.png"), "Open Video Player", self)
        win_btn.setStatusTip("Open VideoPlayer")
        win_btn.triggered.connect(self.new_winVideo)
        tb.addAction(win_btn)

        win_btn = QAction(QIcon("iconos/musicplay.png"), "Open Music Player", self)
        win_btn.setStatusTip("Open MusicPlayer")
        win_btn.triggered.connect(self.new_winMusic)
        tb.addAction(win_btn)

        tb.addSeparator()

        home_btn = QAction(QIcon("iconos/home.png"), "Home", self)
        home_btn.setStatusTip("Go to home page")
        home_btn.triggered.connect(self.gohome)
        tb.addAction(home_btn)
        
        back_btn=QAction(QIcon("iconos/Button-Back-1-512.png"),"Back",self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        tb.addAction(back_btn)

        fwd_btn = QAction(QIcon("iconos/forward.png"), "Forward", self)
        fwd_btn.setStatusTip("Forward to next page")
        fwd_btn.triggered.connect(self.browser.forward)
        tb.addAction(fwd_btn)

        rld_btn = QAction(QIcon("iconos/refresh"), "Reload", self)
        rld_btn.setStatusTip("Reload this page")
        rld_btn.triggered.connect(self.browser.reload)
        tb.addAction(rld_btn)

        #ading URL bar
        self.urlbar=QLineEdit()
        tb.addSeparator()
        self.urlbar.returnPressed.connect(self.navigate_page)
        tb.addWidget(self.urlbar)

        #action to perform when URL is changed
        self.browser.urlChanged.connect(self.update_url)

        stop_btn=QAction(QIcon("iconos/stop.png"),"Stop",self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        tb.addAction(stop_btn)

        self.statusBar().showMessage('Multimedia Center')
        self.show()

    #to open Photo window
    def new_winPhoto(self):
        windo = AppPhoto()
        windo.show()
    
    #to open Music window
    def new_winMusic(self):
        windo = MusicWindow()
        windo.show()
    
    #to open Video window
    def new_winVideo(self):
        self.windo = VideoWindow()
        self.windo.show()
        self.windo.resize(640, 480)
    
    def new_win(self):
        self 

    #edit URL bar
    def update_url(self,q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    #open home page
    def gohome(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    #user entered URL tasks
    def navigate_page(self):
        q=QUrl(self.urlbar.text())
        t=self.urlbar.text()
        if "." not in t:
            t='http://www.google.com/search?q='+t
            self.browser.setUrl(QUrl(t))
        elif q.scheme()=="":
            q.setScheme("http")
            self.browser.setUrl(q)
        else:
            self.browser.setUrl(q)

    #connect shortcut websites
    def conn(self,s):
        self.browser.setUrl(QUrl(s))

    #change status
    def if_link_hover(self, l):
        self.status.showMessage(l)

    def closeEvent(self,event):
        reply = QMessageBox.question(self,'Message','Pres Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if reply == QMessageBox.Yes :
            qApp.quit()
        else :
            try:
                event.ignore()
            except AttributeError:
                pass

#usual
app=QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())
