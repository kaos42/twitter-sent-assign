''' Calculate the top ten hashtags and their frequencies from the tweets
for t in tweets, t["entities"]["hashtags"][hashtag index starting from 0]["text"]
1) build the tweets object
2) for t in tweets, 
'''
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys
import json
import re
import string
from pprint import pprint
import operator
import collections

def parse_tweets(tweet_file): # returns a list of dicts, each dict a tweet object
    tfile = open(tweet_file, 'r')
    tweets = []
    for line in tfile:
        try:
            tweets.append(json.loads(line)) # json.loads() returns a dict       
        except ValueError: pass # lines with wierd escape characters, not bothering to fix now
    tfile.close()
    return tweets

def get_top_dict(tweets): 
    top_dict = {}
    for t in tweets:
     if t.get('entities'):
         htlist = t['entities']['hashtags']
         if htlist: #not empty
             while htlist:
                 h = htlist.pop()
                 htag = h.get("text")
                 #h is a dict of ith hashtag. "text" stores the tag
                 #update the top_dict
                 if htag: #just making sure that there is actually a tag
                     if top_dict.get(htag): #update existing, inc the count
                         top_dict[htag] += 1
                     else: #first entry
                         top_dict[htag] = 1
    return top_dict

def main(): #usage: python top_ten.py output_more.txt
    
    tweet_filename = sys.argv[1]

    # get list of dicts, each dict object is a 
    # streaming message object (mostly tweets)
    tweets = parse_tweets(tweet_filename)

    #get the top hashtag dict
    d = get_top_dict(tweets)

    #print the top 10 hashtags
    topd = collections.Counter(d)
    for k,v in topd.most_common(10):
        print k,v
   
if __name__ == '__main__':
    main()

