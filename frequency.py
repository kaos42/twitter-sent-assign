# -*- coding: utf-8 -*-
import operator
import sys
import json
import re
import string
from pprint import pprint

def regex_url():
    url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    return url_regex

def regex_hashtags():
    ht_regex = re.compile(ur'(?<=^|(?<=[^a-zA-Z0-9-_\\.]))#([A-Za-z]+[A-Za-z0-9_]+)')
    return ht_regex

def regex_users():
    users_regex = re.compile(ur'(?<=^|(?<=[^a-zA-Z0-9-_\\.]))@([A-Za-z]+[A-Za-z0-9_]+)')
    return users_regex

def parse_tweets(tweet_file): # returns a list of dicts, each dict a tweet object
    tfile = open(tweet_file, 'r')
    tweets = []
    for line in tfile:
        tweets.append(json.loads(line)) # json.loads() returns a dict       
    tfile.close()
    return tweets

def string_cleanup(s): #remove punctuation and convert to lowercase
    s1 = s.encode('utf-8').translate(None, string.punctuation)
    s1 = s1.decode('utf-8')
    s1 = s1.lower()
    return s1

def cleanup_tweets(tweets):
    #Remove all non-tweets
    tweets = [t for t in tweets if t.get("text")]

    re_url = regex_url()
    re_hash = regex_hashtags()
    re_users = regex_users()
    for t in tweets:
	try:
	    t["text"] = re_url.sub(" ",t["text"])
	    t["text"] = re_hash.sub(" ",t["text"])
	    t["text"] = re_users.sub(" ",t["text"])
	    t["text"] = string_cleanup(t["text"])
	except KeyError:
	    pass
    return tweets

def build_freq_dict(tweets): #term:freq dict
    freq_dict = {}
    for t in tweets:
	try:
	    words = t["text"].split() #punctuation cleanup is NOT assumed
	    for w in words:
		if not freq_dict.get(w):
		    freq_dict[w] = 1.0
		else:
		    freq_dict[w] += 1.0
	except KeyError:
	    pass
    total_freq = sum(freq_dict.values())
    for w in freq_dict:
	freq_dict[w] /= total_freq
    return freq_dict

# generate the tweets list of dicts
# feed it into a function that will split it by space (no punctuation cleanup)
# build the freq dict

def main():
    tweet_filename = (sys.argv[1])
     
    # get list of dicts, each dict object is a 
    # streaming message object (mostly tweets)
    tweets = parse_tweets(tweet_filename)

    #remove hashtags, users, urls, and misc puctuation from tweets, convert to lowercase
    tweets = cleanup_tweets(tweets)

    # term:freq dict. Only single words
    freq_dict = build_freq_dict(tweets)

    # print the terms in descending order
    sorted_freq = sorted(freq_dict.items(), key = operator.itemgetter(1), reverse = True)
    #for w in freq_dict: print w.encode('utf-8'), freq_dict[w] 
    for w,f in sorted_freq: print w.encode('utf-8'), str(f)

if __name__ == '__main__':
    main()
