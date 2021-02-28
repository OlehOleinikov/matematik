import sys
from gui.gui import *
from gui.gui_settings import Ui_Form
from gui.gui_import_folder import *


from config.config_math import config_get_value, config_set_item, config_save, config_load, config_swipe

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.Qt import QProxyStyle, QStyle
from PyQt5.QtWidgets import QStyleFactory


import colorama
from converter.convert_engine import *
from converter.terminal_messages import *
from analyst.analyst_engine import analysis_type_a
from tqdm import tqdm

import qtmodern.styles
import qtmodern.windows


prog_execute_stage = 0  # етапи програми для відображення активності елементів (до перегону, після перегону), глобальна
supported_types = ('.xls', '.xlsx', '.xml', '.txt', '.csv', '.txt', '.dec')
# Змінна списку файлів, обраних користувачем для опрацювання, з їх властивостями:
# (містить список списків для подальшої роботи з конвертування таблиць, їх розпізнання та експорту -
# 0) повний шлях з найменуванням файлу
# 1) найменування файлу з розширенням
# 2) розмір файлу у строковому форматі "{%d} Kb"
# 3) "відбиток" файлу, що являє строку "{найменування з розширенням[1]} + " " + {розмір[2]}" для перевірки повторного
# додавання файлу до списку (наприклад дублікат файлу з іншої директорії)

# Наступні елементи списку додаються за результатами опрацювання файлів:
# 4) кількість виявлених записів, що будуть включені до експорту
# 5) розпізнано колонок
# 6) виявлено колонок
# 7) потрійний запис абонентів (необхідність визначення дійсного абонента Б)
# 8) необхідність підключення зовнішній довідників БС (відсутність розшифрування адрес БС)
# 9) необхідність розділення АБ (АБ тип - наявні відомості про ІМЕІ та/або місцезнаходження Б)
# 10) розпізнано типів
# 11) виявлено типів
# 12) абонентів А унікальних у файлі
# 13) абонентів Б унікальних у файлі
# 14) ІМЕІ А унікальних у файлі
# 15) ІМЕІ Б унікальних у файлі (для АБ деталізацій, в інших випадках - 0)
# 16) унікальних територіальних зон LAC
# 17) унікальних базових станцій LAC+Cid
# 18) унікальних базових станцій LAC+Cid, які мають розшифрування адреси БС (для КС після опрацювання довідником)
# 19) лог опрацювання файлу для відображення у вікні результатів
availible_sheets_list = []

# Заголовки колонок відображення обраних до опрацювання файлів (для використання у моделі даних Qt):
input_files_default_headers_set = ['Шлях', 'Файл', 'Розмір', 'Відбиток', 'Записів', 'Колонок', 'Типів',
                                   'Абонентів А/Б', 'IMEI', 'Зон/антен', 'Визначений тип']

# Консольні функції (підлягають видаленню після переходу на GUI)
colorama.init()
print_logo()


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------ХЕНДЛЕР ПОДІЙ---------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class HandlerMain(QObject):
    signal_update_statusbar = pyqtSignal()


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------МОДЕЛЬ ТАБЛИЦІ КОНВЕРТЕРУ---------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ModelSheetsListView(QtCore.QAbstractTableModel):
    def __init__(self, parent, columns_headers, input_data):
        QtCore.QAbstractTableModel.__init__(self)
        self.gui = parent
        for row in input_data:  # додавання порожніх клітинок для уникнення помилки IndexError при відображенні
            if len(row) < len(columns_headers):
                while len(row) < len(columns_headers):
                    row.append("-")
        self.colLabels = columns_headers
        self.cached = input_data

    def rowCount(self, parent):
        return len(self.cached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return QtCore.QVariant()
        value = ''
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.cached[row][col]
        return QtCore.QVariant(value)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.colLabels[section])
        return QtCore.QVariant()


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------ГОЛОВНЕ ВІКНО MainWinMatematik----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class MainWinMatematik(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage('Програму завантажено', 5000)
        #

        # ---------------------------------Початкова активність елементів(віджетів):-----------------------------------
        # Активність елементів в залежності від етапу виконнаня програми (підготовка до перегону/ робота з опрацьованими
        # файлами) - залежить від статусу змінної prog_execute_stage:
        self.ui.btn_excel_save.setDisabled(True)
        self.ui.groupBox_3.setDisabled(True)
        self.ui.groupBox_4.setDisabled(True)
        self.ui.btn_sheet_remove.setEnabled(False)  # кнопка активується якщо є виділені рядки списку файлів
        #

        # -----------------------------------Підключення ТАБЛИЦІ конвертеру:-------------------------------------------
        # Підготовка форми таблиці для файлів обраних користувачем (для правильного відображення у віджеті
        # tableView необхідно підготувати форму даних за допомогою класу QAbstractTableModel):
        self.widget_sheets_table_view = self.ui.tableView_import_files_list  # змінна безпосередньо віджету
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view, input_files_default_headers_set,
                                                      availible_sheets_list)  # об'єкт моделі даних
        self.widget_sheets_table_view.setModel(self.sheets_view_object)  # застосування моделі до віджету
        # мінімізація висоти рядків:
        tv_vertical_header_setting = self.widget_sheets_table_view.verticalHeader()
        tv_vertical_header_setting.setDefaultSectionSize(10)
        tv_vertical_header_setting.sectionResizeMode(QtWidgets.QSizePolicy.Fixed)
        # розтягування заголовків колонок відповідно ширини вікна таблиці (список файлів до опрацювання)
        self.widget_sheets_table_view.horizontalHeader().setStretchLastSection(True)
        #

        # -------------------------------------Підключення КНОПОК КОНВЕРТЕРУ--------------------------------------------
        # Кнопки роботи зі списком файлів, що готуються до завантаження:
        # Додати файли:
        self.ui.btn_sheet_add.clicked.connect(self.add_sheet_dialog)
        # Очистити список файлів для опрацювання:
        self.ui.btn_sheet_clear_list.clicked.connect(self.clear_sheets_list)
        # Активувати кнопку видалення, якщо файл виділено в таблиці
        self.widget_sheets_table_view.clicked.connect(self.remove_btn_update)
        # Видалити виділений файл з таблиці (також видаляється з availible_sheets_list)
        self.ui.btn_sheet_remove.clicked.connect(self.remove_sheet_from_list)
        # Відкрити вікно налаштувань
        self.ui.btn_settings_win.clicked.connect(self.open_modalwin_settings)
        # Завантажити список з типової папки імпорту
        self.ui.btn_sheet_import_def_dir.clicked.connect(self.add_sheet_folder_default)
        #

    # -----------------------------------------методи ВІДКРИТТЯ ВІКОН --------------------------------------------------
    def open_modalwin_settings(self):
        window = SettingsWindow(self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        window.setWindowFlags(flags)
        window.show()

    def open_modalwin_import_folder(self):
        mw = ChooseImportFolder(self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        mw.setWindowFlags(flags)
        mw.show()
        #

    # --------------------------------------методи КНОПОК конвертеру --------------------------------------------------
    def remove_btn_update(self):  # активність кнопки видалення залежно від наявності виділеного рядку
        if self.widget_sheets_table_view.selectionModel().hasSelection():
            self.ui.btn_sheet_remove.setEnabled(True)
        else:
            self.ui.btn_sheet_remove.setEnabled(False)

    def remove_sheet_from_list(self):  # видалення інформації з таблиці обраних файлів (тільки до перегону)
        global availible_sheets_list
        if prog_execute_stage == 0 and self.widget_sheets_table_view.selectionModel().hasSelection():
            index = (self.widget_sheets_table_view.selectionModel().currentIndex())
            number_to_remove = index.row()
            if len(availible_sheets_list) > number_to_remove:
                availible_sheets_list.pop(number_to_remove)
                self.update_sheets_list()
                self.ui.btn_sheet_remove.setEnabled(False)

    def update_sheets_list(self):  # оновлення таблиці для відображення (коли змінюється availible_sheets_list)
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view,
                                                      input_files_default_headers_set, availible_sheets_list)
        self.widget_sheets_table_view.setModel(self.sheets_view_object)
        self.widget_sheets_table_view.update()
        # self.widget_sheets_table_view.resizeColumnToContents(1)
        # self.widget_sheets_table_view.resizeColumnToContents(0)
        # self.widget_sheets_table_view.resizeColumnToContents(2)

    # Вікно додавання файлів для опрацювання (деталізації абонентів або моніторингу). Отримує список обраних файлів
    # визначає їх розмір та перевіряє чи вже не доданий кожен з файлів раніше. Після перевірки додає відомсоті про файл
    # в змінну (список списків) availible_sheets_list:
    def add_sheet_dialog(self):
        global availible_sheets_list
        incoming_sheets_list = availible_sheets_list
        user_added_sheets_list = QtWidgets.QFileDialog.getOpenFileNames(self, 'Додати таблиці для опрацювання', '',
                                                                        'Файли деталізацій '
                                                                        '(*.xls *.xlsx *.xml *.csv *.txt *.dec)')
        for file in user_added_sheets_list[0]:
            print(file)
            file_path = file
            print(file)
            file_size = str(round(os.path.getsize(file) / 1024.0)) + ' Kb'
            file_name = os.path.basename(file)
            file_footprint = str(file_name) + str(file_size)
            if file_footprint in [results[3] for results in incoming_sheets_list]:
                pass
            else:
                incoming_sheets_list.append([file_path, file_name, file_size, file_footprint])
        availible_sheets_list = incoming_sheets_list
        print(incoming_sheets_list)
        self.update_sheets_list()
        # У вкладений список sheets_list_prepared додаємо файли, які обрав користувач, та яких ще немає у списку,
        # перевірка на повторення через file_footprint (назва файлу з його розміром)

    def clear_sheets_list(self):
        global availible_sheets_list
        availible_sheets_list = []
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view, input_files_default_headers_set,
                                                      availible_sheets_list)
        self.widget_sheets_table_view.setModel(self.sheets_view_object)
        self.ui.btn_sheet_remove.setEnabled(False)

    def add_sheet_folder_default(self):
        global availible_sheets_list
        new_sheets_list = availible_sheets_list
        current_folder = config_get_value('import_folder_default', 'path')
        print('getting def path ' + current_folder)
        file_list = []
        if current_folder != '':
            for item in os.listdir(current_folder):
                if item.endswith(supported_types):
                    file_list.append(item)
        else:
            self.open_modalwin_import_folder()
        if file_list is not []:
            for file in file_list:
                file_path = str(current_folder+'/'+file)
                file_size = str(round(os.path.getsize(file_path) / 1024.0)) + ' Kb'
                file_footprint = str(file) + str(file_size)
                if file_footprint in [results[3] for results in new_sheets_list]:
                    pass
                else:
                    new_sheets_list.append([file_path, file, file_size, file_footprint])
            availible_sheets_list = new_sheets_list
            print(new_sheets_list)
            self.update_sheets_list()


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------ВІКНО НАЛАШТУВАНЬ SETTINGS--------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, parent=MainWinMatematik):
        super().__init__(parent, QtCore.Qt.Window)
        self.open_modalwin_settings = Ui_Form()
        self.open_modalwin_settings.setupUi(self)
        self.setWindowModality(2)
        self.open_modalwin_settings.label_import_dir_default.setText(config_get_value('import_folder_default', 'path'))
        self.open_modalwin_settings.btn_config_swipe.clicked.connect(config_swipe)
        self.open_modalwin_settings.btn_config_load.clicked.connect(self.choose_file_load_config)
        self.open_modalwin_settings.btn_config_save.clicked.connect(self.choose_file_save_config)
        self.open_modalwin_settings.btn_set_dir_import_default.clicked.connect(self.choose_import_dir_default)
        self.open_modalwin_settings.btn_setup_cancel.clicked.connect(self.settings_win_close_without_save)
        self.open_modalwin_settings.btn_setup_ok.clicked.connect(self.settings_win_close_save_settings)
        self.open_modalwin_settings.btn_setup_accept.setEnabled(True)
        self.open_modalwin_settings.btn_setup_accept.clicked.connect(self.accept_changes_settings)

    def choose_file_load_config(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Завантаження налаштувань', '', 'Файл конфігурації (*.ini)')
        if file[0] != '' and file[0].lower().endswith('.ini'):
            config_load(file[0])

    def choose_file_save_config(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, 'Збереження налаштувань', '', 'Файл конфігурації (*.ini)')
        if file[0] != '':
            config_save(file[0])

    def choose_import_dir_default(self):
        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Обрати папку для швидкого завантаження файлів')
        if new_dir != '':
            config_set_item('import_folder_default', 'path', new_dir)
        self.open_modalwin_settings.label_import_dir_default.setText(config_get_value('import_folder_default', 'path'))

    def settings_win_close_without_save(self):
        config_load('config\\config.ini')
        print('Settings closed without save')
        self.close()

    def settings_win_close_save_settings(self):
        config_save('config\\config.ini')
        print('Settings closed and changes saved')
        self.close()

    def accept_changes_settings(self):
        config_save('config\\config.ini')
        print('Changes accepted and save to config')
        #


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------Вікно ВИБОРУ типової папки імпорту------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ChooseImportFolder(QtWidgets.QWidget):
    def __init__(self, parent=MainWinMatematik):
        super().__init__(parent, QtCore.Qt.Window)
        self.win_set_IF = Ui_modal_win_choose_import_folder()
        self.win_set_IF.setupUi(self)
        self.setWindowModality(2)
        self.win_set_IF.btn_cancel_import_folder_choose.clicked.connect(self.close)
        self.win_set_IF.btn_set_import_folder.clicked.connect(self.set_new_default_import_folder)

    def set_new_default_import_folder(self):
        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Обрати папку для швидкого завантаження файлів')
        if new_dir != '':
            config_set_item('import_folder_default', 'path', new_dir)
        self.close()
        #


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------ВИКОНАННЯ ПРОГРАМИ------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    myapp = qtmodern.windows.ModernWindow(MainWinMatematik())
    myapp.show()
    sys.exit(app.exec_())




''' 
scan_directory()  # collect all data files and get configuration dictionaries

# CHECK FOR KYIVSTAR VOC:
scan_bs_voc()  # harvest address and azimuth voc (KyivStar separated tabs)

# PRECHECK FILES:
files_preview()

# MAIN CONVERT FUNCTION:
burning()

# SAVE HEAP RESULT:
save_heap()

# DIVIDE BY SUBSCRIBERS FILES:
save_divide_by_subscribers()

# COMBINE A & B TYPE (MERGE):
merge_types()

a_list = get_a_subscribers_list()
ab_list = get_merged_subscribers_list()
for subscriber in tqdm(a_list):
    df = export_subscriber_a_tab(subscriber)
    analysis_type_a(df, subscriber)

# FINISH
print("second try")
print('commit test')
print('commit test2')
print_the_end()
'''