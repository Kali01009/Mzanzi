import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt

def draw_trendline(data, timeframe='15T'):
    """
    Function to draw a trendline and detect breakout.
    data: Historical price data
    timeframe: Timeframe for analysis (e.g., '15T' for 15-minutes)
    """
    # Identify peaks and troughs for trendlines (simple approach)
    data['High'] = data['High'].rolling(window=5).max()  # Local maxima (resistance)
    data['Low'] = data['Low'].rolling(window=5).min()    # Local minima (support)
    
    # Identify points where the price touches the trendline
    touches = []
    for i in range(len(data)):
        if data['Close'][i] in [data['High'][i], data['Low'][i]]:
            touches.append(data.index[i])  # Mark price touches
    
    return touches

def detect_patterns(data):
    """
    Detect chart patterns like Head & Shoulders, Double/Triple Tops/Bottoms
    """
    patterns = []
    for i in range(2, len(data)-2):
        if (data['High'][i] > data['High'][i-1] and data['High'][i] > data['High'][i+1]
            and data['High'][i-1] < data['High'][i-2] and data['High'][i+1] < data['High'][i+2]):
            patterns.append('Head & Shoulders')

    return patterns

def check_for_breakouts(data):
    """
    Check for breakouts above trendline and retests on lower timeframes.
    """
    breakouts = []
    for i in range(1, len(data)):
        if data['Close'][i] > data['High'][i-1]:  # Price breaks above resistance
            breakouts.append(data.index[i])  # Mark breakout points
            
            # Check for retest on 5-min and 1-min (example logic, real implementation would use lower timeframes)
            if data['Close'][i-1] < data['High'][i-2] and data['Close'][i] > data['High'][i-1]:
                breakouts.append('Breakout confirmed')
    
    return breakouts

def analyze_selected_indices(selected_indices, market_data):
    """
    Analyze the selected indices and look for signals like reversal at trendline,
    breakouts and confirmations.
    """
    analysis_results = {}
    for index in selected_indices:
        data = pd.DataFrame(market_data)  # Convert market data to pandas DataFrame
        
        # Analyze the 15-minute timeframe (or higher)
        touches = draw_trendline(data)
        patterns = detect_patterns(data)
        breakouts = check_for_breakouts(data)
        
        # Store the results in the dictionary
        analysis_results[index] = {
            'Touches': touches,
            'Patterns': patterns,
            'Breakouts': breakouts
        }
        
        # Optionally, create a plot to visualize detected trendlines and breakouts
        plt.figure(figsize=(10, 6))
        plt.plot(data['Close'], label=f'{index} Close Price', color='blue')
        
        if touches:
            plt.scatter(touches, data['Close'][touches], color='red', label='Touches', zorder=5)
        if breakouts:
            plt.scatter(breakouts, data['Close'][breakouts], color='green', label='Breakouts', zorder=5)
        
        plt.title(f"Analysis for {index}")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"static/{index}_analysis.png")
        
    return analysis_results
