import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def get_pattern_description(pattern):
    """Returns a description of the chart pattern."""
    descriptions = {
        "Double Top": "A bearish reversal pattern with two peaks at similar levels, indicating resistance. Suggests a potential sell opportunity.",
        "Double Bottom": "A bullish reversal pattern with two troughs at similar levels, indicating support. Suggests a potential buy opportunity.",
        "Head and Shoulders": "A bearish reversal pattern with a central peak (head) flanked by two lower peaks (shoulders). Signals a trend reversal.",
        "Flag": "A bullish continuation pattern with a short consolidation after a sharp move, resembling a flag. Suggests a buy on breakout.",
        "Pennant": "A bullish continuation pattern with converging trendlines after a sharp move, resembling a pennant. Suggests a buy on breakout.",
        "Triangle": "A continuation pattern with converging highs and lows. Can be bullish or bearish depending on breakout direction.",
        "Cup and Handle": "A bullish continuation pattern with a rounded bottom (cup) followed by a short consolidation (handle). Suggests a buy on breakout."
    }
    return descriptions.get(pattern, "No description available.")

def detect_patterns(data, sensitivity=1.0):
    """
    Detects chart patterns in the given OHLC data with adjustable sensitivity.
    Returns a dictionary with pattern names, detection status, points, and suggested actions.
    """
    patterns = {
        "Double Top": {"detected": False, "points": [], "action": "Sell"},
        "Double Bottom": {"detected": False, "points": [], "action": "Buy"},
        "Head and Shoulders": {"detected": False, "points": [], "action": "Sell"},
        "Flag": {"detected": False, "points": [], "action": "Buy"},
        "Pennant": {"detected": False, "points": [], "action": "Buy"},
        "Triangle": {"detected": False, "points": [], "action": "Buy on breakout"},
        "Cup and Handle": {"detected": False, "points": [], "action": "Buy"}
    }
    
    close = data['Close'].values
    window = int(20 / sensitivity)  # Adjust window based on sensitivity
    
    # Find local maxima and minima
    maxima = argrelextrema(close, np.greater, order=window)[0]
    minima = argrelextrema(close, np.less, order=window)[0]
    
    # Double Top Detection
    if len(maxima) >= 2:
        last_two_maxima = maxima[-2:]
        threshold = 0.02 * sensitivity
        if abs(close[last_two_maxima[0]] - close[last_two_maxima[1]]) < threshold * close[last_two_maxima[0]]:
            patterns["Double Top"]["detected"] = True
            patterns["Double Top"]["points"] = list(last_two_maxima)
    
    # Double Bottom Detection
    if len(minima) >= 2:
        last_two_minima = minima[-2:]
        if abs(close[last_two_minima[0]] - close[last_two_minima[1]]) < threshold * close[last_two_minima[0]]:
            patterns["Double Bottom"]["detected"] = True
            patterns["Double Bottom"]["points"] = list(last_two_minima)
    
    # Head and Shoulders Detection (simplified)
    if len(maxima) >= 3 and len(minima) >= 2:
        last_three_maxima = maxima[-3:]
        last_two_minima = minima[-2:]
        if (close[last_three_maxima[1]] > close[last_three_maxima[0]] and 
            close[last_three_maxima[1]] > close[last_three_maxima[2]] and
            abs(close[last_three_maxima[0]] - close[last_three_maxima[2]]) < threshold * close[last_three_maxima[1]]):
            patterns["Head and Shoulders"]["detected"] = True
            patterns["Head and Shoulders"]["points"] = list(last_three_maxima) + list(last_two_minima)
    
    # Flag Detection (simplified)
    if len(maxima) > 1 and len(minima) > 1:
        recent_max = maxima[-1]
        recent_min = minima[-1]
        if recent_max > recent_min and close[recent_max] - close[recent_min] < 0.05 * sensitivity * close[recent_max]:
            patterns["Flag"]["detected"] = True
            patterns["Flag"]["points"] = [recent_min, recent_max]
    
    # Pennant Detection (simplified)
    if len(maxima) > 2 and len(minima) > 2:
        if (close[maxima[-1]] - close[minima[-1]] < 0.03 * sensitivity * close[maxima[-1]] and
            close[maxima[-2]] - close[minima[-2]] > 0.05 * sensitivity * close[maxima[-2]]):
            patterns["Pennant"]["detected"] = True
            patterns["Pennant"]["points"] = [minima[-2], maxima[-2], minima[-1], maxima[-1]]
    
    # Triangle Detection (simplified)
    if len(maxima) > 2 and len(minima) > 2:
        highs = close[maxima[-3:]]
        lows = close[minima[-3:]]
        if np.std(highs) < 0.02 * sensitivity * np.mean(highs) and np.std(lows) < 0.02 * sensitivity * np.mean(lows):
            patterns["Triangle"]["detected"] = True
            patterns["Triangle"]["points"] = list(maxima[-3:]) + list(minima[-3:])
    
    # Cup and Handle Detection (simplified)
    if len(minima) > 3:
        cup_min = minima[-4]
        handle_min = minima[-1]
        if close[cup_min] < close[handle_min] and close[maxima[-1]] > close[maxima[-2]]:
            patterns["Cup and Handle"]["detected"] = True
            patterns["Cup and Handle"]["points"] = [cup_min, maxima[-2], handle_min, maxima[-1]]
    
    return patterns
