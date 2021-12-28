# Downlaod market data from yahoo finance

import yfinance as yf
import pandas as pd
import yahooquery as yq
import warnings


def get_yfinance_ticker(query, preferred_exchange="AMS"):
    data = yq.search(query)
    quotes = data["quotes"]
    if len(quotes) == 0:
        warnings.warn(f"Yahoo Finance Ticker not found for Portu Name {query}")
        return "No Symbol Found"

    symbol = quotes[0]["symbol"]
    # print(f"{query}:{[quote['exchange'] for quote in quotes]}")
    for quote in quotes:
        if quote["exchange"] == preferred_exchange:
            symbol = quote["symbol"]
            break
    return symbol


def get_correct_portu_names():
    return {
        "iShares Core S&P 500 EUR Hedged UCITS ETF (Acc)": "iShares VII Public Limited Company - iShares Core S&P 500 UCITS ETF",
        "iShares USD Treasury Bond 20+y UCITS ETF": "iShares IV Public Limited Company - iShares $ Treasury Bond 20+yr UCITS ETF",
        "iShares J.P. Morgan USD EM Bond UCITS ETF": "iShares II Public Limited Company - iShares J.P. Morgan $ Emerging Markets Bond UCITS ETF",
        "iShares Electric Vehicles and Driving Technology UCITS ETF": "IShares Trust - Electric Vehicle Driving Technology UCITS Fund",
        "iShares Edge MSCI Europe Multifactor UCITS ETF EUR (Acc)": "iShares IV Public Limited Company - iShares Edge MSCI Europe Multifactor UCITS ETF",
        "WOOD&Co All Weather dluh. fond": "WOOD&Co All Weather dluh. fond",
        "iShares Core Global Aggregate Bond UCITS ETF": "iShares III Public Limited Company - iShares Global Aggregate Bond UCITS ETF",
        "iShares Global Inflation Linked Govt Bond UCITS ETF": "iShares III Public Limited Company - iShares Global Inflation Linked Government Bond UCITS ETF",
        "X-TRACKERS MSCI Japan EUR Hedged UCITS ETF": "Xtrackers MSCI Japan UCITS ETF 4C EUR Hedged",
        "UBS ETFs plc - CMCI Composite SF UCITS ETF": "UBS (Irl) Fund Solutions plc - CMCI Composite SF UCITS ETF",
        "iShares USD Treasury Bond 1-3yr UCITS ETF": "iShares Public Limited Company - iShares $ Treasury Bond 1-3yr UCITS ETF",
        "UBS ETF - MSCI Emerging Markets Socially Responsible UCITS ETF": "UBS ETF SICAV - MSCI Emerging Markets Socially Responsible UCITS ETF",
        "UBS ETF-MSCI World Socially Responsible UCITS ETF": "UBS (Lux) Fund Solutions - MSCI World Socially Responsible UCITS ETF",
    }


def download_market_data(tickers):
    data = yf.download(tickers=tickers, interval="1d", period="max", group_by="ticker")
    data = data.stack()
    return data


if __name__ == "__main__":
    # Load dataframe with information from Portu
    etf_df = pd.read_csv("Portu_ETF_list.csv")

    # Correct portu names
    etf_df = etf_df.replace({"Instrument": get_correct_portu_names()})

    # For each Intstrument in etf_df, find its yahoofinance ticker
    print("Obtaining Yahoo finance tickers for Portu Instruments...")
    etf_df["yfinance_ticker"] = etf_df.apply(
        lambda x: get_yfinance_ticker(x["Instrument"]), axis=1
    )
    tickers = list(etf_df.yfinance_ticker.values)
    successful_tickers = [ticker for ticker in tickers if ticker != "No Symbol Found"]

    # Download market data from yfinance
    print("Downloading market data from Yahoofinance...")
    market_data = download_market_data(tickers=successful_tickers)
    market_data.to_csv("downloaded/market_data.csv")
