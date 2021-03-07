import os
import time
import numpy as np
from colorama import Back
from lxml import etree as et

from .columns_functions import *
from config.config_math import config_get_dict


counter_bs = 0  # відсоток опрацьованих файлів у функції пошуку довідників БС (для прогресбару)
counter_files = 0  # відсоток опрацьованих файлів з інформацією про з*єднання

FILE_PATH = 0
FILE_NAME = 1
FILE_SIZE = 2
FILE_FOOTPRINT = 3
RECORDS_DETECTED = 4
RECORDS_CONVERTED = 5
COLUMNS_DETECTED = 6
COLUMNS_CONVERTED = 7
TYPES_DETECTED = 8
TYPES_CONVERTED = 9
SIMA_UNIQ = 10
SIMB_UNOQ = 11
IMEIA_UNIQ = 12
IMEIB_UNIQ = 13
LAC_UNIQ = 14
BS_UNIQ = 15
BS_ADR_FIND = 16
FUNC_SIM_CHOICE = 17
FUNC_FORW_CHOICE = 18
FUNC_BS_VOC = 19
TYPE_FOUND = 20
TAB_LOG = 21

DEEP = 100  # num of rows for testing tab's type

# -------------------------------------------------------------------------------------
# ---------------------------------PROGRAM SETTINGS VARS-------------------------------
# -------------------------------------------------------------------------------------

#Список з файлами для опрацювання. Отримується з файлів обраних користувачем в діалоговому вікні.
#Перевіряється на повторне введення одного й того ж файлу.
#Зберігає відомості про файл: абсолютний шлях(0), назва файлу(1), розмір(2), Колонки(3), Типи (4), Соти(5), Тип(6)
#До перегону таблиць містить відомості тільки про шлях, назву файлу та розмір:
# sheets_list_prepared = []


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


def xml_parse_to_pandas(file_name):
    parser = et.XMLParser(recover=True, huge_tree=True)
    tree = et.parse(file_name, parser)
    root = tree.getroot()
    row_num = 0
    data_all_dict = {}
    table = root.find('.//{urn:schemas-microsoft-com:office:spreadsheet}Table')
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





def convert_all(files_sheet: list):
    print('func started')
    global counter_bs  # для відображення прогресбару
    global counter_files
    counter_bs = 0  # скидання прогресбару на нуль перед початком опрацювання
    counter_files = 0

    main_data_frame = pd.DataFrame()  # всі придатні записи додаються до цього фрейму та повертаються результатом
    sheets_list_uploaded = files_sheet.copy()  # копія полотна з вхідними файлами
    separated_sims = []
    dict_bs_adr = {}  # збірник з відомостями про адреси БС (ключ(ЛАК+СІД): значення(строка з адресою))
    dict_bs_azi = {}  # збірник з відомостями про азимути БС (ключ(ЛАК+СІД): значення(азимут))
    bs_files = []  # список файлів (шлях з найменуванням) в яких знайдено довідники (для ігнорування конвертером)

    file_weight_bs = 100/len(sheets_list_uploaded)  # вага одного файлу для корекції статусбару

    for row in range(len(sheets_list_uploaded)):
        try:
            temp_dict_adr, temp_dict_azi, errors = search_bs_voc(sheets_list_uploaded[row], file_weight_bs)
            # повертаються два словники для проставлення адрес БС у таблицях, помилки додаються до відомостей полотна
            if temp_dict_adr is not None:
                dict_bs_adr.update(temp_dict_adr)
                dict_bs_azi.update(temp_dict_azi)
                sheets_list_uploaded[row][BS_UNIQ] = len(temp_dict_adr)
                sheets_list_uploaded[row][BS_ADR_FIND] = len(temp_dict_adr)
                sheets_list_uploaded[row][TYPE_FOUND] = "Довідник БС"
                sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) \
                                                     + '\nДо опрацювання файлів додано відомості про розміщення ' \
                                                       'базових станцій зв\'язку у кількості - ' \
                                                     + str(len(temp_dict_adr))
                if errors != '':
                    sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) + str(errors)
                bs_files.append(sheets_list_uploaded[row][FILE_PATH])
        except Exception as ex:
            print('exception')
            print(ex)
            sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) + \
                                            str('\nПомилка при спробі перевірити наявність словників базових станцій '
                                                'зв\'язку, файл не використовується у формуванні відомостей про '
                                                'розміщення БС')
        print(sheets_list_uploaded[row])
    counter_bs = 100
    return main_data_frame, sheets_list_uploaded, separated_sims


def search_bs_voc(file, weight):
    print('started bsvoc func')
    global counter_bs
    bs_adr = {}
    bs_azi = {}
    errors = ''
    columns_dict = {}
    columns_dict.update(config_get_dict('columns_dict_adr_a'))
    columns_dict.update(config_get_dict('columns_dict_az_a'))
    columns_dict.update(config_get_dict('columns_dict_cid_a'))
    columns_dict.update(config_get_dict('columns_dict_lac_a'))
    # --------------------------В РОБОТІ ЧЕРНЕТКА
    if file[FILE_PATH].endswith(".xls") or file[FILE_PATH].endswith(".xlsx"):
        temp_frame = pd.read_excel(file[FILE_PATH], header=None, nrows=DEEP, index_col=None)
        if temp_frame.shape[1] == 4:
            col_iter = 3  # кількість ітерацій для перевірки 4 колонок
            rows_occur = []  # список для накопичення номерів рядків в яких виявлено заголовки довідника
            keywords = columns_dict.keys()  # список розпізнання
            while col_iter >= 0:  # перебір колонок
                # перевірка наявності записів з урахуванням нижнього регістру:
                res_series = temp_frame[temp_frame[col_iter].str.lower().isin([x.lower() for x in keywords])]
                # накопичення рядків у яких знайдено заголовки:
                rows_occur = rows_occur + list(res_series.index.values)
                col_iter = col_iter - 1  # підготовка до наступної ітерації
            rows_set = set(rows_occur)
            most_common = None
            qty_most_common = 0
            for item in rows_set:  # перебір унікальних номерів рядків
                qty = rows_occur.count(item)
                if qty > qty_most_common:
                    qty_most_common = qty
                    most_common = int(item)
            del temp_frame

            if qty_most_common >= 4:
                bs_frame = pd.read_excel(file[FILE_PATH], header=most_common)
                bs_frame.columns = bs_frame.columns.str.lower()
                bs_frame.rename(columns=columns_dict, inplace=True)
                col_list = list(bs_frame.columns)
                if col_list.count('lac_a') == 1 and col_list.count('cid_a') == 1 and col_list.count(
                        'az_a') == 1 and col_list.count('adr_a') == 1:
                    # 'to_numeric' shows Nan values (rows with bad data values)
                    bs_frame['az_a'] = pd.to_numeric(bs_frame['az_a'], downcast='unsigned', errors='coerce')
                    bs_frame['lac_a'] = pd.to_numeric(bs_frame['lac_a'], downcast='unsigned', errors='coerce')
                    bs_frame['cid_a'] = pd.to_numeric(bs_frame['cid_a'], downcast='unsigned', errors='coerce')

                    # kill rows without LAC or/both CID data
                    bs_frame = bs_frame.dropna(subset=['lac_a', 'cid_a'])

                    # convert to integer LAC and CID values
                    bs_frame[['lac_a']] = bs_frame[['lac_a']].apply(np.uint32)
                    bs_frame[['cid_a']] = bs_frame[['cid_a']].apply(np.uint32)

                    bs_frame['az_a'].replace([None], [999], inplace=True)  # empty azimuth data to '999'
                    bs_frame[['az_a']] = bs_frame[['az_a']].apply(np.uint32)  # set integer type
                    bs_frame['lac_cid'] = bs_frame['lac_a'].astype(str) + '-' + bs_frame['cid_a'].astype(str)
                    bs_adr.update(tuple(zip(bs_frame['lac_cid'], bs_frame['adr_a'])))
                    bs_azi.update(tuple(zip(bs_frame['lac_cid'], bs_frame['az_a'])))
                    errors = errors + str('\n') + str(bs_frame.iloc[[0, 1, 2, 3, 4], [0, 1, 2, 3]])
                    print(bs_frame.iloc[[0, 1, 2, 3, 4], [0, 1, 2, 3]])
                else:
                    bs_adr = None
                    bs_azi = None
                    errors = ''
            else:
                bs_adr = None
                bs_azi = None
                errors = ''
        else:
            bs_adr = None
            bs_azi = None
            errors = ''

    # --------------------------ЗАВЕРШЕННЯ ЧЕРНЕТКИ
    counter_bs += weight
    return bs_adr, bs_azi, errors



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
