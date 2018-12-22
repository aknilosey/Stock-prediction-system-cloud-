import boto3
import requests
import json
import csv 

lambda_client = boto3.client('lambda')
alphaVantageQueryParams = ('function', 'symbol', 'datatype', 'apikey');
alphaVantageQueryParamsValues = ('TIME_SERIES_WEEKLY','csv')


def lambda_handler(event, context):
    finalResponse = dict()

    stockname = event["stockname"]
    apikey = event['apikey']
    
    print("stockname | "+ stockname + " | apikey | "+apikey)
  
    newsTwitterApiQuery=dict()
    newsTwitterApiQuery['stockname'] = stockname
    
    try:
        # TODO: write code...
        responseFromTwitterApi = lambda_client.invoke(
            FunctionName='twitterlambda',
            InvocationType='RequestResponse',
            Payload=json.dumps(newsTwitterApiQuery)
            )
            
        finalResponse['twitter'] = json.loads(responseFromTwitterApi['Payload'].read().decode('utf-8'))['body']
    except Exception:
        print("error")    
    
   
    newsTwitterApiQuery['apikey'] = apikey
    
    try:
        # TODO: write code...
        responseFromNewsApi = lambda_client.invoke(
            FunctionName='newsFeedHandler',
            InvocationType='RequestResponse',
            Payload=json.dumps(newsTwitterApiQuery)
            )
            
        #print(responseFromNewsApi['Payload'].read().decode('utf-8'))        
        finalResponse['news'] = json.loads(responseFromNewsApi['Payload'].read().decode('utf-8'))['body']
    except Exception:
        print("error")
            
            
    print(finalResponse)
   

    return {
        'statusCode': 200,
        'body': finalResponse
    }
    
    