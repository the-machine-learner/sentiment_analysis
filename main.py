from __future__ import print_function, unicode_literals
import subprocess
import requests
import sys
import config
from config import *

try:
  from PyInquirer import prompt, print_json
except Exception:
  subprocess.call([sys.executable, "-m", 'pip', 'install', 'youtube-dl'])
  from PyInquirer import prompt, print_json

try:
  import tweepy
except Exception:
  subprocess.call([sys.executable,"-m",'pip','install','tweepy'])
  import tweepy

try:
  import pandas as pd
except Exception:
  subprocess.call([sys.executable,"-m",'pip','install','pandas'])
  import pandas as pd

try:
  import re
except Exception:
  subprocess.call([sys.executable,"-m",'pip','install','re'])
  import re

try:
  import nltk
  from nltk.sentiment.vader import SentimentIntensityAnalyzer
  nltk.download('vader_lexicon')
except Exception:
  subprocess.call([sys.executable,"-m",'pip','install','nltk'])
  import nltk
  from nltk.sentiment.vader import SentimentIntensityAnalyzer
  nltk.download('vader_lexicon')

question1 = [
{
  'type': 'confirm',
  'name': 'continue',
  'message': 'Do you want to generate a sentiment report ?',
  'default':True,
}
]

question2 = [
{
  'type': 'input',
  'name': 'prod_name',
  'message': 'Please enter the name of product ?',
}
]

#ignoring links and specia characters
def clean_data(prod):
  return " ".join(re.sub('(@[A-Za-z0-9]+)|[^A-Za-z0-9 \t]|(\w+://\S+)', ' ', prod).split())
  
def print_result(score):
  print(score)
  if abs(score)<0.01:
    print(product," has a neutral sentiment")
  elif score<0:
    if(score<-0.1):
      print(product," has a strong negative sentiment")
    else:
      print(product," has a negative sentiment")
  else:
    if(score>0.1):
      print(product," has a strong positive sentiment")
    else:
      print(product," has a positive sentiment")  

def get_sentiments(product):
  
  ##esatblishing connection with twitter and getting tweets
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  auth.set_access_token(access_token, access_token_secret) 
  api = tweepy.API(auth) 
  tweets = api.search(product,count=1000)
  
  #data transformation and cleaning
  data = pd.DataFrame(data=[clean_data(tweet.text) for tweet in tweets], columns = ['tweets'])

  #data analysis
  sid = SentimentIntensityAnalyzer()

  listy = []

  for index, row in data.iterrows():
    ss = sid.polarity_scores(row["tweets"])
    listy.append(ss)
    
  se = pd.Series(listy)
  data['polarity'] = se.values

  #sentiment preiction 
  senti_list = []

  for index,row in data.iterrows():
    pos =  row["polarity"]["pos"]    
    neg =  row["polarity"]["neg"]
    neu =  row["polarity"]["neu"]

    if(pos==0 and neg == 0):
      senti_list.append(0)
    else:
      senti_list.append(pos-neg)
  score = sum(senti_list)/len(senti_list)

  #printing the result according to score
  print_result(score)

if __name__ == '__main__':

  print("-------------product analyser------------")

  while True:
    answer1 = prompt(question1)
    if(answer1['continue']==False):
      sys.exit(0)
    else:
      answer2 = prompt(question2)
      if(answer2['prod_name']==NULL):
        print("Do not leave the product name to be blank")
        continue
      else:
        get_sentiments(answer2['prod_name'])
