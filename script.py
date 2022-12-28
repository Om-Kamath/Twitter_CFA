from pymongo import MongoClient, errors
from twitter_api import fetch_df_tweets
from nlp import chunking
from configparser import ConfigParser

#configuration
config = ConfigParser()
config.read('config.ini')

# Connect to MongoDB
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = config['mongodb']['connection_string']
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial)
   return client['twitter']

def insert_df_tweets(df):
    # Get the database
    dbname = get_database()
    # Get the collection
    collection_tweets = dbname['tweets']
    # Insert dataframe into collection
    try:
        collection_tweets.insert_many(df.to_dict('records'),ordered=False)
    except errors.BulkWriteError:
        print("Skipping duplicate tweets")
  
def insert_df_count(df2):
    # Get the database
    dbname = get_database()
    # Get the collection
    collection_count = dbname['count']
    #Inserting dataframe into collection
    try:
        collection_count.insert_many(df2.to_dict('records'),ordered=False)
    except errors.BulkWriteError:
        print("Skipping duplicate values")

if __name__ == "__main__":  
    #fetch tweets in dataframe 
    df = fetch_df_tweets()
    #insert dataframe into mongodb
    insert_df_tweets(df)
    #chunking tweets 
    df2 = chunking(df)
    #insert dataframe into mongodb (chunks with counts)
    insert_df_count(df2)
    