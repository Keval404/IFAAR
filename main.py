import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import plotly.express as px 
from newsapi import NewsApiClient  

def get_gold_news():
    newsapi = NewsApiClient(api_key='')  # Replace with your NewsAPI key 8e26b930de804bb4a48f8e909f11689a

    # Fetch news articles related to gold
    articles = newsapi.get_everything(q='gold', language='en', sort_by='relevancy')

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

        st.sidebar.markdown(f'<div style="background-color:{recommendation_color}; padding: 10px; border-radius: 5px;"><h2>{aggregated_recommendation}</h2></div>', unsafe_allow_html=True)



    elif option == 'Mutual Fund':
        st.title("Mutual Fund Information")

        # Add content for displaying mutual fund recommendations
        st.subheader("Recommended Mutual Funds")

        # Example list of recommended mutual funds
        recommended_funds = [
            "Vanguard Total Stock Market Index Fund",
            "Fidelity 500 Index Fund",
            "T. Rowe Price Blue Chip Growth Fund",
            # Add more recommended mutual funds here
        ]

        # Display recommended mutual funds
        for fund in recommended_funds:
            st.write(fund)

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