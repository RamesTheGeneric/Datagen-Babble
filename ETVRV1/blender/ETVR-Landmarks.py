import bpy, sys, os, getopt, bmesh
from bpy_extras.object_utils import world_to_camera_view

FRAME_START = bpy.context.scene.frame_start
FRAME_END = bpy.context.scene.frame_end


vertex_list_L = [69631, 69629, 55208, 69627, 69625, 44637, 69642, 37302, 69633, 41122, 55202, 37293, 69621, 37877, 69634, 69635, 55887, 54615, 69619, 69622, 43026, 69623, 42545, 55224, 43809, 55225, 44224, 69626, 44164, 69628, 38676, 42432, 38738, 69632, 
675, 703, 728, 771, 800, 828, 625, 651, 
847, 876, 879, 851, 885, 882, 856, 873]

vertex_list_R = [69656, 69654, 68725, 69652, 69650, 42586, 69649, 40760, 69658, 45487, 68719, 45268, 69646, 44586, 69659, 69660, 68492, 68169, 69644, 69647, 50707, 69648, 50636, 68741, 51871, 68742, 42169, 69651, 43069, 69653, 43272, 51539, 40983, 69657, 
6627, 6655, 6680, 6723, 6752, 6780, 6577, 6603, 
6799, 6828, 6831, 6803, 6837, 6834, 6808, 6825]
 # Dlib Landmarks 49-68

scene = bpy.context.scene
lc = bpy.data.objects['DollyCamera_L'] 
rc = bpy.data.objects['DollyCamera_R'] 
...
obj = bpy.data.objects['BabbleCA_M']
print("Working on object: %s" % obj.name)
for frame in range(FRAME_START, FRAME_END+1):
    bpy.context.scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()

    obj = bpy.data.objects['BabbleCA_M']

    bm = bmesh.new()

    bm.from_object( obj, depsgraph )

    bm.verts.ensure_lookup_table()
    landmarks = []
    for value in vertex_list_L:
        vert = bm.verts[value]
        vert.select = True
        # local to global coordinates
        co = obj.matrix_world @ vert.co
        #co = obj.evaluated_get(context.view_layer.depsgraph).data.vertices[0].co
        print(co)
        coords2d = world_to_camera_view(scene, lc, co) 
        coord = [coords2d.x, coords2d.y]
        for i in range(len(coord)):            # Clip values between 0 - 1
            coord[i] = max(min(coord[i], 1), 0) 
        landmarks.append(coord)
        #print(coord) 
        #print("coords2d: {},{}".format(coords2d.x, coords2d.y))
    print(landmarks) 
    filename = bpy.path.basename(bpy.data.filepath)
    filename = os.path.splitext(filename)[0]
    filename = 'ETVR_Eye_CA_M_' + str(frame).rjust(4, '0') + "_L"
    csvfilename = filename + '.csv'
    pngfilename = filename + '.png'

    if not os.path.exists(bpy.path.abspath("//" + 'eyecsv')):
        os.makedirs(bpy.path.abspath("//" + 'eyecsv'))
    csvfilepath = bpy.path.abspath("//" + 'eyecsv' + "/" + csvfilename)
    pngfilepath = bpy.path.abspath("//" + 'eyeimages' + "/" + pngfilename)
    csvimagepath = ('eyeimages' + '/' + pngfilename)
    landmarks.append(csvimagepath)
    joined_string = ','.join(map(str, landmarks)) 
    joined_string = joined_string.replace("[", "")
    joined_string = joined_string.replace("]", "")
    with open(csvfilepath, 'w') as file:
        file.write(joined_string)
        file.close()
    
    depsgraph = bpy.context.evaluated_depsgraph_get()
            
    obj = bpy.data.objects['BabbleCA_M']

    bm = bmesh.new()

    bm.from_object( obj, depsgraph )

    bm.verts.ensure_lookup_table()
    landmarks = []
    for value in vertex_list_R:
        vert = bm.verts[value]
        vert.select = True
        # local to global coordinates
        co = obj.matrix_world @ vert.co
        #co = obj.evaluated_get(context.view_layer.depsgraph).data.vertices[0].co
        print(co)
        coords2d = world_to_camera_view(scene, rc, co) 
        coord = [coords2d.x, coords2d.y]
        for i in range(len(coord)):            # Clip values between 0 - 1
            coord[i] = max(min(coord[i], 1), 0) 
        landmarks.append(coord)
        #print(coord) 
        #print("coords2d: {},{}".format(coords2d.x, coords2d.y))
    print(landmarks) 
    filename = bpy.path.basename(bpy.data.filepath)
    filename = os.path.splitext(filename)[0]
    filename = 'ETVR_Eye_CA_M_' + str(frame).rjust(4, '0') + "_R"
    csvfilename = filename + '.csv'
    pngfilename = filename + '.png'

    if not os.path.exists(bpy.path.abspath("//" + 'eyecsv')):
        os.makedirs(bpy.path.abspath("//" + 'eyecsv'))
    csvfilepath = bpy.path.abspath("//" + 'eyecsv' + "/" + csvfilename)
    pngfilepath = bpy.path.abspath("//" + 'eyeimages' + "/" + pngfilename)
    csvimagepath = ('eyeimages' + '/' + pngfilename)
    landmarks.append(csvimagepath)
    joined_string = ','.join(map(str, landmarks)) 
    joined_string = joined_string.replace("[", "")
    joined_string = joined_string.replace("]", "")
    with open(csvfilepath, 'w') as file:
        file.write(joined_string)
        file.close()