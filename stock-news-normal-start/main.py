import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "GRW93OQI619U2HYJ"
NEWS_API_KEY = "a18c3715d601437aabd390f95e6e53c4"
TWILIO_SID = "AC22afa3db868a9c64e70cc2598a6ff70e"
AUTH_TOKEN = "b593c3d6c5264aab7bc6f2375f5c0419"

stock_parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK_NAME,
            "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
closing_price_yesterday = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
closing_price_day_before_yesterday = float(day_before_yesterday_data["4. close"])

difference = float(closing_price_yesterday - closing_price_day_before_yesterday)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percent_diff = round((difference/closing_price_yesterday)*100, 2)
if abs(percent_diff) > 2:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news = news_response.json()["articles"][:3]

    article_list = [f"{STOCK_NAME}: {up_down}{percent_diff}%\nHeadline: {article['title']}."
                    f"\nBrief: {article['description']}" for article in news]
    client = Client(TWILIO_SID, AUTH_TOKEN)
    for article in article_list:
        message = client.messages.create(
                             body=article,
                             from_='+13174837336',
                             to='+13852399946'
                         )
