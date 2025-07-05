import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from scipy.optimize import newton

def calculate_xirr(prices: List[Dict]) -> float:
    """
    Calculate XIRR (Extended Internal Rate of Return) for stock prices.
    This assumes you bought the stock at the oldest price and sold at the newest price.
    """
    if len(prices) < 2:
        return 0.0
    
    try:
        # Sort prices by date
        sorted_prices = sorted(prices, key=lambda x: x["date"])
        
        # Create cash flows: negative for purchase, positive for sale
        cash_flows = []
        dates = []
        
        # Initial purchase (negative cash flow)
        initial_price = sorted_prices[0]["close"]
        initial_date = datetime.strptime(sorted_prices[0]["date"], "%Y-%m-%d")
        cash_flows.append(-initial_price)
        dates.append(initial_date)
        
        # Final sale (positive cash flow)
        final_price = sorted_prices[-1]["close"]
        final_date = datetime.strptime(sorted_prices[-1]["date"], "%Y-%m-%d")
        cash_flows.append(final_price)
        dates.append(final_date)
        
        # Calculate XIRR using Newton's method
        def xirr_equation(rate):
            total = 0
            for cf, date in zip(cash_flows, dates):
                days_diff = (date - dates[0]).days
                total += cf / ((1 + rate) ** (days_diff / 365.25))
            return total
        
        # Try to find the rate
        try:
            rate = newton(xirr_equation, 0.1, maxiter=100)
            return rate * 100  # Convert to percentage
        except:
            # Fallback: simple annualized return
            days = (final_date - initial_date).days
            if days > 0:
                total_return = (final_price / initial_price) - 1
                annualized_return = ((1 + total_return) ** (365.25 / days)) - 1
                return annualized_return * 100
            return 0.0
            
    except Exception as e:
        print(f"Error calculating XIRR: {e}")
        return 0.0

def calculate_sharpe_ratio(prices: List[Dict], risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe ratio for stock prices.
    Sharpe ratio = (Return - Risk-free rate) / Standard deviation of returns
    """
    if len(prices) < 2:
        return 0.0
    
    try:
        # Sort prices by date
        sorted_prices = sorted(prices, key=lambda x: x["date"])
        
        # Calculate daily returns
        daily_returns = []
        for i in range(1, len(sorted_prices)):
            prev_price = sorted_prices[i-1]["close"]
            curr_price = sorted_prices[i]["close"]
            daily_return = (curr_price - prev_price) / prev_price
            daily_returns.append(daily_return)
        
        if len(daily_returns) == 0:
            return 0.0
        
        # Convert to numpy array for calculations
        returns = np.array(daily_returns)
        
        # Calculate annualized return and volatility
        mean_daily_return = np.mean(returns)
        std_daily_return = np.std(returns, ddof=1)
        
        # Annualize (assuming 252 trading days per year)
        annualized_return = mean_daily_return * 252
        annualized_volatility = std_daily_return * np.sqrt(252)
        
        # Calculate Sharpe ratio
        if annualized_volatility == 0:
            return 0.0
        
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        return sharpe_ratio
        
    except Exception as e:
        print(f"Error calculating Sharpe ratio: {e}")
        return 0.0

def calculate_volatility(prices: List[Dict]) -> float:
    """
    Calculate annualized volatility (standard deviation of returns) for stock prices.
    """
    if len(prices) < 2:
        return 0.0
    
    try:
        # Sort prices by date
        sorted_prices = sorted(prices, key=lambda x: x["date"])
        
        # Calculate daily returns
        daily_returns = []
        for i in range(1, len(sorted_prices)):
            prev_price = sorted_prices[i-1]["close"]
            curr_price = sorted_prices[i]["close"]
            daily_return = (curr_price - prev_price) / prev_price
            daily_returns.append(daily_return)
        
        if len(daily_returns) == 0:
            return 0.0
        
        # Convert to numpy array for calculations
        returns = np.array(daily_returns)
        
        # Calculate standard deviation
        std_daily_return = np.std(returns, ddof=1)
        
        # Annualize volatility (assuming 252 trading days per year)
        annualized_volatility = std_daily_return * np.sqrt(252) * 100  # Convert to percentage
        
        return annualized_volatility
        
    except Exception as e:
        print(f"Error calculating volatility: {e}")
        return 0.0

def calculate_beta(stock_prices: List[Dict], market_prices: List[Dict]) -> float:
    """
    Calculate beta coefficient (correlation with market).
    This is an additional metric not in the original but useful for stock analysis.
    """
    if len(stock_prices) < 2 or len(market_prices) < 2:
        return 0.0
    
    try:
        # Convert to DataFrames for easier alignment
        stock_df = pd.DataFrame(stock_prices)
        market_df = pd.DataFrame(market_prices)
        
        stock_df['date'] = pd.to_datetime(stock_df['date'])
        market_df['date'] = pd.to_datetime(market_df['date'])
        
        # Merge on date
        merged_df = pd.merge(stock_df, market_df, on='date', suffixes=('_stock', '_market'))
        
        if len(merged_df) < 2:
            return 0.0
        
        # Calculate returns
        merged_df = merged_df.sort_values('date')
        merged_df['stock_return'] = merged_df['close_stock'].pct_change()
        merged_df['market_return'] = merged_df['close_market'].pct_change()
        
        # Remove NaN values
        merged_df = merged_df.dropna()
        
        if len(merged_df) < 2:
            return 0.0
        
        # Calculate beta
        covariance = np.cov(merged_df['stock_return'], merged_df['market_return'])[0][1]
        market_variance = np.var(merged_df['market_return'], ddof=1)
        
        if market_variance == 0:
            return 0.0
        
        beta = covariance / market_variance
        return beta
        
    except Exception as e:
        print(f"Error calculating beta: {e}")
        return 0.0 