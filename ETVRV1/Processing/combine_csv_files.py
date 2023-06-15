import os

# Path to subdirectory containing text files
path_to_files = "eyecsv"

# Output file name
output_file = "ETVR_Landmarks_L.csv"

# Header row
header = str(['LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 
'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 
'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 
'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y', 'LM_X', 'LM_Y',  'filename'])
header = header.replace("'", "")
header = header.replace("[", "")
header = header.replace("]", "")
header = header.replace(' ', "")

count = 0
# Open output file for writing and write header row

with open(output_file, "w", buffering=10000) as outfile:
    outfile.write(header)
    # Loop over all files in subdirectory
    for filename in os.listdir(path_to_files):
        # Only process files with .csv extension
        if filename.endswith("L.csv"):
            with open(os.path.join(path_to_files, filename), "r") as infile:
                # Read data from input file and write to output file
                contents = infile.read()

                if count == 0:
                    outfile.write(f"\n{contents}\n")
                else:
                    outfile.write(f"{contents}\n")
                print(f"Combined {count} files!")
                count += 1
