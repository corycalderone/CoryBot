import praw
import pdb
import re
import os

reddit = praw.Reddit('digestbot')


def get_posts(username):
    # before anything, let's get our log file ready so we can check if we've sent any posts in the past...
    with open("log.txt", "r") as f:
        log = f.read()
        log = log.split("\n")
        log = list(filter(None, log))
    # cool. now let's get a look at some of the hot posts in these two subreddits...
    print("Getting subreddit posts...")

    # only 10 because AskReddit is more popular, only need a few from each to read during lunch.
    asksubmissions = list(reddit.subreddit("askreddit").hot(limit=10))

    # i'd like more from relationship_advice though, some of these stories are *crazy*!
    relsubmissions = list(reddit.subreddit("relationship_advice").hot(limit=50))
    subreddits = [asksubmissions, relsubmissions]

    # now are any of them particularly 'hot'? Say, a thousand comments or more?
    print("Searching for posts...")
    for subreddit in subreddits:
        for submission in subreddit:
            if submission.num_comments >= 1000 and submission.id not in log:
                print("Got one! Sending it over...")
                # add it to the log...
                log.append(submission.id)
                # then let's let someone (me) know about it!
                reddit.redditor(username).message(submission.subreddit.display_name + " post is blowing up!",
                                                  'Check it out: ' + submission.permalink)
                print("Sent!")

    # oh, can't forget about updating that log file! (I did the first time I ran this.)
    with open("log.txt", "w") as f:
        for post_id in log:
            f.write(post_id + "\n")
    print("All done for now.")


for item in reddit.inbox.unread(limit=None):
    if 'update' in item.body:
        get_posts(item.author.name)
