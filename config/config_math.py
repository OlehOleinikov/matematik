from configparser import ConfigParser

default_config = ConfigParser()

default_config['import_folder_default'] = {'path':''}

default_config['types_con_main_display_names'] = {
    'voice_in': 'вх',
    'voice_out': 'вих',
    'message_in': 'вх СМС',
    'message_out': 'вих СМС',
    'network': 'інтернет',
    'forwarding': 'переад',
    'unknown': 'переад'
    }

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

default_config['columns_incoming_names'] = {
    'type': 'Тип з\'єднання',
    'date': 'Дата',
    'date_time': 'Час',
    'dur': 'Тривалість',
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

default_config['types_con_main_enum'] = {
    'voice_in': '1',
    'voice_out': '2',
    'message_in': '3',
    'message_out': '4',
    'network': '5',
    'forwarding': '6',
    'unknown': '7'
    }

default_config['types_con_main_invert_rules'] = {
    'voice_in': 'voice_out',
    'voice_out': 'voice_in',
    'message_in': 'message_out',
    'message_out': 'message_in',
    'network': 'network',
    'forwarding': 'forwarding',
    'unknown': 'unknown'
    }

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

default_config['azimuth_splitters'] = {
    ' \\ ': 'True',
    ' / ': 'True',
    ', AZ=': 'True',
    }

default_config['types_dict_network'] = {
    'gprsCall': '5',
    'aval - pos': '5',
    'bkc': '5',
    'garagegps': '5',
    'internet': '5',
    'lifestatus': '5',
    'mms': '5',
    'nodata': '5',
    'obp': '5',
    'pb': '5',
    'pumb': '5',
    'raxel': '5',
    'yavir': '5',
    'GGSN': '5',
    'GPRS': '5',
    'GPRS.': '5'
    }

default_config['types_dict_voice_out'] = {
    'Вих.': '2',
    'Вихідний': '2',
    'Исх': '2',
    'Исх.': '2',
    'Исходящий': '2',
    'Исходящий звонок': '2',
    'вих': '2',
    'moc': '2',
    'mocAttempt': '2',
    'emergencyCall': '2',
    'исх.звон.': '2',
    'OutgoingCallAttempt': '2',
    'ISDN - Исходящий': '2',
    'исх.0': '2'
    }

default_config['types_dict_message_out'] = {
    'Исходящее SMS': '4',
    'вих СМС': '4',
    'mocSMS': '4',
    'SMS_MO': '4',
    'исх.SMS': '4',
    'Исходящее SMS в роуминге': '4',
    'Вихідне SMS': '4'
    }

default_config['types_dict_voice_in'] = {
    'вх': '1',
    'вх.': '1',
    'вхідний': '1',
    'вхідний виклик': '1',
    'входящий ': '1',
    'входящий звонок': '1',
    'mtc': '1',
    'mtcAttempt': '1',
    'входящий': '1',
    'вх.звон.': '1',
    'Входящий звонок к роумеру': '1',
    'IncomingCall': '1',
    'выз.к роум.': '1',
    'вх.0': '1',
    }

default_config['types_dict_message_in'] = {
    'Входящее SMS': '3',
    'вх СМС': '3',
    'mtcSMS': '3',
    'SMS_MT': '3',
    'вх.SMS': '3',
    'MMS': '3',
    'mtcMMS': '3',
    'Вхідне SMS': '3'
    }

default_config['types_dict_forwarding'] = {
    'callForwardingAttempt' : '6',
    'transitAttempt' : '6',
    'callForwarding' : '6',
    'неопредел.': '6',
    'переадрес.': '6',
    'Переадресация': '6',
    'переадр.': '6',
    'переад': '6',
    'Переадресація': '6'
    }

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

default_config['columns_dict_adr_b'] = {
    'Адреса Б': 'adr_b',
    'Адреса БС Б': 'adr_b',
    'Адресс Б': 'adr_b',
    'Сота B': 'adr_b'}

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

default_config['columns_dict_az_b'] = {
    'Аз.Б': 'az_b',
    'Азимут B': 'az_b'}

default_config['columns_dict_cid_a'] = {
    'CELL': 'cid_a',
    'CELLID': 'cid_a',
    'ci': 'cid_a',
    'cid': 'cid_a',
    'CID A': 'cid_a',
    'Идентификатор ячейки (Cell ID)': 'cid_a',
    'Ідентифікатор (Cell ID)': 'cid_a',
    'Номер БС': 'cid_a'}

default_config['columns_dict_cid_b'] = {
    'CID B': 'cid_b',
    'CID Б': 'cid_b'}

default_config['columns_dict_date'] = {
    'дата': 'date'}

default_config['columns_dict_date_time'] = {
    'CALL_DATE_TIME': 'date_time',
    'STARTTIME': 'date_time',
    'Дата и время соединения': 'date_time',
    'Дата начала': 'date_time',
    'Дата та час': 'date_time',
    'Дата та час з\'єднання': 'date_time',
    'Нач звон': 'date_time'}

default_config['columns_dict_dur'] = {
    'длител.(сек.)': 'dur',
    'длительность': 'dur',
    'Длительность соединения (сек.)': 'dur',
    'Длительность,с': 'dur',
    'Трив.': 'dur',
    'тривалість': 'dur',
    'Тривалість з\'єднання (сек.)': 'dur'}

default_config['columns_dict_imei_a'] = {
    'Imei': 'imei_a',
    'IMEI A': 'imei_a',
    'IMEI А': 'imei_a',
    'IMEI кінцевого обладнання Абонентського номеру': 'imei_a',
    'IMEI конечного оборудования Абонентского номера': 'imei_a',
    'ІМЕІ': 'imei_a',
    'ІМЕІ A': 'imei_a',
    'ІМЕІ А': 'imei_a'}

default_config['columns_dict_imei_b'] = {
    'IMEI B': 'imei_b',
    'IMEI Б': 'imei_b',
    'ІМЕІ Б': 'imei_b'}

default_config['columns_dict_other'] = {
    'IMSI': 'imsi',
    'Ip': 'ip',
    'IP Address доступа в Internet': 'ip',
    'IP-Address доступа в Internet': 'ip',
    'IP-Address доступу в Internet': 'ip',
    'Мережа': 'network'}

default_config['columns_dict_lac_a'] = {
    'AREA': 'lac_a',
    'lac': 'lac_a',
    'LAC A': 'lac_a',
    'Код региона (Local Area Code)': 'lac_a',
    'Код регіону (Local Area Code)': 'lac_a',
    'Регіон БС': 'lac_a'}

default_config['columns_dict_lac_b'] = {
    'LAC B': 'lac_b',
    'LAC Б': 'lac_b'}

default_config['columns_dict_lac_cid'] = {
    'Код региона-идентификатор базовой станции (LAC-CellID)': 'lac_cid'}

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

default_config['columns_dict_sim_b'] = {
    'SIM B': 'sim_b',
    'TB': 'sim_b',
    'Абонент Б': 'sim_b',
    'Б': 'sim_b',
    'Контакт': 'sim_b',
    'набранный ном./звонящий': 'sim_b',
    'Тел. B': 'sim_b'}

default_config['columns_dict_sim_c'] = {
    'Номер, который осуществляет вызов/соединение с Internet/отправляет sms': 'sim_c',
    'Номер, який здійснює виклик, з\'єднання з Internet/відправляє sms': 'sim_c'}

default_config['columns_dict_sim_d'] = {
    'Номер, который принимает вызов/sms': 'sim_d',
    'Номер, який приймає виклик/sms': 'sim_d'}

default_config['columns_dict_time'] = {
    'Время': 'time',
    'час': 'time'}

default_config['columns_dict_lac_cid'] = {
    'GGSN': 'type',
    'тип': 'type',
    'тип звонка': 'type',
    'Тип з\'єднання': 'type',
    'Тип соед.': 'type',
    'Тип соединения': 'type'}

with open('config.ini', 'w') as f:
    default_config.write(f)

for key in default_config['azimuth_splitters']:
    print('key is -' + key + '-end')
