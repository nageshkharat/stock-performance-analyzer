# Stock Performance Analyzer 📈
## Python Version with FastAPI & Streamlit

A modern stock analysis application built with Python, FastAPI, and Streamlit that provides real-time financial metrics using the Alpha Vantage API.

## ✨ Features

- **Real-time Stock Analysis**: Get live stock data from Alpha Vantage API
- **Financial Metrics**: Calculate XIRR, Sharpe Ratio, and Volatility
- **Modern UI**: Beautiful Streamlit interface with dark theme
- **Fast API Backend**: RESTful API built with FastAPI
- **Proper Calculations**: Accurate financial computations using scipy and numpy

## 🏗️ Architecture

- **Backend**: FastAPI (Python) - Handles API requests and financial calculations
- **Frontend**: Streamlit - Interactive web interface
- **Data Source**: Alpha Vantage API - Real-time stock market data
- **Calculations**: NumPy, SciPy, Pandas - Professional-grade financial analysis

## 📊 Metrics Calculated

1. **XIRR (Extended Internal Rate of Return)**
   - Time-weighted annualized return
   - Accounts for irregular cash flows
   - Shows true investment performance

2. **Sharpe Ratio**
   - Risk-adjusted return measure
   - Higher values indicate better risk-adjusted performance
   - Calculated using risk-free rate of 2%

3. **Volatility**
   - Annualized standard deviation of returns
   - Measures price fluctuation risk
   - Expressed as percentage

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Alpha Vantage API key (free from [alphavantage.co](https://www.alphavantage.co/support/#api-key))

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd your-project-directory
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_alpha_vantage_api_key_here
   ```

### Running the Application

The application consists of two parts that need to be run simultaneously:

#### 1. Start the FastAPI Backend Server

In one terminal:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### 2. Start the Streamlit Frontend

In another terminal:
```bash
streamlit run streamlit_app.py
```

The web interface will be available at: http://localhost:8501

## 📱 Usage

1. **Enter a Stock Symbol** (e.g., AAPL, GOOGL, MSFT, TSLA)
2. **Click "Analyze Stock"** to fetch real-time data
3. **View Results**: 
   - XIRR (Extended Internal Rate of Return)
   - Sharpe Ratio (Risk-adjusted return)
   - Volatility (Price fluctuation measure)
4. **Interpret Results** using the built-in guide

## 🔧 API Endpoints

### GET `/api/stock/{symbol}`

Returns financial analysis for a given stock symbol.

**Example Request:**
```bash
curl http://localhost:8000/api/stock/AAPL
```

**Example Response:**
```json
{
  "symbol": "AAPL",
  "xirr": 15.234,
  "sharpe": 1.456,
  "volatility": 23.789
}
```

## 📋 Dependencies

- **fastapi**: Modern, fast web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **streamlit**: Framework for creating web apps
- **httpx**: Async HTTP client for API calls
- **python-dotenv**: Environment variable management
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **scipy**: Scientific computing (for XIRR calculations)
- **plotly**: Interactive visualizations
- **requests**: HTTP library for Streamlit

## 🔒 Environment Variables

Create a `.env` file with the following variables:

```env
# Required
API_KEY=your_alpha_vantage_api_key_here

# Optional
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

## 🆚 Migration from Node.js Version

This Python version replaces the original Node.js/React.js implementation:

### What Changed:
- **Backend**: Express.js → FastAPI
- **Frontend**: React.js → Streamlit
- **Language**: JavaScript → Python
- **Calculations**: Random values → Real financial calculations
- **UI**: React components → Streamlit components

### What Stayed the Same:
- Alpha Vantage API integration
- Core functionality (stock symbol input, analysis display)
- Three key metrics (XIRR, Sharpe, Volatility)
- Similar UI design and user experience

## 🐛 Troubleshooting

### Common Issues:

1. **"API_KEY not found" error**
   - Ensure `.env` file exists with valid `API_KEY`
   - Check that the API key is valid from Alpha Vantage

2. **"Connection error" when analyzing stocks**
   - Make sure FastAPI server is running on port 8000
   - Check that both servers are running simultaneously

3. **"Invalid stock symbol" error**
   - Use valid stock symbols (e.g., AAPL, GOOGL, MSFT)
   - Ensure the symbol exists on US stock markets

4. **"API rate limit exceeded"**
   - Alpha Vantage free tier allows 5 requests per minute
   - Wait a minute before making another request
   - Consider upgrading to premium API key

### Port Conflicts:
- FastAPI runs on port 8000
- Streamlit runs on port 8501
- Make sure these ports are available

## 🏗️ Development

### Project Structure:
```
.
├── main.py              # FastAPI backend server
├── finance_utils.py     # Financial calculation functions
├── streamlit_app.py     # Streamlit frontend
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
└── README_PYTHON.md    # This file
```

### Adding New Features:

1. **New Financial Metrics**: Add calculations to `finance_utils.py`
2. **New API Endpoints**: Add routes to `main.py`
3. **UI Improvements**: Modify `streamlit_app.py`

### Testing API Endpoints:

Visit http://localhost:8000/docs for interactive API documentation.

## 📈 Performance Notes

- **Real Calculations**: Unlike the original version with random values, this implements proper financial calculations
- **Async Operations**: FastAPI uses async/await for better performance
- **Error Handling**: Comprehensive error handling for API failures
- **Rate Limiting**: Respects Alpha Vantage API rate limits

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing free stock market data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Streamlit](https://streamlit.io/) for making beautiful web apps simple
- Original React.js/Node.js version for the foundation

---

**Built with ❤️ using Python, FastAPI, and Streamlit** 