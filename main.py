import sys

import sqlite3

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from UI import Ui_MainWindow


class FilmSearcher(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("films_db.sqlite")
        self.InitUI()

    def InitUI(self):
        self.btn_run.clicked.connect(self.search)

    def search(self):
        year = self.lineEdit_year.text()
        name = self.lineEdit_name.text()
        length = self.lineEdit_length.text()
        query = "SELECT id, title, year, genre, duration FROM films"

        if year or name or length:
            query += " WHERE"
        if year:
            if '>' in year or '<' in year:
                query += f" year{year}"
            else:
                query += f" year={year}"
            if name or length:
                query += " and"
        if name:
            if 'LIKE' in name.upper():
                query += f" title {name}"
            else:
                query += f" title={name}"
            if length:
                query += " and"
        if length:
            if '>' in length or '<' in length:
                query += f" duration{length}"
            else:
                query += f" duration={length}"
        self.set_table(query)

    def set_table(self, query):
        try:
            cur = self.connection.cursor()
            res = cur.execute("""PRAGMA table_info("films")""").fetchall()
            column_names = [i[1] for i in res]
            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            res = cur.execute(query).fetchall()
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        except Exception as ex:
            print(ex)

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FilmSearcher()
    ex.show()
    sys.exit(app.exec())
