TweetSO
=======

By [Sangeeth Saravanaraj](https://github.com/sangeeths)

## About

`TweetSO` is an automated `Python` program which uses `StackExchange APIs` to retrieve the latest unanswered/featured questions from `StackOverflow` on a particular topic/tags (like `C`, `C++`, `C#`, `JavaScript`, `Hadoop`, etc) and tweets the questions using `Twitter APIs` to various Twitter handles.

## Requirements 
* Latest `Python` (> `2.7` preferred)

```
sudo pip install simplejson
sudo pip install tinyurl
sudo pip install apscheduler
sudo pip install oauth2
```

## What is APScheduler?
Advanced Python Scheduler (`APScheduler`) is a light but powerful in-process task scheduler that lets you schedule functions (or any other `Python` callables) to be executed at times of your choosing. `TweetSO` uses APScheduler to schedule the invocation of `StackExchange APIs` to retrieve questions. Further details on `APScheduler` can be found [here](http://pythonhosted.org/APScheduler/)


## What is needed from Stack Exchange?
The `StackExchange.com` provides `APIs` to add/delete/modify/view questions/answers/comments/users/badges/.. etc for sites like `StackOverflow` (and many more). `TweetSO/stackexchange.py::StackExchange:` is the class that is responsible for composing the `api.stackexchange.com` URL with various parameters like `fromdate`, `todate`, `tags`, `filters`, `pagesize`, `site`, etc and to retrieve the recent-unanswered and featured questions from `StackOverflow` for various tags like `C`, `C++`, `C#`, `JavaScript`, `Hadoop`, etc. The `api.stackexchange.com` is a public URL and so no registration is required. 


## What is needed from Twitter?
`TweetSO/twitter.py` is responsible for composing the `Twitter API` URL with data (questions fetched using `StackExchange APIs`) and tweet them to a given Twitter handle. In order to tweet a question, you need a Twitter account. Go to [Twitter](https://twitter.com/) and sign-up. Once after acquring a registered Twitter handle, we need to register a `Twitter App`. So go to [Twitter Dev](https://dev.twitter.com/) and click `sign-in` (top-right corner); enter `username` and `password` of your Twitter account. Once logged-in, click/mouse-over your account name (top-right corner where sign-in used to be) and in the drop down list, click `My applications`, then click `Create a new application`. Enter `Name`, `Description`, `Website`, then click `Create your twitter application`. Once your application is created, [Now comes the important part], you need to generate the following: `Consumer key`, `Consumer secret`, `Access token` and `Access token secret`. Note down the values for these four parameters. They are __important__. Do not share them with anyone. Apart from that you must ensure that the `Access level` is `Read, write, and direct messages`. This is all you need from Twitter! 


## How to use TweetSO?
Firstly, clone `TweetSO` using the following command:

```
git clone git@github.com:sangeeths/TweetSO.git
```

There will be no changes required in `TweetSO/stackexchange.py` and `TweetSO/twitter.py`. All we need to do is to update `TweetSO/stackexchange.py`

By default, `TweetSO/stackexchange.py` is configured to peridocally tweet unanswered/featured questions on various topics like  `C`, `C++`, `C#`, `JavaScript` and `Hadoop`. You can comment/remove them all. 

In order to configure `TweetSO`, you need to address three parts. 

Firstly, create your new function. For example: `def TweetUnAnsweredXXXXXXQuestions():`

### Scheduling
Use `scheduler` variable to schedule any functions. As of now, `TweetSO` uses `cron` scheduling. You are free to use other scheduling functions like `add_data_job()`, `add_interval_job()`, etc. 

### Creating an instance of StackExchange
```
s = StackExchange()
todate = int(time.time())
fromdate = todate - 1200        # last 1-hour
questions = s.get_noanswered_questions(tagged='XXXXX',
                                       fromdate=fromdate,
                                       todate=todate,
#                                      Any other arguments goes here  
                                       pagesize=15)
```

### Creating an instance of Twitter
```
_tweet('TwitterHandle', questions, 'PREFIX')
```

## What is missing? And, Why?
When a twitter handle (for example: `XXX`) is passed to `_tweet()`, the `TweetSO/twitter.py::Twitter` expects a `~/.XXX` file present with the following contents:

```
consumer_key        :   <consumer-key>
consumer_secret     :   <consumer-secret>
access_token_key    :   <access-token-key>
access_token_secret :   <access-token-secret>
```

`Consumer key`, `Consumer secret`, `Access token` and `Access token secret` are the parameters that you must have got when you registered and configured the `Twitter App`. Please add the details here. And, you are ALL set!


Thanks for trying `TweetSO`.

Please drop in an email to sangeeth.saravanaraj@gmail.com for comments and feedback.

`(c) TweetSO`

