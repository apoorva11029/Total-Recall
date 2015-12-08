# -*- coding: utf-8 -*-
import tweepy
import json
import sys
import codecs
from datetime import datetime
from time import mktime
from config import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET

from alchemyapi import AlchemyAPI

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#querys = ['pray4paris','Le Carillon','Eagles of Death Metal','portesouvertes','théâtre Bataclan']
querys = ['pray4paris']
langs=["en"]
count=10
pages=2
filename="tweets1.json"

alchemyapi = AlchemyAPI()

for lang in langs:
    for query in querys:
        for tweets in tweepy.Cursor(api.search, q=query.encode('utf-8'),lang=lang, count=count).pages(pages):
            for tweet in tweets:
                tweet_data = {}
                tweet_data['id'] = str(tweet.id)
                tweet_data['text'] = tweet.text

                #Alchemy Stuff:
                response = json.loads(json.dumps(alchemyapi.entities('text', tweet.text, {'sentiment': 1})))
                # size=len(response['entities'])

                ent=[]
                ent_rele=[]
                ent_type=[]
                if response['status'] == 'OK':
                    for entity in response['entities']:
                        ent.append(entity['text'])
                        ent_rele.append(entity['relevance'])
                        ent_type.append(entity['type'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])
                response = json.loads(json.dumps(alchemyapi.sentiment("text", tweet.text)))
                senti=response["docSentiment"]["type"]


                response = json.loads(json.dumps(alchemyapi.keywords('text', tweet.text, {'sentiment': 1})))
                size=len(response['keywords'])
                keywords=[]
                if response['status'] == 'OK':
                    for word in response['keywords']:
                        keywords.append(word['text'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])


                response=json.loads(json.dumps(alchemyapi.concepts("text",tweet.text)))
                size=len(response['concepts'])
                concept=[]
                if response['status'] == 'OK':

                    for con in response['concepts']:
                        concept.append(con['text'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])
                tweet_data['entities']=ent
                tweet_data['ent_relevance']=ent_rele
                tweet_data['ent_type']=ent_type
                tweet_data['keywords']=keywords
                tweet_data['concepts']=concept
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
                tweet_data['location'] = tweet.user.location
                if tweet.place:
                    tweet_data['place'] = tweet.place.country
                tweet_data["favorite_count"]=tweet.favorite_count
                tweet_data["followers_count"]=tweet.user.followers_count
                with codecs.open(filename,'a', encoding='utf-8') as f:
                    json.dump(tweet_data,f,ensure_ascii=False)
                    f.write('\n')
# -*- coding: utf-8 -*-
import tweepy
import json
import sys
import codecs
from datetime import datetime
from time import mktime
from config import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET

from alchemyapi import AlchemyAPI

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#querys = ['pray4paris','Le Carillon','Eagles of Death Metal','portesouvertes','théâtre Bataclan']
querys = ['pray4paris']
langs=["en"]
count=10
pages=2
filename="tweets1.json"

alchemyapi = AlchemyAPI()

for lang in langs:
    for query in querys:
        for tweets in tweepy.Cursor(api.search, q=query.encode('utf-8'),lang=lang, count=count).pages(pages):
            for tweet in tweets:
                tweet_data = {}
                tweet_data['id'] = str(tweet.id)
                tweet_data['text'] = tweet.text

                #Alchemy Stuff:
                response = json.loads(json.dumps(alchemyapi.entities('text', tweet.text, {'sentiment': 1})))
                # size=len(response['entities'])

                ent=[]
                ent_rele=[]
                ent_type=[]
                if response['status'] == 'OK':
                    for entity in response['entities']:
                        ent.append(entity['text'])
                        ent_rele.append(entity['relevance'])
                        ent_type.append(entity['type'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])
                response = json.loads(json.dumps(alchemyapi.sentiment("text", tweet.text)))
                senti=response["docSentiment"]["type"]


                response = json.loads(json.dumps(alchemyapi.keywords('text', tweet.text, {'sentiment': 1})))
                size=len(response['keywords'])
                keywords=[]
                if response['status'] == 'OK':
                    for word in response['keywords']:
                        keywords.append(word['text'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])


                response=json.loads(json.dumps(alchemyapi.concepts("text",tweet.text)))
                size=len(response['concepts'])
                concept=[]
                if response['status'] == 'OK':

                    for con in response['concepts']:
                        concept.append(con['text'])
                else:
                    print('Error in entity extraction call: ', response['statusInfo'])
                tweet_data['entities']=ent
                tweet_data['ent_relevance']=ent_rele
                tweet_data['ent_type']=ent_type
                tweet_data['keywords']=keywords
                tweet_data['concepts']=concept
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
                tweet_data['location'] = tweet.user.location
                if tweet.place:
                    tweet_data['place'] = tweet.place.country
                tweet_data["favorite_count"]=tweet.favorite_count
                tweet_data["followers_count"]=tweet.user.followers_count
                with codecs.open(filename,'a', encoding='utf-8') as f:
                    json.dump(tweet_data,f,ensure_ascii=False)
                    f.write('\n')
