import requests
from requests_oauthlib import OAuth1

twitter_url = 'https://api.twitter.com/1.1/search/tweets.json'
consumer_api_key="hidden for security purpose"
consumer_api_secret_key="hidden for security purpose"
consumer_access_token="hidden for security purpose"
consumer_access_token_secret="hidden for security purpose"
auth = OAuth1(consumer_api_key, consumer_api_secret_key,consumer_access_token, consumer_access_token_secret)

def requests_handler(event,context):
    tweets_counter=0;
    stock_name = event['stockname']

    PARAMS ={  "q" : stock_name,
                "result_type" : "popular",
                "count":10,
                "lang":"en"
            }
    response = requests.get(url = twitter_url, auth = auth, params = PARAMS)
    twitter_response = response.json()
    twitter_response_status = twitter_response["statuses"]

    print(twitter_response_status)

    tweets_array = []
    for tweet in twitter_response_status:
        tweets_counter=tweets_counter+1
        tweets_array.append( { "tweet" : tweet['text'] , "created" : tweet['created_at'] } )
        if tweets_counter == 10:
            break;

    #print( tweets_array )
    return {
        'statusCode': 200,
        'body': tweets_array
    }
