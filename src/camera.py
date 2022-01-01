import imutils
from imutils.video import VideoStream
import numpy as np
import cv2
import time

def ReplaceChar(string, char, index):
    answer = ""
    
    for i in range(0, index):
        answer += string[i]
        
    answer += char
    
    for i in range(index + 1, len(string)):
        answer += string[i]
        
    return answer
    
def FinishCorner(colorA, colorB):
    if colorA == "X" or colorB == "X" or colorA == colorB:
        return "X"
        
    corners = ["OBY", "BRY", "RGY", "GOY", "OGW", "GRW", "RBW", "BOW"]
    
    for i in range(0, 3):
        for i in range(0, 8):
            if colorA == corners[i][0] and colorB == corners[i][1]:
                return corners[i][2]
            
            popped = corners[i][0]
            corners[i] = corners[i][1:]
            corners[i] = corners[i] + popped
            
    return "X"
    
def TranslateColors(colors):
    charsUnsorted = ''
    
    colorDict = {
      (255, 255, 255): "W",
      (160, 70, 40): "B",
      (0, 230, 230): "Y",
      (0, 170, 40): "G",
      (0, 0, 255): "R",
      (0, 165, 255): "O"
    }
    
    for color in colors:
        if tuple(color) in colorDict.keys():
            charsUnsorted = charsUnsorted + colorDict[tuple(color)]
        else:
            charsUnsorted = charsUnsorted + "X"
        
    charsSorted = ""
    
    for i in range(0, 18):
        charsSorted = charsSorted + charsUnsorted[i]
    for i in range(27, 36):
        charsSorted = charsSorted + charsUnsorted[i]
    for i in range(45, 54):
        charsSorted = charsSorted + charsUnsorted[i]
    for i in range(36, 45):
        charsSorted = charsSorted + charsUnsorted[i]
    for i in range(18, 27):
        charsSorted = charsSorted + charsUnsorted[i]
    
    charsSorted = ReplaceChar(charsSorted, "W", 4)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[38], charsSorted[18]), 6)
    charsSorted = ReplaceChar(charsSorted, "O", 13)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[26], charsSorted[29]), 15)
    charsSorted = ReplaceChar(charsSorted, "B", 22)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[9], charsSorted[8]), 20)
    charsSorted = ReplaceChar(charsSorted, "Y", 31)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[51], charsSorted[17]), 35)
    charsSorted = ReplaceChar(charsSorted, "R", 40)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[0], charsSorted[47]), 36)
    charsSorted = ReplaceChar(charsSorted, "G", 49)
    charsSorted = ReplaceChar(charsSorted, FinishCorner(charsSorted[33], charsSorted[42]), 53)
    
    #solve corners
    
    sideDict = {
      "W": "U",
      "B": "F",
      "Y": "D",
      "G": "B",
      "R": "L",
      "O": "R",
      "X": "X"
    }
    
    completedChars = ""
    
    solved = True
    for i in range(0, 54):
        completedChars += sideDict[charsSorted[i]]
        
        if completedChars[i] == "X":
            solved = False
    
    if solved:
        return completedChars
    else:
        return ""
    
def Hue(color): #works only if R >= G >= B
    return 60.0 * (color[1] - color[0]) / max((color[2] - color[0], 0.1))
    
def StartCameras():
    global vs0, vs1
    vs0 = VideoStream( src = 0 ).start()
    vs1 = VideoStream( src = 1 ).start()

    # setting camera parameters
    #vs0.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
    #vs0.stream.set(cv2.CAP_PROP_AUTO_WB, 0)
    #vs0.stream.set(cv2.CAP_PROP_GAIN, 1)
    
    #vs1.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
    #vs1.stream.set(cv2.CAP_PROP_AUTO_WB, 0)
    #vs1.stream.set(cv2.CAP_PROP_GAIN, 1)

    time.sleep(0.5)

def ReleaseCameras():
    vs0.stop()
    vs1.stop()
    
    cv2.destroyAllWindows()
    
def SampleColor(frame, position, dist = 3):
    numOfPixels = 0
    color = [0.0, 0.0, 0.0]
    
    for x in range(int(position[0]) - dist, int(position[0]) + dist + 1):
        for y in range(int(position[1]) - dist, int(position[1]) + dist + 1):
            
            average = float(float(frame[y][x][0]) + float(frame[y][x][1]) + float(frame[y][x][2])) / 3.0
            if average > -1: #it's not black
                numOfPixels = numOfPixels + 1
                color += frame[y][x]
            
    if numOfPixels == 0:
        return color
        
    return [color[0] / numOfPixels, color[1] / numOfPixels, color[2] / numOfPixels]

def SampleColors(frame, positions):
    colors = [[0] * 3 for i in range(len(positions))]
    
    for i in range(0, len(positions)):
        colors[i] = SampleColor(frame, positions[i])
        
    return colors

def ColorMatch(color):
    if color[0] == 0: color[0] = 1
    if color[1] == 0: color[1] = 1
    if color[2] == 0: color[2] = 1
    
    maxim = max(color[0], color[1], color[2])
    minim = min(color[0], color[1], color[2])
    delta = maxim / minim

    if delta < 1.25 or (maxim == color[0] and delta < 2):
        return [255, 255, 255] #white
        
    if maxim == color[0]:
        return [160, 70, 40] #blue

    hue = Hue(color)
    
    if hue > 30 and hue < 70:
        return [0, 230, 230] #yellow  
    
    if maxim == color[1]:
        return [0, 170, 40] #green


    #don't know if it's red or orange, so set placeholder for now
    return [-1, -1, Hue(color)]
    
    #return [0, 0, 255] #red 
    #return [0, 165, 255] #orange

def ScanColors(marks1, marks2, samplePositions, focusedCamera1, cubeString):
    frame1 = vs0.read()
    frame2 = vs1.read()
    
    colors = [[0] * 3 for i in range(54)]
    
    frame1Valid = hasattr(frame1, "__len__")
    frame2Valid = hasattr(frame2, "__len__")
    
    full1 = True
    for mark in marks1:
        if mark == [-1, -1]:
            full1 = False
            
    full2 = True
    for mark in marks2:
        if mark == [-1, -1]:
            full2 = False
    
    if frame1Valid and full1: #camera 1 exists and every mark is there
        colors[0:27] = SampleColors(frame1, samplePositions[0:27])
            
        colors[4] = [0, 0, 0]
        colors[6] = [0, 0, 0]
        colors[13] = [0, 0, 0]
        colors[15] = [0, 0, 0]
        colors[22] = [0, 0, 0]
        colors[26] = [0, 0, 0]

    if frame2Valid and full2: #camera 2 exists and every mark is there
        colors[27:54] = SampleColors(frame2, samplePositions[27:54])
        
        colors[29] = [0, 0, 0]
        colors[31] = [0, 0, 0]
        colors[36] = [0, 0, 0]
        colors[40] = [0, 0, 0]
        colors[49] = [0, 0, 0]
        colors[53] = [0, 0, 0]

    minRedHue = -1
    maxRedHue = -1
    #color match everything except orange and red
    for i in range(0, 54):
        if colors[i] != [0, 0, 0]:
            colors[i] = ColorMatch(colors[i])

            if colors[i][0] < 0: #color is red or orange
                if minRedHue == -1:
                    minRedHue = colors[i][2]
                    maxRedHue = colors[i][2]
                else:
                    minRedHue = min(minRedHue, colors[i][2])
                    maxRedHue = max(maxRedHue, colors[i][2])   
        
    #color match orange and red
    for i in range(0, 54):  
        if colors[i][0] < 0: #color is red or orange
            redDist = abs(minRedHue - colors[i][2])
            orangeDist = abs(maxRedHue - colors[i][2])

            if redDist < orangeDist:
                colors[i] = [0, 0, 255] #red 
            else:
                colors[i] = [0, 165, 255] #orange
        
        
    if frame1Valid:
        for i in range(0, 27):
            if colors[i] != [0, 0, 0]:
                cv2.circle(frame1, (int(samplePositions[i][0]), int(samplePositions[i][1])), 10, colors[i], 2)
        
    if frame2Valid:
        for i in range(27, 54):
            if colors[i] != [0, 0, 0]:
                cv2.circle(frame2, (int(samplePositions[i][0]), int(samplePositions[i][1])), 10, colors[i], 2)
    
    
    #text = ["UR", "R", "U", "RB", "UB", "B"]
    for i in range(0, 7):
        if marks1[i] != [-1, -1]:
            cv2.circle(frame1, tuple(marks1[i]), 10, (0, 0, 0), 2)
            
            #if full1:
                #cv2.putText(frame1, text[i], tuple(marks1[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
    #text = ["L", "DL", "FL", "D", "F", "FD"]
    for i in range(0, 7):
        if marks2[i] != [-1, -1]:
            cv2.circle(frame2, tuple(marks2[i]), 10, (0, 0, 0), 2)
            
            #if full2:
                #cv2.putText(frame2, text[i], tuple(marks2[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)          
   
    #preparing camera for screen output
    dim  = (640, 480)
    if (frame1Valid):
        frame1 = cv2.resize(frame1, dim) 
    if (frame2Valid):
        frame2 = cv2.resize(frame2, dim)
    
    main = np.full((480, 640, 3), np.uint8(50))   
    if focusedCamera1 and frame1Valid:
        main = frame1
    elif not focusedCamera1 and frame2Valid:
        main = frame2
    
    mini = np.full((480, 640, 3), np.uint8(50))   
    if focusedCamera1 and frame2Valid:
        mini = imutils.resize(frame2, width = int(main.shape[1] / 4))
        main[main.shape[0] - mini.shape[0]:main.shape[0], 0:mini.shape[1]] = mini
    elif not focusedCamera1 and frame1Valid:
        mini = imutils.resize(frame1, width = int(main.shape[1] / 4))
        main[0:mini.shape[0], 0:mini.shape[1]] = mini

    
    blur = main[0:480, 480:640]
    blur = cv2.flip(blur, 1)
    blur = cv2.blur(blur,(10,10))
    
    main = np.hstack((main, blur))
    
    if full1 and full2 and frame1Valid and frame2Valid:
        chars = TranslateColors(colors)
        if chars != "":
            return main, list(chars) 
        
    return main, cubeString
    
   

