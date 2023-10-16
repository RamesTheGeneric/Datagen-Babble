import csv
import random
import numpy as np

babble_shape_index = ["cheekPuffLeft", "cheekPuffRight", "cheekSuckLeft", "cheekSuckRight", "jawOpen", "jawForward", "jawLeft", "jawRight", "noseSneerLeft", "noseSneerRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", 
    "mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmileLeft", 
    "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthUpperUpLeft", 
    "mouthUpperUpRight", "mouthLowerDownLeft", "mouthLowerDownRight", "mouthPressLeft", "mouthPressRight", "mouthStretchLeft", 
    "mouthStretchRight", "tongueOut", "tongueUp", "tongueDown", "tongueLeft", "tongueRight", "tongueRoll", "tongueBendDown", "tongueCurlUp", "tongueSquish", "tongueFlat", "tongueTwistLeft", "tongueTwistRight"]

class BabbleDefines():
    shape_defs = dict(              # 45 shapes
        cheekPuffLeft = [],
        cheekPuffRight = [],
        cheekSuckLeft = [],
        cheekSuckRight = [],
        jawOpen = [],
        jawForward = [],
        jawLeft = [],
        jawRight = [],
        noseSneerLeft = [],
        noseSneerRight = [],
        mouthFunnel = [],
        mouthPucker = [],
        mouthLeft = [],
        mouthRight = [],
        mouthRollUpper = [],
        mouthRollLower = [],
        mouthShrugUpper = [],
        mouthShrugLower = [],
        mouthClose = [],
        mouthSmileLeft = [],
        mouthSmileRight = [],
        mouthFrownLeft = [],
        mouthFrownRight = [],
        mouthDimpleLeft = [],
        mouthDimpleRight = [],
        mouthUpperUpLeft = 	[],
        mouthUpperUpRight = [],
        mouthLowerDownLeft = [],
        mouthLowerDownRight = [],
        mouthPressLeft = [],
        mouthPressRight = [],
        mouthStretchLeft = [],
        mouthStretchRight = [],
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
    )

sd = BabbleDefines.shape_defs
ARKIT_SHAPES = []
def all_values_below_threshold(lst, threshold):
    return all(value < threshold for value in lst)

def recon_cheekpuff(akl):  # Takes a cheekpuff input and creates values for cheekPuffLeft/Right
    rtd = random.randint(0,2)
    cheekPuff = akl[0]
    # Combined even
    if rtd == 0:
        L = cheekPuff
        R = cheekPuff
    # Left Bias
    if rtd == 1: 
        LR = random.uniform(0,1)
        L = cheekPuff
        if LR == 1: R = random.uniform(0, cheekPuff)    
        else: R = 0     #   Left Solo
    # Right Bias
    if rtd == 2: 
        LR = random.uniform(0,1)
        R = cheekPuff
        if LR == 1: L = random.uniform(0, cheekPuff)    
        else: L = 0     #   Right Solo
    return L, R
def recon_cheeksuck(akl):   # Checks if all values are near zero and adds values for cheekSuckLeft/Right
    #print(akl)
    Left,Right = 0,0
    if all_values_below_threshold(akl, 0.15):
        Left = random.uniform(0,1)
        Right = random.uniform(0,1)
    return Left, Right

def recon_tongue(akl):   # Generates tongue shapes
    rtd = random.uniform(0,10)
    tongue = akl[28]
    tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll, tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight = 0,0,0,0,0,0,0,0,0,0,0
    if tongue >= 0.4:
        rtd = random.randint(0,2)
        if rtd == 0: # Directional
            if random.randint(0,1):  # Up or Down
                tongueUp = random.uniform(0, tongue)
            else: 
                tongueDown = random.uniform(0, tongue)
            if random.randint(0,1):  # Left or Right
                tongueLeft = random.uniform(0, tongue)
            else: 
                tongueRight = random.uniform(0, tongue)
        if rtd == 1: # Twisty
            if random.randint(0,1):  # Twist Left or Right
                tongueTwistLeft = random.uniform(0, tongue)
            else: 
                tongueTwistRight = random.uniform(0, tongue)
        if rtd == 2: # Twisty
            roll = random.randint(0,2)
            if roll == 0:  # Twist Left or Right
                tongueRoll = random.uniform(0, tongue)
            if roll == 1: 
                tongueFlat = random.uniform(0, tongue)
            if roll == 2: 
                tongueSquish = random.uniform(0, tongue)
    if tongue <= 0.4:
        rtd = random.randint(0,2)
        if rtd == 0: # Directional
            if random.randint(0,1):  # Up or DownS
                tongueCurlUp = random.uniform(0, tongue)
            else: 
                tongueBendDown = random.uniform(0, tongue)
    
    return tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll, tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight

def fill_babble_shapes(akl, sd, bsi):
    L,R = recon_cheekpuff(akl)
    sd[bsi[0]].append(L)
    sd[bsi[1]].append(R)
    L,R = recon_cheeksuck(akl)
    print(L)
    sd[bsi[2]].append(L)
    sd[bsi[3]].append(R)
    sd[bsi[4]].append(akl[1])
    sd[bsi[5]].append(akl[5])
    sd[bsi[6]].append(akl[3])
    sd[bsi[7]].append(akl[4])
    sd[bsi[8]].append(akl[29])
    sd[bsi[9]].append(akl[30])
    sd[bsi[10]].append(akl[8])
    sd[bsi[11]].append(akl[9])
    sd[bsi[12]].append(akl[14])
    sd[bsi[13]].append(akl[15])
    sd[bsi[14]].append(akl[6])
    sd[bsi[15]].append(akl[7])
    sd[bsi[16]].append(akl[24])
    sd[bsi[17]].append(akl[25])
    sd[bsi[18]].append(akl[2]) # mouthClose
    sd[bsi[19]].append(akl[16])
    sd[bsi[20]].append(akl[17])
    sd[bsi[21]].append(akl[18])
    sd[bsi[22]].append(akl[19])
    sd[bsi[23]].append(akl[22])
    sd[bsi[24]].append(akl[23])
    sd[bsi[25]].append(akl[10])
    sd[bsi[26]].append(akl[11])
    sd[bsi[27]].append(akl[12])
    sd[bsi[28]].append(akl[13])
    sd[bsi[29]].append(akl[26])
    sd[bsi[30]].append(akl[27])
    sd[bsi[31]].append(akl[20])
    sd[bsi[32]].append(akl[21])
    sd[bsi[33]] = akl[28] # Tongue Out
    tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll, tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight = recon_tongue(akl)
    sd[bsi[34]].append(tongueUp)
    sd[bsi[35]].append(tongueDown)
    sd[bsi[36]].append(tongueLeft)
    sd[bsi[37]].append(tongueRight)
    sd[bsi[38]].append(tongueRoll)
    sd[bsi[39]].append(tongueBendDown)
    sd[bsi[40]].append(tongueCurlUp)
    sd[bsi[41]].append(tongueSquish)
    sd[bsi[42]].append(tongueFlat)
    sd[bsi[43]].append(tongueTwistLeft)
    sd[bsi[44]].append(tongueTwistRight)
#CP_LOWER_THRESH = lower_threshold = np.percentile(array, 10)

with open('MySlate_4_iPhone.csv', newline='') as csvfile:
    arkit_list = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        shape_row = [float(row["CheekPuff"]), float(row["JawOpen"]), float(row["MouthClose"]), float(row["JawLeft"]), float(row["JawRight"]), float(row["JawForward"]), 
        float(row["MouthRollUpper"]), float(row["MouthRollLower"]), float(row["MouthFunnel"]), float(row["MouthPucker"]), float(row["MouthUpperUpLeft"]), 
        float(row["MouthUpperUpRight"]), float(row["MouthLowerDownLeft"]), float(row["MouthLowerDownRight"]), float(row["MouthLeft"]), float(row["MouthRight"]), 
        float(row["MouthSmileLeft"]), float(row["MouthSmileRight"]), float(row["MouthFrownLeft"]), float(row["MouthFrownRight"]), float(row["MouthStretchLeft"]), float(row["MouthStretchRight"]), 
        float(row["MouthDimpleLeft"]), float(row["MouthDimpleRight"]), float(row["MouthShrugUpper"]), float(row["MouthShrugLower"]), float(row["MouthPressLeft"]), float(row["MouthPressRight"]), float(row["TongueOut"]), float(row["NoseSneerLeft"]), float(row["NoseSneerRight"])]
        arkit_list.append(shape_row)
    for akl in enumerate(arkit_list):
        fill_babble_shapes(akl[1], sd, babble_shape_index)
    print(sd["cheekSuckLeft"])
    '''
    for i in range(len(sd["jawOpen"])):
        print(sd["jawOpen"][i], sd["mouthClose"][i])
        '''
    #lows = np.asarray(arkit_list)
    #lows = np.percentile(lows[:, 0], 5)
    #print(lows)
    #print(arkit_list[0][28])
    #lower_threshold = np.percentile(lows[], 1)
    #print(lower_threshold)
    #CP_LOWER_THRESH = np.percentile(array, 10)
    #print(lower_threshold)

