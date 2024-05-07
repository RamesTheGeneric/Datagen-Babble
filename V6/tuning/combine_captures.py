import os
import pandas as pd

# Set the directory containing your CSV files
directory = 'W:\RamesTheGeneric\Projects\BabbleTuning2.0'

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read each CSV file into a DataFrame
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames in the list into one DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Optionally, you can write the combined DataFrame to a new CSV file
savepath = 'C://Users//epicm//OneDrive//Desktop//BabbleDatasetV6Dev//csv_dev//Footage-Rames-V2.csv'
combined_df.to_csv(savepath, index=False)
