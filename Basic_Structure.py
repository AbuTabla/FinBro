
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



def myfunction():
    pass

## When greetings: run function
mappings = {
    'greetings' : myfunction 
}
chatbot = GenericAssistant('intents.json', intent_methods= mappings)

chatbot.train_model()

