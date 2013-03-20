from apscheduler.scheduler import Scheduler
from datetime import datetime
import inspect
import logging
import time

from stackexchange import StackExchange
from twitter import Twitter

logging.basicConfig(filename='/tmp/TweetSO.log', 
                    level=logging.DEBUG, 
                    format='[%(asctime)s]: %(levelname)s : %(message)s')

scheduler = Scheduler(standalone=True)

def _tweet(handle, questions, prefix=None, *suffix):
    _title_max = 65
    if handle is None:
        logging.error("No twitter handle!!")
        return -1
    t = Twitter(handle)
    for q in questions:
        status = ""
        # Add prefix: [featured]/[unanswered]
        if prefix is not None:
            status += "[%s] " % prefix
        if len(q['title']) > _title_max:
            status += "%s... " % q['title'][0:_title_max]
        else:
            status += "%s " % q['title']
        status += q['link']
        # NOTE: the suffix is a hashtag!
        for item in suffix:
            status += " #%s" % item
        logging.info("Tweet:[[%s]] length:[[%d]]" % (status, len(status)))
        t.tweet(status)
    logging.info("%s tweeted %d questions [prefix=%s]" % \
                (handle, len(questions), prefix))
    return len(questions)

# =============== CStackOverflow ===============
# Interval : 6-hours
# Tweets : 15-tweets/6-hours (max: 60-tweets/day)
@scheduler.cron_schedule(hour='0,6,12,18')
def TweetUnAnsweredCQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 7200    # last 2-hours
    questions = s.get_noanswered_questions(tagged='c',
                                           fromdate=fromdate,
                                           todate=todate,
                                           pagesize=15)
    _tweet('CStackOverflow', questions,
           'unanswered', 'C', 'StackOverflow')

# Interval : Once in a day @ 10:00 am
# Tweets : 15-tweets/day (max)
@scheduler.cron_schedule(hour='10')
def TweetFeaturedCQuestions():
    s = StackExchange()
# NOTE: for now, do not provide fromdate and todate
#       for featured question on 'C'; Low traffic
#    todate = int(time.time())
#    fromdate = todate - 86400       # last 24-hours
    questions = s.get_featured_questions(tagged='c',
#                                         fromdate=fromdate,
#                                         todate=todate,
                                         pagesize=15)
    _tweet('CStackOverflow', questions,
           'featured', 'C', 'StackOverflow')
# =============================================


# =================== CppSO ===================
# Interval : 6-hours
# Tweets : 15-tweets/6-hours (max: 60-tweets/day)
@scheduler.cron_schedule(hour='2,8,14,20')
def TweetUnAnsweredCppQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 7200    # last 2-hours
    questions = s.get_noanswered_questions(tagged='c++',
                                           fromdate=fromdate,
                                           todate=todate,
                                           pagesize=15)
    _tweet('CppSO', questions, 'unanswered',
           'Cpp', 'StackOverflow')

# Interval : Once in a day @ 11:00 am
# Tweets : 15-tweets/day (max)
@scheduler.cron_schedule(hour='11')
def TweetFeaturedCppQuestions():
    s = StackExchange()
# NOTE: for now, do not provide fromdate and todate
#       for featured question on 'C++'; Low traffic
#    todate = int(time.time())
#    fromdate = todate - 86400       # last 24-hours
    questions = s.get_featured_questions(tagged='c++',
#                                         fromdate=fromdate,
#                                         todate=todate,
                                         pagesize=15)
    _tweet('CppSO', questions, 'featured',
           'Cpp', 'StackOverflow')
# =============================================


# ================== CSharpSO =================
# Interval : 6-hours
# Tweets : 15-tweets/6-hours (max: 60-tweets/day)
@scheduler.cron_schedule(hour='3,9,15,21')
def TweetUnAnsweredCSharpQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 7200    # last 2-hours
    questions = s.get_noanswered_questions(tagged='c#',
                                           fromdate=fromdate,
                                           todate=todate,
                                           pagesize=15)
    _tweet('CSharpSO', questions, 'unanswered',
           'CSharp', 'StackOverflow')

# Interval : Once in a day @ 09:00 am
# Tweets : 15-tweets/day (max)
@scheduler.cron_schedule(hour='9')
def TweetFeaturedCSharpQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 86400       # last 24-hours
    questions = s.get_featured_questions(tagged='c#',
                                         fromdate=fromdate,
                                         todate=todate,
                                         pagesize=15)
    _tweet('CSharpSO', questions, 'featured',
           'CSharp', 'StackOverflow')
# =============================================


# ================== HadoopSO =================
# Interval : 6-hours
# Tweets : 15-tweets/6-hours (max: 60-tweets/day)
@scheduler.cron_schedule(hour='1,7,13,19', minute='30')
def TweetUnAnsweredHadoopQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 21600   # last 6-hours
    questions = s.get_noanswered_questions(tagged='hadoop',
                                           fromdate=fromdate,
                                           todate=todate,
                                           pagesize=15)
    _tweet('HadoopSO', questions, 'unanswered',
           'Hadoop', 'StackOverflow')

# Interval : Twice in a day @ 08:00 and 16:00 hours
# Tweets : 30-tweets/day (max) ; Very low traffic
@scheduler.cron_schedule(hour='8,16')
def TweetFeaturedHadoopQuestions():
    s = StackExchange()
    questions = s.get_featured_questions(tagged='hadoop',
                                         pagesize=15)
    _tweet('HadoopSO', questions, 'featured',
           'Hadoop', 'StackOverflow')
# =============================================


# ================ SOJavaScript ===============
# Interval : 4-hours
# Tweets : 15-tweets/4-hours (max: 90-tweets/day)
@scheduler.cron_schedule(hour='0,4,8,12,16,20')
def TweetUnAnsweredJavaScriptQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 1200        # last 1-hour
    questions = s.get_noanswered_questions(tagged='javascript',
                                           fromdate=fromdate,
                                           todate=todate,
                                           pagesize=15)
    _tweet('SOJavaScript', questions, 'unanswered',
           'JavaScript', 'StackOverflow')

# Interval : Thrice in a day @ 07:00, 15:00 and 23:00 hours
# Tweets : 45-tweets/day (max)
@scheduler.cron_schedule(hour='7,15,23')
def TweetFeaturedJavaScriptQuestions():
    s = StackExchange()
    todate = int(time.time())
    fromdate = todate - 28800       # last 8-hours
    questions = s.get_featured_questions(tagged='javascript',
                                         fromdate=fromdate,
                                         todate=todate,
                                         pagesize=15)
    _tweet('SOJavaScript', questions, 'featured',
           'JavaScript', 'StackOverflow')
# =============================================


print('Press Ctrl+C to exit')
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass


# __END__
