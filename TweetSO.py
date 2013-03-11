from twitter import Twitter
from stackexchange import StackExchange

from datetime import datetime
import inspect
import logging

from apscheduler.scheduler import Scheduler

logging.basicConfig(filename='/tmp/TweetSO.log', 
                    level=logging.DEBUG, 
                    format='[%(asctime)s]: %(levelname)s : %(message)s')

scheduler = Scheduler(standalone=True)

def _get_handlers(op):
    return (Twitter(op), StackExchange())

def _log(func, q):
    logging.info("%s : tweeted %d questions" % (func, q))

@scheduler.cron_schedule(hour='0,4,8,12,16,20')
def TweetUnAnsweredCQuestions():
    (t, s) = _get_handlers('CStackOverflow')
    questions = se.get_unanswered_questions(tagged='c')
    for q in questions:
        t.tweet("[unanswered] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))
    
@scheduler.cron_schedule(hour='0,4,8,12,16,20')
def TweetFeaturedCQuestions():
    (t, s) = _get_handlers('CStackOverflow')
    questions = s.get_featured_questions(tagged='c')
    for q in questions:
        t.tweet("[featured] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='1,5,9,13,17,21')
def TweetUnAnsweredCppQuestions():
    (t, s) = _get_handlers('CppSO')
    questions = se.get_unanswered_questions(tagged='cpp')
    for q in questions:
        t.tweet("[unanswered] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='1,5,9,13,17,21')
def TweetFeaturedCppQuestions():
    (t, s) = _get_handlers('CppSO')
    questions = se.get_featured_questions(tagged='cpp')
    for q in questions:
        t.tweet("[featured] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='2,6,10,14,18,22')
def TweetUnAnsweredCSharpQuestions():
    (t, s) = _get_handlers('CSharpSO')
    questions = se.get_unanswered_questions(tagged='c#')
    for q in questions:
        t.tweet("[unanswered] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='2,6,10,14,18,22')
def TweetFeaturedCSharpQuestions():
    (t, s) = _get_handlers('CSharpSO')
    questions = se.get_featured_questions(tagged='c#')
    for q in questions:
        t.tweet("[featured] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='3,7,11,15,19,23')
def TweetUnAnsweredHadoopQuestions():
    (t, s) = _get_handlers('HadoopSO')
    questions = se.get_unanswered_questions(tagged='hadoop')
    for q in questions:
        t.tweet("[unanswered] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='3,7,11,15,19,23')
def TweetFeaturedHadoopQuestions():
    (t, s) = _get_handlers('HadoopSO')
    questions = se.get_featured_questions(tagged='hadoop')
    for q in questions:
        t.tweet("[featured] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='4,8,12,16,20,24')
def TweetUnAnsweredJavaScriptQuestions():
    (t, s) = _get_handlers('SOJavaScript')
    questions = se.get_unanswered_questions(tagged='javascript')
    for q in questions:
        t.tweet("[unanswered] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))

@scheduler.cron_schedule(hour='4,8,12,16,20,24')
def TweetFeaturedJavaScriptQuestions():
    (t, s) = _get_handlers('SOJavaScript')
    questions = se.get_featured_questions(tagged='javascript')
    for q in questions:
        t.tweet("[featured] %110s - %s" % (q['title'], q['link']))
    _log(inspect.stack()[0][3], len(questions))



print('Press Ctrl+C to exit')
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass


