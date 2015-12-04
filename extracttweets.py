# -*- coding: utf-8 -*-
import tweepy
import json
import sys
import codecs
from datetime import datetime
from time import mktime
from config import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
import urllib
import requests



class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

querys = ['pray4paris','Le Carillon','Eagles of Death Metal','portesouvertes','théâtre Bataclan']
langs=["en"]
count=1000
pages=500
filename="tweets1.json"

def getloc(locname):
    if locname:
        url="https://maps.googleapis.com/maps/api/geocode/json?address="+locname
        response = requests.get(url)
        jsonvalues = response.json()
        if jsonvalues['status']=="OK":
            locvalue=jsonvalues['results'][0]['geometry']['location']
            return [locvalue['lat'],locvalue['lng']]
    return "Null"

for lang in langs:
    for query in querys:
        for tweets in tweepy.Cursor(api.search, q=query.encode('utf-8'),lang=lang, count=count).pages(pages):
            for tweet in tweets:
                tweet_data = {}
                if (not tweet.text.find("RT")) or  (not tweet.entities.get('hashtags')):
                        continue
                tweet_data['id'] = str(tweet.id)
                tweet_data['text'] = tweet.text
                hashtagData  = tweet.entities.get('hashtags')
                hashtagList = []
                if not hashtagData:
                    tweet_data['hashtags'] = hashtagList
                else:
                    for tag in hashtagData:
                        hashtagList.append(tag['text'])
                    tweet_data['hashtags'] = hashtagList
                URLData = tweet.user.entities.get('url')
                if not URLData:
                    tweet_data['urls'] = ""
                else:
                    URLlist = URLData['urls']
                    tweet_data['url'] = URLlist[0].get('expanded_url')
                tweet_data['lang'] = tweet.lang
                fmt = '%Y-%m-%d %H:%M:%SZ'
                created_at = str(tweet.created_at)
                temp = datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
                tweet_data['created_at'] = str(temp.strftime('%A, %B %d, %Y %H:%M:%S'))
                tweet_data['retweet_count'] = tweet.retweet_count
                tweet_data['timezone'] = tweet.user.time_zone
                tweet_data['location'] = getloc(tweet.user.location)
                if tweet.place:
                    tweet_data['place'] = tweet.place.country
                tweet_data["favorite_count"]=tweet.favorite_count
                tweet_data["followers_count"]=tweet.user.followers_count
                with codecs.open(filename,'a', encoding='utf-8') as f:
                    json.dump(tweet_data,f,ensure_ascii=False)
                    f.write('\n')

