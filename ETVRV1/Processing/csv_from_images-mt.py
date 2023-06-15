import os
from PIL import Image
import os
import multiprocessing
from PIL import Image

class EncodeDecode():
    def float_to_uint24(self, f):
        f = round(f, 8)
        f_clamped = max(0, min(1, f))
        uint24 = int(f_clamped * ((1 << 24) - 1))
        return uint24
    
    def uint24_to_float(self, uint24):
        f = uint24 / ((1 << 24) - 1)
        return f

    def encode(self, f, index):  # uint24 to blender pixel (1.0, 1.0, 1.0) 
        hex_str = format(f, '06x')
        hex_str = list(hex_str.strip(" "))
        #print(hex_str)
        #bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[index].default_value = ((int('0x' + hex_str[0] + hex_str[1], 0) / 255),(int('0x' + hex_str[2] + hex_str[3], 0) / 255),(int('0x' + hex_str[4] + hex_str[5], 0) / 255),1)
        return ((int('0x' + hex_str[0] + hex_str[1], 0) / 255),(int('0x' + hex_str[2] + hex_str[3], 0) / 255),(int('0x' + hex_str[4] + hex_str[5], 0) / 255),1)

    def decode(self, pixel):    # Pixel to uint24 (255, 255, 255)
        output_hex = ('0x' + hex(pixel[0]).replace('0x', '').rjust(2, "0") + hex(pixel[1]).replace('0x', '').rjust(2, "0") + hex(pixel[2]).replace('0x', '').rjust(2, "0"))
        output_hex = int(output_hex, 0)
        return(output_hex)

# Path to directory containing images
path_to_files = "C:/Users/epicm/Desktop/BabbleTraining/eyeimages/"

# Output file name
output_file = "ETVR_Shapes.csv"

# Header row
header = str(['EyeLookOutRight', 'EyeLookInRight', 'EyeLookUpRight', 'EyeLookDownRight', 'EyeLookOutLeft', 'EyeLookInLeft', 'EyeLookUpLeft', 'EyeLookDownLeft', 'EyeClosedRight', 'EyeClosedLeft', 'EyeSquintRight', 'EyeSquintLeft', 
    'EyeWideRight', 'EyeWideLeft', 'EyeDilationRight', 'EyeDilationLeft', 'EyeConstrictRight', 'EyeConstrictLeft', 'BrowPinchRight', 'BrowPinchLeft', 'BrowLowererRight', 'BrowLowererLeft', 'BrowInnerUpRight', 'BrowInnerUpLeft', 
    'BrowOuterUpRight', 'BrowOuterUpLeft'])
header = header.replace("'", "")
header = header.replace("[", "")
header = header.replace("]", "")
header = header.replace(' ', "")


# Open output file for writing and write header row

shape_index = ['EyeLookOutRight', 'EyeLookInRight', 'EyeLookUpRight', 'EyeLookDownRight', 'EyeLookOutLeft', 'EyeLookInLeft', 'EyeLookUpLeft', 'EyeLookDownLeft', 'EyeClosedRight', 'EyeClosedLeft', 'EyeSquintRight', 'EyeSquintLeft', 
    'EyeWideRight', 'EyeWideLeft', 'EyeDilationRight', 'EyeDilationLeft', 'EyeConstrictRight', 'EyeConstrictLeft', 'BrowPinchRight', 'BrowPinchLeft', 'BrowLowererRight', 'BrowLowererLeft', 'BrowInnerUpRight', 'BrowInnerUpLeft', 
    'BrowOuterUpRight', 'BrowOuterUpLeft']

def get_shapes(ed, img):    
    px = img.load()
    output = ed.decode(px[0, 256])  # Shape count
    shapes = []
    for i in range(output):
        uint = ed.decode(px[(i + 1), 256])  # Skip the bottom left pixel because it's a uint24 of the shape count
        shapes.append(ed.uint24_to_float(uint))
    return shapes

ed = EncodeDecode()
shape_defs = dict(              # 31 shapes
    EyeLookOutRight = [],
    EyeLookInRight = [],
    EyeLookUpRight = [],
    EyeLookDownRight = [],
    EyeLookOutLeft = [],
    EyeLookInLeft = [],
    EyeLookUpLeft = [],
    EyeLookDownLeft = [],
    EyeClosedRight = [],
    EyeClosedLeft = [],
    EyeSquintRight = [],
    EyeSquintLeft = [],
    EyeWideRight = [],
    EyeWideLeft = [],
    EyeDilationRight = [],
    EyeDilationLeft = [],
    EyeConstrictRight = [],
    EyeConstrictLeft = [],
    BrowPinchRight = [],
    BrowPinchLeft = [],
    BrowLowererRight = [],
    BrowLowererLeft = [],
    BrowInnerUpRight = [],
    BrowInnerUpLeft = [],
    BrowOuterUpRight = [],
    BrowOuterUpLeft = [],
    filename = []
)

def process_file(filename):
    ed = EncodeDecode()
    img = Image.open(path_to_files + filename)
    data = get_shapes(ed, img)
    data.append(path_to_files + filename)
    data = str(data)
    data = data.replace("_L.png", ".png")
    data = data.replace("'", "")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace(' ', "")
    return data

if __name__ == '__main__':
    # Get the list of files to process
    files = [filename for filename in os.listdir(path_to_files) if filename.endswith("_L.png")]

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