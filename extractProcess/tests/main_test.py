""""
Service: Google Cloud Function
Predecessor: reponseProcess Google Cloud Function 
Successor: Slack Bot Wikibot
Trigger: Event from Google PubSub 
Functionality: Scrapping Wikipedia for Finance information of the companies and responding back to Slack Bot
"""
#!/usr/bin/python
# -*- coding: ascii -*-
# -*- coding: utf-8 -*-

import wikipedia
import requests
from bs4 import BeautifulSoup
import re
import sys
from flask import escape
import json
import slack 
import apiclient
from flask import jsonify
import base64

""" Function to match the incoming amount value using regex and convert it to Danish Krone Equivalent"""
def conversion(finInfo):
        forexConversion={'us':6.62,'ca':4.95} #Euro, Pound and other currencies can be added 
        currencyPattern='^us|ca' #Based on the forexConversion, corresponding symbol needs to be added 
        floatPattern="\d+\.\d+|\d" #To derive the amount value from the string 
        infoDict={}
        for infoKey,infoValue in finInfo.items():
                textList=re.split('\s',infoValue.replace(u'\xa0',u' ').strip()) 
                currencyMatch=re.match(currencyPattern,textList[0]) #Matching the currency pattern of US or CA with the string 
                if currencyMatch and infoValue!='':
                        currencyValue=re.findall(floatPattern,textList[0])
                        #Converting the amount value into DKK equivalent 
                        finalCurrency=[float(item)*forexConversion[currencyMatch.group(0)] for item in currencyValue]
                        finalCurrency[0]=round(finalCurrency[0],2)
                        infoDict[infoKey]='DKK '+str(finalCurrency[0])+' '+textList[1]
                else:
                        infoDict[infoKey]=''
        return infoDict

"""Function to extract the data from wikipedia for the incoming text"""
def wikiExtract(slack_text,finInfo):
        temp=finInfo
        try:
                wikiPage = wikipedia.page(slack_text)
                wikiResponse = requests.get(wikiPage.url) #Wiki data retrival 
                textOutput = BeautifulSoup(wikiResponse.text, 'html.parser')
                #Crawling through the xml/html data to get the required information
                for divItem in textOutput.find_all(name='div',class_='mw-parser-output'):
                        for tableItem in divItem.find_all(name='table',class_='infobox vcard'):
                                for trItem in tableItem.find_all(name='tr'):
                                        for finItem in finInfo.keys():
                                                if finItem.lower() in trItem.text.lower(): #Matching the wiki data with required fin info
                                                        temp=trItem.text.lower().replace(finItem.lower(),'')
                                                        finInfo[finItem]=temp.strip()
        except:
                print ("Issue with Wiki Extract")
                finInfo=temp
        return finInfo

"""Simple function to convert the dictionary value to string text for the slack response"""
def conversionProcess(infoDict,responseMessage,responseText,slack_text):
        for infoKey,infoValue in infoDict.items():
                        if infoValue!='':
                                responseText=responseText+"\n"+infoKey+": "+infoValue
        responseMessage['text']=responseText if responseText!=slack_text else 'Finanace Information is not available as expected by the bot'
        return responseMessage

"""Main function to process the data coming from PubSub and respond back to Slack bot with information"""
def extractProcess(data, context):
        finInfo={'Revenue':'','Operating income':'','Net income':'','Total assets':'','Total equity':''} #Required Finance Information
        responseMessage = {'response_type': 'in_channel','text':'','attachments': []} #Intializing response message 
        slack_text='' #testcase
        slack_url='' #testcase 
        try:
                #requestData = base64.b64decode(data['data']).decode('utf-8') #Decoding the data received from PubSub
                #requestData=json.loads(requestData)
                requestData=data #Ignored the above two lines and added a line to enable tests
                slack_url = requestData.get("slack_url") 
                slack_text = requestData.get("text")
                responseText=slack_text
        except:
                print ('Issue with processing the data from queue')
        if slack_url and slack_text: #Check to ensure the start of process 
                finInfo=wikiExtract(slack_text,finInfo) #Function Call
                infoDict=conversion(finInfo) #Function Call 
                responseMessage=conversionProcess(infoDict,responseMessage,responseText,slack_text) #Function Call 
        else:
                responseMessage['text']='Sorry, Not able to process your request at this moment, please try again later'  
        
        try:
                requests.post(slack_url,data=json.dumps(responseMessage)) #Posting the response to the Slack Bot 
        except:
                print ("Issue with posting the message to Slack app")              
        return responseMessage # End of Cloud Function 