from PyQt5.QtWidgets import (QApplication, QLabel, QSpacerItem, QSizePolicy, QPushButton,
                            QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit, QAction)
from PyQt5.QtCore import QEvent, Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont, QCursor
from sys import argv, exit

#Setting up ui size on high resolution
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class UpsideDown(QWidget):
    stylesheet = """
                #Main{
                    background-color: #218c74;
                }
                QLabel{
                    color: #f7f1e3;
                }
                #Upside-O{
                    color: #f7f1e3;
                    border: none;
                    background-color: #2e7e6c;
                }
                QPushButton{
                    background-color: transparent;
                }
                """

    def __init__(self):
        super().__init__()
        #Creating dictionary of normal and upsidedown letters
        self.normal_chars = {n:u for n,u in zip("_∴⁅⁆{}[]<>;.()'&\"!?987654321ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba",
                                      "‾∵⁆⁅}{][><؛˙)(,⅋„¡¿68ㄥ9ϛㄣƐᄅƖZ⅄XϺɅՈꓕSꓤꝹԀONꟽ⅂ꓘᒋIH⅁ᖵƎᗡϽꓭ∀zʎxʍʌnʇsɹbdouɯʅʞɾᴉɥƃⅎǝpɔqɐ")}
        self.upside_chars = {value:key for key, value in self.normal_chars.items()}

        #Declaring width, height, and it's factors
        self.w,self.h = 774, 544
        self.w_factor,self.h_factor = 1,1
        self.copied = False

        #Handling ui components
        self.init_ui()
        self.layout_management()


    def init_ui(self):
        self.fullscreen = QAction("&Fullscreen", self)
        self.title = QLabel("Make it Upside Down !", self)
        self.vspacer = QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vspacer_2 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.create_input()
        self.create_output()

        self.setObjectName("Main")
        self.setWindowIcon(QIcon("Assets/icon.png"))
        self.setWindowTitle("Upside down Text Generator")
        self.setMinimumSize(493, 494)
        self.resize(self.w, self.h)
        self.setStyleSheet(self.stylesheet)

        self.fullscreen.setShortcut("F11")
        self.fullscreen.triggered.connect(self.toggle_fullscreen)
        self.fullscreen.setStatusTip("Change to fullscreen mode")
        self.addAction(self.fullscreen)

        self.title.setObjectName("Title")
        self.upsidedown_output.setObjectName("Upside-O")
        self.input_text.setObjectName("Upside-Input")
        self.upsidedown_input.setFixedSize(350, 50)
        self.upsidedown_input.textChanged.connect(self.send_output)
        self.upsidedown_output.setReadOnly(True)
        self.upsidedown_output.setFixedSize(350, 60)
        self.copy_btn.setFixedSize(64, 64)
        self.copy_btn.setIcon(QIcon("Assets/copy.png"))
        self.copy_btn.setIconSize(QSize(40, 45))
        self.copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.copy_btn.setToolTip("Copy to clipboard")
        self.copy_btn.clicked.connect(self.copy_text) 
        self.copy_btn.installEventFilter(self)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def create_input(self):
        self.input_widget = QWidget()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        spacer = QSpacerItem(6, 0, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.input_text = QLabel("Type text here", self)
        self.upsidedown_input = QTextEdit(self)
        vlayout.addWidget(self.input_text, alignment=Qt.AlignHCenter)
        hlayout.addItem(spacer)
        hlayout.addWidget(self.upsidedown_input)
        vlayout.addLayout(hlayout)
        self.input_widget.setLayout(vlayout)

    def create_output(self):
        self.output_widget = QWidget()
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        self.output_spacer = QSpacerItem(80, 0, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.output_text = QLabel("Result", self)
        self.upsidedown_output = QTextEdit(self)
        self.copy_btn = QPushButton(self)
        vlayout.addWidget(self.output_text, alignment=Qt.AlignHCenter)
        hlayout.addItem(self.output_spacer)
        hlayout.addWidget(self.upsidedown_output)
        hlayout.addWidget(self.copy_btn)
        vlayout.addLayout(hlayout)
        self.output_widget.setLayout(vlayout)

    def layout_management(self):
        layout = QGridLayout()
        ui_arr = ["title", 
                  "input_widget",
                  "spacer",
                  "output_widget"]
        positions = [(i, j) for i in range(1, 5) for j in range(1, 2)]

        layout.addItem(self.vspacer, 0, 1)
        for position, name in zip(positions, ui_arr):
            if name == 'spacer':
                layout.addItem(self.vspacer_2, *position)
            else:
                layout.addWidget(eval(f"self.{name}"), *position, alignment=Qt.AlignHCenter)

        layout.setVerticalSpacing(30)
        layout.addItem(self.vspacer, 5, 1)

        self.setLayout(layout)
            
    def send_output(self):
        #Converting input value to upsidedown and sending them to output
        text = self.get_upside_down(self.upsidedown_input.toPlainText())[::-1]
        self.upsidedown_output.setPlainText(text)

    def copy_text(self):
        def on_click():
            #Setting back button's icon to normal icon
            self.copy_btn.setIcon(QIcon("Assets/copy.png"))
            self.copied = False

        #Copy output text to clipboard 
        self.upsidedown_output.selectAll()
        self.upsidedown_output.copy()
        self.upsidedown_output.setText(self.upsidedown_output.toPlainText())

        #Set button's icon to copied
        self.copy_btn.setIcon(QIcon("Assets/copied.png"))
        self.copied = True
        QTimer.singleShot(1100, on_click)


    def eventFilter(self, widget, event):
        #Event filter on hovering on copy button
        if (event.type() == QEvent.Enter and widget == self.copy_btn):
            widget.setIcon(QIcon("Assets/copy_hover.png"))
        elif (event.type() == QEvent.Leave and widget == self.copy_btn):
            if not self.copied:
                widget.setIcon(QIcon("Assets/copy.png"))

        return super().eventFilter(widget, event)

    def get_upside_down(self, text):
        #Converting letters to it's upsidedown value
        result = ""
        for letter in text:
            try:
                if letter in self.normal_chars:
                    result += self.normal_chars[letter]
                else:
                    result += self.upside_chars[letter]
            except:
                result += letter

        return result

    def resizeEvent(self, event):
        #Resizing widgets, depending on ui window's size
        self.w_factor = self.width() / self.w 
        self.h_factor = self.height() / self.h

        if self.w_factor >= 1:
            self.title.setFont(QFont("Arial", 25*self.h_factor))
            self.input_text.setFont(QFont("Bahnschrift Light", 15*self.h_factor))
            self.output_text.setFont(QFont("Bahnschrift Light", 15*self.h_factor))
            self.upsidedown_input.setFixedSize(309*self.w_factor, 77*self.h_factor)
            self.upsidedown_input.setFont(QFont("Arial", 10*self.h_factor))
            self.upsidedown_output.setFixedSize(309*self.w_factor, 77*self.h_factor)
            self.upsidedown_output.setFont(QFont("Arial", 10*self.h_factor))
            self.output_spacer.changeSize(72*self.w_factor, 54.18000000000001*self.h_factor)
            self.copy_btn.setFixedSize(61*self.w_factor, 61*self.h_factor)
            self.copy_btn.setIconSize(QSize(46*self.w_factor, 46*self.h_factor))
        else:
            self.title.setFont(QFont("Arial", 25))
            self.input_text.setFont(QFont("Bahnschrift Light", 15))
            self.output_text.setFont(QFont("Bahnschrift Light", 15))
            self.upsidedown_input.setFixedSize(309, 77)
            self.upsidedown_input.setFont(QFont("Arial", 10))
            self.upsidedown_output.setFixedSize(309, 77)
            self.upsidedown_output.setFont(QFont("Arial", 10))
            self.output_spacer.changeSize(69.66, 54.18000000000001)
            self.copy_btn.setFixedSize(61, 61)
            self.copy_btn.setIconSize(QSize(46, 46))

if __name__ == '__main__':
    app = QApplication(argv)
    win = UpsideDown()
    win.show()
    exit(app.exec_())


