import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
class DatabaseThread(QThread):
    data_signal = pyqtSignal(tuple)

    def __init__(self, db_config, query, params):
        super().__init__()
        self.db_config = db_config
        self.query = query
        self.params = params

    def run(self):
        conn = pymysql.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute(self.query, self.params)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        self.data_signal.emit(data)

class infoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Data Interface'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)
        self.entry = QLineEdit(self)
        self.get_button = QPushButton('Get Data from Database')
        self.get_button.clicked.connect(self.query_database)
        layout = QVBoxLayout()
        layout.addWidget(self.entry)
        layout.addWidget(self.get_button)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

    def query_database(self):
        name = self.entry.text()
        query = """
        SELECT student_id,academy,name,class,graduation_year,major,image_url
        FROM students WHERE name = %s
        """
        # 创建数据库查询线程
        self.thread = DatabaseThread(
            {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '123', 'charset': 'utf8', 'db': 'school'},
            query,
            (name,)
        )
        self.thread.data_signal.connect(self.show_data_window)
        self.thread.start()

    def show_data_window(self, data):
        if not data:
            QMessageBox.information(self, 'Information', 'No data found.')
            return

        # 创建一个新的窗口来展示数据
        self.data_window = QMainWindow()
        self.data_window.setWindowTitle("Data Display")
        layout = QVBoxLayout()

        # 假设数据的顺序是 (student_id, name, college, class, major, graduation_year)\
        student_id,academy,name,class1,graduation_year,major,image_dir = data

        # 创建标签显示各项信息
        label_name = QLabel(f"Name: {name}", self.data_window)
        layout.addWidget(label_name)

        label_id = QLabel(f"Student ID: {student_id}", self.data_window)
        layout.addWidget(label_id)

        label_college = QLabel(f"Academy: {academy}", self.data_window)
        layout.addWidget(label_college)

        label_class = QLabel(f"Class: {class1}", self.data_window)
        layout.addWidget(label_class)

        label_major = QLabel(f"Major: {major}", self.data_window)
        layout.addWidget(label_major)

        label_grad_year = QLabel(f"Graduation Year: {graduation_year}", self.data_window)
        layout.addWidget(label_grad_year)
        if image_dir:
            pixmap = QPixmap(image_dir)
            if not pixmap.isNull():
                label_image = QLabel(self.data_window)
                label_image.setPixmap(pixmap)
                label_image.setScaledContents(True)  # 图片自适应标签大小
                layout.addWidget(label_image)
            else:
                QMessageBox.warning(self, 'Image Load Error', f"Could not load image from {image_dir}")

        # 创建一个返回按钮
        back_button = QPushButton("Back to Search", self.data_window)
        back_button.clicked.connect(self.data_window.close)
        layout.addWidget(back_button)

        # 设置布局并显示窗口
        container = QWidget()
        container.setLayout(layout)
        self.data_window.setCentralWidget(container)
        self.data_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = infoWindow()
    window.show()
    app.exec_()
