#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
from skypelog import *
import sys, glob, os

# Поля в DBB-файле не только пронумерованы, но и имеют "человеческие" названия.
# Автор skypelog.py положил эти названия в статический массив класса SkypeContact.
# Берём оттуда ID-шники:

class SkypeContactExt(SkypeContact):
    @classmethod
    def get_field_id(contacts, field_name):
        field_names = contacts.FIELD_NAMES.items()
        return [key for key, val in field_names if val == field_name][0]

record_id = SkypeContactExt.get_field_id("recid")
skype_name = SkypeContactExt.get_field_id("skypename")
full_name = SkypeContactExt.get_field_id("fullname")
display_name = SkypeContactExt.get_field_id("given_displayname")

# В папке скайпа обычно много DBB-файлов с контактами. Кстати, вот они:
files = glob.glob(os.path.expanduser(SKYPE_FOLDER + "/user*.dbb"));

# или нет...
if len(files) == 0:
    print "Cannot find Skype contacts data in " + SKYPE_FOLDER
    sys.exit()

# Здесь будут имена наших друзей:
skype_names = []

# Достаём контакты из всех файлов
for f in files:
    # Читаем файл в объект SkypeDBB:
    data = SkypeDBB(f)

    # и берём из него имена:
    for r in data.records():
        if record_id in r:
            id = r[record_id]
            # Признак того, что это контакт (т.к. среди записей могут быть "пустышки")
            if (id > 0) and (skype_name in r) and (r[skype_name] != ""):
                # Здесь skype_name - это обязательный Skype-идентификатор контакта.
                # Поля для получения отображаемого имени подобраны опытным путём.
                # Насколько я понимаю, в скайп-клиенте схема такая:
                if display_name in r: disp_name = r[display_name]
                elif full_name in r:  disp_name = r[full_name]
                else:                 disp_name = r[skype_name]
                # Полученные имена добавляем в наш массив контактов:
                if disp_name != "":
                    skype_names.append({
                        "id":id,
                        "skype_name":r[skype_name],
                        "display_name":disp_name,
                        "comment":DEFAULT_COMMENT
                    })

# Сортируем по display_name (чтобы в конфиге были по алфавиту)
skype_names = sorted(skype_names, key=lambda skype_names: skype_names["display_name"])

# Читаем настройки контактов из существующего конфига, если он есть.
if os.path.isfile(os.path.expanduser(CONTACTS_NOTIFY_LIST)):
    FILE = open(os.path.expanduser(CONTACTS_NOTIFY_LIST), "r")
    for line in FILE:
        contacts = regex.findall(line)
        for contact in contacts:
            comment = contact[0]
            display_name = contact[1].strip()
            skype_name = contact[2].strip()
            # Для каждой строчки конфига находим соответствующий контакт из skype_names,
            # и устанавливаем ему свойство comment
            for contact in skype_names:
                if (contact["skype_name"] == skype_name) or (contact["display_name"] == display_name):
                    contact["comment"] = comment            
    FILE.close()

# Сохраняем конфиг
FILE = open(os.path.expanduser(CONTACTS_NOTIFY_LIST), "w")

FILE.write("\n\tПожалуйста, не меняйте структуру этого файла!\n"
"\n"
"\tВы можете только раскомментировать нужные контакты\n"
"\tили закомментировать ненужные с помощью символа #\n\n")

for contact in skype_names:
    FILE.write(contact["comment"] + "\t" + contact["display_name"] + " " + DELIMITER + " " + contact["skype_name"] + "\n")
FILE.close()

