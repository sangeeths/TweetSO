from twitter import Twitter
from stackexchange import StackExchange

t = Twitter('CStackOverflow')
se = StackExchange(tagged='c')

questions = se.get_unanswered_questions()
for question in questions:
    t.tweet("%s - %s" % (question['title'], question['link']))

print "%d questions tweeted!" % len(questions)


