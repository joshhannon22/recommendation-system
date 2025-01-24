from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv
import os
import requests

def main():
    load_dotenv()
    fred_key = os.getenv("FRED_KEY")
    serper_key = os.getenv("SERPER_KEY")
    get_econ_data(key=fred_key)
    
    # Search for articles about GDP and Inflation
    queries = [
        "GDP growth trends 2024",
        "Inflation impact on economy",
        "US unemployment rate analysis",
        "Interest rate trends and forecasts",
        "Consumer spending and retail sales"
    ]
    articles = {}
    for query in queries:
        print(f"Searching for: {query}")
        results = get_econ_articles(key=serper_key,query=query,num_results=10)
        articles[query] = results['organic']
    
    # Extract relevant data and save to file
    for query, results in articles.items():
        print(f"\nArticles for '{query}':")
        for article in results:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}\n")
            
    breakpoint()
    print("Done")

def get_econ_data(key: str):
    fred = Fred(api_key=key)
    # List of key economic indicators
    indicators = {
        "GDP": "GDP",  # Gross Domestic Product
        "Inflation": "CPIAUCSL",  # Consumer Price Index (All Urban Consumers)
        "Unemployment Rate": "UNRATE",  # Unemployment Rate
        "Interest Rate": "FEDFUNDS",  # Federal Funds Rate
        "Retail Sales": "RSXFS"  # Retail and Food Services Sales
    }

    # Fetch data for each indicator
    data_frames = {}
    for name, series_id in indicators.items():
        print(f"Fetching {name} data...")
        data = fred.get_series(series_id)
        data_frames[name] = data

    # Combine data into a single DataFrame
    df = pd.DataFrame(data_frames)
    df.index = pd.to_datetime(df.index)  # Ensure index is a datetime
    df.sort_index(inplace=True)

    # return data
    return df

def get_econ_articles(key: str, query: str, num_results: int):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": key}
    payload = {
        "q": query,
        "num": num_results
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

if __name__ == "__main__":
    main()