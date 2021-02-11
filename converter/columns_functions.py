from colorama import Fore, Style
import pandas as pd

global dict_types


# check connection type:
def check_contype(s):
    if dict_types.get(s):
        result = dict_types.get(s)
    else:
        result = "unknown"
    return result


# checking IMEI cell
def check_imei(s):
    s = str(s)
    if s.startswith("\'"):
        s = s[1:(len(s))]
    if s.endswith('.0'):
        s = s[:-2]
    if (len(s) == 14 and s.startswith('1') and s.endswith('0')) or (len(s) == 13 and s.startswith('1')):
        a = "0" + s[0:13] + "0"
    elif 14 <= len(s) <= 16:
        a = s[0:14] + "0"
    elif s.isdigit():
        a = s
    elif s == 'nan' or s == 'None' or s == 'Nan' or s == 'NaN' or s is None:
        a = ''
    else:
        print(Fore.RED + "\t\tНеизвестный формат IMEI: ", s, " Записываю исходное значение..." + Style.RESET_ALL)
        a = s
    return a


def check_number(s):
    s = str(s)
    if s.endswith('.0'):
        s = s[:-2]
    if s.startswith('C') and s.endswith('FT'):
        s = s[1:-2]
    if s.startswith('959000') and len(s) > 15:
        s = s[6:]
    if s.startswith('005380') and len(s) == 15:
        s = s[3:]
    if s.isdigit() and len(s) == 9:
        a = "380" + s
    elif s.isdigit() and len(s) == 10 and s.startswith("0"):
        a = "38" + s
    elif s.isdigit() and len(s) == 11 and s.startswith("80"):
        a = "3" + s
    elif s.isdigit() and len(s) == 15 and s.startswith("810380"):
        a = s[-12:]
    else:
        a = s
    return a


# check duration cell:
def check_dur(cell):
    s = str(cell)
    if s.endswith('.0'):
        s = s[:-2]
    if s.isdigit():
        res = pd.to_timedelta(int(s), unit="S", errors="coerce")
    else:
        res = pd.to_timedelta(s, errors='coerce')
    return res


# check LAC and CID cells:
def check_laccid(s):
    s = str(s)
    if s.endswith('.0'):
        s = s[:-2]
    if s.isdigit():
        a = int(s)
    elif s == 'nan' or s is None:
        a = ''
    else:
        print(Fore.RED + "\t\tОшибка формата LAC/Cid: ", s, " Записываю пустое значение...")
        print(Style.RESET_ALL)
        a = ''
    return a


# concat LAC and CID value with separator '-':
def combine_lac_cid(row):
    lac = str(row['lac_a'])
    if lac.endswith('.0'):
        lac = lac[:-2]
    cid = str(row['cid_a'])
    if cid.endswith('.0'):
        cid = lac[:-2]
    if len(lac) > 0 and len(cid) > 0:
        res = lac + '-' + cid
    else:
        res = ''
    return res


# parse azimuth value from address string:
def azimut_from_adress(row):
    a = str(row)
    parts_list = list(a.split(sep=','))
    res = None
    for part in parts_list:
        if part.startswith('AZ=') or part.startswith(' AZ='):
            part_len = len(part)
            i = 0
            integer_comb = ''
            while i < part_len:
                symbol = part[i]
                if symbol.isdigit():
                    integer_comb += symbol
                i += 1
            res = int(integer_comb)
    return res


# remove azimuth string part after parse azimuth value to another cell:
def remove_azimuth_from_long_row(row):
    a = str(row)
    parts_list = list(a.split(sep=','))
    for part in parts_list:
        if part.startswith('AZ=') or part.startswith(' AZ='):
            part_to_remove = part
            parts_list.remove(part_to_remove)
    res = ','.join(parts_list)
    return res


# check azimuth value:
def check_azimut(s):
    s = str(s)
    if s.endswith('.0'):
        s = s[:-2]
    if s == '' or s == 'nan' or s == 'NaN':
        a = ''
    elif s.isdigit():
        s = int(s)
        if (0 <= s <= 360) or s == 999:
            a = s
        else:
            a = 999
    else:
        print(Fore.RED + "\t\tОшибка значения азимута : ", s, " Удаляю значение..." + Style.RESET_ALL)
        a = ''
    return a


# subscriber B choice for Astelit table type:
def choice_sim_b(row):
    a = row['sim_a']
    c = row['sim_c']
    d = row['sim_d']
    if str(a) == str(c):
        return d
    else:
        return c
