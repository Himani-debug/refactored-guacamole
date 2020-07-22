# We would take some tweets and then analyze them using pandas and numpy.
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials

# So we are going to import both pandas and numpy.
# So I am just gonna say import numpy as np and then also import pandas as pd.
# So this is just a general convention this will allow us to refer to anything.
# From the numpy library by just using the dot operator.
# So we can say num np dot the name of the function thats provided from numpy.
# Similarly for pandas and want to access a funtion from pandas we can just say,
# pd dot the name of a function that comes from the module pandas.

import numpy as np
import pandas as pd


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

# I want to add a function in this twitter client class that is going to allow us to essentially,
# just get directly this twitter client API so we can interface with this API.
# And we can essentially extract data from the tweets that we get.
# So I am going to create another function in this twitter client class.
# So lets just go ahead and call it get twitter client API.
# Its gonna take self since its a member of this class and then I sm just going to retrun the variable that we defined up here.
# So we are just gonna return self dot twitter client.
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


# We will create another class which is going to be responsible for analyzing the tweets.
# that we extract from twitter. Lets call this class tweet analyzer.
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    # I want to create a function in this tweet analyzer class.
    # so tweets_to_data_frame is going to take the tweets that we have gotten here.
    # which is just this big JSON string and then convert it to a data frame so in this it will take self
    # as its a member of the class and it will also take the tweets that we want to convert to a data frame.
    def tweets_to_data_frame(self, tweets):

        # So I am going to create the data frame object and I am going to say df..
        # So this DataFrame is a function that is provided to us from pandas.
        # this will allow us to create a data frame based on some content that we feed it.
        # and then what we can do is we can specify the data that we want to make the data frame out of .
        # So we can say data is equal to and what we are going to want to do in this is give it a list and 
        # this list is going to be created from the tweets that we feed in to this funtion.
        # so I am going to say this is equal to the text of the tweet which we can extract by
        # essentially saying tweet.text, then I sm gonna explain what precisely this loop does. 
        # loop: for tweet in tweets.
        # so just to kind of unpack whats going on here we have specified this vairable that 
        # we are feeding into the data frame function and we are creating a list and we are 
        # looping through every single tweet in this tweets thing that we are feeding in here and
        # basically what we are doing is that we want to extract the text from each of those tweets so 
        # we are creating a list where each object in that list is the text of each of the tweets so thats 
        # what this data lists is corresponding to and then what we are going to do is we are gping to specify the 
        # column for which just to specify where these are going to live in the data frame. So I am going to give the
        # column a name so columns is equal to lets say tweets, just to specify kind of what we are storing in this column.
        
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        # Lets say that we also want to store the ID so we can say df['id']. So we are essentially creating a column in our dataframe with 
        # the heading ID and we can feed it in a numpy array which is going to be essentially a list of the content
        # that we are after for each of the tweets so in this case we are intrested in the ID of each of the tweets so we are going to want 
        # to loop through every single one of the tweets in the tweets that were given and then extarct the ID from that so I am just gonna 
        # say np.array so this is just a numpy array object that we are creating here and this is baically what the data frame we are creating a data frame
        # column based on this array and what we are converting to an array is a list so the list that we are going to be feeding into this is similar to what we saw above.
        # So again what we are doing is we take the tweets that we have in from this function, we are looping through each and every single one of those in that
        # list and then we are saying give me the ID of that particular tweet start an array, convert that array into an numpy array and then create a column in this data frame
        # with a heading ID based on every single one of those. So a lot is going in that one line.

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Geo Location'] = np.array([tweet.geo for tweet in tweets])

        


        return df
        # and then I am just going to go ahead and return the data frame that 
        # we have create here so down    


# Lets just go ahead and create a twitter client and then use that function that we created before,
# to allow us to get the API, so we can interface with that beacause thats what we are going to be using 
# to get the tweets before we analyze them.  
if __name__ == '__main__':

# So I am going to say twitter client which is a variable I am going to be defining,
# that equal to the twitter client class and then I am just going to go ahead and 
# call the function that we just created . I am gonna say api is equal to..
    twitter_client = TwitterClient()
# We need to create a tweet analyzer object for the class we have created.
#    
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    # So now API is a variable that has the twitter client object that we created in that.

# So now what I want to do is I also want to start streaming some tweets.
# so lets go ahead and define a variable that will just call tweets and this
# is going to be something that we can obtain from the client that we just created there
# So user timeline is a function that is provided from the twitter client API.
# It is not writtten by us. So this function will allow us to specify a number of things.
# One of the things we can specify is the user that we want to extract tweets from.
# and another thing that we can also specify in this funtion is how many tweets we want 
# to extract from that user.
# API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page]) this,
# Returns the 20 most recent statuses posted from the authenticating user or the user specified.
# screen_name – Specifies the screen name of the user.
# count – Specifies the number of statuses to retrieve.

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)


    #print(dir(tweets[0]))
# We can use the dot id methed here to allow us to extract what the ID of that particular tweet is. The code is: 
    #print(tweets[0].id)
# The output: 1276009507706081282. It showed us the id of first tweet.   
# Similarly we can get the retweet count by the following code: 
    #print(tweets[0].retweet_count)
# The retweet count is 5793. This is the output.
    


# Now we can say that data frame is equal to tweet_anaylzer.tweets_to_dataframe and then
# we will feed in the tweets that we have got this line up here so we have gotten our tweets 
# from using the client API and then what we are doing here is we are creating a data frame object
# which again is being returned from this function and then we are setting that equal to what this 
# function is doing which is essentially taking the tweets we have gotten converting that into a data frame
# and its storing in that data frame in df here.  
    df = tweet_analyzer.tweets_to_data_frame(tweets)

# So just to see what we have got we can go ahead and say print df.head. And this is just going to print out the first 
# couple elements in this case the first ten elements of the data frame we have created .  
    
    print(df.head(10))

# Note: We can figure out what other attributes of these tweets we can actually extract data from
# so if I say print(dir(tweets[0])) , what I am essentially doing is I am printing out the essentially the 
# information that we can extract from just the first tweet so this is going to show us what types of pieces of information we 
# we can extract from every tweet.     
# This is the output:

#['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__',
#  '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
#  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', '_json', 'author', 'contributors', 
# 'coordinates', 'created_at', 'destroy', 'entities', 'extended_entities', 'favorite', 'favorite_count', 'favorited', 'geo', 'id', 'id_str',
#  'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str',
#  'is_quote_status', 'lang', 'parse', 'parse_list', 'place', 'possibly_sensitive', 'retweet', 'retweet_count', 'retweeted', 'retweeted_status',
#  'retweets', 'source', 'source_url', 'text', 'truncated', 'user']


