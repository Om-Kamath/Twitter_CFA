import tweepy
import pandas as pd
from configparser import ConfigParser


#configuration
config = ConfigParser()
config.read('config.ini')

#twitter credentials
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authorization
def twitter_auth():
    auth = tweepy.OAuthHandler(api_key,api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    return auth

#api
def twitter_api():
    auth = twitter_auth()
    api = tweepy.API(auth)
    return api

#converting tweets to dataframe
def converting_to_df(tweets):
    columns = ['_id','User','Tweet','Date and Time']
    data = []
    for tweet in tweets:
        text = tweet.full_text.split()
        resultwords  = filter(lambda x:x[0]!='@', text)
        result = ' '.join(resultwords)
        data.append([tweet.id,tweet.user.screen_name,result, tweet.created_at])
    df = pd.DataFrame(data,columns=columns)
    print(df)
    return df

#fetching tweets
def fetch_df_tweets():
    api = twitter_api()
    query_topic = '@VFSGlobal OR @Vfsglobalcare__ AND urgent OR help -filter:retweets'
    tweets = tweepy.Cursor(api.search_tweets, q=query_topic,count=100,tweet_mode='extended',result_type='recent').items(50)
    return converting_to_df(tweets)

