#!venv/bin/python

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

app = Flask(__name__)
CORS(app)

@app.route('/search/<string:query>', methods=['GET'])
def search(query):
	gs = goslate.Goslate()
	language_id = gs.detect(query)
	#print gs.get_languages()[language_id] #German
	#print language_id #de	
	connection = urlopen('http://athigale.koding.io:8983/solr/projc/select?q=*'+query+'*&wt=json')
	response = simplejson.load(connection)
	#print response['response']['numFound'], "documents found."
	#print response 
	#for document in response['response']['docs']:
  	#	print document['text_en']		
	return make_response(jsonify(response))	
	#return make_response(jsonify({'name': query+"shit"}))

@app.route('/search2/<string:query>', methods=['GET'])
def search2(query):
	gs = goslate.Goslate()
	language_id = gs.detect(query)
	#print gs.get_languages()[language_id] #German
	#print language_id #de	
	# create a connection to a solr server
	s = solr.SolrConnection('http://athigale.koding.io:8983/solr/projc/')
	# do a search
	response = s.query('hashtags:'+query)
	return make_response(jsonify(response))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)