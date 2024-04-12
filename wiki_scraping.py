#Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests

game_ratings_url = 'https://en.wikipedia.org/wiki/2023_in_video_games'
game_highest_selling_url = 'https://en.wikipedia.org/wiki/Best-selling_video_games_in_the_United_States_by_year'

def data_retrieval(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

def create_df(table):
    header = table.find_all('th')
    titles = [title.text.strip() for title in header]
    df = pd.DataFrame(columns = titles)
    return df

def find_rows(table):
    return table.find_all('tr')

def create_csv(data, title):
    data.to_csv(f'{title}.csv', index=False)


ratings_soup = data_retrieval(game_ratings_url)
sales_soup = data_retrieval(game_highest_selling_url)

# Find the specific tables wanted
ratings_table = ratings_soup.find_all('table')[3]
sales_table = sales_soup.find_all('table')[27]

# Create Dataframe from tables
ratings_df = create_df(ratings_table)
sales_df = create_df(sales_table)

ratings_rows = find_rows(ratings_table)
sales_rows = find_rows(sales_table)

# Iterate through each row in the data_rows list, starting from the second row (index 1)
for row in ratings_rows[1:]:
    # Extract all the 'td' elements from the current row
    row_data = row.find_all('td')
    
    # Extract the text from each 'td' element, stripping any leading or trailing whitespace
    single_row_data = [data.text.strip() for data in row_data]
    # Some games have the same publisher/developer but that is not reflected in the data that was scraped, so a duplicate
    # of position 1 needs to be inserted into position 2
    # Check if the length of single_row_data is 5 (indicating there are 5 elements in the row)
    if len(single_row_data) == 5:
        # Insert a duplicate of the second element into the third position
        single_row_data.insert(2, single_row_data[1])
    length = len(ratings_df)
    ratings_df.loc[length] = single_row_data

new_list = []
for row in sales_rows[1:]:
    row_data = row.find_all('td')
    single_row_data = [data.text.strip()for data in row_data]
    new_list.append(single_row_data)
    
new_list[9].insert(3, new_list[8][3])
new_list[6].insert(3, new_list[5][3])

for x in new_list:
    length = len(sales_df)
    sales_df.loc[length] = x
sales_df.drop(columns=['Note'], inplace = True)

create_csv(ratings_df, 'top_rated_games_2023')
create_csv(sales_df, 'top_selling_games_2023')