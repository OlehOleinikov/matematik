from configparser import ConfigParser
from config.default_config_values import *

def config_swipe():
    with open('config\\config.ini', 'w') as x:
        default_config.write(x)
    current_config.clear()
    current_config.read('config\\config.ini')
    print('Settings restored to default')


def config_save(file):
    with open(file, 'w') as y:
        current_config.write(y)
    print('Settings saved to file:' + file)


def config_load(file):
    current_config.clear()
    current_config.read(file)
    with open('config\\config.ini', 'w') as z:
        current_config.write(z)
    print('Settings loaded from file:' + str(file))


def config_get_value(section, option):
    return current_config.get(section, option)


def config_get_options(section):
    return current_config.options(section)
    

def config_set_item(section, option, value):
    current_config.set(section, option, value)


def config_remove_item():
    pass


current_config = ConfigParser()  # об'єкт конфігурації, яка використовується під час роботи
config_file_loaded_status = current_config.read('config\\config.ini') # завантаження користувацьких налаштувань
if config_file_loaded_status == []: # перевірка наявності файлу конфігу, відновлення у разі відсутності
    print('No custom config file in directory... Restoring...')
    config_swipe()
    current_config.read('config\\config.ini')
    print('New custom config file created')
    print('Custom config file swiped to default values and loaded')
else:
    print('Custom config loaded successfully')