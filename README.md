# Twitter Sentiment Analysis Assignment - "Introduction to Data Science"
This repo contains source code of my solutions to the Twitter sentiment analysis assignment from the "Introduction to Data Science" Coursera course. The large tweet dump has not been made available due to space constraints. Descriptions of files:  

*AFINN-111.txt*: Contains a list of pre-computed sentiment scores for (mostly) unigrams and (a few) bigrams. For more information on this file, see the AFINN-README.txt file. Henceforth, this file will be referred to as the "Dictionary".   

*AFINN-README.txt*: See above.  

*assignment1.html*: The assignment, consisting of 6 problems.   

*twitterstream_mod.py*: Source code to download tweets from Twitter API. Values of api_key, api_secret, access_token_key and access_token_secret have been changed.  

*tweet_sentiment.py*: Main solution file to problem 2. In this problem, sentiment scores had to be computed for each tweet. Each tweet's score was calculated as the sum of the scores of its constituent words/phrases. If a tweet contained a bigram from the Dictionary, then scores of the two constituent unigrams were not counted.  

*term_sentiment.py*: Main solution file to problem 3. In this problem, sentiment scores of tweet words NOT present in the Dictionary had to be inferred from the tweet scores calculated in problem 2. This was done by taking the average score of all tweets containing that word.   

*frequency.py*: Main solution file to problem 4. In this problem, relative frequencies of all unigrams in tweets were computed. Hashtags, usernames, urls, and miscellaneous puctuation were removed.  

*happiest_state_cleancopy.py*: Main solution file to problem 5. In this problem, the "happiest state" was to be determined based on the scores of tweets originating from that state. To determine which state a tweet originated from, the existence of the "place" field is checked. If it exists, then it is parsed to obtain the state. Failing that, if the "coordinates" field exists, then a ray-casting algorithm is used to determine which state polygon (i.e. boundary) the tweet coordinates fall into. Failing that, the tweet is discarded. Note: The long xml string of state polygons had to be included in the file since the assignment required self-sufficient execution (no dependence on external files).  

*top_ten.py*: Main solution file to problem 6. In this problem, the top ten most frequently occuring hashtags were to be computed.


