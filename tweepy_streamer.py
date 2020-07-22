# StreamListener is a class that is from the tweepy module.
# It will alow us to listen to the tweets'
# They are kind of firehose of tweets as they cone based on certain keywords or hastags.
from tweepy.streaming import StreamListener
# We also need to import one more module for authentication.
# OAuthHandler, this class is responsible for authenticating.
# Based on the credentials we had saved on the twitter_credentials file.
# for associated with the twitter app.
from tweepy import OAuthHandler
# This will help in streaming.
from tweepy import Stream
 
import twitter_credentials
 
# # # # TWITTER STREAMER # # # #



class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This is a class method so it takes the object of self.
        # So instead of printing just tweets to the terminal we can perhaps.
        # I want to save tweets to a text file or a JSON file so that way I can process them.
        # So I am going to allow the ability for us to pass in a name 
        # which will be the file name of the tweets that will pass in 
        # And then I will also have a hastag list here.
        # So this will just be the list  of keywords or hastags we wish to filetr the tweets out.
        # This handles Twitter authetification and the connection to Twitter Streaming API

        # Lets create a listener object.
        # This is an object of the class StdOutListener.
        # Which is inheriting from the stream listener class.

        listener = StdOutListener(fetched_tweets_filename)

        # Then what we are going to do is we are going to want to authenticate.
        # We are going to authenticate using the credentials that we had stored.
        # So we are gonna create this variable called auth and we are going to say OAuthhandler.
        # which is the class that we are importing from tweepy .
        # which is going to be responsible for actually authenticating to our code.
        # We are going to pass it in the credentials.
        # So this is in order to define this auth object of the  OAuthhandler class.
        # It takes these two arguments that we need to pass in.
        
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        # then in order for us to complete the authentication process we are going to say auth.set access.
        # This is a method which is provided from the OAuthhandler class.
        # This method also takes two agruments and that takes the access token ans acess token secret.
        # At this point our application should be authenticated.
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_secret)
        # So we will create a Twitter stream .
        # We will create a variable called stream equal to this lane which is the class Stream.
        # that we imported above. we are gonna pass two things.
        # The authentication token to verify that we have actually authenticated it properly.
        # And then the listener object that we created .
        # The listener object is just responsible for how do I deal with the data that is tweets.
        # And do I do with the error if I enconuter an error.
        stream = Stream(auth, listener)
        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)
        # One final thing we can do this to filter the tweets.
        # Lets say we want to stream tweets that are focused on some keywords or hashtags.
        # So what we can do is say stream dot filter.
        # This is a method that is also provided by the stream class.
        # This takes a list one of things that we can take is an optional parameter of a list.
        # Which is called track and in this track list we can provide it a list.
        # Of things which if the tweet contains any of these lists objects then it will apply.
        # it will say I will add this to the stream .


# # # # TWITTER STREAM LISTENER # # # #

# This class standard out listener is going to actuaaly inherut from stream listener class.
# Stream listener class provides methods that we can directly override


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    # We will create a constructor for this thing, coz what I want to do is 
    # I want to create a StdOutlistener class or object rather.
    # That may be associated with a filename that these are going to be wirting to.
    # So where do we want to store the tweets so 
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

# So one of the methods is on undersore data.
# its a class method that takes in a parameter data.
# FUNCTION: it is an overrun method which will take in data.
# That is streamed in from the stream listener , the one that is listening for tweets.
# And then it will print that data and we can begin our analysis.
    def on_data(self, data):
        # We can have a try except statement here.

        try:

            # we are just going to print data .
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            # Then return true to make sure that everthing went well. 
            # We will also append them as we want to continually add the tweets as we stram them from the api.
            return True
        # The except will say base exception and then if that exceptipn is hit .
        # It will say print error on data just to make sure that we know if the method we are in .
        # Then lets print out the actual error message so we will print out the string of e.
        # and then we will return true.
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
# There is another one that we can also override called on error.
# This also is a class method and it takes a status variables.
# It will be trigerred if there is an error that occurs.

    def on_error(self, status):
        # Then i just printed out that error which is passed in through this status variable.
         print(status)

# So if we encounter an error what will happen is this method will be triggered.
# and will print the status message of that error to the screen. 


# We need to create an object from this standard out listener class that we just created.
# And then actually get on to streaming the tweets.
# So this will be in the main part of the program.
  
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    # We are going create a hashtag list.
    hash_tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]
    # Lets define our affection tweets filename as tweets dot json
    fetched_tweets_filename = "tweets.txt"

    # Lets define a twitter streamer object , so I will say twitter streamer is equal to.
    # Twitter streamer 
    twitter_streamer = TwitterStreamer()

    # Then we will say twitter stramer there it is dot stream tweets.
    # which is the method that we created up above and we will send ,it takes two things,
    # the file name that we want to write to and then also the list of keywords that we are looking for.
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)