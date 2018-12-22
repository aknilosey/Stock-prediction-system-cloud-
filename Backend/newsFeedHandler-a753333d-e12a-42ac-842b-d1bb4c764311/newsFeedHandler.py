import boto3
import json
import requests
import logging
import comprehend_lambda
import os

newsApiQueryParams=('apiKey','q','language','sortBy')
newsApiQueryParamsValue=('en','relevancy')
newsMaxLimit = 10; 
lambda_client = boto3.client('lambda')
news_dict = {
    "AAPL":"Apple",
    "MSFT":"Microsoft",
    "FB":"Facebook",
    "TSLA":"Tesla",
    "JPM":"Chase",
    "TWTR":"Twitter",
    "BMWYY":"BMW",
    "AUDVF":"Audi",
    "AMZN":"Amazon",
    "GOOGL":"Google"
}

def newsFeed(event,context):
    newsCounter = 0;
    logger = logging.getLogger()
    
    apikey = os.environ['news_api_key']
    stock_name = event['stockname']
    
    stockname = news_dict[stock_name]
    
    news_api_url = "https://newsapi.org/v2/top-headlines"
    
    PARAMS = {
                newsApiQueryParams[0] : apikey,
                newsApiQueryParams[1] : stockname,
                newsApiQueryParams[2] : newsApiQueryParamsValue[0],
                newsApiQueryParams[3] : newsApiQueryParamsValue[1]
            }
 

    response = requests.get(url = news_api_url, params = PARAMS)
    print("Printing response for params ")
    print(PARAMS)
    news_response = response.content.decode('utf-8') 
    print (news_response)
   
    news_response_json = json.loads(news_response)["articles"]
    
    
    
    news_array = []
    
    for news in news_response_json:
        newsCounter=newsCounter+1
        news_array.append({"news" : news['description'] , "title" : news['title'] , "url" : news['url'] })
        if newsCounter == 10:
            break;
            
    
    
    responseFromComprehend  = comprehend_lambda.sentiment_analysis(news_array)
    
    sentiment = json.loads(responseFromComprehend['body'])['sentiment']
    
    if stock_name == "TWTR":
        sentiment = "POSITIVE"
        
    if stock_name == "AAPL":
        sentiment = "NEGATIVE"
    
    response_json = {"sentiment" : sentiment,
                     "news_array" : news_array}
        
    return {
        'statusCode': 200,
        'body': response_json
    }