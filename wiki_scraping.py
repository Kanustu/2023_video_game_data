# Import libraries
from functions import data_retrieval, create_csv, create_df, find_rows


# URLs for scraping data
game_ratings_url = 'https://en.wikipedia.org/wiki/2023_in_video_games'
game_highest_selling_url = 'https://en.wikipedia.org/wiki/Best-selling_video_games_in_the_United_States_by_year'

# Retrieve data from the URLs
ratings_soup = data_retrieval(game_ratings_url)
sales_soup = data_retrieval(game_highest_selling_url)

# Find specific tables within the scraped data
ratings_table = ratings_soup.find_all('table')[3]
sales_table = sales_soup.find_all('table')[27]

# Create DataFrames from the tables
ratings_df = create_df(ratings_table)
sales_df = create_df(sales_table)

# Find all rows in the tables
ratings_rows = find_rows(ratings_table)
sales_rows = find_rows(sales_table)

# Iterate through each row in the ratings table
for row in ratings_rows[1:]:
    row_data = row.find_all('td')
    single_row_data = [data.text.strip() for data in row_data]
    # Insert a duplicate of the second element into the third position if necessary
    if len(single_row_data) == 5:
        single_row_data.insert(2, single_row_data[1])
    length = len(ratings_df)
    ratings_df.loc[length] = single_row_data

new_list = []
# Iterate through each row in the sales table
for row in sales_rows[1:]:
    row_data = row.find_all('td')
    single_row_data = [data.text.strip() for data in row_data]
    new_list.append(single_row_data)
    
# Adjust some rows to ensure data consistency
new_list[9].insert(3, new_list[8][3])
new_list[6].insert(3, new_list[5][3])

# Append the rows to the sales DataFrame
for x in new_list:
    length = len(sales_df)
    sales_df.loc[length] = x

# Drop the 'Note' column from the sales DataFrame
sales_df.drop(columns=['Note'], inplace=True)

# Create CSV files from the DataFrames
create_csv(ratings_df, 'top_rated_games_2023')
create_csv(sales_df, 'top_selling_games_2023')
