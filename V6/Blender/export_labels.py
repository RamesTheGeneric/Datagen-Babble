import bpy, os, bmesh, csv
from bpy_extras.object_utils import world_to_camera_view
import time
from copy import deepcopy

OBJ = bpy.data.objects['generic_neutral_mesh']                                      # The blender object we're targeting
OUTPUT_PATH = "C://Users//epicm//OneDrive//Desktop//BabbleDatasetV6Dev//csv_dev//"  # Path where the CSV file will be saved to
OUTPUT_FILENAME = os.path.splitext(bpy.path.basename(bpy.data.filepath))[0]         # Name of the output CSV file
RENDER_PATH = "BabbleICT-1/"                                                        # Reletive file path of the rendered images
FILENAME = "Babble-ICT_"                                                            # Name of the images minus the suffex and extension

SCENE = bpy.context.scene

FRAME_START = bpy.context.scene.frame_start
FRAME_END = bpy.context.scene.frame_end

SHAPE_INDEX = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
"mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
"mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
"mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
"mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight"]

VERTEX_LIST = [
1225, 1888, 1052, 367, 1719, 1722, 2199, 1447, 966, 3661, 4390, 3927, 3924, 2608, 3272, 4088, 3443, 268, 493, 1914, 2044, 1401, 3615, 4240, 4114, 2734, 2509, 978, 4527, 4942, 4857, 1140, 2075, 1147, 4269, 3360, 1507, 1542, 1537, 1528, 1518, 1511, 3742, 3751, 3756, 3721, 3725, 3732, 5708, 5695, 2081, 0, 4275, 6200, 6213, 6346, 6461, 5518, 5957, 5841, 5702, 5711, 5533, 6216, 6207, 6470, 5517, 5966
]  # Replace with the vertex indices you want to select

possible_suffix = ["VIVE_B_L", "VIVE_B_M", "VIVE_B_R", "VIVE_M_L", "VIVE_M_M", "VIVE_M_R", "VIVE_T_L", "VIVE_T_M", "VIVE_T_R", "OMNICEPT_M_L", "OMNICEPT_M_M", "OMNICEPT_M_R"]
suffix_list = []
for i, suffix in enumerate(possible_suffix):
    if bpy.context.scene.render.views[suffix].use == True:
        suffix_list.append(suffix) 
print(f'suffix_list: {suffix_list}')

# Use bmesh to make a separate mesh of landmarks to make calc_bmesh faster

def generate_3d_landmarks(length):
    fields = []
    for i in range(length):
        fields.append(f'X{i}')
        fields.append(f'Y{i}')
        fields.append(f'Z{i}')
    fields.append('filename')
    fields = ','.join(map(str, fields)) 
    return str(fields)

def calc_bmesh():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(OBJ, depsgraph) 
    bm.verts.ensure_lookup_table()
    return bm

def get_camera_3d_coords(camera, frame, updated_bmesh):
    bm = updated_bmesh
    #print(f"frame {frame} out of {FRAME_END}")
    cam = bpy.data.objects[f"Camera_{camera}"]
    landmarks = []
    for value in VERTEX_LIST:
        vert = bm.verts[value]
        vert.select = True
        co = OBJ.matrix_world @ vert.co
        coords = world_to_camera_view(SCENE, cam, co)
        coord = [coords.x, coords.y, coords.z]
        for i in range(len(coord)):
            coord[i] = max(min(coord[i], 1), 0)
        landmarks.extend(coord)
    return landmarks

shape_keys = OBJ.data.shape_keys.key_blocks

with open(OUTPUT_PATH + OUTPUT_FILENAME + ".csv", 'w') as file:
    labels = ','.join(map(str, SHAPE_INDEX)) 
    file.write(labels + "," + generate_3d_landmarks(len(VERTEX_LIST)) + '\n')
    
    
    # Initialize Time Estimation Vars
    start_time = time.time()
    frames_processed = 0
    for frame in range(FRAME_START, FRAME_END + 1):
        if frames_processed == 0: 
            start_time = time.time()
            #print(f"Start Time {start_time}")
        frames_processed += 1
        if frames_processed == 1000: 
            elapsed_time = (end_time - start_time)/1000                      # Estimate time to compleation
            seconds_left = (FRAME_END - frame)*elapsed_time
            minutes = seconds_left // 60
            hours = minutes // 60
            frames_processed = 0
            print(f"{seconds_left} Seconds Left")
            print(f"{minutes} Minutes Left")
            print(f"{hours} Hours Left")

        bpy.context.scene.frame_set(frame)
        shapes = []
        for key in SHAPE_INDEX:   
            shapes.append(shape_keys.get(key).value)
        updated_bmesh = calc_bmesh()    # Very slow: Copies the mesh's curent vertex positions into python bmesh format so we can read them. 
        for suffix in suffix_list: 
            export_shapes = deepcopy(shapes)
            export_coords = get_camera_3d_coords(suffix, frame, updated_bmesh)
            export_coords.append(RENDER_PATH+(str(f"{FILENAME}{str(frame).zfill(4)}_{suffix}.png")))
            joined_string = ','.join(map(str, export_shapes + export_coords))
            file.write(joined_string + '\n')
        end_time = time.time()

