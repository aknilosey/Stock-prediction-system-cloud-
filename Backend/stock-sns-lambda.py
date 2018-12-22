import json
import boto3
from datetime import datetime
from datetime import timedelta
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')

    table = dynamodb.Table('userStockHistory')
    now = datetime.now().strftime("%Y-%m-%d")

    fe =  Key('searchDate').eq(now)
    pe = "email,phoneNumber,stockName"
    esk = None
    response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe
    )
    # print("db ka respnse")

    userResponsedict = {}
    for i in response['Items']:
        # print(i)
        if (i['phoneNumber'] in userResponsedict):
            userResponsedict[i['phoneNumber']].append(i['stockName'])
        else:
            userResponsedict[i['phoneNumber']]=[i['stockName']]

    print("user resp dict")
    print(userResponsedict)
    client=boto3.client('sns')
    # phone_number = 0
    for k,v in userResponsedict.items():
        phone_number = k
        stockList = v

        string_toSend = " Your stock searches for today are" +str(stockList)  + "\n" + " Thank You for using our service!"
        client.subscribe(TopicArn = 'removing for security purpose',Protocol='SMS',Endpoint=phone_number)
        client.publish(Message=string_toSend, PhoneNumber=phone_number)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
