import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import plotly.express as px 
from newsapi import NewsApiClient 
import plotly.graph_objs as go
# from mutual_fund_forecasting_integration import load_mutual_fund_data, predict_mutual_fund
import ta  # Technical Analysis library, install using: pip install ta
import requests  # Add this line to import the requests library for making API requests



# def plot_indicators(data):
#     # Add MACD
#     data['macd'] = ta.trend.macd_diff(data['Close'])
#     data['signal'] = ta.trend.macd_signal(data['Close'])
#     fig_macd = go.Figure()
#     fig_macd.add_trace(go.Scatter(x=data['Date'], y=data['macd'], name='MACD'))
#     fig_macd.add_trace(go.Scatter(x=data['Date'], y=data['signal'], name='Signal'))
#     fig_macd.update_layout(title='MACD Indicator', xaxis_title='Date', yaxis_title='MACD Value')
#     st.plotly_chart(fig_macd)

#     # Add EMA (Exponential Moving Average)
#     data['ema_short'] = ta.trend.ema_indicator(data['Close'], window=12)
#     data['ema_long'] = ta.trend.ema_indicator(data['Close'], window=26)
#     fig_ema = go.Figure()
#     fig_ema.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Price'))
#     fig_ema.add_trace(go.Scatter(x=data['Date'], y=data['ema_short'], name='EMA Short'))
#     fig_ema.add_trace(go.Scatter(x=data['Date'], y=data['ema_long'], name='EMA Long'))
#     fig_ema.update_layout(title='EMA Indicator', xaxis_title='Date', yaxis_title='EMA Value')
#     st.plotly_chart(fig_ema)

#     # Add RSI (Relative Strength Index)
#     data['rsi'] = ta.momentum.rsi(data['Close'])
#     fig_rsi = go.Figure()
#     fig_rsi.add_trace(go.Scatter(x=data['Date'], y=data['rsi'], name='RSI'))
#     fig_rsi.update_layout(title='RSI Indicator', xaxis_title='Date', yaxis_title='RSI Value')
#     st.plotly_chart(fig_rsi)

#     # Add SMA (Simple Moving Average)
#     data['sma_short'] = ta.trend.sma_indicator(data['Close'], window=12)
#     data['sma_long'] = ta.trend.sma_indicator(data['Close'], window=26)
#     fig_sma = go.Figure()
#     fig_sma.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Price'))
#     fig_sma.add_trace(go.Scatter(x=data['Date'], y=data['sma_short'], name='SMA Short'))
#     fig_sma.add_trace(go.Scatter(x=data['Date'], y=data['sma_long'], name='SMA Long'))
#     fig_sma.update_layout(title='SMA Indicator', xaxis_title='Date', yaxis_title='SMA Value')
#     st.plotly_chart(fig_sma)

# Function to fetch cryptocurrency data from CoinGecko API
def get_crypto_data(api_key):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
        "key": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def plot_crypto_data(data):
    st.subheader("Top 5 Cryptocurrencies by Market Cap")
    for coin in data:
        st.write(f"**{coin['name']} ({coin['symbol'].upper()})**")
        st.write(f"Price: ${coin['current_price']}")
        st.write(f"24h Price Change: {coin['price_change_percentage_24h']}%")
        st.write("---")

def plot_indicators(data, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock Price'))

    # Plot indicators for both historical and predicted data
    fig.add_trace(go.Scatter(x=data['Date'], y=data['macd'], name='MACD'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['signal'], name='Signal'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['ema_short'], name='EMA Short'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['ema_long'], name='EMA Long'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['rsi'], name='RSI'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['sma_short'], name='SMA Short'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['sma_long'], name='SMA Long'))

    fig.update_layout(title=f'{title} with Indicators', xaxis_title='Date', yaxis_title='Value')
    st.plotly_chart(fig)


def plot_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title=f'Candlestick Chart for ',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def redirect_to_page(page_url):
    st.markdown(
        f"""
        <a href="{page_url}" target="_blank" rel="noopener noreferrer">
            <button style="padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">Get Mutual Fund Forecast</button>
        </a>
        """
        , unsafe_allow_html=True
    )

def redirect_to_page_crypto(page_url):
    st.markdown(
        f"""
        <a href="{page_url}" target="_blank" rel="noopener noreferrer">
            <button style="padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">Get Mutual Fund Forecast</button>
        </a>
        """
        , unsafe_allow_html=True
    )

def get_stock_news():
    newsapi = NewsApiClient(api_key='8e26b930de804bb4a48f8e909f11689a')  # Replace with your NewsAPI key d82c64fade7b44dfb1912dcb4985ca43

    # Fetch news articles related to the specified stock symbol
    articles = newsapi.get_everything(q='stocks', language='en', sort_by='relevancy', page_size=10)

    return articles['articles']

def get_gold_news():
    newsapi = NewsApiClient(api_key='8e26b930de804bb4a48f8e909f11689a')  # Replace with your NewsAPI key 8e26b930de804bb4a48f8e909f11689a

    # Fetch news articles related to gold
    articles = newsapi.get_everything(q='gold', language='en', sort_by='relevancy')

    return articles['articles']

def get_crypto_news():
    newsapi = NewsApiClient(api_key='8e26b930de804bb4a48f8e909f11689a')  # Replace with your NewsAPI key 8e26b930de804bb4a48f8e909f11689a

    # Fetch news articles related to gold
    articles = newsapi.get_everything(q='crypto', language='en', sort_by='relevancy')

    return articles['articles']


def calculate_investment_percentage():
    # Replace these with actual data or calculations for percentages
    stock_percentage = 40
    mutual_fund_percentage = 25
    gold_percentage = 20
    crypto_percentage = 15

    return {
        'Stock': stock_percentage,
        'Mutual Fund': mutual_fund_percentage,
        'Gold': gold_percentage,
        'Crypto': crypto_percentage
    }

def add_indicators(data):
    # Add MACD
    data['macd'] = ta.trend.macd_diff(data['Close'])
    data['signal'] = ta.trend.macd_signal(data['Close'])

    # Add EMA (Exponential Moving Average)
    data['ema_short'] = ta.trend.ema_indicator(data['Close'], window=12)
    data['ema_long'] = ta.trend.ema_indicator(data['Close'], window=26)

    # Add RSI (Relative Strength Index)
    data['rsi'] = ta.momentum.rsi(data['Close'])

    # Add SMA (Simple Moving Average)
    data['sma_short'] = ta.trend.sma_indicator(data['Close'], window=12)
    data['sma_long'] = ta.trend.sma_indicator(data['Close'], window=26)




def main():

    st.markdown(
        """
        <style>
        /* Style the navbar */
        .navbar {
            overflow: hidden;
            background-color: #333;
            width: 100vh
        }

        /* Navbar links */
        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
        }

        /* On hover, the links will change color */
        .navbar a:hover {
            background-color: #ffffff;
            color: black;
        }

        .profile {
            float: right !important;
            display: flex;
            align-items: center;
            color: white;
            text-decoration: none;
            # padding: 14px 20px;
        }
        .profile img {
            width: 25px; /* Adjust the width as needed */
            height: auto;
        }

        </style>
        """
        , unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="navbar">
            <a href="#portfolio">Portfolio</a>
            <a href="#support">Support</a>
            <a href="#news">News</a>
            <a href="#blogs">Blogs</a>
            <a class="profile" href="#profile"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="User Icon"> </a>
        </div>
        """
        , unsafe_allow_html=True
    )

    st.markdown("---")
    
    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Go to', ('Stock', 'Mutual Fund', 'Gold', 'Crypto'))

    if option == 'Stock':
        # ... (rest of your code)

        symbol = None  # Declare symbol outside the if block

        # Button to fetch news for the selected stock
        if st.button("Get News for Selected Stock"):
            # Clear existing elements
            st.subheader("Latest News")
            chart_container = st.empty()  # Create an empty container for the chart
            chart_container.text("Fetching news...")

            stock_news = get_stock_news()

            # Display news articles in a loop
            for news in stock_news:
                col1, col2 = st.columns([1, 4])
                col1.image(news['urlToImage'], use_column_width=True)
                col2.write(f"**{news['title']}**")
                col2.write(news['description'])
                col2.write(f"Source: {news['source']['name']}")
                col2.write("---")

                # Update the chart container with the new content or remove it
              

    if option == 'Stock':
        @st.cache_data
        def get_data():
            path = 'stock.csv'
            return pd.read_csv(path, low_memory=False)

        df = get_data()
        df = df.drop_duplicates(subset="Name", keep="first")

        START = "2015-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")

        st.title("Stock Prediction")
        st.write("###")

        stocks = df['Name']
        # stocks = ("AAPL", "NFLX", "GOOG", "MSFT", "INFY", "RPOWER.NS", "BAJFINANCE.NS", "YESBANK.NS", "RCOM.NS", "EXIDEIND.NS", "TATACHEM.NS", "TATAMOTORS.NS", "RUCHI.NS")
        selected_stock = st.selectbox("Select dataset and years for prediction", stocks)

        index = df[df["Name"]==selected_stock].index.values[0]
        symbol = df["Symbol"][index]

        n_years = st.slider("", 1, 5)
        period = n_years * 365

        @st.cache_data
        def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data

        data_load_state = st.text("Load data ...")
        data = load_data(symbol)
        data_load_state.text("Loading data ... Done!")

        st.write("###")

        st.subheader("Raw data")
        st.write(data.tail())

        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
            fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible = True)
            st.plotly_chart(fig)

        plot_raw_data()

        #Forecasting
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)

        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        st.write("***")
        st.write("###")

        st.subheader("Forecast data")
        st.write(forecast.tail())

        fig1 = plot_plotly(m, forecast)
        predicted_data = forecast[['ds', 'yhat']].rename(columns={'ds': 'Date', 'yhat': 'Close'})
        add_indicators(predicted_data)
        plot_indicators(predicted_data, 'Predicted Data')
        st.plotly_chart(fig1)

        st.subheader("Forecast Components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)

        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Recommendation logic based on predicted prices for future dates
        forecast['recommendation'] = 'Hold'  # Default recommendation

        for i in range(len(forecast) - 1):
            if forecast['yhat'].iloc[i] < forecast['yhat'].iloc[-1]:
                forecast.at[i, 'recommendation'] = 'Buy'
            elif forecast['yhat'].iloc[i] > forecast['yhat'].iloc[-1]:
                forecast.at[i, 'recommendation'] = 'Sell'

        # Displaying stock name along with recommendation for future dates
        # forecast['stock_name'] = selected_stock
        # future_forecast = forecast[forecast['ds'] > TODAY]  # Filtering future dates
        # st.write(future_forecast[['ds', 'stock_name', 'yhat', 'recommendation']])

        forecast['stock_name'] = selected_stock
        future_forecast = forecast[forecast['ds'] > TODAY]  # Filtering future dates

        # Aggregating recommendations for a larger timeframe (e.g., 6-12 months)
        timeframe_forecast = future_forecast[future_forecast['ds'] < date.today() + pd.DateOffset(months=6)]  # Adjust the timeframe as needed

        aggregated_recommendation = timeframe_forecast['recommendation'].value_counts().idxmax()
        # Styling the recommendation box based on the recommendation
        if aggregated_recommendation == 'Buy':
            recommendation_color = 'green'
        elif aggregated_recommendation == 'Sell':
            recommendation_color = 'red'
        else:
            recommendation_color = 'blue'

        st.sidebar.title(f"Overall Recommendation for the next 6 months: ")

        st.sidebar.markdown(f'<div style="background-color:{recommendation_color}; padding: 10px; border-radius: 5px;"><h2>\
        {aggregated_recommendation}</h2></div>', unsafe_allow_html=True)


        plot_candlestick_chart(data)
        add_indicators(data)
        plot_indicators(data, 'Historical Data')   



    elif option == 'Mutual Fund':
        st.title("Mutual Fund Information")


        # Add content for displaying mutual fund recommendations
        st.subheader("Recommended Mutual Funds")
        # Save the current page to session state
        if st.button("Get Mutual Fund Forecast"):
            redirect_to_page('http://127.0.0.1:5000/')  # Replace with your desired URL

        

    elif option == 'Gold':
        st.title("Gold Related")
        st.write("Here are the latest news articles related to gold:")
        # Fetch gold-related news articles
        gold_news = get_gold_news()

        # Display news articles in tiled layout
        for news in gold_news:
            col1, col2 = st.columns([1, 4])
            col1.image(news['urlToImage'], use_column_width=True)
            col2.write(f"**{news['title']}**")
            col2.write(news['description'])
            col2.write(f"Source: {news['source']['name']}")
            col2.write("---")
    elif option == 'Crypto':
        st.title("Crypto Information")
        
        # Add content for displaying mutual fund recommendations
        st.subheader("Recommended Mutual Funds")
        # Save the current page to session state
        if st.button("Get Mutual Fund Forecast"):
            redirect_to_page_crypto('http://127.0.0.1:5001/')  # Replace with your desired URL

        crypto_api_key = '457B73C1-9597-4509-9923-1B4B5EF3E6B5'  # Replace with your actual API key
        crypto_data = get_crypto_data(crypto_api_key)

        # Display cryptocurrency data
        plot_crypto_data(crypto_data)

        # ... (code for cryptocurrency)

    # Display pie chart in sidebar for investment percentages
    investment_percentages = calculate_investment_percentage()
    fig = px.pie(
        values=list(investment_percentages.values()),
        names=list(investment_percentages.keys()),
        title='Investment Allocation'
    )
    st.sidebar.plotly_chart(fig)
    
        
if __name__ == "__main__":
    main()