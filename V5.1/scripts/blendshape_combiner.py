import os
import csv
from concurrent.futures import ThreadPoolExecutor

# Directories containing csv files of each blend file
input_directories = ['C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames', 
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames-LCL',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames-Beard1',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames-Beard2',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames-SkinTone1',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Rames-TonguePuffSuck',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Skyrunner',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Summer',
                     'C://Users//epicm//Desktop//csv_blendshapes//SummerBabble-LCL',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Taco',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Tigs',
                     'C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-TigsHair']

# Specify the name of the output CSV file
output_file = 'BabbleDataset_V5.2_FEB_1_2024.csv'

# Initialize an empty list to store all the rows from the CSV files
all_rows = []

def process_csv_file(directory, filename):
    with open(os.path.join(directory, filename), 'r') as file:
        print(filename)
        # Read the CSV file using the csv.reader
        csv_reader = csv.reader(file)
        
        # Skip the header row if there's data in the file
        next(csv_reader)

        # Append each row to the list of all rows
        return list(csv_reader)


# Using ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor() as executor:
    # Iterate through each CSV file in the directories and process concurrently
    for directory in input_directories:
        all_rows.extend(executor.map(process_csv_file, [directory] * len(os.listdir(directory)), [filename for filename in os.listdir(directory) if filename.endswith('.csv')]))

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
