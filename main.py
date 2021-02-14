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
availible_sheets_list = [['Шлях'], ['Файл'], ['Розмір'], ['Відбиток']], [[[0], [1], [2], [3]]]

# availible_sheets_list = [['Шлях'], ['Файл'], ['Розмір'], ['Відбиток'], ['Колонок'], ['Типів'], ['Записів'],
#                          ['Абонентів А/Б'], ['IMEI'], ['Зон/антен'], ['Визначений тип']]
colorama.init()

print_logo()


# print_program_description()
# dialog_user_start()


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
        self.sheets_view_object = ModelSheetsListView(availible_sheets_list)  # об'єкт моделі даних
        self.widget_sheets_table_view.setModel(self.sheets_view_object)  # застосування моделі до віджету

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
                incoming_sheets_list.append(file_path, file_name, file_size, file_footprint)
        availible_sheets_list = incoming_sheets_list
        print(incoming_sheets_list)
        # У вкладений список sheets_list_prepared додаємо файли, які обрав користувач, та яких ще немає у списку,
        # перевірка на повторення через file_footprint (назва файлу з його розміром)


class ModelSheetsListView(QtCore.QAbstractTableModel):
    def __init__(self, input_data):
        super(ModelSheetsListView, self).__init__()
        self._data = input_data

    def __del__(self):
        pass

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


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
