import os
import zipfile
import pandas as pd

# Set the Kaggle API credentials file path
kaggle_credentials_path = 'kaggle(1)'

# Set the dataset path
dataset_path = 'london-bike-sharing-dataset.zip'

# Check if the dataset is already downloaded
if not os.path.exists(dataset_path):
    # Download dataset from Kaggle using Kaggle API
    os.system(f'kaggle datasets download -d hmavrodiev/london-bike-sharing-dataset -p {os.path.dirname(__file__)} -c {kaggle_credentials_path}')

    # Extract the file from the downloaded zip file
    with zipfile.ZipFile(dataset_path, 'r') as file:
        file.extractall()

# Assuming the CSV file is inside the extracted folder, specify the correct path
extracted_folder_path = 'london-bike-sharing-dataset/'
csv_file_path = os.path.join(extracted_folder_path, 'london_merged.csv')

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")

# Load the dataset into a Pandas DataFrame
bikes = pd.read_csv(csv_file_path)

# Now explore the data 
bikes.info()

print(bikes.shape)
print(bikes)

# Count the unique values in the weather code column 
print(bikes.weather_code.value_counts())

# Specify the column names I want to use 
new_cols_dict = {
    'timestamp': 'time',
    'cnt': 'count',
    't1': 'temp_real_C',
    't2': 'temp_feels_like_C',
    'hum': 'humidity_percent',
    'wind_speed': "wind_speed_kph",
    'weather_code': 'weather',
    'is_holiday': 'is_holiday',
    'is_weekend': 'is_weekend',
    'season': 'season'
}

# Renaming the columns to my names 
bikes.rename(columns=new_cols_dict, inplace=True)


#changing the humidity values to percentages 
bikes.humidity_percent = bikes.humidity_percent / 100 

#creating a new dictionary so tha we can map the integers 0-3 to their actuat written values 
season_dict ={
    '0.0':'spring',
    '1.0':'summer',
    '2.0':'autumn',
    '3.0':'winter'
}

#creating a weather dictionary so that you can mapthe integers to their actual written values 
weather_dict ={
    '1.0':'Clear',
    '2.0':'Scattered clouds',
    '3,0':'Broken clouds',
    '4.0':'Cloudy',
    '7.0':'Rain',
    '10.0':'Rain with thuderstorm',
    '26.0':'Snowfall'
}

# changing the seasons column data type to string 
bikes.season = bikes.season.astype('str')
# mapping the values 0-3 to the actual written values 
bikes.season = bikes.season.map(season_dict)

#changing the weather column data type to string 
bikes.weather = bikes.weather.astype('str')
#mapping the values to the actual written weathers
bikes.weather =bikes.weather.map(weather_dict)


#checking our data frames to see if our mapping have worked 
# Checking our DataFrame to see if our mapping has worked 
print(bikes.head())

# Writing the final DataFrame to an Excel file that we will use in our Tableau visualizations.
# The file will be named 'london_bikes_final.xlsx'
bikes.to_excel('london_bikes_final(1)', sheet_name='Data', engine='openpyxl')
