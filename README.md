# TonsserChallenge
Tonsser Challenge

## Approach:
1. Designing best in class serverless architecture to ensure scalability and performance
2. Leveraging Serverless Queueing system to decouple the computing service to increase scalability and fault torelance
3. Building the modules like data reception, data pre-processing, data scraping, applying conversion and formating response in  Cloud Functions using Python
4. Integrating with Queueing system with Cloud Functions
5. Integrating with Slack app to enable the frontend capability
5. Writing unit testcases to performs the tests
6. Deploying the application and performing the end to end testing Manually

## Technology Stack:
Platform: Google Cloud 
Frontend: Slack 
Backend: Google Cloud Functions
Queuing System: Google PubSub
Testcases: pytest

## Technical Architecture:
Wikibot.jpg

## Technical Flow Diagram:


## Technical Description:
Slack: Slack is acts as a presentation layer, Users could enter the company name for which they wanted to know the financial information
Cloud Functions: Serverless compute engine which acts as a backend
1. requestResponse compute: Receive the request from Wikibot app and responds back with status message. In addition, it publishes the message to Cloud PubSub for further processing. 
2. extractResponse compute: Receives the data from topic of Cloud PubSub and performs scrapping, formatting and currency conversion and post the message to the slack.
Cloud PubSub: Serverless Message Queue for decoupling the reception and processing of the messages 

## Assumptions:
Considering Slack Channel as frontend application terminal for interacting with Wikibot
Backend application could be any service not necessarily to be a simple python module
Currency Conversion for North America - Includes logic for US and Canada  
Conversion rate of dollars : US$1 -> 6.62 DKK, CA$1 -> 4.95

## Future Enhancements:
NoSQL DB could be added to store the logs and processes to server the customers better by applying ML
Expanding the currencies available in the world to serve users across the world
Expanding the scraping capability by adding modules for other finance websites like bloomberg.com and investing.com based on the available permissions
Widening the search topics from finance industry to retail based on the requirement 

