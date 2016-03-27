# coding: utf-8

""" Костыли """

def fix_name(name):
    if name.lower() == u'цой':
        return u'Виктор Цой'
    return name
