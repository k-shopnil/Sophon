import yfinance as yf

def get_current_stock_price(ticker):
    
    stock_data = yf.Ticker(ticker)
    company_name = stock_data.info['longName']
    current_price = stock_data.history(period='1d')['Close'].iloc[-1]
    return current_price, company_name

# if __name__ == "__main__":
#     #for debugging purposes
#     ticker = input()
#     current_price,company_name = get_current_stock_price(ticker)
    

