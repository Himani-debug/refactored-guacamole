# We are going to analyze the sentiment of a given tweet,so we are gonna determine whether or not the sentiment of a given tweet is 
# overly positive , negative or neutral and for this purpose we are going to make use of a module called text blob. This particular 
# module has a bulit in sentiment analyzer that is already trained on data so we can just make use of the analyzer itself to apply to
# our tweets to determine whether or not they are positive or negative based on this text blob analyzer.
# 

from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# I will say from textblob import the class TextBlob.
from textblob import TextBlob
 
import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# This module will be made use of to clean the tweet essentially to remove any extra characters or hyperlinks or things that are not 
# necessarily indicative of the actual text content as part of the tweet we want to remove all that because 
# that is not necessarily going to help us in figure it out the sentiment of a given tweet. 
import re


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_secret)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
# I am going to add some functions here in the tweet analyzer class, the first function which I am just going to call it clean tweet 
# will make use of the regular expression library to clean the tweet and remove any hyperlinks or extra characters, so as it is a 
# member of the class it is gonna take self and then also the tweet to be cleaned.
# In return all that is going on here looks a bit complicated but it is just removing special charcters from the string from the tweet
# specifically and then removing the hyperlinks and returning the results of that clean tweet,We have a function 
# that does that , it is responsible for that.
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#  Now we want another function that is going to be responsible for calling text blob and using sentiment analyzer
# provided from text blob and then returning the sentiment so lets call this function analyze_sentiment, this will
# be taking self and then also the tweet that we want to analyze the sentiment of ,so we go ahead and create an object 
# that will be returned to us from text blob , we will call this object analysis and we will set this equal to text blob 
# and then what we are going to feed into this is essentially what we want to analyze the sentiment of which in this case 
# is the cleaned tweet so we are going to say self.clean_tweet and then we are going to feed in that tweet we get into this
# function , make sure that it is clean passing the clean tweet into this text blob thing this class and then this will allow
# us to leverage the sentiment analysis tools the text block provides to us so now what we are gonna do is we are going to do 
# just that. So we are gonna say if analysis.sentiment.polarity. So what we are doing here is: analysis is the object created 
# from textblob there is a fuction to that called sentiment which will make use of the sentiment analysis engine and then there
# is a further function that is called polarity , which is a propertry of that analysis which basically tells us whether or not
# the tweet in this case is positive or negative. So the polarity is a metric of whether or not that tweet is positive or negative 
# in nature. If this is greater than zero we are gonna return one. So this is to indicate that the polarity is positive, so its a
# positively interperted tweet, so we are gonna return one in that case. So else if the analysis.sentiment.polarity , if this is 
# equal to zero then we essentially dont know whether or not its positive or negative. So its just going to be neutral ,so if its 
# just a neutarlly analyzed tweets, we are just going to return zero to denote that. So zero will be the case when the tweet is just 
# a neutral tweet and then otherwise the case would be that the polarity is negative and in that case the sentiment analysis engine 
# determined that this tweet is actually negative so what we are going to do to denote that is return minus one. So that would be the 
# way that we make use of this function to let the user know that the tweet was analyzed to be negative .      
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

# So we are going to add another column to the dataframe which is going to be the sentiment analysis for each of the tweets that we have
# in this dataframe. So what we are going to do is we are going to create another column called as sentiment and this is going to have the
# One , zero or minus one depending on the sentiment analysis of that tweet.
    
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))


    #OUTPUT:
# Tweets    id  len date source likes retweets sentiment
#0  RT @GeraldoRivera: Here’s #RussianBounty story...  1277806112184700935  139 2020-06-30 03:28:12  Twitter for iPhone      0      4152          0
#1  RT @TeamTrump: White House Press Secretary @Ka...  1277805960090845184  140 2020-06-30 03:27:36  Twitter for iPhone      0      5435          0
#2  RT @TeamTrump: White House Press Secretary @Ka...  1277805817039904769  139 2020-06-30 03:27:01  Twitter for iPhone      0      4749          0
#3  RT @TeamTrump: White House Press Secretary @Ka...  1277805779572097027  140 2020-06-30 03:26:52  Twitter for iPhone      0      4489          0
#4  RT @WhiteHouse: "President @realDonaldTrump st...  1277805348435513344  140 2020-06-30 03:25:10  Twitter for iPhone      0      9620          1
#5  RT @PressSec: “Law and Order are the building ...  1277805288859537409  140 2020-06-30 03:24:55  Twitter for iPhone      0     11899         -1
#6  RT @GOPChairwoman: Joe Biden oversaw an anemic...  1277805214511140866  140 2020-06-30 03:24:38  Twitter for iPhone      0      6441          0
#7  RT @GOPChairwoman: We are witnessing the Great...  1277804459230466049  139 2020-06-30 03:21:38  Twitter for iPhone      0      4832          1
#8  RT @RepJimBanks: I just left the White House w...  1277725020639375360  140 2020-06-29 22:05:58  Twitter for iPhone      0     16670          1
#9  RT @realDonaldTrump: Senator Jim Inhofe (@Inho...  1277690894653816832  139 2020-06-29 19:50:22  Twitter for iPhone      0     13154         -1
# So we can conclude that donald trump is a neutral or positive person in all through the sentiment analysis.