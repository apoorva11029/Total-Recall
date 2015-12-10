#!venv/bin/python

import json
import requests
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask.ext.cors import CORS
from urllib2 import *
import simplejson
import goslate
import solr
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search(query):
	#with open('data.json') as data_file:
	#    data = simplejson.load(data_file)
	query = request.args.get('query')
	rowno = request.args.get('row')
	b = TextBlob(u""+query+"")
	language_id = b.detect_language()	
	connection = urlopen('http://athigale.koding.io:8983/solr/projc/select?defType=dismax&q=*'+query+'*&rows=10&start='+rowno+'&sort=name asc&qf=text_'+ language_id +'^1+hashtags^1+concept^0.1+keywords^1&wt=json&facet=true&facet.field=text_'+language_id)
	response = simplejson.load(connection)
	returnArr={}
	tweets=[]
	locations=[]
	for tweet in response['response']['docs']:
		tempd={}
		tempd['text']=tweet['text']
		tempd['user_dp']=tweet['user_dp']
		tempd['user_name']=tweet['user_name']
		tweets.append(tempd)
		if tweet['locationCoordinates']:
			locations.append([tweet['locationCoordinates'][0],tweet['locationCoordinates'][1]])
	returnArr['tweets']=tweets
	returnArr['locations']=locations
	#returnArr['people']=people
	#returnArr['relate_terms']=relatedterms
	return make_response(json.dumps(returnArr))

# @app.route('/search/<string:query>', methods=['GET'])
# def search(query):
# 	#gs = goslate.Goslate()
# 	#language_id = gs.detect(query)
# 	#print gs.get_languages()[language_id] #German
# 	#print language_id #de	='
# 	# Example Query : http://athigale.koding.io:8983/solr/projc/select?defType=dismax&q=*attack*&qf=text_en^3+tweet_hashtags^2+keywords^2&wt=json
# 	b = TextBlob(u""+query+"")
# 	language_id = b.detect_language()	
# 	connection = urlopen('http://athigale.koding.io:8983/solr/projc/select?defType=dismax&q=*'+query+'*&qf=text_'+ language_id +'^1+hashtags^1+concept^0.1+keywords^1&wt=json')
# 	response = simplejson.load(connection)
# 	#print response['response']['numFound'], "documents found."
# 	#print response
# 	#for document in response['response']['docs']:
#   	#	print document['text_en']	
# 	return make_response(jsonify(response))	
# 	#return make_response(jsonify({'name': query+"shit"}))

# @app.route('/search2/<string:query>', methods=['GET'])
# def search2(query):
# 	gs = goslate.Goslate()
# 	language_id = gs.detect(query)
# 	#print gs.get_languages()[language_id] #German
# 	#print language_id #de	
# 	# create a connection to a solr server
# 	s = solr.SolrConnection('http://athigale.koding.io:8983/solr/projc/')
# 	# do a search
# 	response = s.query('hashtags:'+query)
# 	return make_response(jsonify(response))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
