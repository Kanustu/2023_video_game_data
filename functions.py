from bs4 import BeautifulSoup
import pandas as pd
from typing import List
import requests

def data_retrieval(url: str) -> BeautifulSoup:
    """
    Retrieves data from the given URL and returns a BeautifulSoup object.
    """
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

# Function to create a DataFrame from a BeautifulSoup table
def create_df(table: BeautifulSoup) -> pd.DataFrame:
    """
    Creates a DataFrame from the given BeautifulSoup table.
    """
    header = table.find_all('th')
    titles = [title.text.strip() for title in header]
    df = pd.DataFrame(columns=titles)
    return df

# Function to find all rows in a BeautifulSoup table
def find_rows(table: BeautifulSoup) -> List[BeautifulSoup]:
    """
    Finds all rows in the given table.
    """
    return table.find_all('tr')

# Function to create a CSV file from a DataFrame
def create_csv(data: pd.DataFrame, title: str) -> None:
    """
    Creates a CSV file from the given DataFrame.
    """
    data.to_csv(f'{title}.csv', index=False)