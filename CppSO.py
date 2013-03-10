from twitter import Twitter
from stackexchange import StackExchange

t = Twitter('CppSO')
se = StackExchange(tagged='cpp')

questions = se.get_unanswered_questions()
for question in questions:
    t.tweet("%s - %s" % (question['title'], question['link']))

print "%d questions tweeted!" % len(questions)


