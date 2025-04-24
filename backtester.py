import pandas as pd
import numpy as np
from pattern_detector import detect_patterns

def backtest_patterns(data, patterns):
    """
    Backtests the reliability of detected patterns.
    Returns a dictionary with pattern statistics.
    """
    results = {}
    look_forward = 10  # Periods to check post-pattern
    
    for pattern in patterns:
        stats = {"count": 0, "success_rate": 0.0, "avg_return": 0.0}
        temp_data = data.copy()
        
        # Re-detect patterns for historical data
        historical_patterns = detect_patterns(temp_data)
        if historical_patterns[pattern]["detected"]:
            stats["count"] = len(historical_patterns[pattern]["points"])
            returns = []
            
            for point in historical_patterns[pattern]["points"]:
                if point + look_forward < len(temp_data):
                    future_return = (temp_data['Close'].iloc[point + look_forward] - 
                                   temp_data['Close'].iloc[point]) / temp_data['Close'].iloc[point]
                    returns.append(future_return)
            
            if returns:
                stats["avg_return"] = np.mean(returns)
                stats["success_rate"] = len([r for r in returns if r > 0]) / len(returns)
        
        results[pattern] = stats
    
    return results
