import datetime
import requests
import smtplib
import ssl
import time

binance_api_url = "https://api.binance.com/api/v3/ticker/price"
kraken_api_url = "https://api.kraken.com/0/public/Ticker"

alert_threshold = 0.02  # 2% alert threshold


# Email configuration
sender_email = "xyz@gmail.com"
receiver_email = "abc@gmail.com"
password = "APP Password"

def send_email(prices_diff):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = "Price difference for the following coins is above 2%:\n\n"
    for symbol, diff in prices_diff.items():
        binance_price = diff["binance_price"]
        kraken_price = diff["kraken_price"]
        price_diff = diff["price_diff"]
        message += f"{symbol}: Binance Price = {binance_price}, Kraken Price = {kraken_price}, Diff = {price_diff:.2f}%\n"
    subject = f"Binance - Kraken | Crypto Price Alert! - {current_time}"
    body = f"Subject: {subject}\n\n{message}"
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, body)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

while True:
    binance_prices = requests.get(binance_api_url).json()
    kraken_prices = requests.get(kraken_api_url).json()
    
    prices_diff = {}
    
    for symbol in binance_prices:
        binance_price = float(symbol["price"])
        kraken_symbol = (symbol["symbol"].replace("USDT", "") + "USD").upper() # Convert to uppercase and to Kraken format
        
        if kraken_symbol in kraken_prices["result"]:
            kraken_price = float(kraken_prices["result"][kraken_symbol]["c"][0])
            
            if binance_price == 0 or kraken_price == 0:
                continue
                
            price_diff = abs((binance_price - kraken_price) / binance_price)

            if price_diff > alert_threshold:
                prices_diff[symbol["symbol"]] = {"binance_price": binance_price, "kraken_price": kraken_price, "price_diff": round(price_diff*100,4)}
            
            if price_diff > 0.02:
    # If it is, print the results in red
                print(f"\033[31m{symbol['symbol']}: Binance price = {binance_price}, Kraken price = {kraken_price}, Diff = {round(price_diff*100,4)}%\033[0m")
            else:
    # If it is not, print the results normally
                print(f"{symbol['symbol']}: Binance price = {binance_price}, Kraken price = {kraken_price}, Diff = {round(price_diff*100,4)}%")

    if prices_diff:
        send_email(prices_diff)

    time.sleep(10)