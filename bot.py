# coding: utf-8

""" Бот, читает упоминания, отвечает когда кто умер """

import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from twitterbot_utils import Twibot, get_maximum_tweets
from twitterbot_utils.TwiUtils import remove_mentions
from celeb.morpher import Morpher
from celeb.celeb import search

__author__ = "@strizhechenko"

SCHED = BlockingScheduler()
BOT = Twibot()
MORPHY = Morpher()
TIMEOUT = int(os.environ.get('timeout', 1))
TWEET_GRAB = int(os.environ.get('tweet_grab', 3))
print 'fetch answered'
ANSWERED = get_maximum_tweets(BOT.api.mentions_timeline)
print 'fetched answered'

@SCHED.scheduled_job('interval', minutes=TIMEOUT)
def do_tweets():
    """ периодические генерация и постинг твитов """
    print 'New tick'
    tweets = BOT.api.mentions_timeline(count=TWEET_GRAB)
    tweets = [tweet.text for tweet in tweets if tweet.text not in ANSWERED]
    for request in tweets:
        name = remove_mentions(request)
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
