import json
import boto3

def lambda_handler(event, context):

    comparison_response = {}



    stock_names = event["stockname"]
    stocknames = stock_names.split(",")
    stockname1 = stocknames[0]
    stockname2 = stocknames[1]


    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')

    table = dynamodb.Table('stockHistory')

    response1 = table.get_item(
        Key={
            'stockName' : stockname1
        }
    )

    response2 = table.get_item(
        Key={
            'stockName' : stockname2
        }
    )

    stock1_details = {}
    stock2_details = {}

    stock_old_date = response1['Item']['dates']
    stock_future_date = response1['Item']['oldDates']

    stock1_details['dates'] = stock_old_date
    stock1_details['oldDates'] = stock_future_date

    stock2_details['dates'] = stock_old_date
    stock2_details['oldDates'] = stock_future_date


    stock1_old_data = response1['Item']['oldData']
    stock1_future_data = response1['Item']['data']

    stock2_old_data = response2['Item']['oldData']
    stock2_future_data = response2['Item']['data']

    stock1_details['data'] = stock1_future_data
    stock1_details['oldData'] = stock1_old_data

    stock2_details['data'] = stock2_future_data
    stock2_details['oldData'] = stock2_old_data

    comparison_response["company1"] = stock1_details

    comparison_response["company2"] = stock2_details

    print(comparison_response)


    # TODO implement
    return {
        'statusCode': 200,
        'body': comparison_response
    }
