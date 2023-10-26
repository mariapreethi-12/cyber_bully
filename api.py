import tweepy
import credentials

class API():

    __consumer_key = ""
    __consumer_secret = ""
    __access_token = ""
    __access_token_secret = ""
    __api = ""

    def __init__(self) -> None:

        self.__consumer_key =  credentials.API_KEY
        self.__consumer_secret = credentials.API_SECRET_KEY
        self.__access_token = credentials.ACCESS_TOKEN
        self.__access_token_secret = credentials.ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
        auth.set_access_token(self.__access_token, self.__access_token_secret)

        self.__api = tweepy.API(auth,wait_on_rate_limit=True)
        

    def getTweetsByKeyword(self,keyword,count):

        tweets = []
        for tweet in tweepy.Cursor(self.__api.search_tweets, q=keyword,lang='en',count=count).items(10):
            tweets.append(tweet)

        return tweets


api = API()

# print (api.getTweetsByKeyword("iphone",10))
