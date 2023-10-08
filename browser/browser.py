from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5.QtWidgets import QToolBar, QLineEdit 
from PyQt5.QtWidgets import QPushButton, QVBoxLayout 
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.nav_bar = QToolBar()
        self.nav_bar.setMovable(False)
        self.addToolBar(self.nav_bar)

        self.back_button = QPushButton("<--")
        self.nav_bar.addWidget(self.back_button)

        self.forward_button = QPushButton("-->")
        self.nav_bar.addWidget(self.forward_button)

        self.refresh_button = QPushButton("Refresh")
        self.nav_bar.addWidget(self.refresh_button)

        self.url_input = QLineEdit()
        self.nav_bar.addWidget(self.url_input)

        self.go_button = QPushButton("Go")
        self.nav_bar.addWidget(self.go_button)

        self.back_button.clicked.connect(
            self.browser.back)
        self.forward_button.clicked.connect(
            self.browser.forward)
        self.refresh_button.clicked.connect(
            self.browser.reload)
        self.go_button.clicked.connect(
            self.navigate)
        self.url_input.returnPressed.connect(
            self.navigate)

        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.init_menu_bar()

    def init_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def navigate(self):
        input_text = self.url_input.text()
        if input_text.strip():
            # check if input contains URL
            if (not input_text.startswith(
                "http://")) and (
                not input_text.startswith(
                    "https://")):
                # search query
                search_query = input_text
                input_text = "https://www.google.com/"
                input_text = input_text + "search?q=" 
                input_text = input_text + search_query

            self.browser.setUrl(QUrl(input_text))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())
