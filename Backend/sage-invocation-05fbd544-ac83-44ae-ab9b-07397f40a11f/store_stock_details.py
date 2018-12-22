import json
import boto3
from datetime import datetime  
from datetime import timedelta
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('stockHistory')
tableUserStock = dynamodb.Table('userStockHistory')
stockDetails = []
dateDetails = []


def storeRequest(stockname,predictionData):
    # TODO implement
    currentDate = datetime.now()
    currentDate = currentDate.strftime("%Y-%m-%d")
    currentDate = str(currentDate)

    response = table.query(
    KeyConditionExpression=Key('stockName').eq(stockname)
    )

    if response['Count'] == 0: #or (response['Items']['entryDate'] != currentDate):
        table.put_item(
        Item = {
        'stockName': stockname,
        'data': predictionData['data'],
        'dates': predictionData['dates'],
        'oldData': predictionData['oldData'],
        'oldDates': predictionData['oldDates'],
        'entryDate': currentDate
        
        }
        )
        return True 
    else:
        for i in response['Items']:
            if i['entryDate'] != currentDate:
                table.put_item(
                Item = {
                'stockName': stockname,
                'data': predictionData['data'],
                'dates': predictionData['dates'],
                'oldData': predictionData['oldData'],
                'oldDates': predictionData['oldDates'],
                'entryDate': currentDate
                }
                )
                break
            else:
                print("equal")
                
    return False
    
    
def storeUserRequest(stockname,username,email,phoneNumber):
    # TODO implement
    currentDate = datetime.now()
    currentDate = currentDate.strftime("%Y-%m-%d")
    currentDate = str(currentDate)
    tableUserStock.put_item(
    Item = {
        'stockName': stockname,
        'username': (username+'~'+stockname),
        'email': email,
        'phoneNumber': phoneNumber,
        'searchDate':currentDate
        }
    )
    
    return True    
