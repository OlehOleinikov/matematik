from configparser import ConfigParser
# -----------------------------------------------------------------------------
# -----------------СТАНДАРТНІ НАЛАШТУВАННЯ КОНВЕРТЕРУ (КОНФІГ)-----------------
# -----------------------------------------------------------------------------

default_config = ConfigParser()  # об'єкт конфігурації (використовується для відновлення до "заводських" налаштувань

# шлях до папки, з якої можна швидко імпортувати усі файли (визначається користувачем)
default_config['import_folder_default'] = {'path': ''}

# підписи типів у результуючому файлі:
default_config['types_con_main_display_names'] = {
    'voice_in': 'вх',
    'voice_out': 'вих',
    'message_in': 'вх СМС',
    'message_out': 'вих СМС',
    'network': 'інтернет',
    'forwarding': 'переад',
    'unknown': 'переад'
    }

# підписи колонок у результуючому файлі:
default_config['columns_export_names'] = {
    'type': 'Тип',
    'date': 'Дата',
    'time': 'Час',
    'dur': 'Трив.',
    'sim_a': 'Абонент А',
    'imei_a': 'ІМЕІ А',
    'sim_b': 'Абонент Б',
    'imei_b': 'ІМЕІ Б',
    'lac_a': 'LAC A',
    'cid_a': 'Cid A',
    'az_a': 'Аз.А',
    'adr_a': 'Адреса А',
    'lac_b': 'LAC Б',
    'cid_b': 'Cid Б',
    'az_b': 'Аз.Б',
    'adr_b': 'Адреса Б'
    }

# види колонок, які можуть бути в імпортованому файлі та їх підписи в інтерфейсі GUI:
default_config['columns_incoming_names'] = {
    'type': 'Тип з\'єднання',
    'date': 'Дата або Дата/Час (в одній колонці)',
    'time': 'Тільки час',
    'date_end': 'Дата\'час завершення з\'єднання',
    'dur': 'Тривалість з\'єднання',
    'sim_a': 'Абонент А (основний абонент)',
    'imei_a': 'ІМЕІ А',
    'desc_a': 'Підпис власника А',
    'sim_b': 'Абонент Б (співрозмовник)',
    'imei_b': 'ІМЕІ Б',
    'desc_b': 'Підпис власника Б',
    'sim_c': 'Абонент, що здійснює виклик',
    'sim_d': 'Абонент, що приймає виклик',
    'lac_a': 'LAC (зона БС) абонента А',
    'cid_a': 'Cid (номер БС) абонента А',
    'lac_cid': 'LAC+Cid абонента А (в одній колонці)',
    'az_a': 'Азимут БС абонента А',
    'adr_a': 'Адреса розміщення БС - А',
    'adr_az': 'Адреса та азимут БС в одній колонці - А',
    'lac_b': 'LAC (зона БС) абонента Б',
    'cid_b': 'Cid (номер БС) абонента Б',
    'az_b': 'Азимут БС абонента Б',
    'adr_b': 'Адреса розміщення БС - Б',
    'imsi': 'IMSI SIM-картки',
    'network': 'Мережа оператора',
    'ip': 'Окрема колонка ІР-адреси',
    'column_ignore': 'Список колонок для ігнорування програмою'
}
# нумерований список типів з'єднань (можливо краще видалити цей проміжний етап):
default_config['types_con_main_enum'] = {
    'voice_in': '1',
    'voice_out': '2',
    'message_in': '3',
    'message_out': '4',
    'network': '5',
    'forwarding': '6',
    'unknown': '7'
    }

# інвертування типів для зміни абонентів А та Б місцями:
default_config['types_con_main_invert_rules'] = {
    'voice_in': 'voice_out',
    'voice_out': 'voice_in',
    'message_in': 'message_out',
    'message_out': 'message_in',
    'network': 'network',
    'forwarding': 'forwarding',
    'unknown': 'unknown'
    }

# суфікс ідентифікатора БС (у деяких випадках), потребує заміну на відповідну цифру:
default_config['azimuth_sufix'] = {
    '-a': '1',
    '-b': '2',
    '-c': '3',
    '-d': '4',
    '-e': '5',
    '-f': '6',
    '-g': '7',
    '-h': '8'
    }

# типові розділювачі у випадку злиття адреси БС та азимуту в одній колонці:
default_config['azimuth_splitters'] = {
    ' \\ ': 'True',
    ' / ': 'True',
    ', AZ=': 'True',
    }

# --------------------------------------ТИПИ РОЗПІЗНАННЯ---------------------------------------------
# список розпізнання типу - інтернет
default_config['types_dict_network'] = {
    'gprsCall': 'network',
    'aval - pos': 'network',
    'bkc': 'network',
    'garagegps': 'network',
    'internet': 'network',
    'lifestatus': 'network',
    'mms': 'network',
    'nodata': 'network',
    'obp': 'network',
    'pb': 'network',
    'pumb': 'network',
    'raxel': 'network',
    'yavir': 'network',
    'GGSN': 'network',
    'GPRS': 'network',
    'GPRS.': 'network'
    }

# список розпізнання типу - вихідний дзвінок:
default_config['types_dict_voice_out'] = {
    'Вих.': 'voice_out',
    'Вихідний': 'voice_out',
    'Исх': 'voice_out',
    'Исх.': 'voice_out',
    'Исходящий': 'voice_out',
    'Исходящий звонок': 'voice_out',
    'вих': 'voice_out',
    'moc': 'voice_out',
    'mocAttempt': 'voice_out',
    'emergencyCall': 'voice_out',
    'исх.звон.': 'voice_out',
    'OutgoingCallAttempt': 'voice_out',
    'ISDN - Исходящий': 'voice_out',
    'исх.0': 'voice_out'
    }

# список розпізнання типу - вихідне повідомлення:
default_config['types_dict_message_out'] = {
    'Исходящее SMS': 'message_out',
    'вих СМС': 'message_out',
    'mocSMS': 'message_out',
    'SMS_MO': 'message_out',
    'исх.SMS': 'message_out',
    'Исходящее SMS в роуминге': 'message_out',
    'Вихідне SMS': 'message_out'
    }

# список розпізнання типу - вхідний дзвінок:
default_config['types_dict_voice_in'] = {
    'вх': 'voice_in',
    'вх.': 'voice_in',
    'вхідний': 'voice_in',
    'вхідний виклик': 'voice_in',
    'входящий ': 'voice_in',
    'входящий звонок': 'voice_in',
    'mtc': 'voice_in',
    'mtcAttempt': 'voice_in',
    'вх.звон.': 'voice_in',
    'Входящий звонок к роумеру': 'voice_in',
    'IncomingCall': 'voice_in',
    'выз.к роум.': 'voice_in',
    'вх.0': 'voice_in',
    }

# список розпізнання типу - вхідне повідомлення:
default_config['types_dict_message_in'] = {
    'Входящее SMS': 'message_in',
    'вх СМС': 'message_in',
    'mtcSMS': 'message_in',
    'SMS_MT': 'message_in',
    'вх.SMS': 'message_in',
    'MMS': 'message_in',
    'mtcMMS': 'message_in',
    'Вхідне SMS': 'message_in',
    }

# список розпізнання типу - переадресація:
default_config['types_dict_forwarding'] = {
    'callForwardingAttempt': 'forwarding',
    'transitAttempt': 'forwarding',
    'callForwarding': 'forwarding',
    'неопредел.': 'forwarding',
    'переадрес.': 'forwarding',
    'Переадресация': 'forwarding',
    'переадр.': 'forwarding',
    'переад': 'forwarding',
    'Переадресація': 'forwarding'
    }

# ------------------------------------------КОЛОНКИ РОЗПІЗНАННЯ------------------------------------
# список розпізнання колонки - адреса БС абонента А
default_config['columns_dict_adr_a'] = {
    'Address': 'adr_a',
    'Adres': 'adr_a',
    'Adress': 'adr_a',
    'Coverage or Address': 'adr_a',
    'Адрес': 'adr_a',
    'Адрес БС': 'adr_a',
    'Адреса': 'adr_a',
    'Адреса БС': 'adr_a',
    'Адреса БС А': 'adr_a',
    'Адресс А': 'adr_a',
    'БС': 'adr_a',
    'Положение базовой станции': 'adr_a',
    'Сота': 'adr_a',
    'Сота A': 'adr_a',
    'Адрес базовой станции, азимут сигналабазовой станции': 'adr_a',
    'Адрес расположения базовой станции и азимут': 'adr_a',
    'Адреса розташування базової станції та азимут': 'adr_a'}

# список розпізнання колонки - адреса БС абонента Б:
default_config['columns_dict_adr_b'] = {
    'Адреса Б': 'adr_b',
    'Адреса БС Б': 'adr_b',
    'Адресс Б': 'adr_b',
    'Сота B': 'adr_b'}

# список розпізнання колонки - азимут БС абонента А:
default_config['columns_dict_az_a'] = {
    'az': 'az_a',
    'az.': 'az_a',
    'AZI': 'az_a',
    'azimut': 'az_a',
    'azimuth': 'az_a',
    'аз': 'az_a',
    'аз.': 'az_a',
    'Аз.А': 'az_a',
    'азимут': 'az_a',
    'Азимут A': 'az_a'}

# список розпізнання колонки - азимут БС абонента Б:
default_config['columns_dict_az_b'] = {
    'Аз.Б': 'az_b',
    'Азимут B': 'az_b'}

# список розпізнання колонки - номер БС (Сід) абонента А:
default_config['columns_dict_cid_a'] = {
    'CELL': 'cid_a',
    'CELLID': 'cid_a',
    'ci': 'cid_a',
    'cid': 'cid_a',
    'CID A': 'cid_a',
    'Идентификатор ячейки (Cell ID)': 'cid_a',
    'Ідентифікатор (Cell ID)': 'cid_a',
    'Номер БС': 'cid_a'}

# список розпізнання колонки - номер БС (Сід) абонента Б:
default_config['columns_dict_cid_b'] = {
    'CID B': 'cid_b',
    'CID Б': 'cid_b'}

# список розпізнання колонки - Дата:
default_config['columns_dict_date'] = {
    'дата': 'date'}

# список розпізнання колонки - Дата та час:
default_config['columns_dict_date_time'] = {
    'CALL_DATE_TIME': 'date_time',
    'STARTTIME': 'date_time',
    'Дата и время соединения': 'date_time',
    'Дата начала': 'date_time',
    'Дата та час': 'date_time',
    'Дата та час з\'єднання': 'date_time',
    'Нач звон': 'date_time'}

# список розпізнання колонки - Тривалість:
default_config['columns_dict_dur'] = {
    'длител.(сек.)': 'dur',
    'длительность': 'dur',
    'Длительность соединения (сек.)': 'dur',
    'Длительность,с': 'dur',
    'Трив.': 'dur',
    'тривалість': 'dur',
    'Тривалість з\'єднання (сек.)': 'dur'}

# список розпізнання колонки - ІМЕІ абонента А:
default_config['columns_dict_imei_a'] = {
    'Imei': 'imei_a',
    'IMEI A': 'imei_a',
    'IMEI А': 'imei_a',
    'IMEI кінцевого обладнання Абонентського номеру': 'imei_a',
    'IMEI конечного оборудования Абонентского номера': 'imei_a',
    'ІМЕІ': 'imei_a',
    'ІМЕІ A': 'imei_a',
    'ІМЕІ А': 'imei_a'}

# список розпізнання колонки - ІМЕІ абонента Б:
default_config['columns_dict_imei_b'] = {
    'IMEI B': 'imei_b',
    'IMEI Б': 'imei_b',
    'ІМЕІ Б': 'imei_b'}

#  список розпізнання колонок, що не мають значення для роботи конвертеру (додаткові):
default_config['columns_dict_other'] = {
    'IMSI': 'imsi',
    'Ip': 'ip',
    'IP Address доступа в Internet': 'ip',
    'IP-Address доступа в Internet': 'ip',
    'IP-Address доступу в Internet': 'ip',
    'Мережа': 'network'}

# список розпізнання колонки - зони (регіону, ЛАК) абонента А:
default_config['columns_dict_lac_a'] = {
    'AREA': 'lac_a',
    'lac': 'lac_a',
    'LAC A': 'lac_a',
    'Код региона (Local Area Code)': 'lac_a',
    'Код регіону (Local Area Code)': 'lac_a',
    'Регіон БС': 'lac_a'}

# список розпізнання колонки - зони (регіону, ЛАК) абонента Б:
default_config['columns_dict_lac_b'] = {
    'LAC B': 'lac_b',
    'LAC Б': 'lac_b'}

# список розпізнання колонки - в якій поєднано ЛАК та Сід -  абонента А
default_config['columns_dict_lac_cid'] = {
    'Код региона-идентификатор базовой станции (LAC-CellID)': 'lac_cid'}

# список розпізнання колонки - Абонент А (основний номер):
default_config['columns_dict_sim_a'] = {
    'MSISDN': 'sim_a',
    'SIM A': 'sim_a',
    'TA': 'sim_a',
    'А': 'sim_a',
    'Абонент А': 'sim_a',
    'Абонентский номер': 'sim_a',
    'Абонентський номер': 'sim_a',
    'Номер': 'sim_a',
    'Тел. А': 'sim_a'}

# список розпізнання колонки - Абонент Б (співрозмовник):
default_config['columns_dict_sim_b'] = {
    'SIM B': 'sim_b',
    'TB': 'sim_b',
    'Абонент Б': 'sim_b',
    'Б': 'sim_b',
    'Контакт': 'sim_b',
    'набранный ном./звонящий': 'sim_b',
    'Тел. B': 'sim_b'}

# список розпізнання колонки - Абонент, що здійснює виклик (у випадках направленої таблиці у окремих операторах):
default_config['columns_dict_sim_c'] = {
    'Номер, который осуществляет вызов/соединение с Internet/отправляет sms': 'sim_c',
    'Номер, який здійснює виклик, з\'єднання з Internet/відправляє sms': 'sim_c'}

# список розпізнання колонки - Абонент, що отримує виклик (у випадках направленої таблиці у окремих операторах):
default_config['columns_dict_sim_d'] = {
    'Номер, который принимает вызов/sms': 'sim_d',
    'Номер, який приймає виклик/sms': 'sim_d'}

# список розпізнання колонки - Час:
default_config['columns_dict_time'] = {
    'Время': 'time',
    'час': 'time'}

# список розпізнання колонки - Тип:
default_config['columns_dict_type'] = {
    'GGSN': 'type',
    'тип': 'type',
    'тип звонка': 'type',
    'Тип з\'єднання': 'type',
    'Тип соед.': 'type',
    'Тип соединения': 'type'}