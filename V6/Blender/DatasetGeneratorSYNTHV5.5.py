import bpy
import copy
import random
import os
import numpy as np
import time




def set_identity_shapes(interval: int = 1000):
    frames_interval = 1000
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end

    for frame in range(start_frame, end_frame + 1, frames_interval):
        bpy.context.scene.frame_set(frame)
        for i in range(100):  # assuming blend shapes range from 0 to 100
            if random.randint(0,10) == 1:
                blendshape_name = "identity{:03d}".format(i)
                random_value = random.uniform(-6.0, 6.0)  # generate a random value between 0.0 and 1.0
                bpy.data.shape_keys['Key.003'].key_blocks[blendshape_name].value = random_value
                bpy.data.shape_keys['Key.003'].key_blocks[blendshape_name].keyframe_insert(data_path="value")
            else:
                blendshape_name = "identity{:03d}".format(i)
                bpy.data.shape_keys['Key.003'].key_blocks[blendshape_name].value = 0.0
                bpy.data.shape_keys['Key.003'].key_blocks[blendshape_name].keyframe_insert(data_path="value")


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

def add_blendshape_fcurve(ob, shape_name, keyframes):
    
    shape_key = ob.data.shape_keys.key_blocks.get(shape_name)
    if shape_key:
        me = ob.data
        me.shape_keys.animation_data_create()
        action = bpy.data.actions["KeyAction"]
        fc = action.fcurves.new(f'key_blocks["{shape_key.name}"].value')
        fc.keyframe_points.add(count=len(keyframes) // 2)
        fc.keyframe_points.foreach_set("co", keyframes)

class Defines():
    shape_defs = dict(              # 45 shapes
        cheekPuffLeft = 'cheekPuffLeft',
        cheekPuffRight = 'cheekPuffRight',
        cheekSuckLeft = 'cheekSuckLeft', 
        cheekSuckRight = 'cheekSuckRight',
        jawOpen = 'jawOpen',
        jawForward = 'jawForward',     # added
        jawLeft = 'jawLeft',     # added
        jawRight = 'jawRight',     # added
        noseSneerLeft = 'noseSneerLeft', # added
        noseSneerRight = 'noseSneerRight', # added
        mouthFunnel = 'mouthFunnel',     # added
        mouthPucker = 'mouthPucker', # fixed in vrcft master
        mouthLeft = 'mouthLeft',     # added
        mouthRight = 'mouthRight',     # added
        mouthRollUpper = 'mouthRollUpper',     # fixed in vrcft master
        mouthRollLower = 'mouthRollLower',     # fixed in vrcft master
        mouthShrugUpper = 'mouthShrugUpper',     # added
        mouthShrugLower = 'mouthShrugLower',     # added
        mouthClose = 'mouthClose',             # MUST BE EQUAL TO jawOpen
        mouthSmileLeft = 'mouthSmileLeft',     # added
        mouthSmileRight = 'mouthSmileRight',    # added
        mouthFrownLeft = 'mouthFrownLeft',     # added
        mouthFrownRight = 'mouthFrownRight',     # added
        mouthDimpleLeft = 'mouthDimpleLeft',   # added
        mouthDimpleRight = 'mouthDimpleRight',      # added
        mouthUpperUpLeft = 'mouthUpperUpLeft',      # added		
        mouthUpperUpRight = 'mouthUpperUpRight',      # added
        mouthLowerDownLeft = 'mouthLowerDownLeft', 	 # added	
        mouthLowerDownRight = 'mouthLowerDownRight',      # added
        mouthPressLeft = 'mouthPressLeft',      # added
        mouthPressRight = 'mouthPressRight',      # added
        mouthStretchLeft = 'mouthStretchLeft',     # added
        mouthStretchRight = 'mouthStretchRight',    # added
        tongueOut = 'tongueOut',
        tongueUp = 'tongueUp',
        tongueDown = 'tongueDown',
        tongueLeft = 'tongueLeft',
        tongueRight = 'tongueRight',
        tongueRoll = 'tongueRoll',
        tongueBendDown = 'tongueBendDown',
        tongueCurlUp = 'tongueCurlUp',
        tongueSquish = 'tongueSquish',
        tongueFlat = 'tongueFlat',
        tongueTwistLeft = 'tongueTwistLeft',
        tongueTwistRight = 'tongueTwistRight'
    )

    shape_index = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
    "mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
    "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
    "mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
    "mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight"]
    
    exclusives = [            # mark these combinations for special treatment after generating values(combined values, etc...)
        ['mouthClose', 'jawOpen'],
        ['mouthShrugUpper', 'mouthShrugLower'],
        ['tongueOut', 'jawOpen', "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistRight", "tongueTwistLeft"],
        ['mouthSmileLeft', 'mouthSmileRight'],
        ['cheekPuffLeft', 'cheekPuffRight'],
        ['cheekSuckLeft', 'cheekSuckRight']
                    ]

    shape_bl = dict(  
        cheekPuffLeft = ['cheekPuffLeft', 'cheekSuckLeft', 'cheekSuckRight', 'jawOpen', 'mouthFunnel', 'mouthShrugUpper', 'mouthShrugLower', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        cheekPuffRight = ['cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight', 'jawOpen', 'mouthFunnel', 'mouthShrugUpper', 'mouthShrugLower', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        cheekSuckLeft = ['cheekSuckLeft', 'cheekPuffRight', 'cheekPuffLeft', 'jawOpen', 'mouthFunnel', 'mouthShrugUpper', 'mouthShrugLower', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        cheekSuckRight = ['cheekSuckRight', 'cheekPuffRight', 'cheekPuffLeft', 'jawOpen', 'mouthFunnel', 'mouthShrugUpper', 'mouthShrugLower', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        jawOpen = ['cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight', 'jawOpen', 'mouthShrugLower', 'mouthShrugUpper'],
        jawForward = ['jawForward'],
        jawLeft = ['jawLeft', 'jawRight'],
        jawRight = ['jawRight', 'jawLeft'],
        noseSneerLeft = ['noseSneerLeft'],
        noseSneerRight = ['noseSneerRight'],
        mouthFunnel = ['mouthFunnel', 'cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight', 'mouthPucker', 'mouthRollUpper', 'mouthRollLower', 'mouthClose'],
        mouthPucker = ['mouthPucker', 'jawLeft', 'jawRight', 'mouthFunnel', 'mouthRollUpper', 'mouthRollLower', 'mouthClose'],
        mouthLeft = ['mouthLeft', 'mouthRight'],
        mouthRight = ['mouthRight', 'mouthLeft'],
        mouthRollUpper = ['mouthRollUpper', 'jawOpen', 'mouthFunnel', 'mouthPucker', 'mouthClose', 'mouthUpperUpLeft', 'mouthUpperUpRight'],
        mouthRollLower = ['mouthRollLower', 'jawOpen', 'mouthFunnel', 'mouthPucker', 'mouthClose', 'mouthLowerDownLeft', 'mouthLowerDownRight'],
        mouthShrugUpper = ['mouthShrugUpper', 'jawOpen', 'mouthClose', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        mouthShrugLower = ['mouthShrugLower', 'jawOpen', 'mouthClose', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft'],
        mouthClose = ['mouthPucker', 'mouthClose', 'mouthShrugUpper', 'mouthShrugLower', 'tongueOut', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight', 'tongueRoll', 'tongueBendDown', 'tongueCurlUp', 'tongueSquish', 'tongueFlat', 'tongueTwistRight', 'tongueTwistLeft', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight'],
        mouthSmileLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthStretchLeft', 'mouthShrugUpper', 'mouthShrugLower'],
        mouthSmileRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthStretchRight', 'mouthShrugUpper', 'mouthShrugLower'],
        mouthFrownLeft = ['mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft'],
        mouthFrownRight = ['mouthSmileRight', 'mouthFrownRight', 'mouthDimpleRight'],
        mouthDimpleLeft = ['mouthFrownLeft', 'mouthDimpleLeft', 'mouthStretchLeft'],
        mouthDimpleRight = ['mouthFrownRight', 'mouthDimpleRight', 'mouthStretchRight'],
        mouthUpperUpLeft = ['mouthUpperUpLeft', 'mouthRollUpper', 'cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight'],
        mouthUpperUpRight = ['mouthUpperUpRight', 'mouthRollUpper', 'cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight'],	
        mouthLowerDownLeft = ['mouthLowerDownLeft', 'mouthRollLower', 'cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight'],
        mouthLowerDownRight = ['mouthLowerDownRight', 'mouthRollLower', 'cheekPuffLeft', 'cheekPuffRight', 'cheekSuckLeft', 'cheekSuckRight'],		
        mouthPressLeft = ['mouthFrownLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthPressRight = ['mouthFrownRight', 'mouthPressRight', 'mouthStretchRight'],
        mouthStretchLeft = ['mouthSmileLeft', 'mouthDimpleLeft', 'mouthPressLeft', 'mouthStretchLeft'],
        mouthStretchRight = ['mouthSmileRight', 'mouthDimpleRight', 'mouthPressRight', 'mouthStretchRight'],
        tongueOut = ['tongueOut', 'mouthClose', 'tongueBendDown', 'tongueCurlUp'],
        tongueUp = ['tongueUp', 'mouthClose', 'tongueDown'],
        tongueDown = ['tongueDown', 'mouthClose', 'tongueUp'],
        tongueLeft = ['tongueLeft', 'tongueRight', 'mouthClose'],
        tongueRight = ['tongueRight', 'tongueLeft', 'mouthClose'],
        tongueRoll = ['tongueRoll', 'tongueTwistRight', 'tongueTwistLeft', 'tongueFlat', 'mouthClose'],
        tongueBendDown = ['tongueBendDown', 'tongueOut', 'mouthClose', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight'],
        tongueCurlUp = ['tongueCurlUp', 'tongueBendDown', 'mouthClose', 'tongueUp', 'tongueDown', 'tongueLeft', 'tongueRight'],
        tongueSquish = ['tongueSquish', 'tongueFlat', 'tongueRoll', 'mouthClose'],
        tongueFlat = ['tongueFlat', 'tongueSquish', 'tongueRoll', 'mouthClose'],
        tongueTwistLeft = ['tongueTwistLeft', 'tongueTwistRight', 'mouthClose'],
        tongueTwistRight = ['tongueTwistRight', 'tongueTwistLeft', 'mouthClose']
        )
    shape_storage = []

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
        if defs.exclusives[0][0] in self.selected_shapes_index and not defs.exclusives[0][1] in self.selected_shapes_index:  # mouthClose = jawOpen
            self.selected_shapes_index.append(defs.exclusives[0][1])        # Add jawOpen value if missing 
            self.selected_shapes.append(0.0)
        if all(item in self.selected_shapes_index for item in defs.exclusives[0]):       
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[0][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[0][0])]   # set jawOpen = mouthClose

        if defs.exclusives[1][0] in self.selected_shapes_index and not defs.exclusives[1][1] in self.selected_shapes_index:     # mouthShrugLower = mouthShrugUpper
            self.selected_shapes_index.append(defs.exclusives[1][1])        # Add jawOpen value if missing 
            self.selected_shapes.append(self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][0])])
        if defs.exclusives[1][1] in self.selected_shapes_index and not defs.exclusives[1][0] in self.selected_shapes_index:
            self.selected_shapes_index.append(defs.exclusives[1][0])        # Add jawOpen value if missing 
            self.selected_shapes.append(self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][1])])
        if defs.exclusives[1][1] in self.selected_shapes_index and defs.exclusives[1][0] in self.selected_shapes_index:
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[1][0])]


        #Check if tongue shape exists

        
        
        if (defs.exclusives[2][0] in self.selected_shapes_index) and not defs.exclusives[2][1] in self.selected_shapes_index: 
            self.selected_shapes_index.append(defs.exclusives[2][1])        # Add jawOpen value if missing | tongue shapes require jawOpen >= 0.35
            print('adding supplemental jawOpen')
            self.selected_shapes.append(0.0)
        if defs.exclusives[2][0] in self.selected_shapes_index and (self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[2][1])] <= 0.55):
            print('setting supplemental jawOpen')
            self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[2][1])] = clamp(random.uniform(0.35, 1.05), 0, 1)         
        
        if defs.exclusives[3][1] in self.selected_shapes_index and defs.exclusives[3][0] in self.selected_shapes_index:     # randomly make mouthSmileLeft and mouthSmileRight equal to the greater value
            if random.randint(0, 1) == 1:   # 50% chance to make values equal
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][1])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][0])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][0])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][1])]
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][0])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][1])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[3][0])]

        if defs.exclusives[4][1] in self.selected_shapes_index and defs.exclusives[4][0] in self.selected_shapes_index:     # randomly make cheekPuffLeft and cheekPuffRight equal to the greater value
            if random.randint(0, 1) == 1:   # 50% chance to make values equal
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][1])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][0])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][0])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][1])]
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][0])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][1])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[4][0])]

        if defs.exclusives[5][1] in self.selected_shapes_index and defs.exclusives[5][0] in self.selected_shapes_index:     # randomly make cheekSuckLeft and cheekSuckRight equal to the greater value
            if random.randint(0, 1) == 1:   # 50% chance to make values equal
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][1])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][0])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][0])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][1])]
                if self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][0])] > self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][1])]:
                    self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][1])] = self.selected_shapes[self.selected_shapes_index.index(defs.exclusives[5][0])]

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
                self.selected_shapes.append(clamp(random.uniform(-0.1, self.selected_shapes[0] * 0.8), 0, 1))
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
        #bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[index].default_value = ((int('0x' + hex_str[0] + hex_str[1], 0) / 255),(int('0x' + hex_str[2] + hex_str[3], 0) / 255),(int('0x' + hex_str[4] + hex_str[5], 0) / 255),1)
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
shapecount = len(defs.shape_index)  
tick = 0
range_select = 0
range_list = [
              [0.9,1.15],
              [0.8, 0.9],
              [0.7, 0.8],
              [0.6, 0.7],
              [0.5, 0.6],
              [0.4, 0.5],
              [0.3, 0.4],
              [0.2, 0.3],
              [0.1, 0.2]
              ]

mesh = 'generic_neutral_mesh'
ob = bpy.data.objects[mesh]
encdec.encode(shapecount, 1) # Sets shape count
#bpy.data.scenes["Scene"].node_tree.nodes["Group.002"].inputs[1].keyframe_insert(data_path="default_value", frame=0) # Keyframes shape count
for frame in range(FRAME_START, FRAME_END+1):   # Iterate over each frame in the range
    blank_row = np.zeros(len(defs.shape_index))
    model_shapes = []
    print(f"Generated {frame} of {FRAME_END} shapes")
    #ob = ob
    print(tick)
    if tick == ss.total_shapes:
        tick = 0
        range_select += 1
        if range_select > len(range_list) - 1: range_select = 0
    print(range_select)
    values, names = ss.generate_example(defs, range_list[range_select], defs.shape_index[ss.count])
    for i, name in enumerate(names):
       blank_row[defs.shape_index.index(name)] = values[i]
    defs.shape_storage.append(blank_row)
    tick += 1

#Adds Keyframes
defs.shape_storage = np.vstack(defs.shape_storage)
for shape_name in defs.shape_index:
    keyframes = []
    for kf in range(FRAME_START, FRAME_END): # List of random values representing generated ones
        keyframes.append(kf)
        working_list = defs.shape_storage[:, defs.shape_index.index(shape_name)]
        keyframes.append(working_list[kf].tolist())  
    add_blendshape_fcurve(bpy.context.object, shape_name, keyframes)

    ob = bpy.data.objects[mesh]

set_identity_shapes()
print(defs.shape_storage)
