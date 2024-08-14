import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

# 主界面类
class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Interface")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # 创建布局
        layout = QVBoxLayout()

        # csv文件路径输入框
        self.label_picdir = QLabel("CSV文件存放绝对路径:")
        layout.addWidget(self.label_picdir)

        self.input_picdir = QLineEdit()
        layout.addWidget(self.input_picdir)

        # 录入按钮
        self.login_button = QPushButton("录入")
        self.login_button.clicked.connect(self.handle_input)
        layout.addWidget(self.login_button)

        # 设置中央窗口部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_input(self):
        picdir = self.input_picdir.text()

        if picdir:
            try:
                sql_conn = pymysql.connect(
                    host='127.0.0.1', port=3306, user='root',
                    password='123', db='school', charset='utf8', connect_timeout=1000
                )
                cursor = sql_conn.cursor()

                with open(picdir, encoding='Ansi') as file:
                    for line in file:
                        line = line.strip()
                        list_1 = line.split(',', -1)
                        sql_2 = '''
                        INSERT IGNORE INTO students (student_id, academy, name, class, graduation_year, major, image_url)
VALUES (%s, %s, %s, %s, %s, %s, %s);
                        '''
                        cursor.execute(sql_2, (
                            list_1[0], list_1[1], list_1[2], list_1[3], list_1[4], list_1[5], list_1[6]
                        ))
                sql_conn.commit()
                sql_conn.close()
                QMessageBox.information(self, "Success", "Data imported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")
        else:
            QMessageBox.warning(self, "INPUT Failed", "请输入正确路径")

# 登录界面类
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        # 创建布局
        layout = QVBoxLayout()

        # 用户名输入框
        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        layout.addWidget(self.input_username)

        # 密码输入框
        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        # 登录按钮
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # 设置中央窗口部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == "admin" and password == "123":
            QMessageBox.information(self, "Login Successful", "Welcome, admin!")
            self.open_main_interface()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_main_interface(self):
        self.main_interface = MainInterface()
        self.main_interface.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
