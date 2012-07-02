#!/usr/bin/env python
# -*- coding: utf-8 -*-

SKYPE_FOLDER = "~/.Skype/ВАШ-СКАЙП-ID-ЗДЕСЬ"

# Файл с Вашим списком контактов для настройки уведомлений
CONTACTS_NOTIFY_LIST = "~/filter_notify.conf"

# Символы, используемые в нашем файле контактов (CONTACTS_NOTIFY_LIST)
# для комментария и разделителя между именем и скайп-идентификатором.
# Эти символы не должны встречаться в именах и ID. Если Вы меняете символы,
# следует удалить CONTACTS_NOTIFY_LIST и запустить скрипт reload_contacts.
COMMENT = "#"
DELIMITER = "#"

ONLINE_MESSAGE = "снова в сети"


import re
regex = re.compile("(" + COMMENT + "*)([^" + DELIMITER + "]+)" + DELIMITER + "([^\n]+)")

# Статус оповещения для новых добавляемых контактов. Может быть COMMENT
# (закомментированы, т.е. не оповещать) или "" (раскомментированы - оповещать).
# В случае установки параметра DEFAULT_COMMENT = "" оповещение будет происходить
# только после первого запуска reload_contacts.py. В этом случае в скрипт
# filter_notify.py после запуска reload_contacts.py неплохо бы добавить новую
# проверку существования target_skype_name в новом списке контактов.
DEFAULT_COMMENT = COMMENT

