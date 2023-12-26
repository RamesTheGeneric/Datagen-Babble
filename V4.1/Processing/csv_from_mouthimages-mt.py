import os
from PIL import Image
import os
import multiprocessing
from PIL import Image

# Path to directory containing images
path_to_files = "C:/Users/epicm/Desktop/SummerP4/render/"

# Output file name
output_file = "Babble_data.csv"

# Header row
header = str(["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
    "mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
    "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
    "mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
    "mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight", "filename"])
header = header.replace("'", "")
header = header.replace("[", "")
header = header.replace("]", "")
header = header.replace(' ', "")


# Open output file for writing and write header row

shape_index = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
"mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
"mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
"mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
"mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight"]

ed = EncodeDecode()
shape_defs = dict(              # 31 shapes
    cheekPuffLeft = [],
    cheekPuffRight = [],
    cheekSuckLeft = [], 
    cheekSuckRight = [],
    jawOpen = [],
    jawForward = [],     # added
    jawLeft = [],     # added
    jawRight = [],     # added
    noseSneerLeft = [], # added
    noseSneerRight = [], # added
    mouthFunnel = [],     # added
    mouthPucker = [], # fixed in vrcft master
    mouthLeft = [],     # added
    mouthRight = [],     # added
    mouthRollUpper = [],     # fixed in vrcft master
    mouthRollLower = [],     # fixed in vrcft master
    mouthShrugUpper = [],     # added
    mouthShrugLower = [],     # added
    mouthClose = [],             # MUST BE EQUAL TO jawOpen
    mouthSmileLeft = [],     # added
    mouthSmileRight = [],    # added
    mouthFrownLeft = [],     # added
    mouthFrownRight = [],     # added
    mouthDimpleLeft = [],   # added
    mouthDimpleRight = [],      # added
    mouthUpperUpLeft = [],      # added		
    mouthUpperUpRight = [],      # added
    mouthLowerDownLeft = [], 	 # added	
    mouthLowerDownRight = [],      # added
    mouthPressLeft = [],      # added
    mouthPressRight = [],      # added
    mouthStretchLeft = [],     # added
    mouthStretchRight = [],    # added
    tongueOut = [],
    tongueUp = [],
    tongueDown = [],
    tongueLeft = [],
    tongueRight = [],
    tongueRoll = [],
    tongueBendDown = [],
    tongueCurlUp = [],
    tongueSquish = [],
    tongueFlat = [],
    tongueTwistLeft = [],
    tongueTwistRight = [],
    filename = []
)

def process_file(filename):
    #print(filename)
    ed = EncodeDecode()
    img = Image.open(path_to_files + filename)
    data = get_shapes(ed, img)
    data.append(path_to_files + filename)
    data = str(data)
    data = data.replace("'", "")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace(' ', "")
    return data

if __name__ == '__main__':
    # Get the list of files to process
    files = [filename for filename in os.listdir(path_to_files) if filename.endswith(".png")]

    # Set the number of processes to use
    num_processes = multiprocessing.cpu_count()

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Process the files using the pool of processes
    results = pool.map(process_file, files)

    # Open output file for writing and write the results
    with open(output_file, "w", buffering=10000) as outfile:
        outfile.write(header)
        for count, data in enumerate(results):
            if count == 0:
                outfile.write(f"\n{data}\n")
            else:
                outfile.write(f"{data}\n")
            print(f"Combined {count} files!")