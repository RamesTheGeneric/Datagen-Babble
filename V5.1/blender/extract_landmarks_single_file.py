import bpy, os, bmesh, csv
from bpy_extras.object_utils import world_to_camera_view

FRAME_START = bpy.context.scene.frame_start
FRAME_END = bpy.context.scene.frame_end

vertex_list = [
    6130, 4928, 5945, 66, 2931, 1906, 3118, 1740, 2471, 68, 5493, 4762,
    5023, 5039, 132, 2017, 2003, 1996, 103, 5018,
    5560, 140, 2538,
    6122, 6023, 6006, 6037, 6618, 3773, 5726,# Right Cheek
    1110, 3008, 2990, 3022, 434, 2655, 2704, # Left Cheek
    4204, 127, 1182,
    9725, 9694, 9697,
]  # Replace with the vertex indices you want to select

# List to collect all the data
all_data = []

scene = bpy.context.scene

obj = bpy.data.objects['BabbleColinFace']

def get_camera_2d_coords(camera, suffex, frame):
    print(f"frame {frame} out of {FRAME_END}")
    cam = bpy.data.objects[camera]
    bpy.context.scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(obj, depsgraph)
    bm.verts.ensure_lookup_table()
    landmarks = []

    for value in vertex_list:
        vert = bm.verts[value]
        vert.select = True
        co = obj.matrix_world @ vert.co
        coords2d = world_to_camera_view(scene, cam, co)
        coord = [coords2d.x, coords2d.y]
        for i in range(len(coord)):
            coord[i] = max(min(coord[i], 1), 0)
        landmarks.extend(coord)

    filename = bpy.path.basename(bpy.data.filepath)
    filename = os.path.splitext(filename)[0]
    filename = 'RenderSceneV5-Babble-Summer/SummerBabble' + ("{:04d}".format(frame)) + suffex
    landmarks.append(filename)
    all_data.append(landmarks)

for frame in range(FRAME_START, FRAME_END + 1):
    get_camera_2d_coords("Camera_VIVE_M_M", "_VIVE_M_M.png", frame)
    get_camera_2d_coords("Camera_VIVE_M_L", "_VIVE_M_L.png", frame)
    get_camera_2d_coords("Camera_VIVE_M_R", "_VIVE_M_R.png", frame)
    get_camera_2d_coords("Camera_VIVE_T_M", "_VIVE_T_M.png", frame)
    get_camera_2d_coords("Camera_VIVE_B_M", "_VIVE_B_M.png", frame)
# Specify the output CSV file
csvfilename = 'SummerBabble_combined_landmarks.csv'
output_file = bpy.path.abspath("//" + 'lipimages' + "/" + csvfilename)

# Write all the collected data to a single CSV file
with open(output_file, 'w', newline='') as csv_output:
    writer = csv.writer(csv_output)

    # Write a header row if needed
    writer.writerow(['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8', 'X9', 'Y9', 'X10', 'Y10',
    'X11', 'Y11', 'X12', 'Y12', 'X13', 'Y13', 'X14', 'Y14', 'X15', 'Y15', 'X16', 'Y16', 'X17', 'Y17', 'X18', 'Y18', 'X19', 'Y19', 'X20', 'Y20', 
    'X21', 'Y21', 'X22', 'Y22', 'X23', 'Y23', 'X24', 'Y24', 'X25', 'Y25', 'X26', 'Y26', 'X27', 'Y27', 'X28', 'Y28', 'X29', 'Y29', 'X30', 'Y30', 
    'X31', 'Y31', 'X32', 'Y32', 'X33', 'Y33', 'X34', 'Y34','X35', 'Y35', 'X36', 'Y36','X37', 'Y37','X38', 'Y38','X39', 'Y39', 'X40', 'Y40',
    'X41', 'Y41', 'X42', 'Y42','X43', 'Y43',"filename"])  # Include all column headers

    # Write each set of data
    for data in all_data:
        writer.writerow(data)

print(f'All data saved to {output_file}')
