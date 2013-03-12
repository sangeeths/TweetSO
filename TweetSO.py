from apscheduler.scheduler import Scheduler
from datetime import datetime
import inspect
import logging

from stackexchange import StackExchange
from twitter import Twitter

logging.basicConfig(filename='/tmp/TweetSO.log', 
                    level=logging.DEBUG, 
                    format='[%(asctime)s]: %(levelname)s : %(message)s')

scheduler = Scheduler(standalone=True)

def _tweet(handle, questions, prefix=None):
    _title_max = 100
    if handle is None:
        logging.error("No twitter handle!!")
        return -1
    t = Twitter(handle)
    for q in questions:
        status = ""
        if prefix is not None:
            status += "[%s] " % prefix
        if len(q['title']) > _title_max:
            status += "%s... " % q['title'][0:_title_max]
        else:
            status += "%s " % q['title']
        status += q['link']
        t.tweet(status)
    logging.info("%s tweeted %d questions [prefix=%s]" % \
                (handle, len(questions), prefix))
    return len(questions)

@scheduler.cron_schedule(hour='0,4,8,12,16,20')
def TweetUnAnsweredCQuestions():
    s = StackExchange()
    questions = s.get_unanswered_questions(tagged='c')
    _tweet('CStackOverflow', questions, 'unanswered')

@scheduler.cron_schedule(hour='0,4,8,12,16,20')
def TweetFeaturedCQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='c')
    _tweet('CStackOverflow', questions, 'featured')

@scheduler.cron_schedule(hour='1,5,9,13,17,21')
def TweetUnAnsweredCppQuestions():
    s = StackExchange()
    questions = s.get_unanswered_questions(tagged='c++')
    _tweet('CppSO', questions, 'unanswered')

@scheduler.cron_schedule(hour='1,5,9,13,17,21')
def TweetFeaturedCppQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='c++')
    _tweet('CppSO', questions, 'featured')

@scheduler.cron_schedule(hour='2,6,10,14,18,22', minute='35')
def TweetUnAnsweredCSharpQuestions():
    s = StackExchange()
    questions = s.get_unanswered_questions(tagged='c#')
    _tweet('CSharpSO', questions, 'unanswered')

@scheduler.cron_schedule(hour='2,6,10,14,18,22', minute='35')
def TweetFeaturedCSharpQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='c#')
    _tweet('CSharpSO', questions, 'featured')

@scheduler.cron_schedule(hour='3,7,11,15,19,23', minute='6')
def TweetUnAnsweredHadoopQuestions():
    s = StackExchange()
    questions = s.get_unanswered_questions(tagged='hadoop')
    _tweet('HadoopSO', questions, 'unanswered')

@scheduler.cron_schedule(hour='3,7,11,15,19,23', minute='6')
def TweetFeaturedHadoopQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='hadoop')
    _tweet('HadoopSO', questions, 'featured')

@scheduler.cron_schedule(hour='4,8,12,16,20,24')
def TweetUnAnsweredJavaScriptQuestions():
    s = StackExchange()
    questions = s.get_unanswered_questions(tagged='javascript')
    _tweet('SOJavaScript', questions, 'unanswered')

@scheduler.cron_schedule(hour='4,8,12,16,20,24')
def TweetFeaturedJavaScriptQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='javascript')
    _tweet('SOJavaScript', questions, 'featured')


print('Press Ctrl+C to exit')
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass


