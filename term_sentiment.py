# -*- coding: utf-8 -*-
import sys
import json
import re
import string
from pprint import pprint

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
 

def build_new_dict(dict_old, tweets): #builds the dict of new terms
				      #tweets is the list of twitter dict objs
    dict_new = {} #[score, count, finalscore]
    for t in tweets:
	try:
	    # strings are already cleaned up during previous processing
	    wlist = t["text"].split() # assumes cleanup for text already done
	    for w in wlist:
		if dict_old.get(w): #word already in dict_old
		    pass
		else:
		    if not dict_new.get(w): #word not in dict_new, intialize
			dict_new[w] = [t["score_tweet"],1,0]	
		    else:
			dict_new[w][0] +=  t["score_tweet"]
			dict_new[w][1] += 1 
	    
	except KeyError:
	    pass
    for w in dict_new: dict_new[w][2] = dict_new[w][0] / dict_new[w][1] #final score 
    return dict_new
    
def main():
    sent_filename = (sys.argv[1])
    tweet_filename = (sys.argv[2])

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
    
    # get the new term dictionary, with scores stored in 3rd element
    dict_new = build_new_dict(score_dict_s, tweets)
    
    # print out the new terms and their scores
    for w in dict_new: print w.encode('utf-8'), dict_new[w][2]

if __name__ == '__main__':
    main()
