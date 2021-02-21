import sys
from gui.gui import *
from PyQt5.QtCore import Qt

import colorama
from converter.convert_engine import *
from converter.terminal_messages import *
from analyst.analyst_engine import analysis_type_a
from tqdm import tqdm

# **************************************PROGRAM STARTING*****************************************
prog_execute_stage = 0  # етапи роботи для відображення активності кнопок (до перегону, після перегону)
input_files_default_headers_set = ['Шлях', 'Файл', 'Розмір', 'Відбиток', 'Колонок', 'Типів', 'Записів',
                                   'Абонентів А/Б', 'IMEI', 'Зон/антен', 'Визначений тип']
test_data =  [
            ['1', '2'],
            ['1', '2', '3']
            ]

availible_sheets_list = []
colorama.init()

print_logo()


# print_program_description()
# dialog_user_start()

class ModelSheetsListView(QtCore.QAbstractTableModel):
    def __init__(self, parent, columns_headers, input_data):
        QtCore.QAbstractTableModel.__init__(self)
        self.gui = parent
        for row in input_data:
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


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Активність віджетів в залежності від етапу виконнаня програми (підготовка до перегону/ робота з опрацьованими
        # файлами) - залежить від статусу змінної prog_execute_stage:
        if prog_execute_stage > 0:
            self.ui.btn_sheet_add.setDisabled(True)
            self.ui.btn_sheet_remove.setDisabled(True)
            self.ui.btn_sheet_clear_list.setDisabled(True)
            self.ui.btn_sheet_import_def_dir.setDisabled(True)
            self.ui.btn_sheet_start_convert.setDisabled(True)

        if prog_execute_stage == 0:
            self.ui.btn_excel_save.setDisabled(True)
            self.ui.groupBox_3.setDisabled(True)
            self.ui.groupBox_4.setDisabled(True)
        # Кнопки роботи зі списком файлів, що готуються до завантаження:
        self.ui.btn_sheet_add.clicked.connect(self.add_sheet_dialog)

        # Підготовка форми таблиці для файлів обраних користувачем (для правильного відображення у віджеті
        # tableView необхідно підготувати форму даних за допомогою класу QAbstractTableModel):
        self.widget_sheets_table_view = self.ui.tableView_import_files_list  # змінна безпосередньо віджету
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view, input_files_default_headers_set, availible_sheets_list)  # об'єкт моделі даних
        self.widget_sheets_table_view.setModel(self.sheets_view_object)  # застосування моделі до віджету
        tv_vertical_header_setting = self.widget_sheets_table_view.verticalHeader()
        tv_vertical_header_setting.setDefaultSectionSize(10)
        tv_vertical_header_setting.sectionResizeMode(QtWidgets.QSizePolicy.Fixed)
        self.widget_sheets_table_view.horizontalHeader().setStretchLastSection(True)

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
            file_size = str(round(os.path.getsize(file) / 1024.0)) + ' Kb'
            file_name = os.path.basename(file)
            file_footprint = str(file_name) + str(file_size)
            if file_footprint in [results[3] for results in incoming_sheets_list]:
                pass
            else:
                incoming_sheets_list.append([file_path, file_name, file_size, file_footprint])
        availible_sheets_list = incoming_sheets_list
        print(incoming_sheets_list)
        self.sheets_view_object = ModelSheetsListView(self.widget_sheets_table_view, input_files_default_headers_set,
                                                      availible_sheets_list)
        self.widget_sheets_table_view.setModel(self.sheets_view_object)
        self.widget_sheets_table_view.resizeColumnToContents(1)
        self.widget_sheets_table_view.resizeColumnToContents(0)
        self.widget_sheets_table_view.resizeColumnToContents(2)
        # У вкладений список sheets_list_prepared додаємо файли, які обрав користувач, та яких ще немає у списку,
        # перевірка на повторення через file_footprint (назва файлу з його розміром)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

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
