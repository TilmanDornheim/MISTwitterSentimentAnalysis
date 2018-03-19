import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient():
    
        
       

    def tweepy_setup(self):
        
        # Try to authenticate 

        consumer_key = "cMneB3RB6RKEFS8lbauJeAtkR"
        consumer_secret = "ZeQvW4rc9MS5YehTJbnZewYTtvz8igHmYIyK0bRhJKn828BMMH"
        access_token = "974677908286566401-0B5xQWOkP2eJEWFJSWhtJMHnDDKH4pD"
        access_token_secret = "pmx42ZYLAGlLLOwa9m0fkhPM8hCN2vIJVAO24VXIfvGOb"

        try:
                
            # Create OAuthHandler

            auth = OAuthHandler(consumer_key,consumer_secret)    

            # Add token and token_secret to Handler

            auth.set_access_token(access_token,access_token_secret)

            # Create Tweepy Api 

            api = tweepy.API(auth)

            return api


        except Exception as e:
            
            
            print("Error Authenticating: " + str(e))
 
    
    def clean_tweet(self,tweet):
   
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self,tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        # Get Sentiment

        if analysis.sentiment.polarity > 0 :

            return 'positive'

        elif analysis.sentiment.polarity == 0:

            return 'neutral'

        else:

            return 'negative'
 
    def get_tweets(self, query, count = 10):

        # Empty List to later store tweets

        tweets = []

        try:
            
            # Fetch Tweets from Twitter Api

            api = self.tweepy_setup()

            fetched_tweets = api.search(q = query, count = count)

            # Iterate through tweets and parse

            for tweet in fetched_tweets:

                # Empty dict to store tweet params

                parsed_tweet = {}

                # Get Text

                parsed_tweet['Text'] = tweet.text

                # Get Sentiment

                parsed_tweet['Sentiment'] = self.get_tweet_sentiment(tweet.text)

                # Append to List while ensuring that retweeted tweets only get added once

                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:

                        tweets.append(parsed_tweet)
                else:

                    tweets.append(parsed_tweet)

            # Return parsed tweets

            return tweets


        except Exception as e:
        
            print("Error: " + str(e))
 
def main(query):

        client = TwitterClient()


        # Get Tweets

        tweets = client.get_tweets(query = query, count = 200)

        # Select positive tweets 

        pos_tweets = []

        for tweet in tweets:

            if(tweet['Sentiment'] == 'positive'):

                pos_tweets.append(tweet)



        # Select negative tweets 

        neg_tweets = []

        for tweet in tweets:

            if(tweet['Sentiment'] == 'negative'):

                neg_tweets.append(tweet)

        # Select neutral tweets

        ntr_tweets = []

        for tweet in tweets:

            if(tweet['Sentiment'] == 'neutral'):

                ntr_tweets.append(tweet)

        # Get Percentages

        percent_pos = round(100 * (len(pos_tweets) / len(tweets)),2)

        percent_neg = round(100 * (len(neg_tweets) / len(tweets)),2)

        percent_ntr = round(100 * (len(ntr_tweets) / len(tweets)),2)

        # Print Results 

        print("Sentiment Analysis complete for tweets about " + query)

        print('\n')

        print("Percentage of positive tweets = " + str(percent_pos) + "%")

        print("Percentage of neutral tweets = " + str(percent_ntr) + "%")

        print("Percentage of negative tweets = " + str(percent_neg) + "%")

        print('\n')

        # Print 10 positive and 10 negative tweets

        print("Positive Tweets: ")
        print("\n")

        for tweet in pos_tweets[:10]:

            print(tweet['Text'])
            print("\n")

        print("Negative Tweets: ")
        print("\n")

        for tweet in neg_tweets[:10]:

            print(tweet['Text'])
            print("\n")
 
if __name__ == "__main__":
    
    # calling main function
   
    query = input("What topic do you want to analyze? \n")

    main(query)
