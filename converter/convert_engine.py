import os
import time
import numpy as np
from colorama import Back
from lxml import etree as et

from .columns_functions import *


# -------------------------------------------------------------------------------------
# ---------------------------------PROGRAM SETTINGS VARS-------------------------------
# -------------------------------------------------------------------------------------

#Список з файлами для опрацювання. Отримується з файлів обраних користувачем в діалоговому вікні.
#Перевіряється на повторне введення одного й того ж файлу.
#Зберігає відомості про файл: абсолютний шлях(0), назва файлу(1), розмір(2), Колонки(3), Типи (4), Соти(5), Тип(6)
#До перегону таблиць містить відомості тільки про шлях, назву файлу та розмір:
sheets_list_prepared = []


su_text_search = True  # setup to parse txt files in directory
su_save_heap = True
su_save_file_to_file = True
su_save_divide_by_subscriber = True
su_merge_ab_types = True
su_sort_subscriber = False
su_sort_datetime = True

# -------------------------------------------------------------------------------------
# ------------------------------HELPERS VARS (SERVICE VARS)----------------------------
# -------------------------------------------------------------------------------------
tabs_list = []  # results of searching data files in directory
tabs_count = 0  # count of files with data in directory
tabs_to_work = 0  # tabs left
tabs_cur_level = 0  # current stage in iter file(tab)
tabs_done = 0  # number of done tabs
test_frame_deep = 100  # num of rows for testing tab's type
list_to_work = []  # files ready to combine with arguments (subscriber, type, BS voc status, "life" status)
separate_abon_list = []

# -------------------------------------------------------------------------------------
# ------------------------MAIN DICTIONARIES FOR UNDERSTAND DATA------------------------
# -------------------------------------------------------------------------------------
dict_types = {}  # config with connection types understand values
dict_columns = {}  # config of columns understand values
dict_bs = {}  # keys for BS address (mask "lac-cid")
dict_azimuth = {}  # keys for azimuth value (mask "lac-cid")
dict_address_bs = {}  # config with columns understand values (only for BS voc)

# -------------------------------------------------------------------------------------
# -------------------------------------MAIN DEFINES------------------------------------
# -------------------------------------------------------------------------------------
dict_nan = {'nan': '', 'Nan': '', 'NaN': '', None: ''}
dict_print = {True: "Да", False: "Нет"}
dict_invert_types = {"вих": "вх", "вх": "вих", "вих СМС": "вх СМС", "вх СМС": "вих СМС", "переад": "переад",
                     "internet": "internet"}
unknown_con_type_def = 'переад'


render_a_col_set = ['type', 'date', 'time', 'dur_str', 'sim_a', 'imei_a', 'sim_b', 'lac_a', 'cid_a', 'az_a', 'adr_a']
render_b_col_set = ['type', 'date', 'time', 'dur_str', 'sim_a', 'imei_a', 'sim_b', 'imei_b', 'lac_a', 'cid_a', 'az_a',
                    'adr_a', 'lac_b', 'cid_b', 'az_b', 'adr_b']
render_a_header_set = ['Тип', 'Дата', 'Час', 'Трив.', 'Абонент А', 'ІМЕІ А', 'Абонент Б', 'LAC A', 'CID A', 'Аз.А',
                       'Адреса БС А']
render_b_header_set = ['Тип', 'Дата', 'Час', 'Трив.', 'Абонент А', 'ІМЕІ А', 'Абонент Б', 'ІМЕІ Б', 'LAC A', 'CID A',
                       'Аз.А', 'Адреса БС А', 'LAC Б', 'CID Б', 'Аз.Б', 'Адреса БС Б']
analysis_columns_set = render_b_col_set + ['date_time', 'dur']

render_dict_columns = {'type': 'Тип', 'date': 'Дата', 'time': 'Час', 'dur_str': 'Трив.', 'sim_a': 'Абонент А',
                       'imei_a': 'IMEI A', 'sim_b': 'Абонент Б', 'imei_b': 'IMEI Б', 'lac_a': 'LAC А', 'cid_a': 'CID А',
                       'az_a': 'Аз.А', 'adr_a': 'Адреса БС А', 'lac_b': 'LAC Б', 'cid_b': 'CID Б', 'az_b': 'Аз.Б',
                       'adr_b': 'Адреса БС Б'}

# -------------------------------------------------------------------------------------
# -----------------------------------RESULTS FORMS-------------------------------------
# -------------------------------------------------------------------------------------
heap = pd.DataFrame(columns=analysis_columns_set)

extract_a_df = pd.DataFrame(columns=render_b_col_set + ['date_time'])
extract_b_df = pd.DataFrame(columns=render_b_col_set + ['date_time'])
combine_subscribers_df = pd.DataFrame(columns=analysis_columns_set)

extract_a_list = []
extract_b_list = []
combine_subscribers_list = []


# -------------------------------------------------------------------------------------
# -------------------------------CONVERTER'S FUNCTIONS---------------------------------
# -------------------------------------------------------------------------------------

def convert_str_to_time(cell):
    time_cell = str(cell)
    time_cell = pd.to_timedelta(time_cell)
    return time_cell


def dialog_user_start():
    global su_save_heap, su_save_file_to_file, su_save_file_to_file, su_save_divide_by_subscriber, su_merge_ab_types
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + 'ВВОД ЗАДАНИЙ:' + Style.RESET_ALL)
    answer = input('Создать общий файл heap ("куча") для всех фрагментов? (y)')
    if answer == 'y' or answer == 'Y':
        su_save_heap = True
        print(Fore.GREEN + '\tПринято. Будет создан общий файл (heap) для всех записей о соединениях...\n'
              + Style.RESET_ALL)
    else:
        su_save_heap = False
        print(Fore.RED + '\tПропускаю создание общего файла...\n' + Style.RESET_ALL)

    answer = input('Создать отдельные файлы для каждого исходника "file-to-newfile"? (y)')
    if answer == 'y' or answer == 'Y':
        su_save_file_to_file = True
        print(Fore.GREEN + '\tПринято. Для каждого исходника будет создан отдельный файл с форматированными '
                           'записями...\n' + Style.RESET_ALL)
    else:
        su_save_file_to_file = False
        print(Fore.RED + '\tПропускаю создание отдельных файлов для каждого исходника...\n' + Style.RESET_ALL)

    answer = input('Разделить выходные файлы по абонентам (авторазбивка А/Б)? (y)')
    if answer == 'y' or answer == 'Y':
        su_save_divide_by_subscriber = True
        print(Fore.GREEN + '\tПринято. Будут записаны отдельные файлы с разбивкой по абонентам...\n' + Style.RESET_ALL)
    else:
        su_save_divide_by_subscriber = False
        print(Fore.RED + '\tПропускаю создание отдельных файлов с разбивкой по абонентам А/Б\n' + Style.RESET_ALL)

    answer = input('Объединить таблицы типов А и Б? (y)')
    if answer == 'y' or answer == 'Y':
        su_merge_ab_types = True
        print(Fore.GREEN + '\tПринято. Таблицы А и Б будут объеденены...\n' + Style.RESET_ALL)
    else:
        su_merge_ab_types = False
        print(Fore.RED + '\tПропускаю объединение таблиц А и Б\n' + Style.RESET_ALL)

    if su_save_heap == su_save_file_to_file == su_save_divide_by_subscriber == su_merge_ab_types is False:
        print(Fore.RED + Back.LIGHTBLACK_EX + '\tНе введено ни одно задание. Работа остановлена' + Style.RESET_ALL)
        time.sleep(6)
        os.abort()


def xml_parse_to_pandas(file_name):
    parser = et.XMLParser(recover=True, huge_tree=True)
    tree = et.parse(file_name, parser)
    root = tree.getroot()
    print("СПРОБА КОНВЕРТАЦІЇ ТАБЛИЦІ XML")
    print(file_name)
    print(root)
    row_num = 0
    data_all_dict = {}
    table = root.find('.//{urn:schemas-microsoft-com:office:spreadsheet}Table')
    table_attr = table.attrib
    try:
        number_of_columns_xml = int(table_attr.get('{urn:schemas-microsoft-com:office:spreadsheet}ExpandedColumnCount'))
    except TypeError:
        number_of_columns_xml = 10
    rows = table.findall('.//{urn:schemas-microsoft-com:office:spreadsheet}Row')
    for row in rows:
        data_pointers = row.findall('.//{urn:schemas-microsoft-com:office:spreadsheet}Data')
        data = []
        for point in data_pointers:
            data.append(point.text)
        if len(data) > 4:
            data_cur_dict = {row_num: data}
            data_all_dict.update(data_cur_dict)
            row_num += 1
    df_from_xml = pd.DataFrame.from_dict(data_all_dict, orient='index')
    return df_from_xml


def set_new_dict(s):
    print(Fore.GREEN + "Обнаружен файл конфигурации...", s)
    b = pd.read_excel(s, header=None)
    print("Правил принято:", len(b), Style.RESET_ALL)
    c = tuple(zip(b[0], b[1]))
    a = dict(c)
    return a


def scan_directory():
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + 'Загрузка конфигурации, проверка директории...')
    print(Style.RESET_ALL)
    for file in os.listdir():
        if file.endswith(".xlsx") | file.endswith(".xls") | file.endswith(".csv") | file.endswith(".xml"):
            tabs_list.append(file)
    if su_text_search:
        for file in os.listdir():
            if file.endswith(".txt"):
                tabs_list.append(file)

    # starting status info (check files in dir):
    print("\nПоиск файлов данных в директории:")
    print(os.getcwd())
    print("Всего файлов обнаружено:", len(tabs_list), '\n')

    # getting configuration dictionaries
    if tabs_list.count("config_types.xlsx") > 0:
        dict_types.update(set_new_dict("config_types.xlsx"))
        tabs_list.remove("config_types.xlsx")
    else:
        print(Fore.RED + 'Отсутствует файл config_types. Продолжить невозможно! Всё *****, Миша, давай по-новой...')
        print(Style.RESET_ALL)
        time.sleep(6)
        os.abort()
    if tabs_list.count("config_columns.xlsx") > 0:
        dict_columns.update(set_new_dict("config_columns.xlsx"))
        tabs_list.remove("config_columns.xlsx")
    else:
        print(Fore.RED + 'Отсутствует файл config_columns. Продолжить невозможно! Всё *****, Миша, давай по-новой...')
        print(Style.RESET_ALL)
        time.sleep(6)
        os.abort()
    if tabs_list.count("config_bs_voc.xlsx") > 0:
        dict_bs.update(set_new_dict("config_bs_voc.xlsx"))
        tabs_list.remove("config_bs_voc.xlsx")
    else:
        print(Fore.RED + 'Отсутствует файл config_bs_voc. Продолжить невозможно! Всё *****, Миша, давай по-новой...')
        print(Style.RESET_ALL)
        time.sleep(6)
        os.abort()


def files_preview():
    # load a test frame:
    print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Проверка файлов, загрузка тестовых фрагментов:"
          + Style.RESET_ALL)
    for i in tabs_list:
        print('\t', i)
    support_col_names = list(set(dict_columns.values()))
    files_to_test = len(tabs_list)
    global list_to_work
    for file in tabs_list:
        temp_frame = pd.DataFrame
        print("\n" + Fore.MAGENTA + "Проверяю файл:", file, Style.RESET_ALL)
        if file.endswith(".xlsx") | file.endswith(".xls"):
            temp_frame = pd.read_excel(file, header=None, nrows=test_frame_deep, index_col=None)
        elif file.endswith(".csv"):
            temp_frame = pd.read_csv(file, header=None, nrows=test_frame_deep, index_col=None)
        elif file.endswith(".txt"):
            temp_frame = pd.read_table(file, header=None, nrows=test_frame_deep, index_col=None)
        elif file.endswith(".xml"):
            temp_frame = xml_parse_to_pandas(file)
        else:
            print(Fore.RED + "\tТип данных не опознан:", file)
            print(Style.RESET_ALL)

        # check: data shape for minimal requirements
        if temp_frame.shape[1] > 4:
            c = temp_frame.shape[1] - 1  # num of iterations (for all columns tabs)
            print("\tОбнаружено столбцов:", c + 1)
            a = np.array([])  # array for collecting positions of rows with keywords
            b = dict_columns.keys()  # list of keywords from columns' voc (in human format)
            while c >= 0:  # checking columns name in test dataframe
                a = np.append(a, temp_frame.loc[temp_frame[c].isin(b)].index.values)
                c = c - 1
            a = a.tolist()  # convert np array to default list
            a = list(a)
            a_set = set(a)
            most_common = None  # var for most frequency row (with columns' names)
            qty_most_common = 0  # how much columns name detected in most common row
            for item in a_set:  # voting for row with columns' names
                qty = a.count(item)
                if qty > qty_most_common:
                    qty_most_common = qty
                    most_common = int(item)

            if qty_most_common >= 4:
                print('\tЗаголовки на строке: ', most_common + 1)
                temp_frame.columns = temp_frame.iloc[most_common]  # set header
                temp_frame.rename(columns=dict_columns, inplace=True)  # rename headers for sys names
                temp_frame = temp_frame.iloc[most_common + 1:]  # drop rows before headers
                col_list = list(temp_frame.columns)  # get a columns' list

                # check for minimal combination of columns and go on preview:
                if (col_list.count('type') > 0 and col_list.count('sim_a') > 0 and col_list.count('date') > 0) or \
                        (col_list.count('type') > 0 and col_list.count('sim_a') > 0 and col_list.count(
                            'date_time') > 0):

                    found_columns = list(set(col_list) & set(support_col_names))
                    print('\tРаспознано полей: ', len(found_columns), ' из ', temp_frame.shape[1])

                    # *****************CHECK TYPE BLOCK*******************
                    # set status vars to default:
                    ks_voc_status = False
                    life_col_status = False
                    abon_b_adr_status = False
                    type_tab_status = 'heap'
                    # check 'Life' type tab:
                    if col_list.count('sim_c') > 0:
                        life_col_status = True
                        type_tab_status = 'A'
                    # check for missing antenna information:
                    if col_list.count('adr_a') == 0 and col_list.count('adr_az') == 0:
                        ks_voc_status = True
                    # check for 'A' type signs
                    if len(temp_frame["sim_a"].unique()) == 1:
                        type_tab_status = 'A'
                    # check for 'B' type signs
                    if col_list.count('sim_b') == 1:
                        if len(temp_frame["sim_b"].unique()) == 1:
                            type_tab_status = 'B'
                    # checking information about the location of subscriber B
                    if col_list.count('adr_b') == 1:
                        if len(temp_frame["adr_b"].unique()) > 3:
                            abon_b_adr_status = True
                    # print('\tФайл похож на детализацию соединений мобильных терминалов ')
                    print("\tОпределен тип детализации: ", type_tab_status)

                    # adding a task to the scheduler:
                    global list_to_work
                    list_to_work.append([file, type_tab_status, abon_b_adr_status, life_col_status,
                                         ks_voc_status, most_common])
                    global tabs_to_work
                    tabs_to_work = tabs_to_work + 1

                    print('\tНаличие информации о местонахождении абонента "Б": ', dict_print.get(abon_b_adr_status))
                    print('\tТройная запись абонентов (формат "Астелит"):       ', dict_print.get(life_col_status))
                    print('\tНеобходимость подключеня внешних справочников БС:  ', dict_print.get(ks_voc_status))

                    # checking supported connection types:
                    used_types = temp_frame['type'].unique().tolist()
                    support_types = dict_types.keys()
                    new_types = list(set(used_types) - set(support_types))

                    if len(new_types) > 0:
                        print(Fore.RED + "\t\tВ тестовом фрагменте найдены незвестные типы соединений:")
                        for item in new_types:
                            print('\t\t', item)
                        print(Style.RESET_ALL)
                    # show unknown columns' names:
                    if len(found_columns) < len(col_list):
                        print(Fore.RED + "\t\tВ тестовом фрагменте найдены неизвестные заголовки столбцов:\n\t\t",
                              list(set(temp_frame.columns) - set(support_col_names)))
                        print(Style.RESET_ALL)
                else:
                    print(Fore.RED + "\tНедостаточно столбцов для анализа (минимально необходимы: "
                                     "тип, абонент А, дата и время)")
                    print('\t', list(set(temp_frame.columns) - set(support_col_names)))
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + "\tСлишком мало полей для дальнейшей работы. Проверь исходный файл")
                print(Style.RESET_ALL)

    files_accept = len(list_to_work)
    print('\n' + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + '************************РЕЗУЛЬТАТЫ ПРОВЕРКИ'
                                                           '************************')
    print("\tПроверено файлов:    " + Style.RESET_ALL, files_to_test)
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "\tДопущено к перегону: " + Style.RESET_ALL, files_accept)
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + '***********************************'
                                                    '********************************')
    print(Style.RESET_ALL)
    if files_accept == 0:
        print(Fore.RED + 'Нет файлов для анализа. Программа остановлена.' + Style.RESET_ALL)
        time.sleep(5)
        os.abort()


def scan_bs_voc():
    print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Поиск справочников БС Киевстар...")
    print(Style.RESET_ALL)
    for file in tabs_list:  # checking files for files with 4 columns
        if file.endswith(".xls") or file.endswith(".xlsx"):
            temp_frame = pd.read_excel(file, header=None, nrows=test_frame_deep, index_col=None)

            if temp_frame.shape[1] == 4:
                c = 3  # num of iterations (for 4 columns tabs)
                a = np.array([])  # array for collecting num of rows with keywords
                b = dict_bs.keys()  # keywords for BS voc (in human format)
                while c >= 0:  # checking columns name in test dataframe
                    a = np.append(a, temp_frame.loc[temp_frame[c].isin(b)].index.values)
                    c = c - 1
                a = a.tolist()
                a_set = set(a)
                a = list(a)
                most_common = None
                qty_most_common = 0
                for item in a_set:  # voting for row with columns' names
                    qty = a.count(item)
                    if qty > qty_most_common:
                        qty_most_common = qty
                        most_common = int(item)

                if qty_most_common >= 4:
                    print(Fore.GREEN + '\tОбнаружен файл похожий на справочник Киевстар - ', file,
                          '\n\tЗаголовки на строке №', most_common + 1, Style.RESET_ALL)
                    bs_frame = pd.read_excel(file, header=most_common)
                    bs_frame.rename(columns=dict_bs, inplace=True)
                    col_list = list(bs_frame.columns)
                    if col_list.count('LAC') == 1 and col_list.count('CID') == 1 and col_list.count(
                            'azimuth') == 1 and col_list.count('address') == 1:
                        print('\tФайл содержит записи о базовых станциях... Готовлю данные для работы...')

                        # 'to_numeric' shows Nan values (rows with bad data values)
                        bs_frame['azimuth'] = pd.to_numeric(bs_frame['azimuth'], downcast='unsigned', errors='coerce')
                        bs_frame['LAC'] = pd.to_numeric(bs_frame['LAC'], downcast='unsigned', errors='coerce')
                        bs_frame['CID'] = pd.to_numeric(bs_frame['CID'], downcast='unsigned', errors='coerce')

                        # kill rows without LAC or/both CID data
                        bs_frame = bs_frame.dropna(subset=['LAC', 'CID'])

                        # convert to integer LAC and CID values
                        bs_frame[['LAC']] = bs_frame[['LAC']].apply(np.uint32)
                        bs_frame[['CID']] = bs_frame[['CID']].apply(np.uint32)

                        bs_frame['azimuth'].replace([None], [999], inplace=True)  # empty azimuth data to '999'
                        bs_frame[['azimuth']] = bs_frame[['azimuth']].apply(np.uint32)  # set integer type
                        bs_frame['LACCID_key'] = bs_frame['LAC'].astype(str) + '-' + bs_frame['CID'].astype(str)
                        print("\tДанные о базовых станциях Киевстар:", bs_frame.shape[0], ' Добавляю в память.')
                        dict_address_bs.update(tuple(zip(bs_frame['LACCID_key'], bs_frame['address'])))
                        dict_azimuth.update(tuple(zip(bs_frame['LACCID_key'], bs_frame['azimuth'])))
                        print('\tОбразец данных:\n', Fore.LIGHTYELLOW_EX, bs_frame.iloc[[0, 1, 2, 3, 4], [0, 1, 2, 3]])
                        print(Style.RESET_ALL)
                        tabs_list.remove(file)

                    else:
                        print('\t', file, Fore.RED + '-формат не соответствует справочнику Киевстар, '
                                                     'отстутствуют необходимые столбцы')
                        print(Style.RESET_ALL)
                else:
                    print('\nПри проверке файла: "', file, '" обнаружены признаки справочника БС. \n\tПодписи колонок '
                                                           'не распознаны, проверьте заголовки' + Style.RESET_ALL)
            else:
                pass
                # print("\tСправочники базовых станций не обнаружены.")


def burning():
    print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "ЗАПУСКАЕМ ПЕРЕГОН!" + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + 'Обработка исходных файлов...' + Style.RESET_ALL)
    for i in list_to_work:
        global tabs_cur_level
        tabs_cur_level = 0
        file = i[0]
        tab_type = i[1]
        status_adr_b = i[2]
        status_life = i[3]
        status_bs_kyivstar = i[4]
        header_row = i[5]
        print(Fore.MAGENTA + '\n\n___________________________________________________'
                             '__________________________________________', Style.RESET_ALL)
        print(Fore.MAGENTA + 'Работаю с полным фреймом файла: ', file, Style.RESET_ALL)
        print('\tОпределенный исходный тип:', tab_type)
        print('\tНаличие информации о местонахождении абонента "Б": ', dict_print.get(status_adr_b))
        print('\tТройная запись абонентов (формат "Астелит"):       ', dict_print.get(status_life))
        print('\tНеобходимость подключеня внешних справочников БС:  ', dict_print.get(status_bs_kyivstar))
        # load a full frame:
        full_frame = pd.DataFrame
        if file.endswith(".xlsx") | file.endswith(".xls"):
            full_frame = pd.read_excel(file, header=header_row, index_col=None)
        elif file.endswith(".csv"):
            full_frame = pd.read_csv(file, header=header_row, index_col=None)
        elif file.endswith(".txt"):
            full_frame = pd.read_table(file, header=header_row, index_col=None)
        elif file.endswith(".xml"):
            full_frame = xml_parse_to_pandas(file)
            full_frame.columns = full_frame.iloc[header_row]
            full_frame = full_frame.iloc[header_row + 1:]  # drop rows before headers
        else:
            print(Fore.RED + "\tТип данных не опознан:", file)
            print(Style.RESET_ALL)
        rows_count = full_frame.shape[0]
        #print("\tЗаголовки на строке:  ", header_row + 1)
        full_frame.rename(columns=dict_columns, inplace=True)
        col_list = list(full_frame.columns)

        # --------------------------------------------convert TYPE:
        used_types = full_frame['type'].unique().tolist()
        support_types = dict_types.keys()
        new_types = list(set(used_types) - set(support_types))
        if len(new_types) > 0:
            print(Fore.RED + "\tНеизвестные типы соединений (заменяю на", unknown_con_type_def, "):")
            for un_type in new_types:
                print('\t\t\t', un_type)
            print(Style.RESET_ALL)
        full_frame.dropna(subset=['type', 'sim_a'], inplace=True)
        full_frame['type'] = full_frame['type'].map(dict_types)
        full_frame['type'].fillna(unknown_con_type_def, inplace=True)
        tabs_cur_level += 1

        # ------------------------------------convert DATE and TIME:


        if col_list.count('date_time') == 1 and col_list.count('date') == 0 and col_list.count('time') == 0:
            full_frame['date_time'] = pd.to_datetime(full_frame['date_time'], dayfirst=True, errors='coerce')
        elif col_list.count('date_time') == 0 and col_list.count('date') == 1 and col_list.count('time') == 1:
            full_frame['time'] = full_frame['time'].apply(lambda cell: convert_str_to_time(cell))
            full_frame['date_time'] = pd.to_datetime(full_frame['date'], dayfirst=True, errors='coerce') + full_frame['time']
        elif col_list.count('date_time') == 0 and col_list.count('date') == 1 and col_list.count('time') == 0:
            full_frame['date_time'] = pd.to_datetime(full_frame['date'], dayfirst=True, errors='coerce')

        full_frame.dropna(subset=['date_time'], inplace=True)
        full_frame['date'] = full_frame['date_time'].dt.strftime('%d.%m.%Y')
        full_frame['time'] = full_frame['date_time'].dt.strftime('%H:%M:%S')
        tabs_cur_level += 1

        # ----------------------------------------convert DURATION:
        full_frame['dur'] = full_frame['dur'].apply(lambda cell: check_dur(cell))
        full_frame['dur_str'] = full_frame['dur'].astype(str).str[-8:]
        tabs_cur_level += 1

        # ------------------------------------------convert SIM A:
        full_frame['sim_a'] = full_frame['sim_a'].apply(lambda x: check_number(x))
        tabs_cur_level += 1

        # ------------------------------------------convert SIM B:
        # create sim_b for ASTELIT type:
        if list(full_frame.columns).count('sim_b') == 0 and list(full_frame.columns).count('sim_c') == 1 and \
           list(full_frame.columns).count('sim_d') == 1:
            full_frame['sim_b'] = full_frame.apply(lambda row: choice_sim_b(row), axis=1)
        # checking number mask:
        if list(full_frame.columns).count('sim_b') == 1:
            full_frame['sim_b'] = full_frame['sim_b'].apply(lambda x: check_number(x))

        #if have no column for subscriber B:
        if list(full_frame.columns).count('sim_b') == 0 and list(full_frame.columns).count('ip') == 1:
            full_frame['sim_b'] = full_frame['ip']
        tabs_cur_level += 1

        # -----------------------------------------convert IMEI A|B:
        if list(full_frame.columns).count('imei_a') > 0:
            full_frame['imei_a'] = full_frame['imei_a'].apply(lambda x: check_imei(x))
        if list(full_frame.columns).count('imei_b') > 0:
            full_frame['imei_b'] = full_frame['imei_b'].apply(lambda x: check_imei(x))
        tabs_cur_level += 1

        #------------------------------------------convert LAC|CID:
        if list(full_frame.columns).count('lac_a') > 0:
            full_frame['lac_a'] = full_frame['lac_a'].apply(lambda x: check_laccid(x))
        if list(full_frame.columns).count('lac_b') > 0:
            full_frame['lac_b'] = full_frame['lac_b'].apply(lambda x: check_laccid(x))
        if list(full_frame.columns).count('cid_a') > 0:
            full_frame['cid_a'] = full_frame['cid_a'].apply(lambda x: check_laccid(x))
        if list(full_frame.columns).count('cid_b') > 0:
            full_frame['cid_b'] = full_frame['cid_b'].apply(lambda x: check_laccid(x))
        tabs_cur_level += 1

        #-------------------------------USE KYIVSTAR BS HANDBOOK:
        if status_bs_kyivstar is True:
            full_frame['adr_a'] = full_frame.apply(lambda x: combine_lac_cid(x), axis=1)
            full_frame['adr_a'] = full_frame['adr_a'].map(dict_address_bs)
            full_frame['az_a'] = full_frame.apply(lambda x: combine_lac_cid(x), axis=1)
            full_frame['az_a'] = full_frame['az_a'].map(dict_azimuth)

        #-----------------------------FILL NAN BS & AZIMUTH CELLS:
        if list(full_frame.columns).count('adr_a') > 0:
            full_frame['adr_a'] = full_frame['adr_a'].fillna('')
        if list(full_frame.columns).count('adr_b') > 0:
            full_frame['adr_b'] = full_frame['adr_b'].fillna('')
        tabs_cur_level += 1

        #------------------------------------------convert AZIMUTH:
        if list(full_frame.columns).count('az_a') == 0 and list(full_frame.columns).count('adr_az') == 1:
            full_frame['az_a'] = full_frame['adr_az'].apply(lambda x: azimut_from_adress(x))
            full_frame['adr_a'] = full_frame['adr_az'].apply(lambda x: remove_azimuth_from_long_row(x))
        if list(full_frame.columns).count('adr_a') > 0:
            full_frame['adr_a'] = full_frame['adr_a'].fillna('')
        if list(full_frame.columns).count('adr_b') > 0:
            full_frame['adr_b'] = full_frame['adr_b'].fillna('')

        if list(full_frame.columns).count('az_a') > 0:
            full_frame['az_a'] = full_frame['az_a'].apply(check_azimut)
        if list(full_frame.columns).count('az_b') > 0:
            full_frame['az_b'] = full_frame['az_b'].apply(check_azimut)
        tabs_cur_level += 1

        #------------------------------------connect EMPTY COLUMNS:
        absent_columns = list(set(render_b_col_set) - set(full_frame.columns))
        if len(absent_columns) > 0:
            for col in absent_columns:
                full_frame[col] = ''
        tabs_cur_level += 1

        #------------------------------------KILL SERVICE COLUMNS:
        col_list_to_drop = list(set(full_frame.columns) - set(analysis_columns_set))
        full_frame.drop(col_list_to_drop, axis='columns', inplace=True)

        #-----------------------------------------KILL DUPLICATES:
        rows_count_wo_nan = int(full_frame.shape[0])
        full_frame.drop_duplicates(inplace=True, ignore_index=True)
        rows_after_duplicatesdrop = int(full_frame.shape[0])

        #-------------------------------------------PRINT TO FILE:
        print("\t______________________")
        print("\tВсего строк в таблице:", rows_count)
        print('\tЗаписей о соединениях:', rows_count_wo_nan)
        print('\tУдалено дубликатов:   ', rows_count_wo_nan - rows_after_duplicatesdrop)
        print('\tЗаписей в результате: ', rows_after_duplicatesdrop)
        print("\t----------------------")

        file_name = str(file)
        file_name = file_name.split(sep='.')
        del file_name[len(file_name)-1]
        file_name = '.'.join(file_name)

        # save dataframe to heap (concat):
        if su_save_heap is True:
            print(Fore.GREEN + '\t\tЗаписываю соединения в общий файл "HEAP"' + Style.RESET_ALL)
            global heap
            heap = pd.concat([heap, full_frame], ignore_index=True, sort=False)

        # save dataframe to separate file ('file-to-file')
        if su_save_file_to_file is True:
            print(Fore.GREEN + '\t\tФормирую отдельный файл "file-to-file": FtF_', file_name, '.xlsx'
                  + Style.RESET_ALL, sep='')
            if su_sort_subscriber is True:
                full_frame.sort_values(by=['sim_a', 'date_time'], inplace=True)
            elif su_sort_datetime is True:
                full_frame.sort_values(by=['date_time'], inplace=True)

            if status_adr_b is True:
                full_frame.to_excel('FtF_' + file_name + '.xlsx',
                                    columns=render_b_col_set,
                                    header=render_b_header_set,
                                    index=None)
            else:
                full_frame.to_excel('FtF_' + file_name + '.xlsx',
                                    columns=render_a_col_set,
                                    header=render_a_header_set,
                                    index=None)

        # divide separate subscriber to new dataframes:
        if (su_save_divide_by_subscriber is True or su_merge_ab_types is True) and int(full_frame.shape[0]) > 0:
            global separate_abon_list, extract_a_list, extract_a_df, extract_b_list, extract_b_df, \
                combine_subscribers_list, combine_subscribers_df

            uniq_sim_a_names = full_frame['sim_a'].unique().tolist()
            uniq_sim_b_names = full_frame['sim_b'].unique().tolist()
            uniq_sim_a_count = len(uniq_sim_a_names)
            uniq_sim_b_count = len(uniq_sim_b_names)
            print('\n\t\tАвтоматическая разбивка по абонентам А/Б/А+Б:')
            print('\t\t\tУникальных абонентов А:', uniq_sim_a_count)
            print('\t\t\tУникальных абонентов Б:', uniq_sim_b_count)

            if status_adr_b is False and uniq_sim_a_count == 1:
                print('\t\t\tОпределен тип "А" - формирую отдельный датафрейм для абонента ', uniq_sim_a_names[0])
                extract_a_list = list(set(uniq_sim_a_names + extract_a_list))
                extract_a_df = pd.concat([extract_a_df, full_frame], ignore_index=True, sort=False)
            elif status_adr_b is False and uniq_sim_a_count < 8:
                print('\t\t\tОпределен тип "А" - обнаружена информация о нескольких абонентах:')
                for name in uniq_sim_a_names:
                    print('\t\t\t\t', name)
                extract_a_list = list(set(uniq_sim_a_names + extract_a_list))
                extract_a_df = pd.concat([extract_a_df, full_frame], ignore_index=True, sort=False)
            elif status_adr_b is True and uniq_sim_a_count == 1:
                print('\t\t\tОпределен тип "А+Б" - формирую отдельный датафрейм для абонента ', uniq_sim_a_names[0])
                combine_subscribers_list = list(set(uniq_sim_a_names + combine_subscribers_list))
                combine_subscribers_df = pd.concat([combine_subscribers_df, full_frame], ignore_index=True, sort=False)
            elif status_adr_b is False and uniq_sim_b_count == 1:
                print('\t\t\tОпределен тип "Б" - формирую отдельный датафрейм для абонента ', uniq_sim_b_names[0])
                extract_b_list = list(set(uniq_sim_b_names + extract_b_list))
                extract_b_df = pd.concat([extract_b_df, full_frame], ignore_index=True, sort=False)
            elif status_adr_b is True and uniq_sim_b_count == 1:
                print('\t\t\tВ файле имеються обе колонки адреса БС (А и Б), тип определен как Б - нетипичный формат'
                      '\n\t\t\tСохраняю без разбивки - "file-to-file"')
                full_frame.to_excel('res-'+str(uniq_sim_b_names[0])+'-B(with-addr-B).xlsx',
                                    columns=render_b_col_set,
                                    header=render_b_header_set,
                                    index=None)
            else:
                print(Fore.RED + '\t\t\tФайл смешанного типа. Пропускаю файл.' + Style.RESET_ALL)
        #-------------------------------------------END ITER:
        global tabs_done
        global tabs_to_work
        tabs_to_work -= 1
        tabs_done += 1
        print('\n')


def save_heap():
    if su_save_heap is True:
        print(
            "\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Записываю в общий файл, сортирую по времени соединений..."
            + Style.RESET_ALL)
        heap_count_rows = int(heap.shape[0])
        heap.drop_duplicates(ignore_index=True, inplace=True)
        heap_count_after_dup = int(heap.shape[0])
        print(Fore.GREEN + '\tВсего записей:', heap_count_rows)
        print('\tУдалено дубликатов:', heap_count_rows - heap_count_after_dup)
        print('\tВсего записано:', heap_count_after_dup, Style.RESET_ALL)
        heap.sort_values(by=['date_time'], inplace=True)
        heap.to_excel('heap.xlsx',
                      columns=render_a_col_set,
                      header=render_a_header_set,
                      index=None)


def save_divide_by_subscribers():
    if su_save_divide_by_subscriber is True:
        print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Автоматическая разбивка по абонентам А/Б. "
                                                               "Создание отдельных файлов:" + Style.RESET_ALL)
        if len(extract_a_list) == 0 and len(extract_b_list) == 0:
            print(Fore.RED + '\tНе обнаружены таблицы отдельных абонентов, разбивка не проведена' + Style.RESET_ALL)
        else:
            if len(extract_a_list) > 0:
                for subscriber in extract_a_list:
                    frame_temp = extract_a_df.loc[extract_a_df.sim_a == subscriber].copy()
                    frame_temp.drop_duplicates(inplace=True, ignore_index=True)
                    frame_temp.sort_values(by=['date_time'], inplace=True)
                    frame_temp.to_excel('format_' + str(subscriber) + '_A.xlsx',
                                        columns=render_a_col_set,
                                        header=render_a_header_set,
                                        index=None)
                    print(Fore.GREEN + "\tЗаписан файл: format_", subscriber, '_A.xlsx - ', str(frame_temp.shape[0]),
                          ' соединений' + Style.RESET_ALL, sep='')
            if len(extract_b_list) > 0:
                for subscriber in extract_b_list:
                    frame_temp = extract_b_df.loc[extract_b_df.sim_b == subscriber].copy()
                    frame_temp.drop_duplicates(inplace=True, ignore_index=True)
                    frame_temp.sort_values(by=['date_time'], inplace=True)
                    frame_temp.to_excel('format_' + str(subscriber) + '_B.xlsx',
                                        columns=render_a_col_set,
                                        header=render_a_header_set,
                                        index=None)
                    print(Fore.GREEN + "\tЗаписан файл: format_", subscriber, '_B.xlsx - ', str(frame_temp.shape[0]),
                          ' соединений' + Style.RESET_ALL, sep='')


def merge_types():
    global combine_subscribers_df, combine_subscribers_list
    if su_merge_ab_types is True:
        print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Объединение таблиц 'А' и 'Б'. Запись отдельных файлов:"
              + Style.RESET_ALL)
        for subscriber in extract_a_list:
            if extract_b_list.count(subscriber) == 0:
                print(Fore.RED + '\tДля абонента: ', subscriber, " - нет информации по типу 'Б'. Пропускаю абонента..."
                      + Style.RESET_ALL)
            elif extract_b_list.count(subscriber) == 1 and extract_a_list.count(subscriber) == 1:
                frame_a = extract_a_df.loc[extract_a_df.sim_a == subscriber].copy()
                frame_b = extract_b_df.loc[extract_b_df.sim_b == subscriber].copy()
                frame_a.drop(['lac_b', 'cid_b', 'adr_b', 'az_b', 'imei_b'], axis='columns', inplace=True)
                frame_b.drop(['lac_b', 'cid_b', 'adr_b', 'az_b', 'imei_b'], axis='columns', inplace=True)
                frame_b.rename(columns={'az_a': 'az_b', 'adr_a': 'adr_b', 'lac_a': 'lac_b', 'cid_a': 'cid_b',
                                        'sim_a': 'sim_b', 'sim_b': 'sim_a', 'imei_a': 'imei_b'}, inplace=True)
                frame_b['type'] = frame_b['type'].map(dict_invert_types)
                print(Fore.GREEN + '\tДля абонента: ', subscriber, " :\n\t\tСоединений в таблице А - ",
                      str(frame_a.shape[0]),  " :\n\t\tСоединений в таблице Б - ", str(frame_b.shape[0]), " "
                      + Style.RESET_ALL)
                frame_merge = pd.concat([frame_a, frame_b], ignore_index=True, sort=False)
                frame_merge.sort_values(by='date_time', inplace=True)
                frame_merge.reset_index(inplace=True, drop=True)
                list_to_drop = []
                for i in range(1, int(frame_merge.shape[0]-1)):
                    cur_adr_b = frame_merge.at[i, 'adr_b']
                    if type(cur_adr_b) is str:
                        cur_dt = frame_merge.at[i, 'date_time']
                        cur_sim = frame_merge.at[i, 'sim_b']
                        cur_type = frame_merge.at[i, 'type']

                        up_dt = frame_merge.at[i-1, 'date_time']
                        up_sim = frame_merge.at[i-1, 'sim_b']
                        up_type = frame_merge.at[i-1, 'type']
                        dif_up_dt = cur_dt - up_dt
                        if dif_up_dt < pd.Timedelta('0ms'):
                            dif_up_dt = dif_up_dt * (-1)

                        down_dt = frame_merge.at[i+1, 'date_time']
                        down_sim = frame_merge.at[i+1, 'sim_b']
                        down_type = frame_merge.at[i+1, 'type']
                        dif_down_dt = cur_dt - down_dt
                        if dif_down_dt < pd.Timedelta('0ms'):
                            dif_down_dt = dif_down_dt * (-1)

                        if cur_sim == up_sim and cur_type == up_type and dif_up_dt < pd.Timedelta('2s') \
                                and i-1 not in set(list_to_drop):
                            frame_merge.at[i-1, 'lac_b'] = frame_merge.at[i, 'lac_b']
                            frame_merge.at[i-1, 'cid_b'] = frame_merge.at[i, 'cid_b']
                            frame_merge.at[i-1, 'az_b'] = frame_merge.at[i, 'az_b']
                            frame_merge.at[i-1, 'adr_b'] = frame_merge.at[i, 'adr_b']
                            frame_merge.at[i-1, 'imei_b'] = frame_merge.at[i, 'imei_b']
                            list_to_drop.append(int(i))

                        elif cur_sim == down_sim and cur_type == down_type and dif_down_dt < pd.Timedelta('1300ms') \
                                and i+1 not in set(list_to_drop):
                            frame_merge.at[i+1, 'lac_b'] = frame_merge.at[i, 'lac_b']
                            frame_merge.at[i+1, 'cid_b'] = frame_merge.at[i, 'cid_b']
                            frame_merge.at[i+1, 'az_b'] = frame_merge.at[i, 'az_b']
                            frame_merge.at[i+1, 'adr_b'] = frame_merge.at[i, 'adr_b']
                            frame_merge.at[i+1, 'imei_b'] = frame_merge.at[i, 'imei_b']
                            list_to_drop.append(int(i))

                frame_merge.drop(list_to_drop, inplace=True)
                print(Fore.GREEN + '\t\t\tОбъединено строк Б - ', str(int(len(list_to_drop))))
                print(Fore.GREEN + '\t\t\tДобавлено  строк Б - ', str(int(frame_b.shape[0])-int(len(list_to_drop))))
                print('\t\tВсего в файл записано - ', str(int(frame_merge.shape[0])))
                print(Style.RESET_ALL)
                combine_subscribers_df = pd.concat([combine_subscribers_df, frame_merge], ignore_index=True, sort=False)
                combine_subscribers_list.append(subscriber)

        for subscriber in combine_subscribers_list:
            export_df = combine_subscribers_df.loc[combine_subscribers_df.sim_a == subscriber]
            export_df.to_excel('format_' + str(subscriber) + '_A+B.xlsx', engine='xlsxwriter',
                               columns=render_b_col_set,
                               header=render_b_header_set,
                               index=None)


def get_merged_subscribers_list():
    return combine_subscribers_list


def get_a_subscribers_list():
    return extract_a_list


def get_b_subscribers_list():
    return extract_b_list


def export_merged_tab(subscriber):
    return combine_subscribers_df.loc[combine_subscribers_df.sim_a == subscriber]


def export_subscriber_a_tab(subscriber):
    return extract_a_df.loc[extract_a_df.sim_a == subscriber]


def export_subscriber_b_tab(subscriber):
    return extract_b_df.loc[extract_b_df.sim_b == subscriber]


def export_heap():
    return heap
