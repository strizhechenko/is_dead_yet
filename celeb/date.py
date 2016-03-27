# coding: utf-8
""" выдёргивание дат """
from lxml.html import fromstring

NOT_YET = u'ещё нет'
def wiki_date_day(tree, _day):
    day = tree.xpath('//*[contains(@class, "%s")]' % (_day,))
    if not day:
        return NOT_YET
    if day[0].text.strip():
        return day[0].text.strip()
    for i in day:
        if i.tag == 'span':
            return i.text.strip()



def wiki_dates(data):
    """ выдирает даты рождения и смерти из википедии """
    tree = fromstring(data)
    return wiki_date_day(tree, 'bday'), wiki_date_day(tree, 'dday')
