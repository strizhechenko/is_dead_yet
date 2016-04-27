# coding: utf-8

""" Бот, читает упоминания, отвечает когда кто умер """

import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from twitterbot_utils import Twibot, get_maximum_tweets
from twitterbot_utils.TwiUtils import remove_mention
from morpher import Morpher
from celeb import search

__author__ = "@strizhechenko"

SCHED = BlockingScheduler()
BOT = Twibot()
READER = Twibot(username=os.environ.get('reader_name'))
MORPHY = Morpher()
TIMEOUT = int(os.environ.get('timeout', 30))
TEMPLATE = unicode(os.environ.get('template', u''), 'utf-8')
TWEET_GRAB = int(os.environ.get('tweet_grab', 3))
TWEETS_PER_TICK = int(os.environ.get('tweets_per_tick', 2))
POSTED = get_maximum_tweets(BOT.api.home_timeline)
ANSWERED = get_maximum_tweets(BOT.api.mentions_timeline)

@SCHED.scheduled_job('interval', minutes=TIMEOUT)
def do_tweets():
    """ периодические генерация и постинг твитов """
    print 'New tick'
    tweets = BOT.api.mentions_timeline(count=TWEET_GRAB)
    tweets = [tweet for tweet in tweets if tweet not in ANSWERED]
    for request in tweets:
        name = remove_mention(request)
        answer = search(name)
        BOT.tweet(answer)
        ANSWERED.append(request)
    print 'Wait for', TIMEOUT, 'minutes'


if __name__ == '__main__':
    if '--wipe' in sys.argv:
        BOT.wipe()
        exit(0)
    do_tweets()
    if '--test' in sys.argv:
        exit(0)
    SCHED.start()
