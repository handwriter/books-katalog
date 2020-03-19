import sqlite3
from PyQt5.QtGui import QPixmap
import sys
from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QFileDialog, QLabel
from design import Ui_Form as Design


class MyWidget(QWidget, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try:
            self.con = sqlite3.connect(QFileDialog.getOpenFileName()[0])
        except:
            self.close()
        self.pushButton.clicked.connect(self.update_result)
        self.titles = None
        self.count = 0
        self.update_result()

    def update_result(self):
        self.count += 1
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        if self.count == 1:
            result = cur.execute("""SELECT * FROM Info""").fetchall()
        elif self.comboBox.currentIndex() == 1:
            result = cur.execute("""SELECT * FROM Info
                                    WHERE title = ?""",
                                (str(self.lineEdit.text()),)).fetchall()
        else:
            print(8)
            result = cur.execute("""SELECT * FROM Info
                                    WHERE author = ?""",
                                 (str(self.lineEdit.text()),)).fetchall()
        # Заполнили размеры таблицы
        print(9)
        if len(result) == 0:
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
        else:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
        print(10)
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 4:
                    try:
                        self.image = Image.open(str(val))
                    except:
                        self.image = Image.open("data\\images\\default.jpg")
                    a = QLabel()
                    self.image = self.image.convert("RGBA")
                    a.setPixmap(QPixmap.fromImage(ImageQt(self.image)))
                    self.tableWidget.setCellWidget(i, j, a)
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE films SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())