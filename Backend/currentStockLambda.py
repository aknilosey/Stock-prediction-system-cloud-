import json
import os
import boto3
import json
import csv
from datetime import datetime
from datetime import timedelta

def lambda_handler(event, context):

    print(event)
    query = event['message']
    print(query)
    response = calling_lex(query)
    print(response)

    keywordone = response['slots']['slotOne']
    keywordtwo = response['slots']['slotTwo']
    print(keywordone)
    print(keywordtwo)
    if keywordone == None:
       res = keywordtwo
    if keywordtwo == None:
       res = keywordone
    res = keywordone
    # print(res)
    lambda_client = boto3.client('lambda')
    claims = lambda_client.invoke(FunctionName='jwt-token-decoder',
            InvocationType='RequestResponse',
            Payload=json.dumps( { 'token' : event['token'] } ))

    claims =json.loads(claims['Payload'].read())
    print(claims)
    alphaVantageQueryParams = ('function', 'symbol','interval', 'datatype', 'apikey');
    alphaVantageQueryParamsValues = ('TIME_SERIES_INTRADAY','json')
    alphaVantageQuery = dict()
    apikey = event['apikey']
    stockname = res
    print(stockname)
    # print("stockname | "+stockname+" | apikey | "+apikey)

    alphaVantageQuery[alphaVantageQueryParams[0]] = alphaVantageQueryParamsValues[0]
    # alphaVantageQuery[alphaVantageQueryParams[2]] = alphaVantageQueryParamsValues[1]
    alphaVantageQuery[alphaVantageQueryParams[1]] = stockname
    alphaVantageQuery[alphaVantageQueryParams[3]] = 'json'
    alphaVantageQuery[alphaVantageQueryParams[2]] = '15min'
    alphaVantageQuery[alphaVantageQueryParams[4]] = apikey

    responseFromAlphaVantage = lambda_client.invoke(
            FunctionName='alpha-vantage-lambda',
            InvocationType='RequestResponse',
            Payload=json.dumps(alphaVantageQuery)
            )

    # responseFromAlphaVantage=responseFromAlphaVantage.decode("utf-8")
    print(responseFromAlphaVantage)
    jsonResponse =responseFromAlphaVantage['Payload'].read().decode("utf-8")
    # jsonResponse= jsonResponse['body']
    print(json.loads(jsonResponse))
    # print("alphaVantageCSVContent")
    alphaVantageCSVContent=json.loads(jsonResponse)

    frontEndresponse = alphaVantageCSVContent['body']['Time Series (15min)']

    # print(type(frontEndresponse))
    dictlist = {}
    i = 0
    for key, value in frontEndresponse.items():
        i += 1
        dictlist = value
        print("temp type")
        print(value.items())
        for k,v in value.items():
            dictlist[k] = v
        print("temp")
        if i == 1:
            break
    
    currStock ={"name" : res, "stockVal" : dictlist}
    # print(currStock)
    return {
        'statusCode': 200,
        'body': currStock,
    }

def calling_lex(query):

    client = boto3.client('lex-runtime')
    response = client.post_text(botName='botforcurrentstock', botAlias='$LATEST', userId='USER', inputText=query)

    print(json.dumps(response))
    return response
