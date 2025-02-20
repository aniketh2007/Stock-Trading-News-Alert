import requests
from pyexpat.errors import messages
from twilio.rest import Client
STOCK_NAME = "EXIDEIND"
COMPANY_NAME = "Exide Industries Ltd"
TWILIO_ACCOUNT_SID = YOUR_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = YOUR_TWILIO_AUTH_TOKEN
STOCK_API_KEY = YOUR_STOCK_API_KEY
NEWS_API_KEY = YOUR_NEWS_API_KEY
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
VIRTUAL_TWILIO_NUMBER = YOUR_NUMBER
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
#Get yesterday's closing stock price
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : "EXIDEIND.BSE",
    "outputsize" : "full",
    "apikey" : STOCK_API_KEY

}
response = requests.get(STOCK_ENDPOINT,params=params)
response.raise_for_status()
stock_data = response.json()
yesterdays_closing_price = stock_data["Time Series (Daily)"]["2025-02-19"]["4. close"]

#Get the day before yesterday's closing stock price
day_before_yesterdays_closing_price = stock_data["Time Series (Daily)"]["2025-02-18"]["4. close"]

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. 
difference = float(yesterdays_closing_price)- float(day_before_yesterdays_closing_price)
up_down = None
if difference > 0:
    up_down= "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterdays_closing_price)) *100)
print(diff_percent)
# If  percentage is greater than 1 then print("Get News").
#Use the News API to get articles related to the COMPANY_NAME.
#Use Python slice operator to create a list that contains the first 3 articles.
## STEP 2: Get the actually get the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q" : COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    ## STEP 3: Use Twilio to send a seperate message with each article's title and description to your phone number.
    #Create a new list of the first 3 article's headline and description using list comprehension.
    formated_articles = [f"{STOCK_NAME} {up_down} {diff_percent}%\nHeadline: {articles['title']}. \nBrief:{articles['description']}" for article in three_articles]
    
    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formated_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to="+917348900930"
            
        )

