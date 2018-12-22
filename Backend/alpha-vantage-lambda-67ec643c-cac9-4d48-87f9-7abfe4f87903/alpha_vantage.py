import boto3
import json
import requests
import logging
import csv

def lambda_handler(event,context):
    logger = logging.getLogger()
    
    function_name = event['function']
    symbol_name = event['symbol']
    api_key = event['apikey']
    datatype = event['datatype']
    interval = event['interval']
    
    alpha_vantage_api_url = "https://www.alphavantage.co/query"
    
    if interval == 'None':
        PARAMS = {"function" : function_name,
              "symbol" : symbol_name,
              "apikey" : api_key,
              "datatype" : datatype
        }
    else:
        PARAMS = {"function" : function_name,
              "symbol" : symbol_name,
              "apikey" : api_key,
              "datatype" : datatype,
              "interval" : interval
        }
 
    response = requests.get(url = alpha_vantage_api_url, params = PARAMS)
    
    
    if 'csv' == datatype:
        print(PARAMS)
        decoded_content = response.content.decode('utf-8')
        print(decoded_content)
        alpha_reponse = {"alpha_response" : decoded_content}
    
        return {
        'statusCode': 200,
        'body': json.dumps(alpha_reponse)
        }
    else:
        decoded_content = response.content.decode('utf-8')
        return {
        'statusCode': 200,
        'body': json.loads(decoded_content)
        }