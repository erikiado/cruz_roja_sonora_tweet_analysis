#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
from dotenv import load_dotenv
import pickle
import os


load_dotenv()
#Twitter API credentials
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_key = os.environ.get("ACCESS_KEY")
access_secret = os.environ.get("ACCESS_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")
username = "CruzRojaSonora"

def get_all_tweets(screen_name):
  #Twitter only allows access to a users most recent 3240 tweets with this method
  auth = tweepy.OAuth2BearerHandler(f"{bearer_token}")

  api = tweepy.API(auth)
  
  #initialize a list to hold all the tweepy Tweets
  alltweets = []
  with open(f'{username}_tweets.pickle', 'rb') as f:
    alltweets = pickle.load(f)
  new_tweets = alltweets[-200:]
  if not alltweets:
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended')
    #save most recent tweets
    alltweets.extend(new_tweets)
  
  #save the id of the oldest tweet less one
  oldest = alltweets[-1].id - 1
  
  uname = username.lower()
  
  #keep grabbing tweets until there are no tweets left to grab
  while len(new_tweets) > 0:
    print("getting tweets before {}".format(oldest))
    
    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
    # print(new_tweets)
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...{} tweets downloaded so far".format(len(alltweets)), end="")
    with open(f'{username}_tweets.pickle', 'wb') as handle:
      pickle.dump(alltweets, handle, protocol=pickle.HIGHEST_PROTOCOL)
      print(' - saving...')
  #transform the tweepy tweets into a 2D array that will populate the csv	
  outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
  
  #write the csv	
  with open('{}_tweets.csv'.format(screen_name), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","text"])
    writer.writerows(outtweets)
    print('{}_tweets.csv was successfully created.'.format(screen_name))
  pass


if __name__ == '__main__':
  #pass in the username of the account you want to download
  get_all_tweets(username)