import os
import pandas as pd

# Specify the directory where your CSV files are located
directory = 'C://Users//epicm//Desktop//csv_dev//'
directory = 'Z://BabbleDataGeneration//BabbleDataGeneration//Humans 5.0//avatars//lipimages'

# List all CSV files in the specified directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through each CSV file and append its data to the combined_data DataFrame
for file in csv_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    combined_data = combined_data.append(df, ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv('combined_landmarks.csv', index=False)
