import requests
import datetime as dt
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
alpha_api_key = "GRW93OQI619U2HYJ"
news_api_key = "a18c3715d601437aabd390f95e6e53c4"
acct_sid = "AC22afa3db868a9c64e70cc2598a6ff70e"
auth_token = "3fd9702bafbcee446824b827a7e50a90"

today = dt.datetime.today()
yesterday = today - dt.timedelta(days=1)
yesterday_date = yesterday.date()

parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK_NAME,
            "apikey": alpha_api_key,
}

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday_date,
    "sortBy": "popularity",
    "apiKey": news_api_key,
}



response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
stock_price_data = response.json()
closing_price = stock_price_data["Time Series (Daily)"]

price_dict = [value for (key, value) in closing_price.items()]
close_price = price_dict[0]["4. close"]
closing_price_yesterday = float(close_price)

before_yesterday = price_dict[1]["4. close"]
day_before_yesterday = float(before_yesterday)

difference = abs(closing_price_yesterday - day_before_yesterday)

percent_diff = round((difference/day_before_yesterday)*100, 2)
if percent_diff < 5:
    print("Got News")


news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news = news_response.json()["articles"][:3]

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
desc_list = [(n["title"], n["description"]) for n in news]
print(desc_list)
#TODO 9. - Send each article as a separate message via Twilio. 
client = Client(acct_sid, auth_token)
message = client.messages \
                .create(
                     body=f"{STOCK_NAME}: {percent_diff}% \nHeadline:{desc_list[0]}\nBrief:{0}",
                     from_='+13174837336',
                     to='+13852399946'
                 )

print(message.sid)

