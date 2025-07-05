import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import time

# Configure the page
st.set_page_config(
    page_title="Stock Performance Analyzer 📈",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling (similar to original design)
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f141e 0%, #1a1f2e 100%);
        color: #dcdcdc;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f141e 0%, #1a1f2e 100%);
    }
    
    .title {
        color: #ffbe3c;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-transform: uppercase;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00e296;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #dcdcdc;
        margin-bottom: 5px;
    }
    
    .error-message {
        color: #ff5050;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background: rgba(255, 80, 80, 0.1);
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .success-message {
        color: #00e296;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background: rgba(0, 226, 150, 0.1);
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="title">Stock Performance Analyzer 📈</h1>', unsafe_allow_html=True)

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'loading' not in st.session_state:
    st.session_state.loading = False

# API Configuration
API_BASE_URL = "http://localhost:8000"  # FastAPI server URL

def fetch_stock_data(symbol: str):
    """Fetch stock analysis data from FastAPI backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/stock/{symbol}", timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 429:
            return None, "API rate limit exceeded. Try again later."
        elif response.status_code == 400:
            return None, "Invalid stock symbol"
        elif response.status_code == 404:
            return None, "Stock data not found"
        else:
            return None, f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Input section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Enter Stock Symbol")
    symbol = st.text_input(
        "",
        placeholder="Enter Stock Symbol (e.g., AAPL, GOOGL, MSFT)",
        help="Enter a valid stock symbol to analyze",
        key="stock_symbol"
    ).upper()
    
    analyze_button = st.button(
        "🔍 Analyze Stock", 
        use_container_width=True,
        type="primary"
    )

# Analysis section
if analyze_button and symbol:
    if len(symbol) < 1:
        st.markdown('<div class="error-message">Please enter a stock symbol</div>', unsafe_allow_html=True)
    else:
        # Show loading spinner
        with st.spinner(f"Analyzing {symbol}... This may take a few moments."):
            data, error = fetch_stock_data(symbol)
            
            if error:
                st.markdown(f'<div class="error-message">{error}</div>', unsafe_allow_html=True)
            else:
                st.session_state.analysis_data = data
                st.markdown(f'<div class="success-message">Analysis complete for {symbol}!</div>', unsafe_allow_html=True)

# Display results
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    
    st.markdown("---")
    st.markdown(f"### 📊 Analysis Results for {data['symbol']}")
    
    # Create metrics display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">XIRR (Extended IRR)</div>
                <div class="metric-value">{data['xirr']:.2f}%</div>
                <small>Annualized return considering time-weighted cash flows</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Sharpe Ratio</div>
                <div class="metric-value">{data['sharpe']:.3f}</div>
                <small>Risk-adjusted return (higher is better)</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Volatility</div>
                <div class="metric-value">{data['volatility']:.2f}%</div>
                <small>Annualized price volatility</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Interpretation section
    st.markdown("---")
    st.markdown("### 📝 Interpretation Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **XIRR (Extended Internal Rate of Return)**
        - Positive: Stock gained value over time
        - Negative: Stock lost value over time
        - Higher values indicate better performance
        """)
        
        st.markdown("""
        **Sharpe Ratio**
        - > 1.0: Good risk-adjusted returns
        - > 2.0: Very good risk-adjusted returns
        - < 0: Poor risk-adjusted returns
        """)
    
    with col2:
        st.markdown("""
        **Volatility**
        - Low (< 20%): Stable stock
        - Medium (20-40%): Moderate risk
        - High (> 40%): High risk/reward
        """)
        
        # Risk assessment
        volatility = data['volatility']
        if volatility < 20:
            risk_level = "🟢 Low Risk"
            risk_color = "#00e296"
        elif volatility < 40:
            risk_level = "🟡 Medium Risk"
            risk_color = "#ffbe3c"
        else:
            risk_level = "🔴 High Risk"
            risk_color = "#ff5050"
        
        st.markdown(f"**Risk Assessment:** <span style='color: {risk_color}; font-weight: bold;'>{risk_level}</span>", unsafe_allow_html=True)

# Instructions section
if not st.session_state.analysis_data:
    st.markdown("---")
    st.markdown("### 🚀 How to Use")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        1. **Enter a Stock Symbol** (e.g., AAPL, GOOGL, MSFT, TSLA)
        2. **Click Analyze** to fetch real-time data
        3. **Review the Results** showing key financial metrics
        4. **Use the Interpretation Guide** to understand the numbers
        """)
    
    with col2:
        st.markdown("""
        **Popular Stock Symbols to Try:**
        - AAPL (Apple Inc.)
        - GOOGL (Alphabet Inc.)
        - MSFT (Microsoft Corp.)
        - TSLA (Tesla Inc.)
        - AMZN (Amazon.com Inc.)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; margin-top: 2rem;'>
    <small>
        📈 Stock Performance Analyzer | Built with ❤️ by Nagesh Kharat<br>
    </small>
</div>
""", unsafe_allow_html=True)

# Auto-refresh option
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    if st.button("🔄 Clear Results"):
        st.session_state.analysis_data = None
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips
    - Use standard stock symbols (e.g., AAPL, GOOGL)
    - Analysis is based on daily historical data
    - Results update in real-time from Alpha Vantage
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("- [Alpha Vantage](https://www.alphavantage.co/)")
    st.markdown("- [FastAPI Docs](http://localhost:8000/docs)") 