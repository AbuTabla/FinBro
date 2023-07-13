
# Financial Assistant Chatbot

### Kareem Hamoudeh

from neuralintents import GenericAssistant
import matplotlib.pyplot as plt 
import pandas as pd 
import pandas_datareader as pdr
import mplfinance as mpf 
import pickle 
import sys
import datetime as dt 
import pygame
import os
import random
from pymongo import MongoClient
import getpass
import yfinance as yf
import plotly.graph_objects as go


# Ask the user for username and password
# Connect to your MongoDB cluster
client = MongoClient('mongodb+srv://hamoudehkareem88:yClFOe3bRO2NMNO8@cluster0.x1ahtsy.mongodb.net/')
db = client['cbf']
collection = db['portfolios']
# Create global variables for username and password
username = None
password = None

def user_login():
    global username, password

    # Ask the user for username and password
    username = input("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")

    # Query the MongoDB collection to find the user's document
    document = collection.find_one({'username': username, 'password': password})

    if document is None:
        print("Invalid username or password.")
    else:
        return document

document = None
while document is None:
    document = user_login()

# Now that a valid user is logged in, load the portfolio
portfolio = document['portfolio']





# Load the portfolio from the user's document
portfolio = document['portfolio']


def play_sound(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def greeting():
    print("Suuuuuuh Dude!")
    audio_directory = './data/audio/Suhs'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    play_sound(audio_path)


def save_portfolio():
    # Update the user's document in the MongoDB collection
    collection.update_one({'username': username, 'password': password}, {'$set': {'portfolio': portfolio}})

def add_portfolio():
    ticker = input("Which are you adding: ").upper()
    amount = input("How many shares are we adding: ")

    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()



def remove_portfolio():
    ticker = input("Which stock do you want to sell: ").upper()
    amount = input("How many shares do you want to sell: ")

    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            if portfolio[ticker] == 0:
                del portfolio[ticker]
            save_portfolio()
        else:
            play_sound('./data/audio/Misc/you_not_guy.mp3')
            print("You don't have the facilities for that big man!")
    else:
        play_sound('./data/audio/Misc/you_not_guy.mp3')
        print(f"You don't own any shares of {ticker}")

def show_portfolio():
    print("Your Portfolio:")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")


def portfolio_worth():
    total = 0
    for ticker in portfolio.keys():
        data = pdr.DataReader(ticker, 'yahoo')
        price = data['Close'].iloc[-1]
        total += price * portfolio[ticker]

    print(f"Your portfolio is worth {total} USD")

def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYY-MM-DD): ")
    total_now = 0
    total_then = 0
    for ticker in portfolio.keys():
        data = pdr.DataReader(ticker, 'yahoo')
        price_now = data['Close'].iloc[-1]
        price_then = data.loc[data.index == starting_date]['Close'].values[0]
        total_now += price_now * portfolio[ticker]
        total_then += price_then * portfolio[ticker]

    print(f"Relative Gains: {((total_now - total_then) / total_then) * 100}%")
    print(f"Absolute Gains: {total_now - total_then} USD")


def plot_chart():
    while True:
        try:
            ticker = input("Choose a Ticker Symbol: ")
            starting_string = input("Choose a starting date (DD/MM/YYYY): ")

            start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
            end = dt.datetime.now()

            data = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])

            fig.update_layout(
                title='Interactive candlestick chart',
                yaxis_title='Stock Price (USD per Shares)',
                xaxis_title='Date'
            )

            fig.show()
            
            break
        
        except ValueError:
            print("Wrong date format. Please enter the date in DD/MM/YYYY format.")
        except KeyError:
            print("Invalid ticker symbol. Please try again.")

def bye():
    print("Peace Out Broski!")
    audio_directory = './data/audio/Ahaas'
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audio_file = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, audio_file)
    play_sound(audio_path)
#   sys.exit(0)     # Delete this line when making it a web application, keep for terminal application



mappings = {
    'greeting': greeting,
    'plot_chart' : plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'bye': bye
}
assistant = GenericAssistant('intents.json', mappings, "Jafire")

assistant.train_model()
assistant.save_model('Jafire','./data/ML_Models/')
while True:
    message = input("Go: ")
    assistant.request(message)

