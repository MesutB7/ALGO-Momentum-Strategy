#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Load the CHF/JPY data from Yahoo Finance
data = yf.download('CHFJPY=X', start='2022-01-01', end='2024-08-30')

# Function to calculate cumulative returns
def calculate_cumulative_returns(signals):
    signals['returns'] = signals['price'].pct_change()
    signals['strategy_returns'] = signals['signal'].shift(1) * signals['returns']
    signals['cumulative_returns'] = (1 + signals['strategy_returns']).cumprod()
    return signals

# Momentum Strategy
def momentum_strategy(data, window=20):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['momentum'] = data['Close'].diff(window)
    signals['signal'] = np.where(signals['momentum'] > 0, 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    
    # Calculate cumulative returns
    signals = calculate_cumulative_returns(signals)
    
    # Plotting - Price and Signals
    plt.figure(figsize=(12, 8))
    plt.plot(signals['price'], label='CHF/JPY Price', color='black')
    plt.plot(signals[signals['positions'] == 1.0].index, 
             signals['price'][signals['positions'] == 1.0],
             '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(signals[signals['positions'] == -1.0].index, 
             signals['price'][signals['positions'] == -1.0],
             'v', markersize=10, color='r', label='Sell Signal')
    plt.title('Momentum Strategy')
    plt.legend()
    plt.show()
    
    # Plotting - Cumulative Returns
    plt.figure(figsize=(12, 8))
    plt.plot(signals['cumulative_returns'], label='Cumulative Returns', color='blue')
    plt.title('Cumulative Returns - Momentum Strategy')
    plt.legend()
    plt.show()
    
    return signals


# Backtest the strategies
momentum_signals = momentum_strategy(data)


# In[ ]:




