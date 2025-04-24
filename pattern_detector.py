import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def detect_patterns(data):
    """
    Detects chart patterns in the given OHLC data.
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
    window = 20  # Window for detecting extrema
    
    # Find local maxima and minima
    maxima = argrelextrema(close, np.greater, order=window)[0]
    minima = argrelextrema(close, np.less, order=window)[0]
    
    # Double Top Detection
    if len(maxima) >= 2:
        last_two_maxima = maxima[-2:]
        if abs(close[last_two_maxima[0]] - close[last_two_maxima[1]]) < 0.02 * close[last_two_maxima[0]]:
            patterns["Double Top"]["detected"] = True
            patterns["Double Top"]["points"] = list(last_two_maxima)
    
    # Double Bottom Detection
    if len(minima) >= 2:
        last_two_minima = minima[-2:]
        if abs(close[last_two_minima[0]] - close[last_two_minima[1]]) < 0.02 * close[last_two_minima[0]]:
            patterns["Double Bottom"]["detected"] = True
            patterns["Double Bottom"]["points"] = list(last_two_minima)
    
    # Head and Shoulders Detection (simplified)
    if len(maxima) >= 3 and len(minima) >= 2:
        last_three_maxima = maxima[-3:]
        last_two_minima = minima[-2:]
        if (close[last_three_maxima[1]] > close[last_three_maxima[0]] and 
            close[last_three_maxima[1]] > close[last_three_maxima[2]] and
            abs(close[last_three_maxima[0]] - close[last_three_maxima[2]]) < 0.02 * close[last_three_maxima[1]]):
            patterns["Head and Shoulders"]["detected"] = True
            patterns["Head and Shoulders"]["points"] = list(last_three_maxima) + list(last_two_minima)
    
    # Flag Detection (simplified)
    if len(maxima) > 1 and len(minima) > 1:
        recent_max = maxima[-1]
        recent_min = minima[-1]
        if recent_max > recent_min and close[recent_max] - close[recent_min] < 0.05 * close[recent_max]:
            patterns["Flag"]["detected"] = True
            patterns["Flag"]["points"] = [recent_min, recent_max]
    
    # Pennant Detection (simplified)
    if len(maxima) > 2 and len(minima) > 2:
        if (close[maxima[-1]] - close[minima[-1]] < 0.03 * close[maxima[-1]] and
            close[maxima[-2]] - close[minima[-2]] > 0.05 * close[maxima[-2]]):
            patterns["Pennant"]["detected"] = True
            patterns["Pennant"]["points"] = [minima[-2], maxima[-2], minima[-1], maxima[-1]]
    
    # Triangle Detection (simplified)
    if len(maxima) > 2 and len(minima) > 2:
        highs = close[maxima[-3:]]
        lows = close[minima[-3:]]
        if np.std(highs) < 0.02 * np.mean(highs) and np.std(lows) < 0.02 * np.mean(lows):
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