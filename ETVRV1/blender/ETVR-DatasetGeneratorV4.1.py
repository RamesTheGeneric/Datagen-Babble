import bpy
import copy
import random
import os
import time
def get_objs(collection):                   # Returns all meshes in a collection
    collection = bpy.data.collections[collection]
    for obj in collection.all_objects:
        ob = bpy.data.objects[str(obj.name)]
        if ob.type == 'MESH':
            mesh_name = obj.name
            #shapekey_name = shapekey_name.split()
    return mesh_name 

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def zero(ob):
    ob = bpy.data.objects[ob]
    for shape in ob.data.shape_keys.key_blocks:
        shape.value=0
        shape.keyframe_insert(data_path="value", frame=bpy.context.scene.frame_current)

class Defines():
    shape_defs = dict(              # 26 shapes
    EyeLookOutRight = 'EyeLookOutRight',
    EyeLookInRight = 'EyeLookInRight',
    EyeLookUpRight = 'EyeLookUpRight',
    EyeLookDownRight = 'EyeLookDownRight',
    EyeLookOutLeft = 'EyeLookOutLeft',
    EyeLookInLeft = 'EyeLookInLeft',
    EyeLookUpLeft = 'EyeLookUpLeft',
    EyeLookDownLeft = 'EyeLookDownLeft',
    EyeClosedRight = 'Expressions_eyeClosedR_max',
    EyeClosedLeft = 'Expressions_eyeClosedL_max',
    EyeSquintRight = 'Expressions_eyeSquintR_max', 
    EyeSquintLeft = 'Expressions_eyeSquintL_max', 
    EyeWideRight = 'Expressions_eyeClosedR_min',
    EyeWideLeft = 'Expressions_eyeClosedL_min', 
    EyeDilationRight = 'EyeDilationRight',
    EyeDilationLeft = 'EyeDilationLeft',
    EyeConstrictRight = 'EyeConstrictRight',
    EyeConstrictLeft = 'EyeConstrictLeft', 
    BrowPinchRight = 'BrowPinchRight',
    BrowPinchLeft = 'BrowPinchLeft',
    BrowLowererRight = 'BrowLowererRight',
    BrowLowererLeft = 'BrowLowererLeft',
    BrowInnerUpRight = 'BrowInnerUpRight',
    BrowInnerUpLeft = 'BrowInnerUpLeft',
    BrowOuterUpRight = 'Expressions_browOutVertR_max',
    BrowOuterUpLeft = 'Expressions_browOutVertL_max'
    )

    shape_index = ['EyeLookOutRight', 'EyeLookInRight', 'EyeLookUpRight', 'EyeLookDownRight', 'EyeLookOutLeft', 'EyeLookInLeft', 'EyeLookUpLeft', 'EyeLookDownLeft', 'EyeClosedRight', 'EyeClosedLeft', 'EyeSquintRight', 'EyeSquintLeft', 
    'EyeWideRight', 'EyeWideLeft', 'EyeDilationRight', 'EyeDilationLeft', 'EyeConstrictRight', 'EyeConstrictLeft', 'BrowPinchRight', 'BrowPinchLeft', 'BrowLowererRight', 'BrowLowererLeft', 'BrowInnerUpRight', 'BrowInnerUpLeft', 
    'BrowOuterUpRight', 'BrowOuterUpLeft']
    
    exclusives = [            # mark these combinations for special treatment after generating values(combined values, etc...)
        ['NoExclusives'],
                    ]

    shape_bl = dict(  
    EyeLookOutRight = ['EyeLookOutRight', 'EyeLookInRight'],
    EyeLookInRight = ['EyeLookInRight', 'EyeLookOutRight'],
    EyeLookUpRight = ['EyeLookUpRight', 'EyeLookDownRight'],
    EyeLookDownRight = ['EyeLookDownRight', 'EyeLookUpRight'],
    EyeLookOutLeft = ['EyeLookOutLeft', 'EyeLookInLeft'],
    EyeLookInLeft = ['EyeLookInLeft', 'EyeLookOutLeft'],
    EyeLookUpLeft = ['EyeLookUpLeft', 'EyeLookDownLeft'],
    EyeLookDownLeft = ['EyeLookDownLeft', 'EyeLookUpLeft'],
    EyeClosedRight = ['EyeClosedRight', 'EyeSquintRight'],
    EyeClosedLeft = ['EyeClosedLeft' ,'EyeSquintLeft'],
    EyeSquintRight = ['EyeSquintRight', 'EyeClosedRight'], 
    EyeSquintLeft = ['EyeSquintLeft', 'EyeClosedLeft'], 
    EyeWideRight = ['EyeWideRight', 'EyeClosedRight'],
    EyeWideLeft = ['EyeWideLeft', 'EyeClosedLeft'], 
    EyeDilationRight = ['EyeDilationRight', 'EyeConstrictRight'],
    EyeDilationLeft = ['EyeDilationLeft', 'EyeConstrictLeft'],
    EyeConstrictRight = ['EyeConstrictRight', 'EyeDilationRight'],
    EyeConstrictLeft = ['EyeConstrictLeft', 'EyeDilationLeft'],
    BrowPinchRight = ['BrowPinchRight'],
    BrowPinchLeft = ['BrowPinchLeft'],
    BrowLowererRight = ['BrowLowererRight', 'BrowInnerUpRight'],
    BrowLowererLeft = ['BrowLowererLeft', 'BrowInnerUpLeft'],
    BrowInnerUpRight = ['BrowInnerUpRight', 'BrowLowererRight'],
    BrowInnerUpLeft = ['BrowInnerUpLeft', 'BrowLowererLeft'],
    BrowOuterUpRight = ['BrowOuterUpRight'],
    BrowOuterUpLeft = ['BrowOuterUpLeft']
    )

class ShapeSetter():
    def __init__(self):
        self.blacklist = []           
        self.randomized_shapes = []
        self.possible_shapes = []
        self.selected_shapes = []
        self.selected_shapes_index = []
        self.total_shapes = 0
        self.count = 0

    def reset(self, DefsClass):     
        defs = DefsClass
        self.blacklist = []                 
        self.randomized_shapes = []
        self.selected_shapes = []
        self.selected_shapes_index = []
        self.total_shapes = len(defs.shape_defs)
        self.possible_shapes = copy.copy(defs.shape_index)
        
    def convert_to_defined(self, defs):
        defines_list = []
        for i in range(len(self.selected_shapes_index)):
            defines_list.append(defs.shape_defs[self.selected_shapes_index[i]])
        return(defines_list)

    def get_avalible_shapes(self, defs, shape):         # Adds the shape's blacklist to the list and returns the remaining potential shapes
        self.blacklist.append(defs.shape_bl[shape])
        for i in range(len(self.possible_shapes)):   
            for j in range(len(self.blacklist)):
                for k in range(len(self.blacklist[j])):    
                    if self.blacklist[j][k] in self.possible_shapes:
                        self.possible_shapes.pop(self.possible_shapes.index(self.blacklist[j][k]))
        return(self.possible_shapes)
    
    def process_exclusives(self, defs):         
        print('No Exclusives to process')

    def generate_example(self, DefsClass, range, classExample):
        defs = DefsClass
        self.reset(defs)
        if type(classExample) == int: classExample = defs.shape_index[classExample]             # Take either String or int
        if type(classExample) == str: classExample = defs.shape_index[defs.shape_index.index(classExample)]
        self.selected_shapes.append(clamp(random.uniform(range[0], range[1]), 0, 1))
        self.selected_shapes_index.append(classExample)
        shape = random.choice(self.get_avalible_shapes(defs, classExample))  
        while len(self.possible_shapes) > 0:
            if 0.75 >= random.uniform(0,1):     # 75% chance for shape to be set
                self.selected_shapes.append(clamp(random.uniform(-0.1, self.selected_shapes[0] - 0.1), 0, 1))
                self.selected_shapes_index.append(shape)
            try: shape = random.choice(self.get_avalible_shapes(defs, shape))  
            except: break
        self.process_exclusives(defs)
        self.tick()
        return self.selected_shapes, self.convert_to_defined(defs)
    
    def tick(self):
        self.count += 1
        if self.count == self.total_shapes:
            self.count = 0
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
        bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[index].default_value = ((int('0x' + hex_str[0] + hex_str[1], 0) / 255),(int('0x' + hex_str[2] + hex_str[3], 0) / 255),(int('0x' + hex_str[4] + hex_str[5], 0) / 255),1)
        return ((int('0x' + hex_str[0] + hex_str[1], 0) / 255),(int('0x' + hex_str[2] + hex_str[3], 0) / 255),(int('0x' + hex_str[4] + hex_str[5], 0) / 255),1)

    def decode(self, pixel):    # Pixel to uint24 (255, 255, 255)
        output_hex = ('0x' + hex(pixel[0]).replace('0x', '').rjust(2, "0") + hex(pixel[1]).replace('0x', '').rjust(2, "0") + hex(pixel[2]).replace('0x', '').rjust(2, "0"))
        output_hex = int(output_hex, 0)
        return(output_hex)
    
FRAME_START = bpy.context.scene.frame_start
FRAME_END = bpy.context.scene.frame_end

defs = Defines()
ss = ShapeSetter()
encdec = EncodeDecode()
tick = 0
range_select = 0
range_list = [
              [0.6,1.05],
              [0.4, 0.7],
              [-0.2, 0.5]
              ]

mesh = 'BabbleCA_M.003'
ob = bpy.data.objects[mesh]
for frame in range(FRAME_START, FRAME_END+1):   # Iterate over each frame in the range
    model_shapes = []
    print(f"Generated {frame} of {FRAME_END} shapes")
    ob = ob
    if tick == ss.total_shapes:
        tick = 0
        range_select += 1
        if range_select > 2:range_select = 0
    values, names = ss.generate_example(defs, range_list[range_select], defs.shape_index[ss.count])
    bpy.context.scene.frame_set(frame)# Go to the current frame
    zero(mesh)
    shapecount = len(defs.shape_index)  
    for i in range(shapecount):             # Reset compositor data
        encdec.encode(encdec.float_to_uint24(ob.data.shape_keys.key_blocks[defs.shape_defs[defs.shape_index[i]]].value), i + 2)
    for i in range(shapecount):             # Write reset Compositor data
        bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[i + 2].keyframe_insert(data_path="default_value", frame=frame)
    
    for i in range(len(values)):    # Iterate over each shape key   
        ob.data.shape_keys.key_blocks[names[i]].value = values[i]
        key = ob.data.shape_keys.key_blocks[names[i]]
        key.keyframe_insert(data_path="value", frame=frame)
        
    hmd_type = random.randint(0,2)
    # No HMD Randomization
    camera_type = random.randint(0,1)
    # No Camera Swapping
 
    ob = bpy.data.objects[mesh]
    encdec.encode(shapecount, 1)
    bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[1].keyframe_insert(data_path="default_value", frame=frame)
    
    for i in range(shapecount):
        encdec.encode(encdec.float_to_uint24(ob.data.shape_keys.key_blocks[defs.shape_defs[defs.shape_index[i]]].value), i + 2)
    for i in range(shapecount):
        bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[i + 2].keyframe_insert(data_path="default_value", frame=frame)
    tick += 1
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath) # Save file once generation has finished.
