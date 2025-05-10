# co2_eda.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Seaborn style
sns.set(style="whitegrid")
import requests
from io import StringIO

def load_data(from_url=True, local_path="data/annual-co2-emissions.csv"):
    if from_url:
        print("Loading data from URL...")
        url = "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv?v=1&csvType=full&useColumnShortNames=true"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Perform the request
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Read the CSV data into a pandas DataFrame
            df = pd.read_csv(StringIO(response.text))
            
            # Save a local copy
            os.makedirs("data", exist_ok=True)
            df.to_csv(local_path, index=False)
            print("Data loaded and saved successfully!")
        else:
            print(f"Failed to retrieve data, HTTP Status Code: {response.status_code}")
            df = None
    else:
        print("Loading data from local file...")
        df = pd.read_csv(local_path)
    
    return df

def basic_exploration(df):
    print("\n=== Data Head ===")
    print(df.head())

    print("\n=== Info ===")
    print(df.info())

    print("\n=== Description ===")
    print(df.describe())

    print("\n=== Missing Values ===")
    print(df.isnull().sum())

def plot_emissions(df, countries):
    df_filtered = df[df['Entity'].isin(countries)]

    plt.figure(figsize=(12, 6))
    for country in countries:
        country_data = df_filtered[df_filtered['Entity'] == country]
        plt.plot(country_data['Year'], country_data['emissions_total'], label=country)  # Corrected column name

    plt.title("Annual CO₂ Emissions by Country")
    plt.xlabel("Year")
    plt.ylabel("Emissions (tonnes)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("co2_emissions_plot.png")  # Save the plot
    plt.show()

def main():
    # Step 1: Load the data
    df = load_data(from_url=True)

    # Step 2: Basic exploration
    basic_exploration(df)

    # Step 3: Plot emissions for selected countries
    top_countries = ['India', 'China', 'United States', 'Germany', 'Russia']
    plot_emissions(df, top_countries)

if __name__ == "__main__":
    main()
