import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Any
from dotenv import load_dotenv
from finance_utils import calculate_xirr, calculate_sharpe_ratio, calculate_volatility

# Load environment variables
load_dotenv()

app = FastAPI(title="Stock Analyzer API", description="Stock performance analysis using Alpha Vantage API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this more restrictively in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found in environment variables. Please set it in .env file")

@app.get("/")
async def root():
    return {"message": "Stock Analyzer API is running"}

@app.get("/api/stock/{symbol}")
async def get_stock_analysis(symbol: str) -> Dict[str, Any]:
    """
    Get stock analysis including XIRR, Sharpe ratio, and volatility for a given symbol.
    """
    try:
        symbol = symbol.upper()
        
        # Fetch data from Alpha Vantage API
        async with httpx.AsyncClient() as client:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
            response = await client.get(url)
            data = response.json()
        
        # Handle API errors
        if "Note" in data:
            raise HTTPException(status_code=429, detail="API rate limit exceeded. Try again later.")
        
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail="Invalid stock symbol")
        
        if "Time Series (Daily)" not in data:
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        # Process stock data
        stock_data = data["Time Series (Daily)"]
        prices = []
        
        for date, values in stock_data.items():
            prices.append({
                "date": date,
                "close": float(values["4. close"])
            })
        
        # Sort prices by date (newest first)
        prices.sort(key=lambda x: x["date"], reverse=True)
        
        # Calculate financial metrics
        xirr = calculate_xirr(prices)
        sharpe = calculate_sharpe_ratio(prices)
        volatility = calculate_volatility(prices)
        
        return {
            "symbol": symbol,
            "xirr": round(xirr, 3),
            "sharpe": round(sharpe, 3),
            "volatility": round(volatility, 3)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stock data")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 