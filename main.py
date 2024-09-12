import sqlite3 as sql
import random
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys

class FilmRecommender(QMainWindow):
    def __init__(self):
        super(FilmRecommender, self).__init__()
        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle('Film Önerici')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 20px;
            font-family: Arial;
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.label_film = QLabel("Şansını dene", self)
        self.label_film.setAlignment(Qt.AlignCenter)
        self.label_film.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            padding: 20px;
            margin: 10px;
        """)
        main_layout.addWidget(self.label_film)

        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(20, 20, 20, 20)
        middle_layout.setSpacing(20)

        self.label_left = QLabel("Yönetmen: ", self)
        self.label_left.setStyleSheet("""
            background-color: #e0e0e0;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            margin: 10px;
            width: 250px;
        """)
        middle_layout.addWidget(self.label_left, alignment=Qt.AlignLeft)
        zar_container = QWidget(self)
        zar_layout = QVBoxLayout(zar_container)
        zar_layout.setAlignment(Qt.AlignCenter)

        self.zar_gorsel = QPushButton(self)
        pixmap = QtGui.QPixmap("images/fe1.PNG")
        self.zar_gorsel.setIcon(QtGui.QIcon(pixmap))
        self.zar_gorsel.setIconSize(pixmap.size())
        self.zar_gorsel.setStyleSheet("""
            border: 2px solid #4CAF50;
            border-radius: 50px;
            background-color: #4CAF50;
            width: 130px;  
            height: 110px; 
        """)
        self.zar_gorsel.clicked.connect(self.get_random_film)
        zar_layout.addWidget(self.zar_gorsel)

        middle_layout.addWidget(zar_container, alignment=Qt.AlignCenter)

        self.label_right = QLabel("IMDb Puanı: ", self)
        self.label_right.setStyleSheet("""
            background-color: #e0e0e0;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            margin: 10px;
            width: 250px;
        """)
        middle_layout.addWidget(self.label_right, alignment=Qt.AlignRight)

        main_layout.addLayout(middle_layout)

        self.label_tur = QLabel("Film Türü", self)
        self.label_tur.setAlignment(Qt.AlignCenter)
        self.label_tur.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            margin: 10px;
        """)
        main_layout.addWidget(self.label_tur)

        self.combo_tur = QComboBox(self)
        self.combo_tur.addItem("Hiç farketmez")
        self.combo_tur.addItems(["Drama", "Crime", "Action", "Adventure", "Biography", "Sci-Fi", "Animation"])
        self.combo_tur.setStyleSheet("""
            border: 1px solid #2196F3;
            border-radius: 5px;
            font-size: 14px;
            padding-left: 5px;
            margin: 10px;
        """)
        main_layout.addWidget(self.combo_tur)

    def initDatabase(self):
        try:
            self.conn = sql.connect('FilmList.db')
            self.cursor = self.conn.cursor()
        except sql.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı bağlantısı yapılamadı: {e}")
            self.close()

    def get_random_film(self):
        film_turu = self.combo_tur.currentText()
        query = "SELECT FilmAdi, Yonetmen, IMDbPuanı FROM FILM"
        params = []

        if film_turu != "Hiç farketmez":
            query += " WHERE FilmTuru = ?"
            params.append(film_turu)

        try:
            self.cursor.execute(query, params)
            films = self.cursor.fetchall()

            if films:
                random_film = random.choice(films)
                film_ad, yonetmen, imdb_puani = random_film
                self.label_film.setText(f"Önerilen Film: {film_ad}")
                self.label_left.setText(f"Yönetmen: {yonetmen}")
                self.label_right.setText(f"IMDb Puanı: {imdb_puani}")
            else:
                QMessageBox.warning(self, "Uyarı", "Uygun film bulunamadı!")
                self.label_film.setText("Şansını dene")
                self.label_left.setText("Yönetmen: ")
                self.label_right.setText("IMDb Puanı: ")
        except sql.Error as e:
            QMessageBox.critical(self, "Sorgu Hatası", f"Sorgu çalıştırılamadı: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'conn'):
            self.conn.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = FilmRecommender()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
