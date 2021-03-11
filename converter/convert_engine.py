from config.const_conv import *

import numpy as np
from lxml import etree as et

from .columns_functions import pd, check_dur, check_number, choice_sim_b, choice_sim_b_forw, check_imei, check_laccid, \
    combine_lac_cid, azimut_from_adress, remove_azimuth_from_long_row, check_azimut
from config.config_math import config_get_dict, config_get_options, config_get_value


counter_bs = 0  # відсоток опрацьованих файлів у функції пошуку довідників БС (для прогресбару)
counter_files = 0  # відсоток опрацьованих файлів з інформацією про з*єднання
current_file = ''
current_action = ''

DEEP = 100  # num of rows for testing tab's type

# -------------------------------------------------------------------------------------
# ---------------------------------PROGRAM SETTINGS VARS-------------------------------
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# ------------------------------HELPERS VARS (SERVICE VARS)----------------------------
# -------------------------------------------------------------------------------------
separate_abon_list = []

# -------------------------------------------------------------------------------------
# ------------------------MAIN DICTIONARIES FOR UNDERSTAND DATA------------------------
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# -------------------------------------MAIN DEFINES------------------------------------
# -------------------------------------------------------------------------------------

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
heap = pd.DataFrame(columns=config_get_options('main_frame_columns_set'))

extract_a_df = pd.DataFrame(columns=render_b_col_set + ['date_time'])
extract_b_df = pd.DataFrame(columns=render_b_col_set + ['date_time'])
combine_subscribers_df = pd.DataFrame(columns=analysis_columns_set)

extract_a_list = []
extract_b_list = []
combine_subscribers_list = []


# -------------------------------------------------------------------------------------
# -------------------------------CONVERTER'S FUNCTIONS---------------------------------
# -------------------------------------------------------------------------------------
def list_to_sring(list_in):
    return str(list_in).strip('[]')


def convert_str_to_time(cell):
    time_cell = str(cell)
    time_cell = pd.to_timedelta(time_cell)
    return time_cell


def add_log_text(log_cell:str, log_text: str):
    if log_cell.endswith('\n'):
        new_log_cell = log_cell + log_text
    elif log_cell == '':
        new_log_cell = log_text
    else:
        new_log_cell = log_cell + str('\n') + log_text
    return new_log_cell


def get_columns_map_dict():
    dict_map = {}
    dict_map.update(config_get_dict('columns_dict_adr_a'))
    dict_map.update(config_get_dict('columns_dict_adr_b'))
    dict_map.update(config_get_dict('columns_dict_az_a'))
    dict_map.update(config_get_dict('columns_dict_az_b'))
    dict_map.update(config_get_dict('columns_dict_cid_a'))
    dict_map.update(config_get_dict('columns_dict_cid_b'))
    dict_map.update(config_get_dict('columns_dict_date'))
    dict_map.update(config_get_dict('columns_dict_dur'))
    dict_map.update(config_get_dict('columns_dict_imei_a'))
    dict_map.update(config_get_dict('columns_dict_imei_b'))
    dict_map.update(config_get_dict('columns_dict_column_ignore'))
    dict_map.update(config_get_dict('columns_dict_lac_a'))
    dict_map.update(config_get_dict('columns_dict_lac_b'))
    dict_map.update(config_get_dict('columns_dict_lac_cid'))
    dict_map.update(config_get_dict('columns_dict_sim_a'))
    dict_map.update(config_get_dict('columns_dict_sim_b'))
    dict_map.update(config_get_dict('columns_dict_sim_c'))
    dict_map.update(config_get_dict('columns_dict_sim_d'))
    dict_map.update(config_get_dict('columns_dict_time'))
    dict_map.update(config_get_dict('columns_dict_type'))
    dict_map.update(config_get_dict('columns_dict_forw'))
    dict_map.update(config_get_dict('columns_dict_date_end'))
    dict_map.update(config_get_dict('columns_dict_desc_a'))
    dict_map.update(config_get_dict('columns_dict_desc_b'))
    return dict_map


def get_types_map_dict():
    dict_map = {}
    dict_map.update(config_get_dict('types_dict_network'))
    dict_map.update(config_get_dict('types_dict_voice_out'))
    dict_map.update(config_get_dict('types_dict_message_out'))
    dict_map.update(config_get_dict('types_dict_voice_in'))
    dict_map.update(config_get_dict('types_dict_message_in'))
    dict_map.update(config_get_dict('types_dict_forwarding'))
    return dict_map


def find_header_in_df(columns_dict, temp_frame):
    col_iter = temp_frame.shape[1] - 1  # кількість ітерацій для перевірки всіх колонок
    rows_occur = []  # список для накопичення номерів рядків в яких виявлено заголовки
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
    if qty_most_common == 0:
        return None, None
    else:
        return most_common, qty_most_common


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
    print('Converting started...')
    global counter_bs  # для відображення прогресбару
    global counter_files
    global current_file
    global current_action
    counter_bs = 0  # скидання прогресбару на нуль перед початком опрацювання
    counter_files = 0

    main_data_frame = pd.DataFrame(columns=config_get_options('main_frame_columns_set'))  # всі придатні записи додаються до цього фрейму та повертаються результатом
    sheets_list_uploaded = files_sheet.copy()  # копія полотна з вхідними файлами
    separated_sims = []
    dict_bs_adr = {}  # збірник з відомостями про адреси БС (ключ(ЛАК+СІД): значення(строка з адресою))
    dict_bs_azi = {}  # збірник з відомостями про азимути БС (ключ(ЛАК+СІД): значення(азимут))
    bs_files = []  # список файлів (шлях з найменуванням) в яких знайдено довідники (для ігнорування конвертером)

    file_weight = int(100/len(sheets_list_uploaded))  # вага одного файлу для корекції статусбару

    # -------------------------------
    # ---ОПРАЦЮВАННЯ ДОВІДНИКІВ БС---
    # -------------------------------
    for row in range(len(sheets_list_uploaded)):
        sheets_list_uploaded[row][TAB_LOG] = ''
        try:
            temp_dict_adr, temp_dict_azi, errors = search_bs_voc(sheets_list_uploaded[row])
            # повертаються два словники для проставлення адрес БС у таблицях, помилки додаються до відомостей полотна
            if temp_dict_adr is not None:
                dict_bs_adr.update(temp_dict_adr)
                dict_bs_azi.update(temp_dict_azi)
                sheets_list_uploaded[row][BS_A_UNIQ] = len(temp_dict_adr)
                sheets_list_uploaded[row][ADR_A_UNIQ] = len(temp_dict_adr)
                sheets_list_uploaded[row][TYPE_FOUND] = "Довідник БС"
                if errors != '':
                    sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) + str(errors)
                sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) \
                                                     + '\nДо опрацювання файлів додано відомості про розміщення ' \
                                                       'базових станцій зв\'язку у кількості - ' \
                                                     + str(len(temp_dict_adr))
                bs_files.append(sheets_list_uploaded[row][FILE_PATH])
                counter_bs += file_weight
        except ValueError as ex:
            print('Помилка під час перевірки файлу ' + str(sheets_list_uploaded[row][FILE_NAME])
                  + 'на наявність довідників, виключення:')
            print(ex)
            sheets_list_uploaded[row][TAB_LOG] = str(sheets_list_uploaded[row][TAB_LOG]) + \
                                            str('\nКритична помилка при перевірці наявності словників базових станцій '
                                                'зв\'язку, файл не використовується у формуванні відомостей про '
                                                'розміщення БС')
            counter_bs += file_weight
    counter_bs = 100


    # ------------------------------
    # -----ОПРАЦЮВАННЯ ТАБЛИЦЬ -----
    # ------------------------------
    for row in range(len(sheets_list_uploaded)):
        if sheets_list_uploaded[row][FILE_PATH] in bs_files:
            counter_files += file_weight
            continue
        try:
            new_row, temp_df = burning(sheets_list_uploaded[row], dict_bs_adr, dict_bs_azi)
            sheets_list_uploaded[row] = new_row
            main_data_frame = pd.concat([main_data_frame, temp_df], ignore_index=True, sort=False)
            counter_files += file_weight
        except Exception as burn_ex:
            print('EXCEPTION')
            print(burn_ex)
            sheets_list_uploaded[row][TAB_LOG] = 'Критична помилка у функції burning - ' + str(burn_ex)
            counter_files += file_weight

    counter_files = 99
    current_file = 'Майже завершено...'
    current_action = 'Видаляю дублікати записів...'
    main_data_frame.drop_duplicates(ignore_index=True, inplace=True)
    current_action = 'Сортую записи датафрейму...'
    main_data_frame.sort_values(by=['date_time'], inplace=True)
    counter_files = 100
    print(sheets_list_uploaded)
    return main_data_frame, sheets_list_uploaded


def search_bs_voc(file):
    global counter_bs
    bs_adr = {}
    bs_azi = {}
    errors = ''
    columns_dict = {}
    columns_dict.update(config_get_dict('columns_dict_adr_a'))
    columns_dict.update(config_get_dict('columns_dict_az_a'))
    columns_dict.update(config_get_dict('columns_dict_cid_a'))
    columns_dict.update(config_get_dict('columns_dict_lac_a'))

    if file[FILE_PATH].endswith(".xls") or file[FILE_PATH].endswith(".xlsx"):
        temp_frame = pd.read_excel(file[FILE_PATH], header=None, nrows=DEEP, index_col=None)
        if temp_frame.shape[1] == 4:
            header_row, headers_located = find_header_in_df(columns_dict, temp_frame)
            errors = add_log_text(errors, 'Виявлено структуру схожу на довідник БС, перевіряю заголовки...')
            del temp_frame

            if headers_located == 4:
                errors = add_log_text(errors, str('Заголовки довідника на рядку - ' + str(header_row+1)))
                bs_frame = pd.read_excel(file[FILE_PATH], header=header_row)
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
                    errors = add_log_text(errors, str('Завантажено інформацію про розміщення БС - ' + str(bs_frame.shape[0])))
                    errors = add_log_text(errors, str(bs_frame.iloc[[0, 1, 2, 3, 4], [0, 1, 2, 3]]))
                    del bs_frame

                else:
                    bs_adr = None
                    bs_azi = None
                    errors = add_log_text(errors, 'Помилка при розпізнанні заголовків довідника - неповний комплект')
            else:
                bs_adr = None
                bs_azi = None
                errors = add_log_text(errors, 'Помилка при розпізнанні заголовків довідника - неповний комплект')
        else:
            bs_adr = None
            bs_azi = None
            errors = ''

    return bs_adr, bs_azi, errors


def burning(info_row, dict_address_bs, dict_azimuth):
    # Глобальні змінні для відображення тексту лоадбару:
    global current_file
    global current_action
    current_file = info_row[FILE_NAME]
    current_action = 'Перевірка структури файлу...'

    # Особливі випадки роботи конвертеру:
    ks_voc_status = False  # потрібно підписати адреси БС з окремого словника
    ks_forw_status = False  # є колонка переадресації, потрібно змінити абонента Б окремих випадках
    life_col_status = False  # направлений запис абонента Б, потрібно обрати одного з пари (інший буде цільовий А)
    lac_cid_merged_status = False  # значення ЛакСід злиті, потрібно розділити по колонкам
    abon_b_adr_status = False  # таблиця з відомостями про місцезнаходження абонента Б, потрібно виділити записи з
    # відомостями про адреси абонентів Б та інвертувати їх, потім додати до загального датафрейму +
    # внести до списку абонентів Б для подальшого експорту або обєднання при видачі таблиці по типу АБ
    type_tab_status = 'Змішана'

    # Оновлення довідника для підстановки колонок та типів:
    dict_columns = get_columns_map_dict()
    service_col_names = dict_columns.values()
    support_col_names = list(set(dict_columns))

    dict_types = get_types_map_dict()
    service_types_names = dict_types.values()
    supported_types_names = list(set(dict_types))

    temp_frame = None

    # для запису основної інформації про результати та логу (відображення у вікні конвертеру)
    new_row = info_row.copy()
    print(new_row)
    # Завантаження датафрейму файлу
    try:
        if info_row[FILE_PATH].endswith(".xlsx") | info_row[FILE_PATH].endswith(".xls"):
            full_frame = pd.read_excel(info_row[FILE_PATH], header=None, index_col=None)
            temp_frame = full_frame.iloc[:15]
        elif info_row[FILE_PATH].endswith(".xml"):
            full_frame = xml_parse_to_pandas(info_row[FILE_PATH])
        else:
            new_row[TYPE_FOUND] = 'Не розпізнано'
            new_row[TAB_LOG] = 'Формат не підтримується'
            return new_row, None
        new_row[COLUMNS_DETECTED] = full_frame.shape[1]
    except Exception as parse_error_ex:
        print('Переривання функції завантаження датафрейму з файлу ' + str(info_row[FILE_NAME]) + ', виключення:')
        print(parse_error_ex)
        new_row[TYPE_FOUND] = 'Не розпізнано'
        new_row[TAB_LOG] = 'Критична помилка парсеру, виключення: ' + str(parse_error_ex)
        return new_row, None
    # Пошук заголовків по першим записам таблиці
    header_row, headers_located = find_header_in_df(dict_columns, temp_frame)
    if header_row is None:
        new_row[TYPE_FOUND] = 'Не розпізнано'
        new_row[TAB_LOG] = 'Не виявлено заголовки колонок'
        return new_row, None
    new_row[COLUMNS_CONVERTED] = headers_located

    # Перейменування заголовків для аналізу:
    start_columns_names_list = full_frame.iloc[header_row]  # встановлення заголовку первинного
    full_frame = full_frame[header_row+1:]
    new_row[RECORDS_DETECTED] = full_frame.shape[0]
    full_frame = full_frame.rename(columns=start_columns_names_list)  # відмежування (видалення) записів до заголовку
    full_frame.columns = full_frame.columns.str.lower()  # для співставлення зі словником (ключі ловеркейс)
    full_frame.rename(columns=dict_columns, inplace=True)  # застосування словника для перейменування
    col_list = full_frame.columns.tolist()  # список заголовків для подальшої перевірки наявності окремих
    unknown_columns_list = list(set(col_list) - set(service_col_names))
    print(unknown_columns_list)
    if len(unknown_columns_list) > 0:
        new_row[TAB_LOG] = add_log_text(new_row[TAB_LOG], str('Нерозпізнані колонки: ') + list_to_sring(unknown_columns_list))

    # Перевірка на достатність колонок для подальшої роботи:
    if not (col_list.count('type') > 0
            and col_list.count('sim_a') > 0
            and col_list.count('date') > 0):
        new_row[TYPE_FOUND] = 'Не розпізнано'
        new_row[TAB_LOG] = add_log_text(new_row[TAB_LOG],
                                        'Не виявлено достатній набір колонок для роботи (тип, дата, абонент А)')
        return new_row, None

    # Визначення особливостей конвертування таблиці:

    # Перевірка наявності запису Київстар про переадресацію (третя колонка - Переадресація: містить мало записів,
    # але застосовується, коли абонент надсилає повідомлення. Необхідно, у випадках наявності
    # значення в колонці "Переадресація", врахувати їх як абонента Б, для вихідних повідомлень. Також бажано додатково
    # перевірити наявність переадресацій інших типів та у інших випадках)
    if col_list.count('forw') > 0:
        ks_forw_status = True
        type_tab_status = 'По абоненту А'

    # перевірка подвійного запису абонента Б (має дві колонки окремо від цільового абонента А(sim_a):
    # абонент, що здійснює виклик - sim_c та абонент, що приймає виклик - sim_d. Один з них буде абонентом А)
    elif col_list.count('sim_c') > 0 or col_list.count('sim_d') > 0:
        life_col_status = True
        type_tab_status = 'По абоненту А'

    # Перевірка відсутності адреси БС (для підключення довідників, переважно Київстар):
    if col_list.count('adr_a') == 0 and col_list.count('adr_az') == 0:
        ks_voc_status = True

    # Перевірка на тип АБ (для подальшого виділення записів по Б та конвертування їх до загального датафрейму)
    if 'adr_b' in col_list:
        if len(full_frame["adr_b"].unique()) > 3:
            abon_b_adr_status = True

    # Перевірка злиття ЛАК-СІД:
    if 'lac_cid' in col_list and 'lac_a' not in col_list and 'cid_a' not in col_list:
        lac_cid_merged_status = True

    # --------------------------------------------convert TYPE:
    current_action = 'Конвертування типів з\'єднань...'
    print('converting types...')
    rows_before = full_frame.shape[0]
    full_frame['type'] = full_frame['type'].str.lower()
    used_types = full_frame['type'].unique().tolist()
    new_row[TYPES_DETECTED] = len(used_types)
    new_types = list(set(used_types) - set(supported_types_names))
    new_row[TYPES_CONVERTED] = len(used_types) - len(new_types)
    if len(new_types) > 0:
        new_row[TAB_LOG] = add_log_text(new_row[TAB_LOG], 'У таблиці виявлено невідомі типи з\'єднань - '
                                        + list_to_sring(new_types) + '. Замінені на '
                                        + str(config_get_value('types_con_main_display_names', 'unknown')))
    full_frame.dropna(subset=['type', 'sim_a'], inplace=True)
    rows_after = full_frame.shape[0]
    if rows_before > rows_after:
        new_row[TAB_LOG] = add_log_text(new_row[TAB_LOG], 'Під час опрацювання типів видалено записів - '
                                        + str(rows_before-rows_after))
    full_frame['type'] = full_frame['type'].map(dict_types)
    full_frame['type'].fillna(config_get_value('unknown', 'unknown'), inplace=True)

    # ------------------------------------convert DATE and TIME:
    current_action = 'Конвертування дати та часу з\'єднань...'
    rows_before = full_frame.shape[0]
    if col_list.count('date') == 1 and col_list.count('time') == 0:
        full_frame['date_time'] = pd.to_datetime(full_frame['date'], dayfirst=True, errors='coerce')
    elif col_list.count('date') == 1 and col_list.count('time') == 1:
        full_frame['time'] = full_frame['time'].apply(lambda cell: convert_str_to_time(cell))
        full_frame['date_time'] = pd.to_datetime(full_frame['date'], dayfirst=True, errors='coerce') + full_frame[
            'time']
    full_frame.dropna(subset=['date_time'], inplace=True)
    rows_after = full_frame.shape[0]
    if rows_before > rows_after:
        new_row[TAB_LOG] = add_log_text(new_row[TAB_LOG], 'Під час опрацювання дат та часу видалено записів - '
                                        + str(rows_before-rows_after))

    # ----------------------------------------convert DURATION:
    current_action = 'Перевірка записів про тривалість...'
    if col_list.count('dur'):
        full_frame['dur'] = full_frame['dur'].apply(lambda cell: check_dur(cell))
        full_frame['dur_str'] = full_frame['dur'].astype(str).str[-8:]
        full_frame['date'] = full_frame['date_time'].dt.strftime('%d.%m.%Y')
        full_frame['time'] = full_frame['date_time'].dt.strftime('%H:%M:%S')

    # ------------------------------------------convert SIM A:
    current_action = 'Форматування записів номеру абонента А...'
    full_frame['sim_a'] = full_frame['sim_a'].apply(lambda x: check_number(x))
    uniq_sim_a_names = full_frame['sim_a'].unique().tolist()
    new_row[SIMA_UNIQ] = len(uniq_sim_a_names)

    # ------------------------------------------convert SIM B:
    current_action = 'Форматування записів номерів співрозмовників...'
    # create sim_b for ASTELIT type:
    if list(full_frame.columns).count('sim_b') == 0 and list(full_frame.columns).count('sim_c') == 1 and \
            list(full_frame.columns).count('sim_d') == 1:
        full_frame['sim_b'] = full_frame.apply(lambda row: choice_sim_b(row), axis=1)
    # вибір абонента Б для потрійного запису Київстар з переадресацією:

    if list(full_frame.columns).count('forw') == 1 and list(full_frame.columns).count('sim_b'):
        full_frame['sim_b'] = full_frame.apply(lambda row: choice_sim_b_forw(row), axis=1)
    # checking number mask:
    if list(full_frame.columns).count('sim_b') == 1:
        full_frame['sim_b'] = full_frame['sim_b'].apply(lambda x: check_number(x))

    # if have no column for subscriber B:
    if list(full_frame.columns).count('sim_b') == 0 and list(full_frame.columns).count('ip') == 1:
        full_frame['sim_b'] = full_frame['ip']

    new_row[SIMB_UNIQ] = full_frame['sim_b'].nunique()

    # -----------------------------------------convert IMEI A|B:
    current_action = 'Форматування записів номерів ІМЕІ...'
    if 'imei_a' in col_list:
        full_frame['imei_a'] = full_frame['imei_a'].apply(lambda x: check_imei(x))
        imei_a_list = full_frame['imei_a'].unique().tolist()
        if '' in imei_a_list:
            imei_a_list.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        new_row[IMEIA_UNIQ] = len(imei_a_list)
    else:
        new_row[IMEIA_UNIQ] = 0

    if 'imei_b' in col_list:
        full_frame['imei_b'] = full_frame['imei_b'].apply(lambda x: check_imei(x))
        imei_b_list = full_frame['imei_b'].unique().tolist()
        if '' in imei_b_list:
            imei_b_list.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        new_row[IMEIB_UNIQ] = len(imei_b_list)
    else:
        new_row[IMEIB_UNIQ] = 0

    # ------------------------------------------convert LAC|CID:
    current_action = 'Перевірка правильності записів LAC - Cell ID...'
    if 'lac_a' in col_list:
        full_frame['lac_a'] = full_frame['lac_a'].apply(lambda x: check_laccid(x))
    if 'lac_b' in col_list:
        full_frame['lac_b'] = full_frame['lac_b'].apply(lambda x: check_laccid(x))
    if 'cid_a' in col_list:
        full_frame['cid_a'] = full_frame['cid_a'].apply(lambda x: check_laccid(x))
    if 'cid_b' in col_list:
        full_frame['cid_b'] = full_frame['cid_b'].apply(lambda x: check_laccid(x))

    if 'lac_a' in col_list and 'cid_a' in col_list and 'lac_cid' not in col_list:
        full_frame['lac_cid'] = full_frame['lac_a'].astype(str) + '-' + full_frame['cid_a'].astype(str)

    if 'lac_cid' in full_frame.columns:
        bs_list = full_frame['lac_cid'].tolist()
        while '' in bs_list:
            bs_list.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        while '-' in bs_list:
            bs_list.remove('-')  # для точності кількості BS (порожні рядки заповнені "-")
        new_row[BS_A_UNIQ] = len(bs_list)
    else:
        new_row[BS_A_UNIQ] = 0
    
    if 'lac_b' in col_list and 'cid_b' in col_list and 'lac_cid_b' not in col_list:
        full_frame['lac_cid_b'] = full_frame['lac_b'].astype(str) + '-' + full_frame['cid_b'].astype(str)

    if 'lac_cid_b' in full_frame.columns:
        bs_list_b = full_frame['lac_cid_b'].tolist()
        while '' in bs_list_b:
            bs_list_b.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        while '-' in bs_list_b:
            bs_list_b.remove('-')  # для точності кількості BS (порожні рядки заповнені "-")
        new_row[BS_B_UNIQ] = len(bs_list_b)
    else:
        new_row[BS_B_UNIQ] = 0
        # -------------------------------USE KYIVSTAR BS HANDBOOK:
    if ks_voc_status is True and len(dict_address_bs) > 0:
        current_action = 'Доповнення таблиці записами довідників базових станцій...'
        full_frame['adr_a'] = full_frame.apply(lambda x: combine_lac_cid(x), axis=1)
        full_frame['adr_a'] = full_frame['adr_a'].map(dict_address_bs)
        full_frame['az_a'] = full_frame.apply(lambda x: combine_lac_cid(x), axis=1)
        full_frame['az_a'] = full_frame['az_a'].map(dict_azimuth)

    # -----------------------------FILL NAN BS & AZIMUTH CELLS:
    if 'adr_a' in full_frame.columns:
        full_frame['adr_a'] = full_frame['adr_a'].fillna('')
        adr_a_list = full_frame['adr_a'].tolist()
        while '' in adr_a_list:
            adr_a_list.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        new_row[ADR_A_UNIQ] = len(adr_a_list)
    else:
        new_row[ADR_A_UNIQ] = 0
        
    if 'adr_b' in full_frame.columns:
        full_frame['adr_b'] = full_frame['adr_b'].fillna('')
        adr_b_list = full_frame['adr_a'].tolist()
        while '' in adr_b_list:
            adr_b_list.remove('')  # для точності кількості BS (порожні рядки заповнені "")
        new_row[ADR_B_UNIQ] = len(adr_b_list)
    else:
        new_row[ADR_B_UNIQ] = 0

    # ------------------------------------------convert AZIMUTH:
    current_action = 'Перевірка правильності значень азимутів БС...'
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

    # ------------------------------------connect EMPTY COLUMNS:
    current_action = 'Підготовка опрацьованої таблиці до завантаження...'
    absent_columns = list(set(render_b_col_set) - set(full_frame.columns))
    if len(absent_columns) > 0:
        for col in absent_columns:
            full_frame[col] = ''

    # ------------------------------------KILL SERVICE COLUMNS:
    col_list_to_drop = list(set(full_frame.columns) - set(analysis_columns_set))
    full_frame.drop(col_list_to_drop, axis='columns', inplace=True)

    # -----------------------------------------KILL DUPLICATES:
    full_frame.drop_duplicates(inplace=True, ignore_index=True)
    new_row[RECORDS_CONVERTED] = full_frame.shape[0]
    return new_row, full_frame
