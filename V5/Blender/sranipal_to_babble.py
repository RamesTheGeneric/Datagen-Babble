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

def recon_funnelpucker(akl):
    jawOpen = akl[3]
    pout = akl[11]
    funnel = pout * (jawOpen)
    pucker = pout - funnel
    return funnel, pucker


def recon_jawopenclose(akl):
    sr_jawOpen = akl[3]
    sr_apeShape = akl[11]
    bbl_jawOpen = sr_jawOpen + sr_apeShape
    bbl_mouthClose = bbl_jawOpen * sr_apeShape
    return bbl_jawOpen, bbl_mouthClose

def recon_upperlowerlr(akl):
    sr_mouthRightUp = akl[5]
    sr_mouthLeftUp = akl[6]
    sr_mouthRightDown = akl[7]
    sr_mouthLeftDown = akl[8]
    mouthRight = max(sr_mouthRightUp, sr_mouthRightDown)
    mouthLeft = max(sr_mouthLeftUp, sr_mouthLeftDown)
    return mouthLeft, mouthRight

def recon_cheeksuck(akl):  # Takes a cheeksuck input and creates values for cheekSuckLeft/Right
    rtd = random.randint(0,2)
    cheekSuck = akl[18]
    # Combined even
    if rtd == 0:
        L = cheekSuck
        R = cheekSuck
    # Left Bias
    if rtd == 1: 
        LR = random.uniform(0,1)
        L = cheekSuck
        if LR == 1: R = random.uniform(0, cheekSuck)    
        else: R = 0     #   Left Solo
    # Right Bias
    if rtd == 2: 
        LR = random.uniform(0,1)
        R = cheekSuck
        if LR == 1: L = random.uniform(0, cheekSuck)    
        else: L = 0     #   Right Solo
    return L, R

def recon_tongue(akl):   # Generates tongue shapes
    rtd = random.uniform(0,10)
    tongueOut = (akl[26] + akl[32]) / 2
    tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll = akl[29], akl[30], akl[27], akl[28], akl[31]
    tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight = 0,0,0,0,0,0
    if tongueOut >= 0.6:
        rtd = random.randint(1,2)
        if rtd == 1: # Twisty
            if random.randint(0,1):  # Twist Left or Right
                tongueTwistLeft = random.uniform(0, tongueOut)
            else: 
                tongueTwistRight = random.uniform(0, tongueOut)
        if rtd == 2: # Twisty
            roll = random.randint(1,2)
            if roll == 1: 
                tongueFlat = random.uniform(0, tongueOut)
            if roll == 2: 
                tongueSquish = random.uniform(0, tongueOut)
    if tongueOut <= 0.3:
        rtd = random.randint(0,2)
        if rtd == 0: # Directional
            if random.randint(0,1):  # Up or DownS
                tongueCurlUp = random.uniform(0, tongueOut)
            else: 
                tongueBendDown = random.uniform(0, tongueOut)
    
    return tongueOut, tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll, tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight

def fill_babble_shapes(akl, sd, bsi):
    bbl_jawOpen, bbl_mouthClose = recon_jawopenclose(akl)
    sd[bsi[0]].append(akl[17])
    sd[bsi[1]].append(akl[16])
    L,R = recon_cheeksuck(akl)
    sd[bsi[2]].append(L)
    sd[bsi[3]].append(R)
    sd[bsi[4]].append(bbl_jawOpen) #jawOpen
    sd[bsi[5]].append(akl[2])   #jawForward
    sd[bsi[6]].append(akl[1])   #jawLeft
    sd[bsi[7]].append(akl[0])   #jawRight
    if random.randint(0,15) == 0: nsl = random.uniform(0,1)
    else: nsl = 0
    if random.randint(0,15) == 0: nsr = random.uniform(0,1)
    else: nsr = 0
    sd[bsi[8]].append(nsl)
    sd[bsi[9]].append(nsr)  #nosesneerright
    funnel, pucker = recon_funnelpucker(akl)
    sd[bsi[10]].append(funnel)  #funnel
    sd[bsi[11]].append(pucker)  #pucker
    mouthLeft, mouthRight = recon_upperlowerlr(akl)
    sd[bsi[12]].append(mouthLeft) #mouthLeft
    sd[bsi[13]].append(mouthRight) #mouthRight
    sd[bsi[14]].append(akl[23])  #mouthRollUpper
    sd[bsi[15]].append(akl[24])  #mouthRollLower
    sd[bsi[16]].append(akl[9]) #mouthShrugUpper
    sd[bsi[17]].append(akl[10]) #mouthShrugLower
    sd[bsi[18]].append(bbl_mouthClose) # mouthClose
    sd[bsi[19]].append(akl[16]) #mouthSmileLeft
    sd[bsi[20]].append(akl[17]) #mouthSmileRight
    sd[bsi[21]].append(akl[18]) #mouthFrownLeft
    sd[bsi[22]].append(akl[19]) #mouthFrownRight
    sd[bsi[23]].append(0) #DimpleLeft
    sd[bsi[24]].append(0) #DimpleRight
    sd[bsi[25]].append(akl[20]) #UpperUpLeft
    sd[bsi[26]].append(akl[19]) #UpperUpRight
    sd[bsi[27]].append(akl[22]) #LowerDownLeft
    sd[bsi[28]].append(akl[21]) #LowerDownRight
    sd[bsi[29]].append(0) #pressLeft
    sd[bsi[30]].append(0) #pressRight
    sd[bsi[31]].append(0) #stretchLeft
    sd[bsi[32]].append(0) #stretchRight
    tongueOut, tongueUp, tongueDown, tongueLeft, tongueRight, tongueRoll, tongueBendDown, tongueCurlUp, tongueSquish, tongueFlat, tongueTwistLeft, tongueTwistRight = recon_tongue(akl)
    sd[bsi[33]].append(tongueOut) # Tongue Out
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

with open('DESKTOP-HSMKF9L - v1.0.0 - 1.6.2023 8.56.39 AM.csv', newline='') as csvfile:
    arkit_list = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        shape_row = ['lip.JawRight', 'lip.JawLeft', 'lip.JawForward', 'lip.JawOpen', 'lip.MouthApeShape', 'lip.MouthUpperRight', 'lip.MouthUpperLeft', 'lip.MouthLowerRight', 'lip.MouthLowerLeft', 'lip.MouthUpperOverturn', 'lip.MouthLowerOverturn', 'lip.MouthPout', 
        'lip.MouthSmileRight', 'lip.MouthSmileLeft', 'lip.MouthSadRight', 'lip.MouthSadLeft', 'lip.CheekPuffRight', 'lip.CheekPuffLeft', 'lip.CheekSuck', 'lip.MouthUpperUpRight', 'lip.MouthUpperUpLeft', 
        'lip.MouthLowerDownRight', 'lip.MouthLowerDownLeft', 'lip.MouthUpperInside', 'lip.MouthLowerInside', 'lip.MouthLowerOverlay', 'lip.TongueLongStep1', 'lip.TongueLeft', 'lip.TongueRight', 'lip.TongueUp', 'lip.TongueDown', 
        'lip.TongueRoll', 'lip.TongueLongStep2']
        shape_row = [float(row[item]) for item in shape_row]
        arkit_list.append(shape_row)
    transposed_data = np.array(arkit_list).T
    percentiles = []
    for column in transposed_data:
        tenth_percentile = np.percentile(column, 10)
        ninetieth_percentile = np.percentile(column, 98)
        percentiles.append((tenth_percentile, ninetieth_percentile))
    #print(percentiles)
    for j in range(len(arkit_list)):
        for i in range(len(arkit_list[j])):
            #print(percentiles[i])
            #print(arkit_list[j][i])
            #print(percentiles[i][0])
            #print(percentiles[i][1])
            arkit_list[j][i] = np.clip(((arkit_list[j][i] - percentiles[i][0]) / (percentiles[i][1] - percentiles[i][0])),0,1)
    #print(arkit_list)
    for akl in enumerate(arkit_list):
        fill_babble_shapes(akl[1], sd, babble_shape_index)
    #print(sd["tongueOut"])
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

