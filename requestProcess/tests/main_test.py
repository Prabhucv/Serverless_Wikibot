""""
Program Name: main.py
Service: Google Cloud Function
Predecessor: Slack Bot Wikibot
Successor: extractProcess Google Cloud Function 
Trigger: http call from Slack bot 
Functionality: Receiving the data from Slack bot and pushing it to Google PubSub for further processing 
"""
#!/usr/bin/python

import requests
import sys
from flask import escape
import json
import slack 
import apiclient
from flask import jsonify
import base64
#from google.cloud import pubsub_v1

"""Main function to processing the incoming requests from Slackbot and Pushes the information to Queue for processing"""
def requestProcess(request):
        responseMessage = {'response_type': 'in_channel','text': '','attachments': []} #Intializing the responseMessage for Slack
        #Commenting PubSub Components to perform the tests
        #publisher = pubsub_v1.PublisherClient() #PubSub Client
        #topic_path = publisher.topic_path("wikibot-243109", "wikiqueue") #Queue Topic: wikiqueue, Project Name: wikibot-243109
        try:
                if request.args.get("text"):#replaced form with args for tests
                        data=json.dumps({'slack_url':request.args.get("response_url"),'text':request.args.get("text")}).encode('utf-8') #Creating a packet data for further processing 
                        #publisher.publish(topic_path, data=data) #Publishing the data to PubSub topic 
                        responseMessage['text'] = 'Processing your request, One Moment...'
                else:
                        responseMessage['text'] = 'Please enter a valid text'
        except:
                print ("Issue with getting the response/Pushing data to queue")
                responseMessage['text'] = 'Issue with getting the response'
        return json.dumps(responseMessage) #Returning the status/temporary response to Slack bot, response should be provided within 3000ms    