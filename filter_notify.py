#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
import sys, os

argv = sys.argv
argc = len(argv) - 1

# Аргументов нет?
if argc < 1:
    print "Launch this script with skype_name and display_name parameters"
    sys.exit()

# Берём имена из аргументов, которые передал нам скайп, в переменные для удобства:
target_skype_name = argv[1]
if argc > 1:
    target_disp_name = argv[2]
else:
    target_disp_name = ""

# Ищем по файлу эти переменные:
if os.path.isfile(os.path.expanduser(CONTACTS_NOTIFY_LIST)):
    FILE = open(os.path.expanduser(CONTACTS_NOTIFY_LIST), "r")
    for line in FILE:
        contacts = regex.findall(line)
        for contact in contacts:
            comment = contact[0]
            display_name = contact[1].strip()
            skype_name = contact[2].strip()
            
            # Имя найдено, но закомментировано - выходим:
            if (comment == COMMENT) and (
                (skype_name == target_skype_name)
                or
                ((target_disp_name != "") and (display_name == target_disp_name))
                ): sys.exit()
            
            # Имя найдено и не закомментировано - оповещаем:
            if (comment == "") and (
                (skype_name == target_skype_name)
                or
                ((target_disp_name != "") and (display_name == target_disp_name))
                ):
                os.system("notify-send -i skype '" + display_name + "' '" + ONLINE_MESSAGE + "'")
                sys.exit()

    FILE.close()

    # Не можем найти target_skype_name, target_disp_name в списке контактов - перезагружаем список:
    os.system(os.path.dirname(os.path.abspath(__file__)) + "/reload_contacts.py")
    
else: print "ERROR: Cannot find settings file " + CONTACTS_NOTIFY_LIST
