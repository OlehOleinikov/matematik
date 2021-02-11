from colorama import Style, Fore
import time
import os

# -------------------------------------------------------------------------------------
# ----------------------------INTRO IMAGE AND DESCRIPTION------------------------------
# -------------------------------------------------------------------------------------
image_str = "                      `                      " \
            "\n                    .yNs`                    " \
            "\n                  `oNMMMNo`                  " \
            "\n                  sMMMMMMMo                  " \
            "\n                  sMMMMMMMo                  " \
            "\n                  sMMMMMMMo                  " \
            "\n                  sMMMMMMMo                  " \
            "\n       .o.        sMMMMMMMo        -o.       " \
            "\n       -MMdo-     sMMMMMMMo     -omMN.       " \
            "\n       -MMMMMm.   sMMMMMMMo   -mMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n       -MMMMMM.   sMMMMMMMo   -MMMMMN.       " \
            "\n        .odMMM.   sMMMMMMMo   -MMMdo.        " \
            "\n           .od.   sMMMMMMMo   -d+.           " \
            "\n                  sMMMMMMMo                  " \
            "\n                  +mMMMMMm/                  " \
            "\n                    :sds-                    " \
            "\n                                             " \
            "\n                                             \n\n"


def print_program_description():
    print(Fore.LIGHTCYAN_EX + 'ПЕРЕГОНЩИК - 2020 (ver.1.0 - build 251120) by MATEMATIK \u00a9\n\n' + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + '\tДля работы программы:'
                              '\n\t\t- скопировать исходные файлы детализации в директорию с программой '
                              '(.xls .xlsx .xml .txt .csv) '
                              '\n\t\t- при выборе заданий: ввести "y" - для подтверждения, другое значение '
                              '- для пропуска'
                              '\n\t\t- для остановки программы в любой момент -> CTRL + C\n' + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + '\tВ корневом каталоге программы должны находиться файлы конфигурации (доступны '
                              'для редактирования):'
                              '\n\t\tconfig_columns.xlsx - со списком заголовков столбцов для распознавания '
                              '\n\t\tconfig_types.xlsx - со списком типов соединений'
                              '\n\t\tconfig_bs_voc.xlsx - со списком типичных захоловков справочников БС Киевстар\n'
          + Style.RESET_ALL)


def print_logo():
    print(Fore.LIGHTCYAN_EX + image_str + Style.RESET_ALL)


def print_the_end():
    print("\n" + Fore.GREEN + 'Работа закончена.\nПрограмма остановлена' + Style.RESET_ALL)
    input('ENTER для закрытия окна')


def print_request_to_continue():
    dmv = input('Продолжить работу?(y/n)')
    print(Style.RESET_ALL)
    if dmv == 'y' or dmv == 'Y':
        pass
    else:
        print(Fore.RED + 'Работа остановлена')
        print(Style.RESET_ALL)
        time.sleep(5)
        os.abort()
