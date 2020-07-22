from tweepy import API 
# For performing pagination we import the cursor module.
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials

# # # # TWITTER CLIENT # # # #

class TwitterClient():
    # Lets first create a client constructor object.
    def __init__(self, twitter_user=None):
        # Then we will create an authenticator object, so this is why we created the authenticator class.
        # This is just going to be the auth object so that we can properly authenticate to communicate with the twitter API.
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        # Then we are going to define another variable which is called twitter client.
        # This is going to be equal to API which you will notice is one of the two things..
        # that we imported from .
        self.twitter_client = API(self.auth)

        # So if we want to do that for a specific user someone other than myself.
        # So we are going to create another variable here which we will call self.twitter_user=
        # twitter_user , we have a defined Twitter user yet we are going to pass it into the int constructor.
        # As an argument basically what we will do is we will instantiate an object a twitter client object and
        # what what we want to do is we want to allow the person who is using this code to specift a user that
        # they can get the timeline tweets from but actually what we are gonna want to do is we are going to
        # put in a default argument of none . This is a default argument and if nothing id specified here for twitter
        # user it just defaults to none and it will go to our own timeline. 
        self.twitter_user = twitter_user

# Lets start off with a function that will allow us to get tweets from the user timeline.
# We are going to pass in the parameter self , since this is a class method.
# and then we are also going to pass in another argument here which is called num_tweets.
# and this will allow us to determine how many tweets we want to actually show or extract. 
    def get_user_timeline_tweets(self, num_tweets):
        # So we are going to define a list called tweets an empty list.
        # So we are gonna loop through a certain number of tweets
        # and then for each one we are going to store that in the list.
        # and then return that list to the user. 
        tweets = []
        # So we want to specify a user so we will be doing that. so the 
        # way that we tell the tweepy API that we have specified a user is in this cusor funtion here.
        # this method wil say ID is equal to self.twiiter_user, so that will do that.
        # So now that we will actually get the user title ID tweets for whatever user we specify.
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
        # So we import a cursor, this is a class that will allow us to essentially get the user timeline tweets.
        # The client object had been created in the constructor..there is method for every object derived from this,
        # API class that has this user timeline functionality and allows you specifying a user to get the tweets off that users timeline.
        # So if we havent specified a user and in that case , it just defaults to you.
        # So if that argument is none which it is by default then it will just get your own timeline tweets.
        # Then there is a parameter for the cursor object called dot items and that will tell this thing how many tweets to actually get from
        # from the timeline so we can specify that as an argument sent in this function here.
        # So what we will do in this loop we are a liitle bit through every tweet that this cursor object provides us.
        # And what we can do it we could say tweets dot append to tweet is the list that we are storing these things in.
        # And then we can just return the tweets list and that will now consist of a list of all the user timeline tweets.
    
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
    # What we will do in this class is , we are going to have a function.
    # So we are going to define a function called authenticate twitter app.
    # Its class method so it will take self as a parameter.


    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_secret)
        return auth
        # Then we are going to return the auth object that we createdin this function.


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


    # If we might want to do a little bit more checking here namely tweepy api.
    # It imposes these things most specifically the twitter api imposes these things called rate limits.
    # And essentially if you are throtting the twitter api, trying to get all this information.
    # and twitter dosent like that, it might try to stop you from abuding the system.
    # So basically if twitter thinks that you are doing that, its going to give you an error messsage.
    #  which is going to be a 420 message and thats going to be like hey if you keep doing this..
    # that will essentially kick you out. 
    # So basically the first time you get this message there is a window of time there.
    # where we havr to wait to access the tweets again and if you keep accessing tweets and,
    # you ignore those messages that window of time increases exponentially , so you could lock yourself out of accessses information.
    # So its worthwhile to check that the status message the error code that you are receiving are of not this form.
    # So what we want to do is we want to say if the status is equal to this error code which is 42o in this case.,
    # We want to just return false outright, thats it we just want to kill the connection.
    # so that way you dont accidentally boot youself from accessing information on twitter.      
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]
    fetched_tweets_filename = "tweets.txt"

# Lets go ahead and give that a run to verify that actually worked so the way 
# that we are going to do that remember is instantiate the twitter client object based 
# On who we want to get the timeline tweets tweets from so in this case I am going to 
# specify based on a user PyCon. It is a conference that focuses on the python programming language.
# It is this user form which we want to extract the tweets. 
# We can try something different.
# Refer to this for more methods of api:  http://docs.tweepy.org/en/v3.5.0/api.html.

    twitter_client = TwitterClient('pycon')
    print(twitter_client.get_user_timeline_tweets(1))

#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)