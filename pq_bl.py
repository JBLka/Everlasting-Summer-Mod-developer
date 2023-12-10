import sys
import os
import vlc
import codecs
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor, QPixmap
from PyQt5.QtCore import QPointF
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sqlite3

def persons_of_es(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS ES(
       Персонаж TEXT PRIMARY KEY,
       Кодировка TEXT);
    """)
    for i in persons:
        cur.execute(f"""INSERT INTO ES(Персонаж, Кодировка)
           VALUES('{i}', '{persons[i]}');""")

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("es.sqlite")
        self.cur = self.con.cursor()
        persons_of_es(self.cur)
        MyWidget.setFixedSize(self, 450, 250)
        self.setWindowTitle("Создание мода БЛ")
        self.name_of_file = ''
        self.name_of_mod = ''
        self.name_of_chapter = ''
        self.mod_start = ''
        self.all_commands = ['']
        self.command = ''
        self.a = ''
        self.b = ''
        self.c = ''
        self.d = ''
        self.f = ''
        self.h = ''
        self.path_to_pix = ''
        self.with_bg = False
        self.play_now = False
        self.start1()

    def start1(self):
        loadUi("tmp/start_tmp.ui", self)
        self.btn.clicked.connect(self.start2)

    def start2(self):
        self.name_of_file = self.txt.text()
        self.name_of_mod = self.txt_2.text()
        self.name_of_chapter = self.txt_3.text()
        self.mod_start = f'init:\n\n    $ mods["{self.name_of_chapter}"]=u"{self.name_of_mod}"\n' \
                         f'\nlabel {self.name_of_chapter}:\n    \n    '
        self.menu()

    def menu(self):
        loadUi("tmp/menu_tmp.ui", self)
        if self.all_commands[-1] != self.command:
            print(self.command)
            self.all_commands.append(self.command)
        self.command = ''
        self.bg_none()
        self.btn1.clicked.connect(self.add1)
        self.btn2.clicked.connect(self.music1)
        self.btn4.clicked.connect(self.end)
        self.btn5.clicked.connect(self.text1)
        self.btn6.clicked.connect(self.bg1)

    def add1(self):
        loadUi("tmp/add_tmp.ui", self)
        self.pix2 = QPixmap('wtf.png').scaledToWidth(150)
        self.lbl3.setPixmap(self.pix2)
        self.lbl2.move(200, 30)
        self.lbl3.move(215, 77)
        self.lbl3.hide()
        self.lbl2.hide()
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_5.hide()
        self.comboBox_6.hide()
        self.btn.hide()
        self.comboBox.addItems(["Выберите персонажа"] + pers)
        self.comboBox.currentTextChanged.connect(self.add2)
        self.btn_ex.clicked.connect(self.add_ext)

    def add2(self):
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_5.hide()
        self.comboBox_6.hide()
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.lbl2.hide()
        self.lbl3.hide()
        self.btn.hide()
        if self.comboBox.currentText() != 'Выберите персонажа':
            self.comboBox_2 = QComboBox(self)
            self.comboBox_2.setGeometry(30, 80, 161, 21)
            self.comboBox_2.show()
            for i in self.cur.execute(f"SELECT Кодировка FROM ES WHERE Персонаж == '{self.comboBox.currentText()}'"):
                self.a = i[0]
            if self.a in persons_now:
                self.comboBox_2.addItems(["Не изменилась"] + emotions_of_persons[self.comboBox.currentText()])
            else:
                self.comboBox_2.addItems(["Выберите эмоцию"] + emotions_of_persons[self.comboBox.currentText()])
            self.comboBox_2.currentTextChanged.connect(self.add3)

    def add3(self):
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_5.hide()
        self.comboBox_6.hide()
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.lbl2.hide()
        self.lbl3.hide()
        self.btn.hide()
        if self.comboBox_2.currentText() != 'Выберите эмоцию':
            self.comboBox_3 = QComboBox(self)
            self.comboBox_3.setGeometry(30, 110, 161, 21)
            self.comboBox_3.show()
            for i in self.cur.execute(f"SELECT Кодировка FROM ES WHERE Персонаж == '{self.comboBox.currentText()}'"):
                self.a = i[0]
            if self.a not in ['el', 'sh', 'pi', 'uv', 'tl']:
                if self.a in persons_now:
                    self.comboBox_3.addItems(
                        ["Не изменилась"] + clothes_of_persons[self.a])
                    self.add4()
                else:
                    self.comboBox_3.addItems(
                        ["Выберите одежду"] + clothes_of_persons[self.a])
            elif self.comboBox.currentText() == "Юля":
                self.comboBox_3.addItems(["Платье"])
                self.add4()
            else:
                self.comboBox_3.addItems(["Форма"])
                self.add4()
        self.comboBox_3.currentTextChanged.connect(self.add4)

    def add4(self):
        self.comboBox_5.hide()
        self.comboBox_6.hide()
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.lbl2.move(200, 30)
        self.lbl3.move(215, 77)
        self.btn.hide()
        for i in self.cur.execute(f"SELECT Кодировка FROM ES WHERE Персонаж == '{self.comboBox.currentText()}'"):
            a = i[0]
        if self.comboBox_3.currentText() != 'Выберите одежду':
            self.path_to_pix = f'spr/{a} '
            if clothes[self.comboBox_3.currentText()] == '':
                self.path_to_pix += f'{emotions[self.comboBox_2.currentText()]}.png'
            elif os.path.exists(
                    self.path_to_pix + f'{emotions[self.comboBox_2.currentText()]} {clothes[self.comboBox_3.currentText()]}.png'):
                self.path_to_pix += f'{emotions[self.comboBox_2.currentText()]} ' + \
                                    f'{clothes[self.comboBox_3.currentText()]}.png'
            elif os.path.exists(
                    self.path_to_pix + f'{clothes[self.comboBox_3.currentText()]} {emotions[self.comboBox_2.currentText()]}.png'):
                self.path_to_pix += f'{clothes[self.comboBox_3.currentText()]} ' + \
                                    f'{emotions[self.comboBox_2.currentText()]}.png'
            elif 'panama' in clothes[self.comboBox_3.currentText()]:
                if os.path.exists(
                        self.path_to_pix + f'{clothes[self.comboBox_3.currentText()].split()[1]} {emotions[self.comboBox_2.currentText()]} {clothes[self.comboBox_3.currentText()].split()[0]}.png'):
                    self.path_to_pix += f'{clothes[self.comboBox_3.currentText()].split()[1]} ' + \
                                        f'{emotions[self.comboBox_2.currentText()]} ' + \
                                        f'{clothes[self.comboBox_3.currentText()].split()[0]}.png'
                else:
                    self.path_to_pix = 'sprite.jpg'
            elif a == 'pi':
                self.path_to_pix += f'{emotions[self.comboBox_2.currentText()]}.png'
            else:
                self.path_to_pix = 'sprite.jpg'
            if self.path_to_pix == 'sprite.jpg':
                self.comboBox_4.hide()
                self.lbl2.move(200, 60)
                self.pix = QPixmap(self.path_to_pix).scaledToHeight(170)
            else:
                self.pix = QPixmap(self.path_to_pix).scaledToHeight(225)
                self.comboBox_4.show()
            self.lbl2.setPixmap(self.pix)
            self.lbl2.show()
            if self.comboBox_3.currentText() == "Голая":
                self.lbl3.show()
            else:
                self.lbl3.hide()
        self.comboBox_4.currentTextChanged.connect(self.add5)

    def add5(self):
        self.comboBox_6.hide()
        self.btn.hide()
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        if self.comboBox_4.currentText() != 'Где находится персонаж?':
            self.comboBox_5.show()
            self.path_to_pix = self.path_to_pix.replace(" far", "", 1)
            self.path_to_pix = self.path_to_pix.replace(" close", "", 1)
            self.path_to_pix = self.path_to_pix[:-4] + position[self.comboBox_4.currentText()] + self.path_to_pix[-4:]
            self.pix = QPixmap(self.path_to_pix).scaledToHeight(225)
            self.lbl2.setPixmap(self.pix)
            if self.comboBox_4.currentText() == "Близко":
                self.lbl2.move(175, 30)
                self.lbl3.move(200, 95)
            elif self.comboBox_4.currentText() == "Далеко":
                self.lbl2.move(225, 30)
                self.lbl3.move(210, 80)
            else:
                self.lbl2.move(200, 30)
                self.lbl3.move(215, 77)
        else:
            self.comboBox_5.hide()
        self.comboBox_5.currentTextChanged.connect(self.add6)

    def add6(self):
        self.comboBox_6.setCurrentIndex(0)
        if self.comboBox_5.currentText() != "Где находится персонаж?":
            self.comboBox_6.show()
        else:
            self.comboBox_6.hide()
            self.btn.hide()
        self.comboBox_6.currentTextChanged.connect(self.add7)

    def add7(self):
        if self.comboBox_6.currentText() != "Время появления персонажа":
            self.btn.show()
        else:
            self.btn.hide()
        self.btn.clicked.connect(self.add8)

    def add8(self):
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        h = self.path_to_pix[4:len(self.path_to_pix) - 4].split()
        persons_now[h[0]] = h[1:]
        self.command = 'show ' + self.path_to_pix[4:len(self.path_to_pix) - 4] + time[self.comboBox_6.currentText()] + \
                       position[self.comboBox_5.currentText()] + '\n    \n    '
        self.menu()

    def add_ext(self):
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.menu()

    def text1(self):
        loadUi("tmp/text_tmp.ui", self)
        self.btn.clicked.connect(self.text2)
        self.btn_ex.clicked.connect(self.menu)

    def text2(self):
        for i in self.cur.execute(f"SELECT Кодировка FROM ES WHERE Персонаж == '{self.comboBox.currentText()}'"):
            self.a = i[0]
        self.command = f"{self.a} '{self.txt.toPlainText()}'\n    \n    "
        self.menu()

    def music1(self):
        global music
        self.play_now = False
        loadUi("tmp/music_tmp.ui", self)
        self.comboBox.clear()
        self.comboBox.addItems(music)
        self.btn.clicked.connect(self.music2)
        self.btn_2.clicked.connect(self.music_play)
        self.btn_3.clicked.connect(self.music_stop)
        self.comboBox.currentTextChanged.connect(self.music_together)
        self.btn_ex.clicked.connect(self.menu)

    def music2(self):
        p.stop()
        self.command = f'play music music_list["{music_path[self.comboBox.currentText()][:-4]}"]' + \
                       f' fadein {self.txt.value()}\n    \n    '
        self.menu()

    def music_play(self):
        global p
        p.stop()
        p = vlc.MediaPlayer(
            f"/music/{music_path[self.comboBox.currentText()][:len(music_path[self.comboBox.currentText()])]}")
        p.play()
        self.play_now = True

    def music_stop(self):
        global p
        p.stop()
        self.play_now = False

    def music_together(self):
        if self.play_now:
            self.music_stop()
            self.music_play()

    def bg_font(self):
        if self.comboBox_2.currentText() == "Катакомбы":
            self.b = bgs[self.comboBox_3.currentText()]
        else:
            self.c = bgs[self.comboBox.currentText()]
            if "int_catacombs_entrance" in self.b or "int_catacombs_hole" in self.b:
                self.b = ''
        if self.c == 'int_' and self.a == "Клубы":
            self.h = self.c + 'clubs_male' + self.b
            oImage = QImage(f"backgrounds/{self.c + 'clubs_male' + self.b}.png")
        else:
            self.h = self.c + bgs[self.a] + self.b
            oImage = QImage(f"backgrounds/{self.c + bgs[self.a] + self.b}.png")
            print(f"backgrounds/{self.c + bgs[self.a] + self.b}.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.with_bg = True

    def bg_none(self):
        oImage = QImage("0.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)

    def bg_false(self):
        self.with_bg = False
        self.bg_none()

    def bg1(self):
        self.b = ''
        self.c = ''
        self.d = ''
        loadUi("tmp/bg_tmp.ui", self)
        self.bg_none()
        shadow = QGraphicsDropShadowEffect(self, blurRadius=20.0, color=QColor("#f0f0f0"), offset=QPointF(0.0, 0.0))
        self.lbl.setGraphicsEffect(shadow)
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox.clear()
        self.comboBox.addItems(
            ['Выберите тип фона', 'Город', 'Совёнок (на улице)', 'Совёнок (внутри зданий)', 'Катакомбы'])
        self.comboBox.currentTextChanged.connect(self.bg_choice)
        self.comboBox_4.currentTextChanged.connect(self.bg_time)
        self.btn_ex.clicked.connect(self.bg_ext)

    def bg_choice(self):
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setGeometry(50, 125, 161, 21)
        self.a = self.comboBox.currentText()
        if self.a == 'Выберите тип фона':
            self.bg1()
        elif self.a == 'Город':
            self.bg_city()
        elif self.a == 'Катакомбы':
            self.bg_cats()
        elif self.a == 'Совёнок (на улице)':
            self.bg_street()
        elif self.a == 'Совёнок (внутри зданий)':
            self.bg_homes()

    def bg_city(self):
        self.bg_none()
        self.comboBox_2.show()
        self.comboBox_4.hide()
        self.comboBox_2.addItems(['Выберите фон', 'Комната Семёна', 'Вид из окна квартиры', 'Автобусная остановка',
                                  'В автобусе (едет в совёнок)'])
        self.comboBox_2.currentTextChanged.connect(self.bg2)
        self.comboBox.currentTextChanged.connect(self.bg_choice)

    def bg_cats(self):
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_2.show()
        self.comboBox_4.hide()
        self.comboBox_2.addItems(['Выберите тип фона', "Дверь/Решётка", "Шахты", "Катакомбы", "Комнаты"])
        self.comboBox_2.currentTextChanged.connect(self.bg_cats2)

    def bg_cats2(self):
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        if self.comboBox_2.currentText() != 'Выберите тип фона':
            self.comboBox_3 = QComboBox(self)
            self.comboBox_3.setGeometry(50, 165, 161, 21)
            self.comboBox_3.show()
            self.comboBox_3.clear()
            self.comboBox_3.addItems(bg2[self.comboBox_2.currentText()])
            self.comboBox_3.currentTextChanged.connect(self.bg2)

    def bg_street(self):
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_2.show()
        self.comboBox_2.clear()
        self.comboBox_2.addItems(
            ['Выберите место', "Домик Ольги Дмитриевны", "Площадь", "Здание столовой", "Крыльцо столовой", "Медпункт",
             "Ворота", "Остановка без автобуса", "Остановка с автобусом", "Клубы", "Музклуб", "Баня", "Пляж",
             "Лодочная станция", "Домик Алисы", "Домик Слави", "Домик Лены", "Домики", "Остров", "Библиотека",
             "Старый лагерь", "Лес", "Тропинка", "Поляна", "Спортплощадка", "Дорога", "Здание сцены", "Перед сценой",
             "Умывальник(и)"])
        self.comboBox_2.currentTextChanged.connect(self.bg_street2)

    def bg_street2(self):
        self.a = self.comboBox_2.currentText()
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_3 = QComboBox(self)
        self.comboBox_3.setGeometry(50, 165, 161, 21)
        self.comboBox_3.show()
        if self.a in bg2:
            asd = bg2[self.a]
        elif self.a in bgs_with_sunset:
            asd = ["Выберите фон", "День", "Рассвет / Закат", "Ночь"]
        else:
            asd = ["Выберите фон", "День", "Ночь"]
        self.comboBox_3.addItems(asd)
        if self.comboBox_3.count() == 1:
            self.bg_homes3()
        self.comboBox_3.currentTextChanged.connect(self.bg_street3)

    def bg_street3(self):
        if self.comboBox_3.currentText() == "Выберите фон":
            self.a = self.a
        elif (self.a == "Остановка без автобуса" or self.a == "Остановка с автобусом") and \
                self.comboBox_3.currentText() == "День":
            self.b = ''
        else:
            self.b = bgs[self.comboBox_3.currentText()]
        self.bg2()

    def bg_homes(self):
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_2.show()
        self.comboBox_2.clear()
        self.comboBox_2.addItems(
            ['Выберите место', "Домик Ольги Дмитриевны", "Столовая", "Медпункт", "Автобус", "Клубы", "Подсобка клубов",
             "Музклуб", "Домик Алисы", "Домик Слави", "Домик Лены", "Библиотека", "Старый лагерь", "Лиаз"])
        self.comboBox_2.currentTextChanged.connect(self.bg_homes2)

    def bg_homes2(self):
        self.a = self.comboBox_2.currentText()
        self.bg_none()
        self.btn.hide()
        self.btn_2.hide()
        self.btn_3.hide()
        self.comboBox_3.hide()
        self.comboBox_4.hide()
        self.comboBox_3 = QComboBox(self)
        self.comboBox_3.setGeometry(50, 165, 161, 21)
        self.comboBox_3.show()
        self.comboBox_3.addItems(bgs2[self.a])
        if self.comboBox_3.count() == 1:
            self.bg_homes3()
        self.comboBox_3.currentTextChanged.connect(self.bg_homes3)

    def bg_homes3(self):
        if self.comboBox_3.currentText() == "Выберите фон":
            self.a = self.a
        elif self.a == "Автобус" and self.comboBox_3.currentText() == "День":
            self.b = ''
        elif self.a == "Лиаз":
            self.b = ''
        elif self.a == "Домик Ольги Дмитриевны" and self.comboBox_3.currentText() == "Ночь без света":
            self.b = '_night2'
        elif self.a == "Библиотека" and self.comboBox_3.currentText() == "Ночь без света":
            self.b = '_night'
        elif self.a == "Библиотека" and self.comboBox_3.currentText() == "Ночь со светом":
            self.b = '_night2'
        else:
            self.b = bgs[self.comboBox_3.currentText()]
        self.bg2()

    def bg2(self):
        if self.comboBox_2.currentText() in bgs:
            self.a = self.comboBox_2.currentText()
        else:
            self.a = self.comboBox_3.currentText()
        if self.sender().currentText() == "Выберите фон" or self.sender().currentText() == " ":
            self.btn.hide()
            self.btn_2.hide()
            self.btn_3.hide()
            self.comboBox_4.hide()
            self.bg_none()
        else:
            if self.with_bg:
                self.bg_font()
            self.btn_2.show()
            self.btn_3.show()
            self.comboBox_4.show()
            if self.comboBox_4.currentText() != "Время появления фона":
                self.btn.show()
        self.btn.clicked.connect(self.bg3)
        self.btn_2.clicked.connect(self.bg_font)
        self.btn_3.clicked.connect(self.bg_false)
        self.comboBox.currentTextChanged.connect(self.bg_choice)

    def bg3(self):
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.command += f"scene bg {self.h} {self.d}\n    \n    "
        self.menu()

    def bg_ext(self):
        self.comboBox_2.hide()
        self.comboBox_3.hide()
        self.menu()

    def bg_time(self):
        if self.comboBox_4.currentText() == "Время появления фона":
            self.btn.hide()
        else:
            self.d = time[self.comboBox_4.currentText()]
            self.btn.show()

    def end(self):
        if not os.path.isdir("mod"):
            os.mkdir("mod")
        with codecs.open(f'mod/{self.name_of_file}.rpy', 'w+', "utf-16") as file:
            file.write(self.mod_start + ''.join(self.all_commands) + 'return')
            exit()


p = vlc.MediaPlayer('')

pers = ['Алиса', 'Славя', 'Лена', 'Ульяна', 'Мику', 'Ольга Дмитриевна', 'Электроник', 'Шурик', 'Женя', 'Виола',
        'Пионер', 'Юля', 'Толик']

persons = {
    'Алиса': 'dv',
    'Виола': 'cs',
    'Электроник': 'el',
    'Мику': 'mi',
    'Ольга Дмитриевна': 'mt',
    'Ольга Дмит.': 'mt',
    'Женя': 'mz',
    'Пионер': 'pi',
    'Шурик': 'sh',
    'Славя': 'sl',
    'Лена': 'un',
    'Ульяна': 'us',
    'Юля': 'uv',
    'Толик': 'tl',
    'Семен': 'me',
    'Семён': 'me',
    'Автор': '',
}

persons_now = {}

emotions = {
    'Не меняется': '',
    'Пионер': '',
    'Обычная': 'normal',
    'Обычный': 'normal',
    'Застенчивая': 'shy',
    'Веселая': 'smile',
    'Веселый': 'smile',
    'Улыбается': 'smile',
    'Злая': 'angry',
    'Злой': 'angry',
    'Плачет': 'cry',
    'Ухмыляется': 'grin',
    'Виноватая': 'guilty',
    'Смеётся': 'laugh',
    'Смеется': 'laugh',
    'В ярости': 'rage',
    'Грустная': 'sad',
    'Грустный': 'sad',
    'Печальная': 'sad',
    'Печальный': 'sad',
    'Испуганная': 'scared',
    'Испуганный': 'scared',
    'Напуганная': 'scared',
    'Напуганный': 'scared',
    'Шокированная': 'shocked',
    'Шокированный': 'shocked',
    'Удивлённая': 'surprise',
    'Удивлённый': 'surprise',
    'Серьёзный': 'serious',
    'Серьёзная': 'serious',
    'Серьезный': 'serious',
    'Серьезная': 'serious',
    'Расстроенный': 'upset',
    'Расстроенная': 'upset',
    'Недовольная': 'dontlike',
    'Недовольный': 'dontlike',
    'Счастлива': 'happy',
    'Счастлив': 'happy',
    'Счастливая': 'happy',
    'Счастливый': 'happy',
    'Спокойная': 'bukal',
    'Спокойный': 'bukal',
    'Нежная': 'tender',
    'Боится': 'fear',
    'Улыбка со слезами': 'cry_smile',
    'Нормально улыбается': 'normal_smile',
    'Улыбается 2': 'smile2',
    'Улыбается 3': 'smile3',
    'Злая 2': 'angry2',
    'Злая улыбка': 'evil_smile',
    'Плачет 2': 'cry2',
    'Смеется 2': 'laugh2',
    'Смеется 3': 'laugh3',
    'Смеётся 2': 'laugh2',
    'Смеётся 3': 'laugh3',
    'Застенчивая 2': 'shy2',
    'Задумалась': 'calml',
    'Удивленная счастливая': 'surp1',
    'Удивленная': 'surp2',
    'Удив. шокированная': 'surp3',
    'Удив. 2': 'surprise2',
    'С синяком': 'fingal'
}

emotions_of_persons = {
    "Виола": ['Обычная', 'Застенчивая', 'Улыбается'],
    "Алиса": ['Обычная', 'Злая', 'Плачет', 'Ухмыляется', 'Виноватая', 'Смеётся', 'В ярости', 'Грустная', 'Испуганная',
              'Шокированная', 'Застенчивая', 'Улыбается', 'Удивлённая'],
    "Славя": ['Обычная', 'Злая', 'Счастлива', 'Смеётся', 'Грустная', 'Напуганная', 'Серьёзная', 'Застенчивая',
              'Улыбается', 'Улыбается 2', 'Удивлённая', 'Нежная'],
    "Электроник": ['Обычный', 'Злой', 'С синяком', 'Ухмыляется', 'Смеётся', 'Грустный', 'Напуганный', 'Серьёзный',
                   'Шокированный', 'Улыбается', 'Удивлённый', 'Расстроенный'],
    "Мику": ['Обычная', 'Злая', 'Плачет', 'Улыбка со слезами', 'Недовольная', 'Ухмыляется', 'Счастлива', 'Смеётся',
             'В ярости', 'Грустная', 'Испуганная', 'Серьёзная', 'Шокированная', 'Застенчивая', 'Улыбается'],
    "Ольга Дмитриевна": ['Обычная', 'Злая', 'Ухмыляется', 'Смеётся', 'В ярости', 'Грустная', 'Испуганная',
                         'Шокированная', 'Улыбается', 'Удивлённая'],
    "Женя": ['Обычная', 'Злая', 'Спокойная', 'Смеётся', 'В ярости', 'застенчивая', 'Улыбается'],
    "Шурик": ['Обычный', 'Смеётся', 'Улыбается', 'Нормально улыбается', 'В ярости', 'Напуганный', 'Серьёзный',
              'Удивлённый', 'Расстроенный'],
    "Лена": ['Обычная', 'Злая', 'Злая 2', 'Плачет', 'Смеётся', 'В ярости', 'Грустная', 'Напуганная', 'Серьёзная',
             'Шокированная', 'Застенчивая', 'Улыбается', 'Улыбается 2', 'Улыбается 3', 'Улыбка со слезами',
             'Злая улыбка', 'Удивлённая'],
    "Ульяна": ['Обычная', 'Злая', 'Плачет', 'Плачет 2', 'Недовольная', 'Боится', 'Ухмыляется', 'Смеётся', 'Смеётся 2',
               'Грустная', 'Застенчивая', 'Застенчивая 2', 'Улыбается', 'Задумалась', 'Счастливая',
               'Удивленная', 'Удив. шокированная', 'Расстроенная'],
    "Юля": ['Обычная', 'Недовольная', 'Ухмыляется', 'Виноватая', 'Смеётся', 'В ярости', 'Грустная', 'Шокированная',
            'Улыбается', 'Удивлённая', 'Удив. 2', 'Расстроенная'],
    "Толик": ['Обычный', 'В ярости'],
    "Пионер": ['Обычный', 'Улыбается']
}

clothes = {
    'Не меняется': '',
    'Халат': '',
    'С очками': 'glasses',
    'С тетоскопом': 'stethoscope',
    'Форма': 'pioneer',
    'Завязанной форма': 'pioneer2',
    'Купальник': 'swim',
    'Форма с панамой': 'panama pioneer',
    'Платье': 'dress',
    'Платье с панамой': 'panama dress',
    'Купальник с панамой': 'panama swim',
    'Форма с очками': 'pioneer glasses',
    'Форма без очков': 'pioneer',
    'Спортивная форма': 'sport',
    'Голая': 'body',
}

clothes_of_persons = {
    'cs': ['Халат', 'С очками', 'С тетоскопом'],
    'dv': ['Форма', 'Завязанной форма', 'Купальник', 'Голая'],
    'mi': ['Форма', 'Купальник'],
    'mt': ['Форма', 'Форма с панамой', 'Платье', 'Платье с панамой', 'Купальник', 'Купальник с панамой'],
    'mz': ['Форма с очками', 'Форма без очков'],
    'sl': ['Форма', 'Спортивная форма', 'Купальник', 'Платье'],
    'un': ['Форма', 'Спортивная форма', 'Купальник', 'Платье', 'Голая'],
    'us': ['Форма', 'Спортивная форма', 'Купальник', 'Платье']
}

position = {
    'Не меняется': '',
    'Средне': '',
    'Далеко': ' far',
    'Близко': ' close',
    'По центру': '',
    'Слева': ' at left',
    'Немного левее': ' at cleft',
    'Справа': ' at right',
    'Немного правее': ' at cright',
}

time = {
    '0 с.': '',
    '1 с.': ' with dissolve',
    '0.2 с.': ' with dspr',
    '0 с': '',
    '1 с': ' with dissolve',
    '0.2 с': ' with dspr',
}

music_path = {
    '410': '410.mp3',
    'A promice from distant days': 'a_promise_from_distant_days.mp3',
    'A promise from distant days V2': 'a_promise_from_distant_days_v2.mp3',
    'Afterword': 'afterword.mp3',
    'Always ready': 'always_ready.mp3',
    'Awakening power': 'awakening_power.mp3',
    'Blow with the fires': 'blow_with_the_fires.mp3',
    'Confession oboe': 'confession_oboe.mp3',
    'Dance of fireflies': 'dance_of_fireflies.mp3',
    'Doomed to be defeated': 'doomed_to_be_defeated.mp3',
    'Door to nightmare': 'door_to_nightmare.mp3',
    'Drown': 'drown.mp3',
    'Eat some trouble': 'eat_some_trouble.mp3',
    'Eternal longing': 'eternal_longing.mp3',
    'Everlasting summer': 'everlasting_summer.mp3',
    'Feeling Good': 'everyday_theme.mp3',
    'Faceless': 'faceless.mp3',
    'Farewell to the past (короткая вер.)': 'farewell_to_the_past_edit.mp3',
    'Farewell to the past (полная вер.)': 'farewell_to_the_past_full.mp3',
    'Forest maiden': 'forest_maiden.mp3',
    'Gentle predator': 'gentle_predator.mp3',
    'Get to know me better': 'get_to_know_me_better.mp3',
    'Glimmering coals': 'glimmering_coals.mp3',
    'Goodbye home shores': 'goodbye_home_shores.mp3',
    'Heather': 'heather.mp3',
    'I dont blame you': 'i_dont_blame_you.mp3',
    'I want to play': 'i_want_to_play.mp3',
    'Into the unknown': 'into_the_unknown.mp3',
    'Just think': 'just_think.mp3',
    "Let's be friends": 'lets_be_friends.mp3',
    'Lightness': 'lightness.mp3',
    'Lightness (радио вер.)': 'lightness_radio_bus.mp3',
    'Meet me there': 'meet_me_there.mp3',
    'Memories': 'memories.mp3',
    'Memories (пиано вер.)': 'memories_piano_outdoors.mp3',
    'Песня Мику на флейте': 'miku_song_flute.mp3',
    'Песня Мику с голосом': 'miku_song_voice.mp3',
    'My daily life': 'my_daily_life.mp3',
    'Mystery girl': 'mystery_girl_v2.mp3',
    'No tresspassing': 'no_tresspassing.mp3',
    'Opening': 'opening.mp3',
    'Orchid': 'orchid.mp3',
    'Pile': 'pile.mp3',
    'Raindrops': 'raindrops.mp3',
    'Reflection on water': 'reflection_on_water.mp3',
    'Reminiscences': 'reminiscences.mp3',
    'Revenga': 'revenga.mp3',
    'Scarytale': 'scarytale.mp3',
    'She is kind': 'she_is_kind.mp3',
    'Silhouette in sunset': 'silhouette_in_sunset.mp3',
    'Smooth machine': 'smooth_machine.mp3',
    'So good to be careless': 'so_good_to_be_careless.mp3',
    'Sparkles': 'sparkles.mp3',
    'Sunny day': 'sunny_day.mp3',
    'Sweet darkness': 'sweet_darkness.mp3',
    'Take me beautifully': 'take_me_beautifully.mp3',
    "That's our madhouse": 'that_s_our_madhouse.mp3',
    'Timid girl': 'timid_girl.mp3',
    'Torture': 'torture.mp3',
    'Trapped in dreams': 'trapped_in_dreams.mp3',
    'Tried to bring it back': 'tried_to_bring_it_back.mp3',
    'Two glasses of melancholy': 'two_glasses_of_melancholy.mp3',
    'Waltz of doubts': 'waltz_of_doubts.mp3',
    'Went fishing caught a girl': 'went_fishing_caught_a_girl.mp3',
    'What do you think of me': 'what_do_you_think_of_me.mp3',
    'You lost me': 'you_lost_me.mp3',
    "You won't let me down": 'you_won_t_let_me_down.mp3',
    'Your bright side': 'your_bright_side.mp3'
}

bgs = {
    'Автобусная остановка': 'bus_stop',
    'В автобусе (едет в совёнок)': 'intro_xx',
    'Комната Семёна': 'semen_room',
    'Вид из окна квартиры': 'semen_room_window',
    "Дверь в катакомбах": 'int_catacombs_door',
    "Дверь в шахте": 'int_mine_door',
    "Решётка (выход на площадь)": 'int_mine_exit_night_nolight',
    "Решётка с фонариком": 'int_mine_exit_night_light',
    "Решётка с факелом": 'int_mine_exit_night_torch',
    "Шахта": 'int_mine',
    "Пещера": 'int_mine_coalface',
    "Развилка": 'int_mine_crossroad',
    "Поворот направо": 'int_mine_halt',
    "Коридор": 'int_catacombs_entrance',
    "Коридор с красным светом": 'int_catacombs_entrance_red',
    "Дыра в катакомбах": 'int_catacombs_hole',
    "Бункер": 'int_catacombs_living',
    "Бункер с упавшей дверью": 'int_catacombs_living_nodoor',
    "Комната в шахте": 'int_mine_room',
    "Комната с красным светом": 'int_mine_room_red',
    "Домик Ольги Дмитриевны": 'house_of_mt',
    "Площадь": 'square',
    "Столовая": 'dining_hall',
    "Здание столовой": 'dining_hall_away',
    "Крыльцо столовой": 'dining_hall_near',
    "Медпункт": 'aidpost',
    "Ворота": 'camp_entrance',
    "Остановка без автобуса": 'no_bus',
    "Остановка с автобусом": 'bus',
    "Автобус": 'bus',
    "Клубы": 'clubs',
    "Музклуб": 'musclub',
    "Баня": 'bathhouse',
    "Пляж": 'beach',
    "Лодочная станция": 'boathouse',
    "Домик Алисы": 'house_of_dv',
    "Домик Слави": 'house_of_sl',
    "Домик Лены": 'house_of_un',
    "Домики": 'houses',
    "Остров": 'island',
    "Библиотека": 'library',
    "Старый лагерь": 'old_building',
    "Лес": 'path2',
    "Тропинка": 'path',
    "Поляна": 'polyana',
    "Спортплощадка": 'playground',
    "Дорога": 'road',
    "Здание сцены": 'stage_big',
    "Перед сценой": 'stage_normal',
    "Умывальник(и)": 'washstand',
    "День с яблоком": "_day_apple",
    "День": "_day",
    "День с людьми": "_people_day",
    "Ночь с людьми": "_people_night",
    "Ночь": "_night",
    "Рассвет / Закат": "_sunset",
    "Ночь со светом": "_night",
    "Ночь со светом без фонарика": "_noitem_night",
    "Ночь без света": "_night_without_light",
    "Ночь в лунном свете": "_night_moonlight",
    "Ночь с городом": "_night",
    "Ночь без города": "_night2",
    "Ночь с тенями": "_black",
    "День с городом": "_day_city",
    "Ночь вечеринка": "_night_party",
    "Ночь после вечеринки": "_night_party2",
    "Умывальник": "2_day",
    "Умывальники": "_day",
    "Лиаз": "liaz",
    "Со светом": "_night",
    "Без света": "_night_nolight",
    "Подсобка клубов": "clubs_male2",
    "Совёнок (на улице)": "ext_",
    "Совёнок (внутри зданий)": "int_",
    "Город": "",
    "Катакомбы": "",
}

bgs_with_sunset = ['Пляж', 'Здание столовой', 'Крыльцо столовой', 'Домик Ольги Дмитриевны', 'Остановка без автобуса',
                   'Остановка c автобусом', 'Тропинка', 'Поляна']

bgs2 = {
    "Домик Ольги Дмитриевны": ["Выберите фон", "День", "Рассвет / Закат", "Ночь без света", "Ночь со светом",
                               "Ночь со светом без фонарика"],
    "Столовая": ["Выберите фон", "День", "День с людьми", "Рассвет / Закат", "Ночь"],
    "Медпункт": ["Выберите фон", "День", "День с яблоком", "Ночь"],
    "Автобус": ["Выберите фон", "День", "День с людьми", "Ночь", "Ночь с людьми", "Ночь с тенями"],
    "Клубы": ["Выберите фон", "День", "Рассвет / Закат"],
    "Подсобка клубов": ["Выберите фон", "Со светом", "Без света"],
    "Музклуб": ["День"],
    "Домик Алисы": ["Выберите фон", "День", "Ночь"],
    "Домик Слави": ["День"],
    "Домик Лены": ["Выберите фон", "День", "Ночь"],
    "Библиотека": ["Выберите фон", "День", "Ночь без света", "Ночь со светом"],
    "Старый лагерь": ["Ночь"],
    "Лиаз": ["Ночь"],
}

music = ['410', 'A promice from distant days', 'A promise from distant days V2', 'Afterword', 'Always ready',
         'Awakening power', 'Blow with the fires', 'Confession oboe', 'Dance of fireflies', 'Doomed to be defeated',
         'Door to nightmare', 'Drown', 'Eat some trouble', 'Eternal longing', 'Everlasting summer', 'Feeling Good',
         'Faceless', 'Farewell to the past (короткая вер.)', 'Farewell to the past (полная вер.)', 'Forest maiden',
         'Gentle predator', 'Get to know me better', 'Glimmering coals', 'Goodbye home shores', 'Heather',
         'I dont blame you', 'I want to play', 'Into the unknown', 'Just think', "Let's be friends", 'Lightness',
         'Meet me there', 'Memories', 'Memories (пиано вер.)', 'Песня Мику на флейте', 'Песня Мику с голосом',
         'My daily life', 'Mystery girl', 'No tresspassing', 'Opening', 'Orchid', 'Pile', 'Raindrops',
         'Reflection on water', 'Reminiscences', 'Revenga', 'Scarytale', 'She is kind', 'Silhouette in sunset',
         'Smooth machine', 'So good to be careless', 'Sparkles', 'Sunny day', 'Sweet darkness', 'Take me beautifully',
         "That's our madhouse", 'Timid girl', 'Torture', 'Trapped in dreams', 'Tried to bring it back',
         'Two glasses of melancholy', 'Waltz of doubts', 'Went fishing caught a girl', 'What do you think of me',
         'You lost me', "You won't let me down", 'Your bright side']

bg2 = {
    "Дверь/Решётка": ["Выберите фон", "Дверь в катакомбах", "Дверь в шахте", "Решётка (выход на площадь)",
                      "Решётка с фонариком", "Решётка с факелом"],
    "Шахты": ["Выберите фон", "Шахта", "Пещера", "Развилка", "Поворот направо"],
    "Катакомбы": ["Выберите фон", "Коридор", "Коридор с красным светом", "Дыра в катакомбах"],
    "Комнаты": ["Выберите фон", "Бункер", "Бункер с упавшей дверью", "Комната в шахте", "Комната с красным светом"],
    "Домик Ольги Дмитриевны": ["Выберите фон", "День", "Рассвет / Закат", "Ночь со светом", "Ночь без света"],
    "Домики": ["Выберите фон", "День", "Рассвет / Закат"],
    "Старый лагерь": ["Выберите фон", "Ночь", "Ночь в лунном свете"],
    "Дорога": ["Выберите фон", "День", "Рассвет / Закат", "Ночь без города", "Ночь с городом"],
    "Площадь": ["Выберите фон", "День", "День с городом", "Рассвет / Закат", "Ночь", "Ночь вечеринка",
                "Ночь после вечеринки"],
    "Умывальник(и)": ["Выберите фон", "Умывальник", "Умывальники"],
    "Здание сцены": ["Ночь"],
    "Домик Слави": ["День"],
    "Домик Лены": ["День"],
    "Музклуб": ["День"],
    "Баня": ["Ночь"]
}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
