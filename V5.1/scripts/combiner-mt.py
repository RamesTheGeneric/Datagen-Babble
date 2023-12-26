import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor

# Specify the directory containing your CSV files
input_directory = 'C://Users//epicm//Desktop//csv_dev'

# Specify the name of the output CSV file
output_file = 'combined_blendshapes.csv'

# Initialize an empty list to store all the rows from the CSV files
all_rows = []

def process_csv_file(filename):
    with open(os.path.join(input_directory, filename), 'r') as file:
        print(filename)
        # Read the CSV file using the csv.reader
        csv_reader = csv.reader(file)
        # Skip the header row
        next(csv_reader)
        
        # Append each row to the list of all rows
        return list(csv_reader)

# Using ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor() as executor:
    # Iterate through each CSV file in the directory and process concurrently
    all_rows = list(executor.map(process_csv_file, [filename for filename in os.listdir(input_directory) if filename.endswith('.csv')]))

# Flatten the list of lists
all_rows = [row for sublist in all_rows for row in sublist]

# Write the combined data to the output CSV file
with open(output_file, 'w', newline='', buffering=10000) as outfile:
    csv_writer = csv.writer(outfile)
    
    # Write the header row
    header = [
        "cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight",
        "jawOpen", "jawForward", "jawLeft", "jawRight",
        "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker",
        "mouthLeft", "mouthRight", "mouthRollUpper", "mouthRollLower",
        "mouthShrugUpper", "mouthShrugLower", "mouthClose",
        "mouthSmileLeft", "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight",
        "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", "mouthUpperUpRight",
        "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight",
        "mouthStretchLeft", "mouthStretchRight", "tongueOut", "tongueUp", "tongueDown",
        "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp",
        "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight", "filename"
    ]
    csv_writer.writerow(header)
    
    # Write all the rows from the list to the output file
    csv_writer.writerows(all_rows)

print(f"Combined data written to {output_file}")
