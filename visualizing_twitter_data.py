from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials
import numpy as np
import pandas as pd
# I am importing the matplot library specifically from that I am importing pyplot and then I am 
# going to refer to that as plt as a shorthand similar to what we did for numpy and for pandas
import matplotlib.pyplot as plt


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

    #print(dir(tweets[0]))
    #print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

# Lets say we want to figure out what is the average length of all the tweets that we have in our data
# frame so we here collect 20 tweets and we want to figure out , what is the average length of all of those 
# 20 tweets and of course we can change this count from 20 to 200 or 400.
# Now that we have stored everything in this dataframe its going to make it really easy form us to just manipulate the data
# thats already present in that data frame and then just get this answer and the way that we can do that is by manipulating 
# the mean function in numpy which is just going to be something that we are going to run on a list in the data frame so I am 
# just going to print out the result that comes from running the mean function, so I am going to say np.mean , so I am calling 
# the mean function and what am I calling the mean function on I want to figure out the mean of the length of the tweets so I am 
# saying df['len'] so basically what I am doing there is df length is going to return a list its going to return a list of all of 
# the links of all of the 20 tweets in this case and the we are going to be running the mean function which is provided to us from
# numpy on that list and that we are going to get a single number which we are printing out to the screen, so thats what is going on in
# this line .


    # Get average length over all tweets:
    #print(np.mean(df['len']))

# Another thing we can ask is lets say we want to figure out what is the tweet that received the most
# likes in the sample that we have gotten. Here instead of taking the mean over a list what I want to 
# do is take the max because what we want to do is we want to figure out the maximum no. of likes that 
# is from the likes column in our data frame so the likes column stored all of the number of likes for 
# every given tweet. I am taking the max of that list using the max function and then I am printing that 
# out to the screen .

    # Get the number of likes for the most liked tweet:
    #print(np.max(df['likes']))

# Similarly we can get the most no. of retweets by following the same syntax.
    # Get the number of retweets for the most retweeted tweet:
    #print(np.max(df['retweets']))
    
    #print(df.head(10))

    # Time Series

#   Lets say hypothetically that we want to do is we want to create a time series plot thats
# going to show us the number of lets say likes that Donald Trump recevied on any given day over 
# the course of some days which we can extract from, you know some given count here so we extract lets 
# say two hundred tweets maybe thats over you know ranged over some number of days and then for every one 
# of those days donald trump got a certain number of likes, we want to plot that number of likes and he got 
# on a given day and then just plot that for every given day over this time series of dates.

# So lets create a variable which we will call time_likes this is going to be equal to a panda's series object.
# So we are essentially creating a series onject- so we can eventually plot this as a time series so I want to say
# this is equal to pd.Series and then this takes two things the data, so there is a data frame that we want to feed
# it which is going to be tough values so this is pd data frame of likes so we want to actually get in the number of
# likes. So we are getting the values of the each of the likes, so every day there is going to be a certain number of 
# likes that are given and we are extracting the values from that and then what we also want to receive in this time series 
# function is the index and the index is essentially the x-axis so what we are plotting and then for each what we want to do
# is for each day show the number of likes so the number of likes is kind of the y-axis, the date is the time series isself 
# the number of days so we are going to set the index is equal to the data frame of the date which is something that we have 
# already extracted from before from our data frame so this is our time series object we have created from pandas and now thats 
# ready for us to actually just go ahead and plot that so what we can do is we could say a time_likes.plot and what we can do is 
# we can feed this a few arguments, I am going to be feeding this plot funtion with two arguments, baically just the size of the 
# figure which specifies how big this graph is going to be and lets say the color so this is going to be the color of the line thats 
# plotted throughout the days for every given day so I am gonna say figsize is equal to (16,4) that just the XY axis of the image that
# we are gonna see and then also the color which we can put as red so the function takes in a string in this case its just a single 
# character that corresponds to a given color .
# So then what we do once we have kind of craated our  data that we are going to plot once we have created our plot that we are going 
# to show we actually need to show the plot so we are going to say plt.show(). So now this plt is something that we need to import from matplotlib.
# which is going to allow us to show the plots that we have created. 


    #time_likes = pd.Series(data=df['len'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), color='r')
    #plt.show()
    
    #time_favs = pd.Series(data=df['likes'].values, index=df['date'])
    #time_favs.plot(figsize=(16, 4), color='r')
    #plt.show()

# Lets do the time series for retweets , instead of time_likes lets call this time_retweets.
# We still want to see how the number of retweets changes over the course of a given set of days. 
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), color='r')
    #plt.show()

# To compare two graps we can bunch the time series together onto one plot so instead of plotting two
# spearate time series where we have one for the number of likes and one for the no. of retweets one thing 
# we can do is we can just put them on the same plot and see how they correlate.
# I am going to add a label because we are going to have two lines on this time series
# one is going to be a label for the number of likes and one is going to be a label for
# the number of retweets. And then I am going to put in a legend=true. So this basically 
# will put in a little box in the time series chart which will show us what line corresponds
# to what label and that is going to be kind of helpful because whats nice about pandas and matlpotlib
# is that if we plot multiplr lines here it will be smart enough to distinguish them by assigning them a
# different color and then what we are doing here is we are essentially just labeling to each of those lines 
# from whatever they represent and then we are going to put in a legend which is essentially going to correspond
# to this blue line is likes , this orange line is retweets, its going to be easier for us to kind of visualize 
# whats going on. 
 
    # Layered Time Series:
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    
    plt.show()

    # Trial time series 
    #time_likes= pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16,4),color='r')
    #plt.show()