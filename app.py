import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
consumer_key = 'cNpnMrJi2fIdSG3FmHZeJWJSt'
consumer_secret = 'fpj28AdLR6gVdmX7xWiBbqq7AuO5cmJWJa4YDW0z19IG3RANce'
access_token = '738382254230110208-LPfiYV5MqW0bklI8ijSSzTXIiMfnz76'
access_token_secret = 'umdOCQ74X4Yt3Eptl5d61AAFgL8gqI2UpCn2LCYqlMzH6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

from flask import Flask, render_template, request
app = Flask(__name__)

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
 
def clean_tweet(tweet):
       return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
    
def get_tweets(query):
    tweets = []

    fetched_tweets = api.user_timeline(screen_name = query, count = 200)
 
    for tweet in fetched_tweets:
        parsed_tweet = {}
 
        parsed_tweet['text'] = tweet.text
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
 
        if tweet.retweet_count > 0:
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)
 
    return tweets
 
def analyze(query):
    tweets = get_tweets(query)

    output = ""
    
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    output += "Positive tweets: {}%".format(100 * len(ptweets)/len(tweets))
    output += "<br>"
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    output += "Negative tweets: {}%".format(100 * len(ntweets)/len(tweets))
    output += "<br>"
    netweets=[tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    output += "Neutral tweets: {}%".format(100 * len(netweets)/len(tweets) + 1)
    output += "<br>"
    
    #output += "<br><br>Positive tweets:"
    #output += "<br>"

    #for tweet in ptweets[:10]:
    #    output += tweet['text']
    #    output += "<br>"
 
    output += "<br><br>Negative tweets:"
    output += "<br>"

    for tweet in ntweets[:10]:
        output += tweet['text']
        output += "<br>"

    return output

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/results', methods=['GET', 'POST'])
def confirmation():
    text = request.form.get('data')
    results = analyze(text)
    return results


