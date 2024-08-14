import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from information import infoWindow  # 导入infoWindow类
from Login import LoginWindow  # 导入LoginWindow类

# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 在布局中添加中间的文本
        self.label = QLabel("大连外国语学校校友查询", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # 创建一个水平布局用于按钮
        button_layout = QHBoxLayout()

        # 添加按钮并连接到方法
        button1 = QPushButton("校友查询", self)
        button1.clicked.connect(self.open_info_window)
        button_layout.addWidget(button1)

        button2 = QPushButton("毕业合影查询", self)
        button2.clicked.connect(self.open_option2)
        button_layout.addWidget(button2)

        button3 = QPushButton("管理员", self)
        button3.clicked.connect(self.open_login_window)
        button_layout.addWidget(button3)

        # 将按钮布局添加到主布局中
        layout.addLayout(button_layout)

        # 创建中央小部件并设置布局
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_info_window(self):
        self.info_window = infoWindow()  # 创建infoWindow实例
        self.info_window.show()

    def open_option2(self):
        self.option_window = OptionWindow("毕业合影查询")
        self.option_window.show()

    def open_login_window(self):
        self.login_window = LoginWindow()  # 创建LoginWindow实例
        self.login_window.show()

# 选项窗口类
class OptionWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(150, 150, 400, 300)
        self.initUI(title)

    def initUI(self, title):
        layout = QVBoxLayout()

        label = QLabel(f"You have selected {title}", self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

