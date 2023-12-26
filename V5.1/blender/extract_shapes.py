import bpy
from copy import deepcopy

shape_index = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
"mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
"mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
"mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
"mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight"]


lables_name = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
"mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
"mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
"mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
"mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight", "filename"]


object_name = "BabbleColinFace"  # Change this to your object's name
shape_keys = bpy.data.objects[object_name].data.shape_keys.key_blocks

start_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end
suffix_list_old = ["OMNICEPT_T_M","PHONE_T_L", "PHONE_T_M", "PHONE_T_R",
  "PHONE_M_L", "PHONE_M_M", "PHONE_M_R",
  "PHONE_B_L", "PHONE_B_M", "PHONE_B_R",
  "VIVE_M_M", "VIVE_T_L", "VIVE_T_R", 
  "VIVE_T_M", "VIVE_M_L", "VIVE_M_R", 
  "VIVE_B_L", "VIVE_B_R", "VIVE_B_M"]
  
suffix_list = ["VIVE_M_L", "VIVE_M_M", "VIVE_M_R", "VIVE_B_M", "VIVE_T_M"]


# name ex: colin_0001_VIVE_M_M.png
for frame in range(start_frame, end_frame + 1):
    bpy.context.scene.frame_set(frame)
    print(f"Frame {frame}:")
    shapes = []
    for key in shape_index:   
        shapes.append(shape_keys.get(key).value)
    for suffix in suffix_list:
        path = "C://Users//epicm//Desktop//csv_blendshapes//RenderSceneV5-Babble-Summer//"
        export_shapes = deepcopy(shapes)
        filename = str(f"SummerBabble{str(frame).zfill(4)}_{suffix}.csv")
        img_filename = str(f"RenderSceneV5-Babble-Summer/SummerBabble{str(frame).zfill(4)}_{suffix}.png")
        export_shapes.append(img_filename)
        joined_string = ','.join(map(str, export_shapes))
        lables = ','.join(map(str, lables_name)) 
        #print(shapes)
        print(f"wrote {filename}")
        with open(path + filename, 'w') as file:
            file.write('{}\n{}\n'.format(lables, joined_string))
            file.close()