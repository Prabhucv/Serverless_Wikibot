# TonsserChallenge
Tonsser Challenge - Serverless Wikibot: A bot scrapping finance information from Wikipedia 

## Approach
1. Designing best in class serverless architecture to ensure scalability and performance
2. Leveraging Serverless Queueing system to decouple the computing service to increase scalability and fault torelance
3. Building the modules like data reception, data pre-processing, data scraping, applying conversion and formating response in  Cloud Functions using Python
4. Integrating with Queueing system with Cloud Functions
5. Integrating with Slack app to enable the frontend capability
5. Writing unit testcases to performs the tests
6. Deploying the application and performing the end to end testing Manually

## Technology Stack
* Platform: Google Cloud 
* Programming Language: Python 3.7
* Frontend: Slack 
* Backend: Google Cloud Functions
* Queuing System: Google PubSub
* Testcases: pytest

## Technical Architecture

![Wikibot](https://user-images.githubusercontent.com/9641775/59161811-c7d0f100-8b04-11e9-99b7-a36d768722fb.jpg)

## Technical Flow Diagram

![flowdiagram](https://user-images.githubusercontent.com/9641775/59161812-cacbe180-8b04-11e9-873a-9c2f70fd06b4.jpg)

## Technical Description
* Slack: Slack is acts as a presentation layer, Users could enter the company name for which they wanted to know the financial information
* Cloud Functions: Serverless compute engine which acts as a backend
    * requestResponse compute: Receive the request from Wikibot app and responds back with status message. In addition, it publishes the message to Cloud PubSub for further processing. 
    * extractResponse compute: Receives the data from topic of Cloud PubSub and performs scrapping, formatting and currency conversion and post the message to the slack.
* Cloud PubSub: Serverless Message Queue for decoupling the reception and processing of the messages 

## Usage
1. Click on the below link and join the wikibot channel

      [Click here to join the wikibot slack channel](https://join.slack.com/t/wikibotai/shared_invite/enQtNjQ0MjYzMzc2OTk0LWYyYzBjMTU1ZGQyZWIzOWMzYWZlZjY5ZWUwZjdiZjIyMDJmNTgyMDFjNmY1ODcwYTAxMmY5NzI5YmRkNjg5Yjc)

2. Use slash command: /fininfo "Company Name"
   * Examples: /fininfo Ford Motor Company 
3. View the corresponding finance information related to the company
###### Note: Wikibot channel join invite link expires in 25 days

## Running the Testcases
1. Create a virtual Envirnoment using the command: 
   > python3 -m venv testenv
2. Activate the test envirnoment with the command: 
   > source env/bin/activate
2. Install the requirement using PIP command: 
   > pip3 install -r requirements.txt
3. Run the tests with the command: 
   > pytest eventTriggerTest.py / pytest httpTriggerTest.py 

## Deploying the code to Google Cloud
1. Configure the gcloud utility in the command prompt with the command: 
     > gcloud init
2. Go to the directory of the main function and perform the command: 
   * For extractProcess:
     > gcloud functions deploy extractProcess --runtime python37 --trigger-topic wikiqueue --project wikibot-243109

   * For requestProcess:
     > gcloud functions deploy requestProcess --runtime python37 --trigger-http --project wikibot-243109
###### Note: Google Cloud Account is pre-requisite 

## Assumptions
* Considering Slack Channel as frontend application terminal for interacting with Wikibot
* Backend application could be any service not necessarily to be a simple python module
* Currency Conversion for North America - Included logics for US and Canada  
* Conversion rate of dollars : US$1 -> 6.62 DKK, CA$1 -> 4.95

## Future Enhancements
* NoSQL DB could be added to store the logs and processes to server the customers better by applying ML
* Expanding the currencies available in the world to serve users across the world
* Expanding the scraping capability by adding modules for other finance websites like bloomberg.com and investing.com based on the available permissions
* Widening the search topics across domains like finance, retail, etc based on the requirement 

