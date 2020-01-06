from flask import Flask, render_template, request, redirect, url_for
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
    # code.interact(local=dict(globals(), **locals()))
    neg_percent = 0
    pos_percent = 0
    neu_percent = 0
    return render_template('index.html', negative=neg_percent, positive=pos_percent, neutral=neu_percent)


@app.route('/analyze', methods=['POST'])
def analyze():
    consumer_key = 'tI1A1TXXpYqALOEXQ8GrTYTaE'
    consumer_secret = 'qKrpnuD9qGEA7DTgLVkna1sSqLvTjpjqhTLAALZ1IjyOpw26Qx'
    access_token = '1398879151-H6Sjo2ujuLYYIBhdEY79jT2w5wFStehEPXD9d5E'
    access_token_secret = 'JnX173zNIzJ5jOaTYxpUkEhK2hjJzZJZVNwaag3qERvp1'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    search_term = request.form['search']
    # code.interact(local=dict(globals(), **locals()))
    tweets = api.search(search_term, count=200)

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

    neg_percent = (len(negative)/200)*100

    pos_percent = (len(positive)/200)*100
    neu_percent = (len(neutral)/200)*100

    return redirect(url_for('index', _anchor='courses-section', negative=neg_percent, positive=pos_percent, neutral=neu_percent,analyzed='true'))


if __name__ == "__main__":
    app.run(debug=True)
