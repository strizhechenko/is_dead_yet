# coding: utf-8

""" узнаём о знаменитостях живы ли они ещё, когда умерли/сколько лет """

import urllib2
from date import wiki_dates
from custom import fix_name

WIKI = 'https://ru.wikipedia.org/wiki/'


def __name2url(name):
    """ превращает имя в URL на wikipedia """
    return WIKI + name.replace(' ', '_')


def download(name):
    """ вытягивает статью википедии """
    url = __name2url(name).encode('utf-8')
    return urllib2.urlopen(url).read()


def search(name):
    """ Логика для примера """
    name = fix_name(name)
    try:
        data = download(name)
    except urllib2.HTTPError:
        return u'%s? Это кто вообще?' % (name,)
    birth, death = wiki_dates(data)
    return u'%s: рождение - %s, смерть - %s' % (name, birth, death)


def test_work():
    test_data = [
        u'Людмила Гурченко',
        u'Борис Моисеев',
        u'Алла Пугачёва',
        u'Ленин',
        u'Ельцин',
        u'Твоя мамка',
        u'Цой',
    ]
    for n in test_data:
        print search(n).encode('utf-8')

if __name__ == '__main__':
    test_work()
