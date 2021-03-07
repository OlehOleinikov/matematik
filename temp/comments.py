# Приклад застосування фільтру натискання миші (зняття виділення зі списку)
# self.open_modalwin_settings.listView_voice_in.installEventFilter(self)
# self.open_modalwin_settings.listView_voice_in.viewport().installEventFilter(self)

# def eventFilter(self, source, event):
#     if ((source is self.open_modalwin_settings.listView_voice_in and
#          event.type() == QEvent.KeyPress and
#          event.key() == Qt.Key_Escape and
#          event.modifiers() == Qt.NoModifier) or
#         (source is self.open_modalwin_settings.listView_voice_in.viewport() and
#          event.type() == QEvent.MouseButtonPress and
#          not self.open_modalwin_settings.listView_voice_in.indexAt(event.pos()).isValid()) or
#         (source is self.open_modalwin_settings.listView_voice_in.viewport() and
#         event.type() == QEvent.MouseButtonPress and
#          not self.open_modalwin_settings.listView_voice_in.indexAt(event.pos()).isValid())):
#         self.open_modalwin_settings.listView_voice_in.selectionModel().clear()
#     return super(SettingsWindow, self).eventFilter(source, event)


# def files_preview():
#     # load a test frame:
#     print("\n" + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "Проверка файлов, загрузка тестовых фрагментов:"
#           + Style.RESET_ALL)
#     for i in tabs_list:
#         print('\t', i)
#     support_col_names = list(set(dict_columns.values()))
#     files_to_test = len(tabs_list)
#     global list_to_work
#     for file in tabs_list:
#         temp_frame = pd.DataFrame
#         print("\n" + Fore.MAGENTA + "Проверяю файл:", file, Style.RESET_ALL)
#         if file.endswith(".xlsx") | file.endswith(".xls"):
#             temp_frame = pd.read_excel(file, header=None, nrows=DEEP, index_col=None)
#         elif file.endswith(".csv"):
#             temp_frame = pd.read_csv(file, header=None, nrows=DEEP, index_col=None)
#         elif file.endswith(".txt"):
#             temp_frame = pd.read_table(file, header=None, nrows=DEEP, index_col=None)
#         elif file.endswith(".xml"):
#             temp_frame = xml_parse_to_pandas(file)
#         else:
#             print(Fore.RED + "\tТип данных не опознан:", file)
#             print(Style.RESET_ALL)
#
#         # check: data shape for minimal requirements
#         if temp_frame.shape[1] > 4:
#             c = temp_frame.shape[1] - 1  # num of iterations (for all columns tabs)
#             print("\tОбнаружено столбцов:", c + 1)
#             a = np.array([])  # array for collecting positions of rows with keywords
#             b = dict_columns.keys()  # list of keywords from columns' voc (in human format)
#             while c >= 0:  # checking columns name in test dataframe
#                 a = np.append(a, temp_frame.loc[temp_frame[c].isin(b)].index.values)
#                 c = c - 1
#             a = a.tolist()  # convert np array to default list
#             a = list(a)
#             a_set = set(a)
#             most_common = None  # var for most frequency row (with columns' names)
#             qty_most_common = 0  # how much columns name detected in most common row
#             for item in a_set:  # voting for row with columns' names
#                 qty = a.count(item)
#                 if qty > qty_most_common:
#                     qty_most_common = qty
#                     most_common = int(item)
#
#             if qty_most_common >= 4:
#                 print('\tЗаголовки на строке: ', most_common + 1)
#                 temp_frame.columns = temp_frame.iloc[most_common]  # set header
#                 temp_frame.rename(columns=dict_columns, inplace=True)  # rename headers for sys names
#                 temp_frame = temp_frame.iloc[most_common + 1:]  # drop rows before headers
#                 col_list = list(temp_frame.columns)  # get a columns' list
#
#                 # check for minimal combination of columns and go on preview:
#                 if (col_list.count('type') > 0 and col_list.count('sim_a') > 0 and col_list.count('date') > 0) or \
#                         (col_list.count('type') > 0 and col_list.count('sim_a') > 0 and col_list.count(
#                             'date_time') > 0):
#
#                     found_columns = list(set(col_list) & set(support_col_names))
#                     print('\tРаспознано полей: ', len(found_columns), ' из ', temp_frame.shape[1])
#
#                     # *****************CHECK TYPE BLOCK*******************
#                     # set status vars to default:
#                     ks_voc_status = False
#                     life_col_status = False
#                     abon_b_adr_status = False
#                     type_tab_status = 'heap'
#                     # check 'Life' type tab:
#                     if col_list.count('sim_c') > 0:
#                         life_col_status = True
#                         type_tab_status = 'A'
#                     # check for missing antenna information:
#                     if col_list.count('adr_a') == 0 and col_list.count('adr_az') == 0:
#                         ks_voc_status = True
#                     # check for 'A' type signs
#                     if len(temp_frame["sim_a"].unique()) == 1:
#                         type_tab_status = 'A'
#                     # check for 'B' type signs
#                     if col_list.count('sim_b') == 1:
#                         if len(temp_frame["sim_b"].unique()) == 1:
#                             type_tab_status = 'B'
#                     # checking information about the location of subscriber B
#                     if col_list.count('adr_b') == 1:
#                         if len(temp_frame["adr_b"].unique()) > 3:
#                             abon_b_adr_status = True
#                     # print('\tФайл похож на детализацию соединений мобильных терминалов ')
#                     print("\tОпределен тип детализации: ", type_tab_status)
#
#                     # adding a task to the scheduler:
#                     global list_to_work
#                     list_to_work.append([file, type_tab_status, abon_b_adr_status, life_col_status,
#                                          ks_voc_status, most_common])
#                     global tabs_to_work
#                     tabs_to_work = tabs_to_work + 1
#
#                     print('\tНаличие информации о местонахождении абонента "Б": ', dict_print.get(abon_b_adr_status))
#                     print('\tТройная запись абонентов (формат "Астелит"):       ', dict_print.get(life_col_status))
#                     print('\tНеобходимость подключеня внешних справочников БС:  ', dict_print.get(ks_voc_status))
#
#                     # checking supported connection types:
#                     used_types = temp_frame['type'].unique().tolist()
#                     support_types = dict_types.keys()
#                     new_types = list(set(used_types) - set(support_types))
#
#                     if len(new_types) > 0:
#                         print(Fore.RED + "\t\tВ тестовом фрагменте найдены незвестные типы соединений:")
#                         for item in new_types:
#                             print('\t\t', item)
#                         print(Style.RESET_ALL)
#                     # show unknown columns' names:
#                     if len(found_columns) < len(col_list):
#                         print(Fore.RED + "\t\tВ тестовом фрагменте найдены неизвестные заголовки столбцов:\n\t\t",
#                               list(set(temp_frame.columns) - set(support_col_names)))
#                         print(Style.RESET_ALL)
#                 else:
#                     print(Fore.RED + "\tНедостаточно столбцов для анализа (минимально необходимы: "
#                                      "тип, абонент А, дата и время)")
#                     print('\t', list(set(temp_frame.columns) - set(support_col_names)))
#                     print(Style.RESET_ALL)
#             else:
#                 print(Fore.RED + "\tСлишком мало полей для дальнейшей работы. Проверь исходный файл")
#                 print(Style.RESET_ALL)
#
#     files_accept = len(list_to_work)
#     print('\n' + Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + '************************РЕЗУЛЬТАТЫ ПРОВЕРКИ'
#                                                            '************************')
#     print("\tПроверено файлов:    " + Style.RESET_ALL, files_to_test)
#     print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + "\tДопущено к перегону: " + Style.RESET_ALL, files_accept)
#     print(Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + '***********************************'
#                                                     '********************************')
#     print(Style.RESET_ALL)
#     if files_accept == 0:
#         print(Fore.RED + 'Нет файлов для анализа. Программа остановлена.' + Style.RESET_ALL)
#         time.sleep(5)
#         os.abort()