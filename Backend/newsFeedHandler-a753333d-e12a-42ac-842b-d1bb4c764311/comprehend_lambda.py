import json
import boto3

def sentiment_analysis(news_array):
    
    text = " "
    for i in news_array:
        if text == " " :
            if 'news' in news_array:
                text = i['news']
        else:
            text = text + i['news']
            
    print (text)
    
    
    comprehend = boto3.client("comprehend")
    
    response = comprehend.detect_sentiment(Text = text , LanguageCode = 'en')
    sentiment = response['Sentiment']

    return {
        'statusCode': 200,
        'body': json.dumps({"sentiment" : sentiment})
    }
