import sys
# from temp.fake import fake_func

from gui.gui import *
from gui.gui_settings import Ui_Form
from gui.gui_splash import Ui_SplashScreen
from gui.gui_converting import Ui_LoadingConverter
from gui.gui_import_folder import *

from PyQt5.QtCore import Qt, pyqtSignal, QObject

import qtmodern.styles
import qtmodern.windows

from config.config_math import config_get_value, config_set_item, config_save, config_load, config_swipe, \
    config_get_options, config_remove_item, config_get_dict





import colorama
from converter.convert_engine import *
from converter.terminal_messages import *
from analyst.analyst_engine import analysis_type_a



current_version = 'ver.1.1 build070321(unstable)'
counter = 0  # рахунок заповнення статус бару ВІКНА ЗАВАНТАЖЕННЯ
prog_execute_stage = 0  # етапи програми для відображення активності елементів (до перегону, після перегону), глобальна
supported_types = ('.xls', '.xlsx', '.xml', '.txt', '.csv', '.txt', '.dec')


availible_sheets_list = []  # список файлів для конвертування та результати опрацювання (детально в tasks.py)
main_app_df = pd.DataFrame()  # конвертовані дані з усіх файлів (для подальшого експорту або аналізу)
subscriber_a_list = []  # список всіх знайдених цільових абонентів (основні абоненти у файлі)
subscriber_b_list = []  # список всіх цільових абонентів по яким є вибірка типу "Б"
subscriber_ab_list = []  # список абонентів щодо яких у одному файлі є відомості про місцезнаходження і співрозмовника


# Консольні функції (підлягають видаленню після переходу на GUI)
colorama.init()  # ініціалізація модулю виводу у консоль різними кольорами
print_logo()  # друк логотипу під час старту програми


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------ХЕНДЛЕР ПОДІЙ---------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class HandlerFirst(QObject):
    signal_update_statusbar = pyqtSignal(str)
    signal_settings_changed = pyqtSignal()
    signal_converter_pb = pyqtSignal(list)

# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------МОДЕЛЬ ТАБЛИЦІ КОНВЕРТЕРУ---------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ModelSheetsListView(QtCore.QAbstractTableModel):
    def __init__(self, parent, input_data):
        QtCore.QAbstractTableModel.__init__(self)
        self.gui = parent
        self.input_files_default_headers_set = ['Файл', 'Розмір', 'Записи', 'Колонки', 'Типи', 'SIM\nА/Б',
                                           'ІМЕІ\nА/Б', 'LAC', 'БС/Адрес', 'Визначений тип']

        for row in input_data:  # додавання порожніх клітинок для уникнення помилки IndexError при відображенні
            if len(row) < len(self.input_files_default_headers_set):
                while len(row) < len(self.input_files_default_headers_set):
                    row.append("-")
        self.colLabels = self.input_files_default_headers_set
        self.converted_data = []
        for row in input_data:
            new_row = [row[1], row[2], str(row[4])+'/'+str(row[5]), str(row[6])+'/'+str(row[7]), str(row[8])+
                       '/'+str(row[9]), str(row[10])+'/'+str(row[11]), str(row[12])+'/'+str(row[13]), row[14],
                       str(row[15])+'/'+str(row[16]), row[20]]
            self.converted_data.append(new_row)
        self.cached = self.converted_data

    def rowCount(self, parent):
        return len(self.cached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif (index.column() == 1 and role == QtCore.Qt.TextAlignmentRole):
            return QtCore.Qt.AlignRight
        elif (index.column() in [2, 3, 4, 5, 6, 7, 8] and role == QtCore.Qt.TextAlignmentRole):
            return QtCore.Qt.AlignCenter
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
        self.win_loading = LoadingScreen()
        #

        # ---------------------------------Початкова активність елементів(віджетів):-----------------------------------
        # Активність елементів в залежності від етапу виконнаня програми (підготовка до перегону/ робота з опрацьованими
        # файлами) - залежить від статусу змінної prog_execute_stage:
        self.ui.btn_excel_save.setDisabled(True)
        self.ui.groupBox_3.setDisabled(True)
        self.ui.groupBox_4.setDisabled(True)
        self.ui.btn_sheet_remove.setEnabled(False)  # кнопка активується якщо є виділені рядки списку файлів
        self.ui.btn_sheet_start_convert.setDisabled(True)

        # -----------------------------------Підключення ТАБЛИЦІ конвертеру:-------------------------------------------
        # Підготовка форми таблиці для файлів обраних користувачем (для правильного відображення у віджеті
        # tableView необхідно підготувати форму даних за допомогою класу QAbstractTableModel):
        self.widget_sheets_table_view = self.ui.tableView_import_files_list  # змінна безпосередньо віджету
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view,
                                                      availible_sheets_list)  # об'єкт моделі даних
        self.widget_sheets_table_view.setModel(self.sheets_view_object)  # застосування моделі до віджету
        for col in range(2, 9, 1):
            self.widget_sheets_table_view.setColumnWidth(col, 55)
        self.widget_sheets_table_view.resizeColumnToContents(0)
        self.widget_sheets_table_view.resizeColumnToContents(1)
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
        # Підключення кнопки СТАРТУ КОНВЕРТУВАННЯ:
        self.ui.btn_sheet_start_convert.clicked.connect(self.start_convert)
        #

    # -----------------------------------------методи ВІДКРИТТЯ ВІКОН --------------------------------------------------
    def open_modalwin_settings(self):
        # flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # self.win_settings.setWindowFlags(flags)
        self.win_settings.show()

    def open_modalwin_import_folder(self):
        mw = ChooseImportFolder(self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.Window)
        mw.setWindowFlags(flags)
        mw.show()

    def start_converting(self):
        self.win_loading.show()
        # convert_all(availible_sheets_list)

    def start_convert(self):
        global availible_sheets_list
        global main_app_df
        main_app_df, availible_sheets_list = convert_all(availible_sheets_list)
        self.update_sheets_list()
        print('Records loaded: ' + str(main_app_df.shape[0]))


    def print_statusbar(self, text):
        self.ui.statusbar.showMessage(str(text), 5000)

    # --------------------------------------методи КНОПОК конвертеру --------------------------------------------------
    def remove_btn_update(self):  # активність кнопки видалення залежно від наявності виділеного рядку
        if self.widget_sheets_table_view.selectionModel().hasSelection():
            self.ui.btn_sheet_remove.setEnabled(True)
        else:
            self.ui.btn_sheet_remove.setEnabled(False)

    def upd_btn_converter_start(self):
        if len(availible_sheets_list) > 0:
            self.ui.btn_sheet_start_convert.setEnabled(True)
        else:
            self.ui.btn_sheet_start_convert.setDisabled(True)

    def remove_sheet_from_list(self):  # видалення інформації з таблиці обраних файлів (тільки до перегону)
        global availible_sheets_list
        if prog_execute_stage == 0 and self.widget_sheets_table_view.selectionModel().hasSelection():
            index = (self.widget_sheets_table_view.selectionModel().currentIndex())
            number_to_remove = index.row()
            if len(availible_sheets_list) > number_to_remove:
                availible_sheets_list.pop(number_to_remove)
                self.update_sheets_list()
                self.ui.btn_sheet_remove.setEnabled(False)
        self.upd_btn_converter_start()

    def update_sheets_list(self):  # оновлення таблиці для відображення (коли змінюється availible_sheets_list)
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view,
                                                      availible_sheets_list)
        self.widget_sheets_table_view.setModel(self.sheets_view_object)
        self.widget_sheets_table_view.resizeColumnToContents(0)
        self.widget_sheets_table_view.resizeColumnToContents(1)
        self.widget_sheets_table_view.update()
        self.upd_btn_converter_start()
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
                incoming_sheets_list.append([file_path, file_name, file_size, file_footprint, '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])
        availible_sheets_list = incoming_sheets_list
        print(incoming_sheets_list)
        self.update_sheets_list()
        self.upd_btn_converter_start()
        # У вкладений список sheets_list_prepared додаємо файли, які обрав користувач, та яких ще немає у списку,
        # перевірка на повторення через file_footprint (назва файлу з його розміром)

    def clear_sheets_list(self):
        global availible_sheets_list
        availible_sheets_list = []
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view, availible_sheets_list)
        self.widget_sheets_table_view.setModel(self.sheets_view_object)
        self.ui.btn_sheet_remove.setEnabled(False)
        self.upd_btn_converter_start()

    def add_sheet_folder_default(self):
        global availible_sheets_list
        new_sheets_list = availible_sheets_list
        current_folder = config_get_value('import_folder_default', 'path')
        print('getting def path ' + current_folder)
        file_list = []
        if current_folder != '':
            try:
                for item in os.listdir(current_folder):
                    if item.endswith(supported_types):
                        file_list.append(item)
            except FileNotFoundError:
                print('Помилка доступу до папки, можливо типова папка видалена')
                self.open_modalwin_import_folder()
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
                    new_sheets_list.append([file_path, file, file_size, file_footprint, '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])
            availible_sheets_list = new_sheets_list
            print(new_sheets_list)
            self.update_sheets_list()
        self.upd_btn_converter_start()


# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------------------ВІКНО НАЛАШТУВАНЬ SETTINGS--------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, parent=MainWinMatematik):  # втрачається центрування до батьківського вікна
        QtWidgets.QWidget.__init__(self)
        # super().__init__()
        self.win_settings = Ui_Form()
        self.win_settings.setupUi(self)
        self.setWindowModality(2)
        self.signal = HandlerFirst()

        # Функції кнопок першої вкладки налаштувань та основних кнопок: ------------------------------------------------
        self.win_settings.label_import_dir_default.setText(config_get_value('import_folder_default', 'path'))
        self.win_settings.btn_config_swipe.clicked.connect(self.swipe_to_factory)
        self.win_settings.btn_config_load.clicked.connect(self.choose_file_load_config)
        self.win_settings.btn_config_save.clicked.connect(self.choose_file_save_config)
        self.win_settings.btn_set_dir_import_default.clicked.connect(self.choose_import_dir_default)
        self.win_settings.btn_setup_cancel.clicked.connect(self.settings_win_close_without_save)
        self.win_settings.btn_setup_ok.clicked.connect(self.settings_win_close_save_settings)
        self.win_settings.btn_setup_accept.setEnabled(True)
        self.win_settings.btn_setup_accept.clicked.connect(self.accept_changes_settings)
        self.signal.signal_settings_changed.connect(self.update_settings_gui)  # сигнал оновлення всього вікна
                                                                               # налаштувань з config.ini

        # Підключення функції кнопок ТИПІВ РОЗПІЗНАННЯ:-----------------------------------------------------------------
        # Функції кнопок - редагування списку ВХІДНИХ ДЗВІНКІВ
        self.win_settings.btn_add_voice_in.setEnabled(False)
        self.win_settings.btn_remove_voice_in.setEnabled(False)
        self.win_settings.btn_remove_voice_in.clicked.connect(self.remove_voice_in_item)
        self.win_settings.btn_add_voice_in.clicked.connect(self.add_item_voice_in)
        self.win_settings.listView_voice_in.clicked.connect(self.upd_btn_remove_voice_in)
        # Функції кнопок - редагування списку ВИХІДНИХ ДЗВІНКІВ
        self.win_settings.btn_add_voice_out.setEnabled(False)
        self.win_settings.btn_remove_voice_out.setEnabled(False)
        self.win_settings.btn_remove_voice_out.clicked.connect(self.remove_voice_out_item)
        self.win_settings.btn_add_voice_out.clicked.connect(self.add_item_voice_out)
        self.win_settings.listView_voice_out.clicked.connect(self.upd_btn_remove_voice_out)
        # Функції кнопок - редагування списку ВХІДНИХ ПОВІДОМЛЕНЬ
        self.win_settings.btn_add_message_in.setEnabled(False)
        self.win_settings.btn_remove_message_in.setEnabled(False)
        self.win_settings.btn_remove_message_in.clicked.connect(self.remove_message_in_item)
        self.win_settings.btn_add_message_in.clicked.connect(self.add_item_message_in)
        self.win_settings.listView_message_in.clicked.connect(self.upd_btn_remove_message_in)
        # Функції кнопок - редагування списку ВИХІДНИХ ПОВІДОМЛЕНЬ
        self.win_settings.btn_add_message_out.setEnabled(False)
        self.win_settings.btn_remove_message_out.setEnabled(False)
        self.win_settings.btn_remove_message_out.clicked.connect(self.remove_message_out_item)
        self.win_settings.btn_add_message_out.clicked.connect(self.add_item_message_out)
        self.win_settings.listView_message_out.clicked.connect(self.upd_btn_remove_message_out)
        # Функції кнопок - редагування списку ІНТЕРНЕТ
        self.win_settings.btn_add_network.setEnabled(False)
        self.win_settings.btn_remove_network.setEnabled(False)
        self.win_settings.btn_remove_network.clicked.connect(self.remove_network_item)
        self.win_settings.btn_add_network.clicked.connect(self.add_item_network)
        self.win_settings.listView_network.clicked.connect(self.upd_btn_remove_network)
        # Функції кнопок - редагування списку ПЕРЕАДРЕСАЦІЇ
        self.win_settings.btn_add_forwarding.setEnabled(False)
        self.win_settings.btn_remove_forwarding.setEnabled(False)
        self.win_settings.btn_remove_forwarding.clicked.connect(self.remove_forwarding_item)
        self.win_settings.btn_add_forwarding.clicked.connect(self.add_item_forwarding)
        self.win_settings.listView_forwarding.clicked.connect(self.upd_btn_remove_forwarding)

        # Встановлення АКТИВНОСТІ КНОПКИ ДОДАВАННЯ типів з'єднань для розпізнання
        self.win_settings.lineEdit_add_voice_in.textChanged.connect(self.upd_btn_add_voice_in)
        self.win_settings.lineEdit_add_voice_out.textChanged.connect(self.upd_btn_add_voice_out)
        self.win_settings.lineEdit_add_message_in.textChanged.connect(self.upd_btn_add_message_in)
        self.win_settings.lineEdit_add_message_out.textChanged.connect(self.upd_btn_add_message_out)
        self.win_settings.lineEdit_add_network.textChanged.connect(self.upd_btn_add_network)
        self.win_settings.lineEdit_add_forwarding.textChanged.connect(self.upd_btn_add_forwarding)

        # Активація СПИСКУ найменувань КОЛОНОК для РОЗПІЗНАННЯ:
        self.model_col_names_incoming = QtGui.QStandardItemModel()
        self.model_col_names_incoming.clear()
        self.win_settings.listView_keywords_col_replace.setModel(self.model_col_names_incoming)
        self.sel_model_col_names_incoming = self.win_settings.listView_keywords_col_replace.selectionModel()
        self.dict_inc_col_var_desc = config_get_dict('columns_incoming_names')
        self.inv_dict_inc_col = {v: k for k, v in self.dict_inc_col_var_desc.items()}
        self.dict_inc_col_var_to_config_section = {
            'type': 'columns_dict_type',
            'date': 'columns_dict_date',
            'time': 'columns_dict_time',
            'date_end': 'columns_dict_date_end',
            'dur': 'columns_dict_dur',
            'sim_a': 'columns_dict_sim_a',
            'imei_a': 'columns_dict_imei_a',
            'desc_a': 'columns_dict_desc_a',
            'sim_b': 'columns_dict_sim_b',
            'imei_b': 'columns_dict_imei_b',
            'desc_b': 'columns_dict_desc_b',
            'sim_c': 'columns_dict_sim_c',
            'sim_d': 'columns_dict_sim_d',
            'forw': 'columns_dict_forw',
            'lac_a': 'columns_dict_lac_a',
            'cid_a': 'columns_dict_cid_a',
            'lac_cid': 'columns_dict_lac_cid',
            'az_a': 'columns_dict_az_a',
            'adr_a': 'columns_dict_adr_a',
            'lac_b': 'columns_dict_lac_b',
            'cid_b': 'columns_dict_cid_b',
            'az_b': 'columns_dict_az_b',
            'adr_b': 'columns_dict_adr_b',
            'column_ignore': 'columns_dict_column_ignore'
        }
        self.win_settings.comboBox_choose_import_column.currentIndexChanged.connect(self.upd_list_col_incoming)
        self.win_settings.btn_add_keyword_column.setEnabled(False)
        self.win_settings.lineEdit_add_keyword_column.textChanged.connect(self.upd_btn_add_keyword_column)

        self.win_settings.btn_remove_keyword_column.setEnabled(False)
        self.win_settings.btn_remove_keyword_column.clicked.connect(self.remove_keyword_column_item)
        self.win_settings.btn_add_keyword_column.clicked.connect(self.add_item_keyword_column)
        self.win_settings.listView_keywords_col_replace.clicked.connect(self.upd_btn_remove_keyword_column)

        # self.dict_export_column_names = config_get_dict('columns_export_names')
        # self.column_export_names_count = len(self.dict_export_column_names)
        # self.win_settings.table_columns_exportnames.setRowCount(self.column_export_names_count)
        # self.column_export_names_tpl = [[k, v] for k, v in self.dict_export_column_names.items()]
        # for row_col_export in range(self.column_export_names_count):
        #     self.win_settings.table_columns_exportnames.setItem(row_col_export, 0, QtWidgets.QTableWidgetItem(str(self.column_export_names_tpl[row_col_export][0])))
        #     self.win_settings.table_columns_exportnames.setItem(row_col_export, 1, QtWidgets.QTableWidgetItem(str(self.column_export_names_tpl[row_col_export][1])))
        #     self.win_settings.table_columns_exportnames.item(row_col_export, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        # self.win_settings.table_columns_exportnames.resizeRowsToContents()
        self.column_export_names_count = len(config_get_dict('columns_export_names'))
        self.win_settings.table_columns_exportnames.setRowCount(self.column_export_names_count)
        self.win_settings.table_columns_exportnames.itemChanged.connect(self.upd_col_export_name_config)
        self.upd_col_export_names_list()


        # Завантаження НАЙМЕНУВАНЬ ТИПІВ для відображення у ЕКСПОРТОВАНИХ ТАБЛИЦЯХ:-------------------------------------
        self.win_settings.lineEdit_exportname_voice_in.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'voice_in', str(x)))
        self.win_settings.lineEdit_exportname_voice_out.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'voice_out', str(x)))
        self.win_settings.lineEdit_exportname_message_in.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'message_in', str(x)))
        self.win_settings.lineEdit_exportname_message_out.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'message_out', str(x)))
        self.win_settings.lineEdit_exportname_network.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'network', str(x)))
        self.win_settings.lineEdit_exportname_forwarding.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'forwarding', str(x)))
        self.win_settings.lineEdit_exportname_unknowntypes.textChanged.connect(
            lambda x: config_set_item('types_con_main_display_names', 'unknown', str(x)))

        # ЗАПОВНЕННЯ ListView ТИПІВ РОЗПІЗНАННЯ:------------------------------------------------------------------------
        self.model_voice_in = QtGui.QStandardItemModel()
        self.win_settings.listView_voice_in.setModel(self.model_voice_in)
        voice_in_types = config_get_options('types_dict_voice_in')
        for i in voice_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_voice_in.appendRow(item)
        self.sel_model_voice_in = self.win_settings.listView_voice_in.selectionModel()
        self.sel_model_voice_in.selectionChanged.connect(self.upd_btn_remove_voice_in)

        self.model_voice_out = QtGui.QStandardItemModel()
        self.win_settings.listView_voice_out.setModel(self.model_voice_out)
        voice_out_types = config_get_options('types_dict_voice_out')
        for i in voice_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_voice_out.appendRow(item)
        self.sel_model_voice_out = self.win_settings.listView_voice_out.selectionModel()
        self.sel_model_voice_out.selectionChanged.connect(self.upd_btn_remove_voice_out)

        self.model_message_out = QtGui.QStandardItemModel()
        self.win_settings.listView_message_out.setModel(self.model_message_out)
        message_out_types = config_get_options('types_dict_message_out')
        for i in message_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_message_out.appendRow(item)
        self.sel_model_message_out = self.win_settings.listView_message_out.selectionModel()
        self.sel_model_message_out.selectionChanged.connect(self.upd_btn_remove_message_out)

        self.model_message_in = QtGui.QStandardItemModel()
        self.win_settings.listView_message_in.setModel(self.model_message_in)
        message_in_types = config_get_options('types_dict_message_in')
        for i in message_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_message_in.appendRow(item)
        self.sel_model_message_in = self.win_settings.listView_message_in.selectionModel()
        self.sel_model_message_in.selectionChanged.connect(self.upd_btn_remove_message_in)

        self.model_network = QtGui.QStandardItemModel()
        self.win_settings.listView_network.setModel(self.model_network)
        network_types = config_get_options('types_dict_network')
        for i in network_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_network.appendRow(item)
        self.sel_model_network = self.win_settings.listView_network.selectionModel()
        self.sel_model_network.selectionChanged.connect(self.upd_btn_remove_network)

        self.model_forwarding = QtGui.QStandardItemModel()
        self.win_settings.listView_forwarding.setModel(self.model_forwarding)
        forwarding_types = config_get_options('types_dict_forwarding')
        for i in forwarding_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_forwarding.appendRow(item)
        self.sel_model_forwarding = self.win_settings.listView_forwarding.selectionModel()
        self.sel_model_forwarding.selectionChanged.connect(self.upd_btn_remove_forwarding)

        # ЗАПОВНЕННЯ ComboBox КОЛОНОК РОЗПІЗНАННЯ:----------------------------------------------------------------------
        self.win_settings.comboBox_choose_import_column.clear()
        incoming_col_types_var = config_get_options('columns_incoming_names')
        incoming_col_types_names = []
        for var in incoming_col_types_var:
            incoming_col_types_names.append(config_get_value('columns_incoming_names', str(var)))
        self.win_settings.comboBox_choose_import_column.addItems(incoming_col_types_names)
        self.win_settings.comboBox_choose_import_column.insertSeparator(5)
        self.win_settings.comboBox_choose_import_column.insertSeparator(12)
        self.win_settings.comboBox_choose_import_column.insertSeparator(16)
        self.win_settings.comboBox_choose_import_column.insertSeparator(26)

    # Функції кнопок списку типів розпізнання ВХІДНІ ДЗВІНКИ
    def upd_btn_remove_voice_in(self):
        if self.sel_model_voice_in.hasSelection():
            self.win_settings.btn_remove_voice_in.setEnabled(True)
        else:
            self.win_settings.btn_remove_voice_in.setEnabled(False)

    def upd_btn_add_voice_in(self):
        if self.win_settings.lineEdit_add_voice_in.text() != '':
            self.win_settings.btn_add_voice_in.setEnabled(True)
        else:
            self.win_settings.btn_add_voice_in.setEnabled(False)

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
            config_remove_item('types_dict_voice_in', str(text))
            self.model_voice_in.removeRow(row)
            self.sel_model_voice_in.clearSelection()

    def add_item_voice_in(self):
        if self.win_settings.lineEdit_add_voice_in.text() != '':
            config_set_item('types_dict_voice_in', str(self.win_settings.lineEdit_add_voice_in.text()), str('True'))
            self.win_settings.lineEdit_add_voice_in.clear()
            self.upd_list_voice_in()

    # Функції кнопок списку типів розпізнання ВИХІДНІ ДЗВІНКИ
    def upd_btn_remove_voice_out(self):
        if self.sel_model_voice_out.hasSelection():
            self.win_settings.btn_remove_voice_out.setEnabled(True)
        else:
            self.win_settings.btn_remove_voice_out.setEnabled(False)

    def upd_btn_add_voice_out(self):
        if self.win_settings.lineEdit_add_voice_out.text() != '':
            self.win_settings.btn_add_voice_out.setEnabled(True)
        else:
            self.win_settings.btn_add_voice_out.setEnabled(False)

    def upd_list_voice_out(self):
        self.model_voice_out.clear()
        voice_out_types = config_get_options('types_dict_voice_out')
        for i in voice_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_voice_out.appendRow(item)

    def remove_voice_out_item(self):
        if self.sel_model_voice_out.hasSelection():
            index = self.sel_model_voice_out.currentIndex()
            text = index.data()
            row = index.row()
            config_remove_item('types_dict_voice_out', str(text))
            self.model_voice_out.removeRow(row)
            self.sel_model_voice_out.clearSelection()

    def add_item_voice_out(self):
        if self.win_settings.lineEdit_add_voice_out.text() != '':
            config_set_item('types_dict_voice_out', str(self.win_settings.lineEdit_add_voice_out.text()), str('True'))
            self.win_settings.lineEdit_add_voice_out.clear()
            self.upd_list_voice_out()

    # Функції кнопок списку типів розпізнання ВХІДНІ ПОВІДОМЛЕННЯ 
    def upd_btn_remove_message_in(self):
        if self.sel_model_message_in.hasSelection():
            self.win_settings.btn_remove_message_in.setEnabled(True)
        else:
            self.win_settings.btn_remove_message_in.setEnabled(False)

    def upd_btn_add_message_in(self):
        if self.win_settings.lineEdit_add_message_in.text() != '':
            self.win_settings.btn_add_message_in.setEnabled(True)
        else:
            self.win_settings.btn_add_message_in.setEnabled(False)

    def upd_list_message_in(self):
        self.model_message_in.clear()
        message_in_types = config_get_options('types_dict_message_in')
        for i in message_in_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_message_in.appendRow(item)

    def remove_message_in_item(self):
        if self.sel_model_message_in.hasSelection():
            index = self.sel_model_message_in.currentIndex()
            text = index.data()
            row = index.row()
            config_remove_item('types_dict_message_in', str(text))
            self.model_message_in.removeRow(row)
            self.sel_model_message_in.clearSelection()

    def add_item_message_in(self):
        if self.win_settings.lineEdit_add_message_in.text() != '':
            config_set_item('types_dict_message_in', str(self.win_settings.lineEdit_add_message_in.text()), str('True'))
            self.win_settings.lineEdit_add_message_in.clear()
            self.upd_list_message_in()

    # Функції кнопок списку типів розпізнання ВИХІДНІ ПОВІДОМЛЕННЯ 
    def upd_btn_remove_message_out(self):
        if self.sel_model_message_out.hasSelection():
            self.win_settings.btn_remove_message_out.setEnabled(True)
        else:
            self.win_settings.btn_remove_message_out.setEnabled(False)

    def upd_btn_add_message_out(self):
        if self.win_settings.lineEdit_add_message_out.text() != '':
            self.win_settings.btn_add_message_out.setEnabled(True)
        else:
            self.win_settings.btn_add_message_out.setEnabled(False)

    def upd_list_message_out(self):
        self.model_message_out.clear()
        message_out_types = config_get_options('types_dict_message_out')
        for i in message_out_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_message_out.appendRow(item)

    def remove_message_out_item(self):
        if self.sel_model_message_out.hasSelection():
            index = self.sel_model_message_out.currentIndex()
            text = index.data()
            row = index.row()
            config_remove_item('types_dict_message_out', str(text))
            self.model_message_out.removeRow(row)
            self.sel_model_message_out.clearSelection()

    def add_item_message_out(self):
        if self.win_settings.lineEdit_add_message_out.text() != '':
            config_set_item('types_dict_message_out', str(self.win_settings.lineEdit_add_message_out.text()), str('True'))
            self.win_settings.lineEdit_add_message_out.clear()
            self.upd_list_message_out()

    # Функції кнопок списку типів розпізнання ІНТЕРНЕТ 
    def upd_btn_remove_network(self):
        if self.sel_model_network.hasSelection():
            self.win_settings.btn_remove_network.setEnabled(True)
        else:
            self.win_settings.btn_remove_network.setEnabled(False)

    def upd_btn_add_network(self):
        if self.win_settings.lineEdit_add_network.text() != '':
            self.win_settings.btn_add_network.setEnabled(True)
        else:
            self.win_settings.btn_add_network.setEnabled(False)

    def upd_list_network(self):
        self.model_network.clear()
        network_types = config_get_options('types_dict_network')
        for i in network_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_network.appendRow(item)

    def remove_network_item(self):
        if self.sel_model_network.hasSelection():
            index = self.sel_model_network.currentIndex()
            text = index.data()
            row = index.row()
            config_remove_item('types_dict_network', str(text))
            self.model_network.removeRow(row)
            self.sel_model_network.clearSelection()

    def add_item_network(self):
        if self.win_settings.lineEdit_add_network.text() != '':
            config_set_item('types_dict_network', str(self.win_settings.lineEdit_add_network.text()), str('True'))
            self.win_settings.lineEdit_add_network.clear()
            self.upd_list_network()

    # Методи кнопок списку типів розпізнання ПЕРЕАДРЕСАЦІЯ
    def upd_btn_remove_forwarding(self):
        if self.sel_model_forwarding.hasSelection():
            self.win_settings.btn_remove_forwarding.setEnabled(True)
        else:
            self.win_settings.btn_remove_forwarding.setEnabled(False)

    def upd_btn_add_forwarding(self):
        if self.win_settings.lineEdit_add_forwarding.text() != '':
            self.win_settings.btn_add_forwarding.setEnabled(True)
        else:
            self.win_settings.btn_add_forwarding.setEnabled(False)

    def upd_list_forwarding(self):
        self.model_forwarding.clear()
        forwarding_types = config_get_options('types_dict_forwarding')
        for i in forwarding_types:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_forwarding.appendRow(item)

    def remove_forwarding_item(self):
        if self.sel_model_forwarding.hasSelection():
            index = self.sel_model_forwarding.currentIndex()
            text = index.data()
            row = index.row()
            config_remove_item('types_dict_forwarding', str(text))
            self.model_forwarding.removeRow(row)
            self.sel_model_forwarding.clearSelection()

    def add_item_forwarding(self):
        if self.win_settings.lineEdit_add_forwarding.text() != '':
            config_set_item('types_dict_forwarding', str(self.win_settings.lineEdit_add_forwarding.text()), str('True'))
            self.win_settings.lineEdit_add_forwarding.clear()
            self.upd_list_forwarding()

    # -------------------------------------------------------------------------------
    # МЕТОДИ КНОПОК ГОЛОВНОЇ ВКЛАДКИ НАЛАШТУВАНЬ ------------------------------------
    # -------------------------------------------------------------------------------
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

    # ---------------------------------------------------------------------
    # Робота з НАЛАШТУВАННЯМ КОЛОНОК---------------------------------------
    # ---------------------------------------------------------------------
    def upd_list_col_incoming(self):
        self.model_col_names_incoming.clear()
        current_columns_text = str(self.win_settings.comboBox_choose_import_column.currentText())
        var_of_column_type = self.inv_dict_inc_col.get(current_columns_text)
        section_to_view = self.dict_inc_col_var_to_config_section.get(var_of_column_type)
        items_to_view = config_get_options(section_to_view)
        for i in items_to_view:
            if i != '':
                item = QtGui.QStandardItem(i)
                self.model_col_names_incoming.appendRow(item)

    def upd_btn_add_keyword_column(self):
        if self.win_settings.lineEdit_add_keyword_column.text() != '':
            self.win_settings.btn_add_keyword_column.setEnabled(True)
        else:
            self.win_settings.btn_add_keyword_column.setEnabled(False)

    def upd_btn_remove_keyword_column(self):
        if self.sel_model_col_names_incoming.hasSelection():
            self.win_settings.btn_remove_keyword_column.setEnabled(True)
        else:
            self.win_settings.btn_remove_keyword_column.setEnabled(False)

    def remove_keyword_column_item(self):
        if self.sel_model_col_names_incoming.hasSelection():
            index = self.sel_model_col_names_incoming.currentIndex()
            text = index.data()
            row = index.row()
            column_human_name = self.win_settings.comboBox_choose_import_column.currentText()
            column_var_name = self.inv_dict_inc_col.get(column_human_name)
            config_selection_name = self.dict_inc_col_var_to_config_section.get(column_var_name)
            config_remove_item(config_selection_name, str(text))
            self.model_col_names_incoming.removeRow(row)
            self.sel_model_col_names_incoming.clearSelection()
            self.upd_btn_remove_keyword_column()

    def add_item_keyword_column(self):
        if self.win_settings.lineEdit_add_keyword_column.text() != '':
            column_human_name = self.win_settings.comboBox_choose_import_column.currentText()
            column_var_name = self.inv_dict_inc_col.get(column_human_name)
            config_selection_name = self.dict_inc_col_var_to_config_section.get(column_var_name)
            config_set_item(config_selection_name, str(self.win_settings.lineEdit_add_keyword_column.text()), str(column_var_name))
            self.win_settings.lineEdit_add_keyword_column.clear()
            self.upd_list_col_incoming()

    def upd_col_export_name_config(self, cell):
        if cell.column() == 1:
            row = cell.row()
            text = cell.text()
            option = self.win_settings.table_columns_exportnames.item(row, 0).text()
            config_set_item('columns_export_names', option, text)

    def upd_col_export_names_list(self):
        cur_dict = config_get_dict('columns_export_names')
        cur_list = [[k, v] for k, v in cur_dict.items()]
        for row_col_export in range(len(cur_list)):
            self.win_settings.table_columns_exportnames.setItem(row_col_export, 0, QtWidgets.QTableWidgetItem(str(cur_list[row_col_export][0])))
            self.win_settings.table_columns_exportnames.setItem(row_col_export, 1, QtWidgets.QTableWidgetItem(str(cur_list[row_col_export][1])))
            self.win_settings.table_columns_exportnames.item(row_col_export, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.win_settings.table_columns_exportnames.resizeRowsToContents()
    # -------------------------------------------------------------------------------
    # МЕТОДИ ОНОВЛЕННЯ ВСЬОГО ВІКНА НАЛАШТУВАНЬ- ------------------------------------
    # -------------------------------------------------------------------------------
    def update_settings_gui(self):
        self.win_settings.label_import_dir_default.setText(
            config_get_value('import_folder_default', 'path'))  # оновлення типової папки імпорту
        # Оновлення рядків зі списоком типів (як будуть відображатися в готовій таблиці):
        self.win_settings.lineEdit_exportname_voice_in.setText(
            config_get_value('types_con_main_display_names', 'voice_in'))
        self.win_settings.lineEdit_exportname_voice_out.setText(
            config_get_value('types_con_main_display_names', 'voice_out'))
        self.win_settings.lineEdit_exportname_message_in.setText(
            config_get_value('types_con_main_display_names', 'message_in'))
        self.win_settings.lineEdit_exportname_message_out.setText(
            config_get_value('types_con_main_display_names', 'message_out'))
        self.win_settings.lineEdit_exportname_network.setText(
            config_get_value('types_con_main_display_names', 'network'))
        self.win_settings.lineEdit_exportname_forwarding.setText(
            config_get_value('types_con_main_display_names', 'forwarding'))
        self.win_settings.lineEdit_exportname_unknowntypes.setText(
            config_get_value('types_con_main_display_names', 'unknown'))
        # Оновлення списків типів для розпізнання:
        self.upd_list_voice_in()
        self.upd_list_voice_out()
        self.upd_list_message_in()
        self.upd_list_message_out()
        self.upd_list_network()
        self.upd_list_forwarding()
        self.upd_list_col_incoming()
        self.upd_col_export_names_list()


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
# -------------------------------------------ВІКНО ЗАВАНТАЖЕННЯ SPLASH WIN-----------------------------------------
# -----------------------------------------------------------------------------------------------------------------
class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(5)

        self.show()

    def progress(self):
        global counter
        self.ui.pb_splash.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.app = QtWidgets.QApplication(sys.argv)
            qtmodern.styles.dark(self.app)
            self.myapp = qtmodern.windows.ModernWindow(MainWinMatematik())
            self.myapp.show()
            # sys.exit(app.exec_())
            self.close()
        counter +=1

# -----------------------------------------------------------------------------------------------------------------
# -------------------------------------------ВІКНО РОБОТИ КОНВЕРТЕРУ-----------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
class LoadingScreen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_LoadingConverter()
        self.ui.setupUi(self)
        self.setWindowModality(2)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(45)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 90))
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.setWindowTitle('Опрацювання')

        self.thread = ThreadClass()
        self.thread.start()

        self.thread.progress_upd.connect(self.upd_all_progressbars)

    def upd_all_progressbars(self, val):
        self.ui.pb_voc.setValue(val[0])
        self.ui.pb_splash.setValue(val[1])


class ThreadClass(QtCore.QThread):
    progress_upd = pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        global counter_bs
        global counter_files
        while 1:
            val = [counter_bs, counter_files]
            self.progress_upd.emit(val)
            time.sleep(3)


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------ВИКОНАННЯ ПРОГРАМИ------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # qtmodern.styles.dark(app)
    myapp = SplashScreen()
    # myapp.show()
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