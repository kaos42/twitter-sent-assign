# -*- coding: utf-8 -*-
import sys
import json
import re
import string
from pprint import pprint

# def hw():
#     print 'Hello, world!'

def lines(fp):
    f = open(fp, 'r')
    print str(len(f.readlines()))
    f.close()

def build_score_dict(sent_file): # term : score. 
    afinnfile = open(sent_file, 'r')
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t") # The file is tab-delimited 
        uterm = term.decode('utf-8') # Convert all byte strings to unicode
        scores[uterm] = int(score)  # Convert the score to an integer.
    afinnfile.close()
    return scores

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

def calc_phrases(tweets, dict_phrases): # calculates scores from phrases
                                         # tweets is a list of dicts
    sum = 0
    for t in tweets:
        try:
            t["text"] = string_cleanup(t["text"])
            for phrase in dict_phrases:
            # match phrase in t string, note that only tweets have field "text" 
            # count all instances of phrase, and replace by @   
                myregex = r'\b' + re.escape(phrase) + r'\b'
                count = len(re.findall(myregex, t["text"])) 
                t["text"] = re.sub(myregex, " @ ", t["text"])
                sum += (count * dict_phrases[phrase])
        except KeyError: # catching non-tweets
            pass
        t[u"score_tweet"] = sum
        sum = 0
    return tweets # list of tweet dicts, each dict has a score_phrase key/value

def calc_singles(tweets, dict_singles): # calcualtes scores from single words
                                        # tweets is a list of dicts
                                        # assumes phrases have been replaced by @
    sum = 0
    for t in tweets: 
        try:
            wlist = t["text"].split() # assumes cleanup for text already done
            for w in wlist:
                if dict_singles.get(w): sum += dict_singles[w]
        except KeyError: # catching non-tweets
            pass
        try:
            t["score_tweet"] += sum # Add the single score to the phrase score
        except KeyError:
            print "Error in calc_singles: Tweets (list of dicts) has \
                not been updated with new score field"
            exit(0)
        sum = 0
    return tweets

def split_dict(dict_full):
	dict_phrase = {}
	dict_single = {}
	for k,v in dict_full.items():
		if re.search(r'\s', k):
			dict_phrase[k] = v
		else:
			dict_single[k] = v
	return (dict_phrase, dict_single)
    

def main(): #usage: python tweet_sentiment.py sentiment_file output_file
    
    # sentiment file is "AFINN-111.txt"
    sent_filename = sys.argv[1]
    tweet_filename = sys.argv[2]

    # Build the term:score dictionary. 
    score_dict = build_score_dict(sent_filename)
    
    # split into single word and phrase dictionaries
    score_dict_p, score_dict_s = split_dict(score_dict)
    
    # get list of dicts, each dict object is a 
    # streaming message object (mostly tweets)
    tweets = parse_tweets(tweet_filename)
    
    # get scores from phrases: update tweets with score_phrases field
    tweets = calc_phrases(tweets, score_dict_p)   
         
    # get scores from single words: 
    tweets = calc_singles(tweets, score_dict_s)
    
    # print scores to stdout
    for t in tweets: 
        print t["score_tweet"]
      

if __name__ == '__main__':
    main()
