import json
import os
import boto3
import json
import csv
import store_stock_details
from datetime import datetime  
from datetime import timedelta

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.Session().client(service_name='sagemaker-runtime')
alphaVantageQueryParams = ('function', 'symbol', 'datatype', 'apikey');
alphaVantageQueryParamsValues = ('TIME_SERIES_WEEKLY','csv')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    alphaVantageQuery = dict()
    stockname = event['stockname']
    # print(event)
    claims = lambda_client.invoke(FunctionName='jwt-token-decoder',
            InvocationType='RequestResponse',
            Payload=json.dumps( { 'token' : event['token'] } ))
    
    claims =json.loads(claims['Payload'].read())
    print(claims)
    
    if claims:
        print(claims)
    else:
        return {
        'statusCode': 401,
        'body': {"message":"Invalid Authentication."}
        }
    
    apikey = event['apikey']
    
    print("stockname | "+stockname+" | apikey | "+apikey)
    
    alphaVantageQuery[alphaVantageQueryParams[0]] = alphaVantageQueryParamsValues[0]
    alphaVantageQuery[alphaVantageQueryParams[2]] = alphaVantageQueryParamsValues[1]
    alphaVantageQuery[alphaVantageQueryParams[1]] = stockname
    alphaVantageQuery[alphaVantageQueryParams[3]] = apikey
    alphaVantageQuery['interval']='None'
    
    responseFromAlphaVantage = lambda_client.invoke(
            FunctionName='alpha-vantage-lambda',
            InvocationType='RequestResponse',
            Payload=json.dumps(alphaVantageQuery)
            )

    jsonResponse =json.loads(responseFromAlphaVantage['Payload'].read())['body']
    
    print(jsonResponse)
    
    alphaVantageCSVContent=json.loads(jsonResponse)["alpha_response"]
    
    
    #print("alphaVantageCSVContent | "+alphaVantageCSVContent)
    
    csvResponse = csv.reader(alphaVantageCSVContent.splitlines(), delimiter=',')
    
    my_list = list(csvResponse)
    my_list = my_list[1:]
    my_list.reverse()
    finalCsv = ''
    counter=0;
    
    oldDate=[]
    oldStockPrices=[]
    dbData = []
    
    for row in my_list:
        if counter==0:
            counter=1
        else:
            oldDate.append(row[0])
            dbData.append({"score":row[1]})
            oldStockPrices.append({"score":float(row[1])})
            i=0
            while i<58:
                row[1] = row[1]+',0'
                i=i+1
            finalCsv = finalCsv+row[1]+'\n'
        
    response = runtime.invoke_endpoint(EndpointName = ENDPOINT_NAME ,ContentType='text/csv',Body =finalCsv)
    
    jsonResponse =json.loads(response['Body'].read())['predictions']
    
    jsonResponse= jsonResponse[-7:]
    

    i=1;
    now = datetime.now()
    dateArray=[];
    dateArray.append(now.strftime("%Y-%m-%d"))
    while i<7:
        now = now + timedelta(days=1)
        dateArray.append(now.strftime("%Y-%m-%d"))
        i=i+1
   
    finalJson=dict()
    finalJson['oldDates'] = oldDate[-8:]
    finalJson['oldData'] = oldStockPrices[-8:]
    finalJson['data'] = jsonResponse
    finalJson['dates'] = dateArray
    
    futureDataArray = []
    for futureData in jsonResponse:
        futureDataArray.append({"score":str(futureData['score'])})
        
    
    dbDict= {'data':futureDataArray,'dates':dateArray,'oldDates':finalJson['oldDates'],'oldData':dbData[-8:]}
    
    store_stock_details.storeRequest(stockname = stockname,predictionData = dbDict)
    store_stock_details.storeUserRequest(stockname = stockname,username = claims['cognito:username'],email=claims['email'],phoneNumber=claims['phone_number'])
    
    return {
        'statusCode': 200,
        'body': finalJson
    }
