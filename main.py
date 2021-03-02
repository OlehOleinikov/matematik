import sys
from gui.gui import *
from gui.gui_settings import Ui_Form
from gui.gui_import_folder import *


from config.config_math import config_get_value, config_set_item, config_save, config_load, config_swipe, \
    config_get_options, config_remove_item

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QEvent
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
class HandlerFirst(QObject):
    signal_update_statusbar = pyqtSignal(str)
    signal_settings_changed = pyqtSignal()


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

        self.win_settings = SettingsWindow()
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
        self.ui.btn_settings_win.clicked.connect(self.win_settings.update_settings_gui)
        self.ui.btn_settings_win.clicked.connect(self.open_modalwin_settings)
        # Завантажити список з типової папки імпорту
        self.ui.btn_sheet_import_def_dir.clicked.connect(self.add_sheet_folder_default)
        # Сигнал оновлення статусбару:
        self.win_settings.signal.signal_update_statusbar.connect(self.print_statusbar)
        #

    # -----------------------------------------методи ВІДКРИТТЯ ВІКОН --------------------------------------------------
    def open_modalwin_settings(self):
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.win_settings.setWindowFlags(flags)
        self.win_settings.show()

    def open_modalwin_import_folder(self):
        mw = ChooseImportFolder(self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        mw.setWindowFlags(flags)
        mw.show()

    def print_statusbar(self, text):
        self.ui.statusbar.showMessage(str(text), 5000)

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
    def __init__(self, parent=MainWinMatematik):  # втрачається центрування до батьківського вікна
        QtWidgets.QWidget.__init__(self)
        # super().__init__()
        self.open_modalwin_settings = Ui_Form()
        self.open_modalwin_settings.setupUi(self)
        self.setWindowModality(2)
        self.signal = HandlerFirst()
        self.open_modalwin_settings.label_import_dir_default.setText(config_get_value('import_folder_default', 'path'))
        self.open_modalwin_settings.btn_config_swipe.clicked.connect(self.swipe_to_factory)
        self.open_modalwin_settings.btn_config_load.clicked.connect(self.choose_file_load_config)
        self.open_modalwin_settings.btn_config_save.clicked.connect(self.choose_file_save_config)
        self.open_modalwin_settings.btn_set_dir_import_default.clicked.connect(self.choose_import_dir_default)
        self.open_modalwin_settings.btn_setup_cancel.clicked.connect(self.settings_win_close_without_save)
        self.open_modalwin_settings.btn_setup_ok.clicked.connect(self.settings_win_close_save_settings)
        self.open_modalwin_settings.btn_setup_accept.setEnabled(True)
        self.open_modalwin_settings.btn_setup_accept.clicked.connect(self.accept_changes_settings)
        self.signal.signal_settings_changed.connect(self.update_settings_gui)

        self.open_modalwin_settings.btn_add_voice_in.setEnabled(False)
        self.open_modalwin_settings.btn_remove_voice_in.setEnabled(False)
        self.open_modalwin_settings.btn_remove_voice_in.clicked.connect(self.remove_voice_in_item)
        self.open_modalwin_settings.btn_add_voice_in.clicked.connect(self.add_item_voice_in)
        self.open_modalwin_settings.listView_voice_in.clicked.connect(self.upd_btn_remove_voice_in)

        self.open_modalwin_settings.lineEdit_add_voice_in.textChanged.connect(self.upd_btn_add_voice_in)
        #---------------------Завантаження даних про вихідні типи (підпис у результуючій таблиці)-----------------------
        self.open_modalwin_settings.lineEdit_exportname_voice_in.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'voice_in', str(x)))


        self.open_modalwin_settings.lineEdit_exportname_voice_out.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'voice_out', str(x)))
        self.open_modalwin_settings.lineEdit_exportname_message_in.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'message_in', str(x)))
        self.open_modalwin_settings.lineEdit_exportname_message_out.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'message_out', str(x)))
        self.open_modalwin_settings.lineEdit_exportname_network.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'network', str(x)))
        self.open_modalwin_settings.lineEdit_exportname_forwarding.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'forwarding', str(x)))
        self.open_modalwin_settings.lineEdit_exportname_unknowntypes.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'unknown', str(x)))

        # -------------------------Завантаження типів для розпізнання у вхідних таблицях--------------------------------
        self.model_voice_in = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_voice_in.setModel(self.model_voice_in)
        voice_in_types = config_get_options('types_dict_voice_in')
        for i in voice_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_voice_in.appendRow(item)
        self.sel_model_voice_in = self.open_modalwin_settings.listView_voice_in.selectionModel()
        self.sel_model_voice_in.selectionChanged.connect(self.upd_btn_remove_voice_in)


        model_voice_out = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_voice_out.setModel(model_voice_out)
        voice_out_types = config_get_options('types_dict_voice_out')
        for i in voice_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                model_voice_out.appendRow(item)

        model_message_out = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_message_out.setModel(model_message_out)
        message_out_types = config_get_options('types_dict_message_out')
        for i in message_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                model_message_out.appendRow(item)

        model_message_in = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_message_in.setModel(model_message_in)
        message_in_types = config_get_options('types_dict_message_in')
        for i in message_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                model_message_in.appendRow(item)

        model_network = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_network.setModel(model_network)
        network_types = config_get_options('types_dict_network')
        for i in network_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                model_network.appendRow(item)

        model_forwarding = QtGui.QStandardItemModel()
        self.open_modalwin_settings.listView_forwarding.setModel(model_forwarding)
        forwarding_types = config_get_options('types_dict_forwarding')
        for i in forwarding_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                model_forwarding.appendRow(item)

    def upd_btn_remove_voice_in(self):
        if self.sel_model_voice_in.hasSelection():
            self.open_modalwin_settings.btn_remove_voice_in.setEnabled(True)
        else:
            self.open_modalwin_settings.btn_remove_voice_in.setEnabled(False)

    def upd_btn_add_voice_in(self):
        if self.open_modalwin_settings.lineEdit_add_voice_in.text() != '':
            self.open_modalwin_settings.btn_add_voice_in.setEnabled(True)
        else:
            self.open_modalwin_settings.btn_add_voice_in.setEnabled(False)

    def upd_list_voice_in(self):
        self.model_voice_in.clear()
        voice_in_types = config_get_options('types_dict_voice_in')
        for i in voice_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_voice_in.appendRow(item)

    def remove_voice_in_item(self):
        if self.sel_model_voice_in.hasSelection():
            index = self.sel_model_voice_in.currentIndex()
            text = index.data()
            row = index.row()
            print(row)
            config_remove_item('types_dict_voice_in', str(text))
            self.model_voice_in.removeRow(row)
            self.sel_model_voice_in.clearSelection()

    def add_item_voice_in(self):
        if self.open_modalwin_settings.lineEdit_add_voice_in.text() != '':
            config_set_item('types_dict_voice_in', str(self.open_modalwin_settings.lineEdit_add_voice_in.text()), str('True'))
            self.open_modalwin_settings.lineEdit_add_voice_in.clear()
            self.upd_list_voice_in()


    def swipe_to_factory(self):
        config_swipe()
        self.signal.signal_settings_changed.emit()
        text = 'Налаштування програми СКИНУТО ДО ПОЧАТКОВИХ'
        self.signal.signal_update_statusbar.emit(text)

    def choose_file_load_config(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Завантаження налаштувань', '', 'Файл конфігурації (*.ini)')
        if file[0] != '' and file[0].lower().endswith('.ini'):
            config_load(file[0])
            text = 'Налаштування програми завантажено з файлу: ' + str(file[0])
            self.signal.signal_update_statusbar.emit(text)
            self.signal.signal_settings_changed.emit()

    def choose_file_save_config(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, 'Збереження налаштувань', '', 'Файл конфігурації (*.ini)')
        if file[0] != '':
            config_save(file[0])
            text = 'Налаштування програми збережено у файл: ' + str(file[0])
            self.signal.signal_update_statusbar.emit(text)

    def choose_import_dir_default(self):
        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Обрати папку для швидкого завантаження файлів')
        if new_dir != '':
            config_set_item('import_folder_default', 'path', new_dir)
            text = 'Визначено типову для імпорту папку: ' + str(new_dir)
            self.signal.signal_update_statusbar.emit(text)
            self.signal.signal_settings_changed.emit()


    def settings_win_close_without_save(self):
        config_load('config\\config.ini')
        print('Settings closed without save')
        text = 'Налаштування завершені без збереження'
        self.signal.signal_update_statusbar.emit(text)
        self.signal.signal_settings_changed.emit()
        self.close()

    def settings_win_close_save_settings(self):
        config_save('config\\config.ini')
        print('Settings closed and changes saved')
        text = 'Налаштування завершені та збережені'
        self.signal.signal_update_statusbar.emit(text)
        self.close()

    def accept_changes_settings(self):
        config_save('config\\config.ini')
        text = 'Виконані зміни у налаштуваннях зафіксовано'
        self.signal.signal_update_statusbar.emit(text)
        print('Changes accepted and save to config')

    # ---------------------------МЕТОД оновлення значень вікна налаштувань при їх зміні--------------------------------
    def update_settings_gui(self):
        self.open_modalwin_settings.label_import_dir_default.setText(
            config_get_value('import_folder_default', 'path'))  # оновлення типової папки імпорту

        # Оновлення рядків зі списоком типів (як будуть відображатися в готовій таблиці):
        self.open_modalwin_settings.lineEdit_exportname_voice_in.setText(
            config_get_value('types_con_main_display_names', 'voice_in'))
        self.open_modalwin_settings.lineEdit_exportname_voice_out.setText(
            config_get_value('types_con_main_display_names', 'voice_out'))
        self.open_modalwin_settings.lineEdit_exportname_message_in.setText(
            config_get_value('types_con_main_display_names', 'message_in'))
        self.open_modalwin_settings.lineEdit_exportname_message_out.setText(
            config_get_value('types_con_main_display_names', 'message_out'))
        self.open_modalwin_settings.lineEdit_exportname_network.setText(
            config_get_value('types_con_main_display_names', 'network'))
        self.open_modalwin_settings.lineEdit_exportname_forwarding.setText(
            config_get_value('types_con_main_display_names', 'forwarding'))
        self.open_modalwin_settings.lineEdit_exportname_unknowntypes.setText(
            config_get_value('types_con_main_display_names', 'unknown'))

        # Оновлення списків типів для розпізнання:
        self.upd_list_voice_in()
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
            config_save('config\\config.ini')
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