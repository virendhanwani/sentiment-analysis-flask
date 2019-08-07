from flask import Flask, render_template, request
import tweepy
import pandas as pd
import code
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv
app = Flask(__name__)
dotenv_path = '../.env'
load_dotenv(dotenv_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    search_term = request.form['search']
    tweets = api.search(search_term, count=200)
    # code.interact(local=dict(globals(), **locals()))

    data = pd.DataFrame(
        data=[tweet.text for tweet in tweets], columns=['Tweets'])

    head = data.head(10)

    sid = SentimentIntensityAnalyzer()

    listy = []

    for index, row in data.iterrows():
        ss = sid.polarity_scores(row["Tweets"])
        listy.append(ss)

    se = pd.Series(listy)
    data['polarity'] = se.values

    # display(data.head(100))
    # print(se.values[0])

    negative = []
    for ne in se.values:
        if ne['neg'] > 0:
            negative.append(ne['neg'])

    print(len(negative))

    positive = []
    for ps in se.values:
        if ps['pos'] > 0:
            positive.append(ps['pos'])

    print(len(positive))
    neutral = []
    for nt in se.values:
        if nt['neu'] > 0:
            neutral.append(nt['neu'])

    print(len(neutral))

    return render_template('analyze.html', negative=len(negative), positive=len(positive), neutral=len(neutral))


if __name__ == "__main__":
    app.run(debug=True)
