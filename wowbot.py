import pytesseract
from PIL import ImageOps, ImageGrab
import pygetwindow
import time
import re
import math
import ctypes
from pynput.mouse import Controller, Listener
from pynput.keyboard import Key, Controller

# Create a Controller object for the keyboard
keyboard = Controller()

# Set the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

### IMPORTANT for angle calculations ###
Retail = True  # retail or classic WoW flag

# angular average speed constant (Angle, Angular Velocity in Rads), WITHOUT moving
constAVrad360 = (360, 3.306939635357677)                    # 1.9 s (retail)
constAVrad180 = (180, 3.5298793860559474589467903182916)    # 0.89 s
constAVrad90 = (90, 4.0276828892176836390546710042045)      # 0.39 s
constAVrad45 = (45, 5.6099868814103450686832917558563)      # 0.14 s
constAVrad33 = (33.75, 8.4149803221155176030249376337844)   # 0.07 s
constAVrad22 = (22.5, 20.138414446088418195273355021022)    # 0.0195 s

constAVradClassic = (360, 3.1573795513465258678016516414869) # 1.99s, same AV for any angle in Classic

# angular average speed constant WHILE moving Forward (on approximately flat ground)
constAVrad360Moving = (360, 2.3674398293819089965807410574827)    # 2.654

def lineThroughPoints(pnt1, pnt2):
    x1, y1 = pnt1
    x2, y2 = pnt2
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return lambda x: m * x + b
# if angle is less than 22 we use constAVrad22[1]
line1 = lineThroughPoints(constAVrad22, constAVrad33)
line2 = lineThroughPoints(constAVrad33, constAVrad45)
line3 = lineThroughPoints(constAVrad45, constAVrad90)
line4 = lineThroughPoints(constAVrad90, constAVrad180)
line5 = lineThroughPoints(constAVrad180, constAVrad360)     # not needed since angles should be (-180, 180]

# movement average walk speed constant, units per second
constSpeed = 0.368524675

# hold our last known point
lastPoint = (0,0)

# paths
path1 = [(607,531),(591,514),(618,489)]

def sleepX(seconds):
    # Windows API sleep using high precision timers (nanoseconds)
    ctypes.windll.kernel32.SleepEx(int(seconds * 1000), True)  # Windows Sleep in milliseconds

def convertImageToMapCoords(X, Y):
    # map dimensions are (x,y): (1024, 683)
    return (X/1024)*100, (Y/683)*100

def convertMapCoordsToImage(X, Y):
    return (X/100)*1024, (Y/100)*683

def extractData():
    # Capture the screenshot of the region
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    
    # Convert the screenshot to grayscale for better OCR accuracy
    screenshot = screenshot.convert('L')

    # Optionally, invert colors if text is white on black (for better OCR)
    screenshot = ImageOps.invert(screenshot)

    # uncomment for debugging only
    #screenshot.save("screenshot.png")

    # Configure Tesseract for large text (PSM 6 works well for a block of text)
    custom_config = r'--oem 3 --psm 6'

    # Extract text from the screenshot using Tesseract
    textExtract = pytesseract.image_to_string(screenshot, config=custom_config)
    textExtract = textExtract.replace(" ", "")  # Remove spaces for easier regex matching
    textExtract = re.sub(r'\n+', '\n', textExtract)
    return textExtract

# avg time to extract data
def extractDataTime():
    startTime = time.perf_counter()
    textExtract = extractData()
    return time.perf_counter() - startTime

def searchEnemy():
    while True:
        #update data every iteration
        textExtract = extractData()

        # Using regular expression to match T value
        targetData = re.search(r"T=([A-Za-z]+)", textExtract).group(1)

        #cancel search by pressing x
        if keyboard.is_pressed('x'):
            break
        else:
            # Only proceed if targetData is not None
            if targetData is not None:
                # If target is E, attempt to attack
                if targetData == "E":
                    print('Attempting to attack target.')
                    keyboard.press('1')
                    keyboard.release('1')

                    # first update to check if player is casting, Using regular expression to match C value
                    textExtract = extractData()
                    castData = re.search(r"C=([A-Za-z]+)", textExtract).group(1)

                    # check if casting
                    if castData == "F" or castData is None:
                        # if not casting then rotate the player
                        keyboard.press('a')
                        sleepX(0.2)
                        keyboard.release('a')

                # If target not an E, then search for an E
                else:
                    print('No enemy target found. Searching for a new target...')
                    keyboard.press('tab')
                    keyboard.release('tab')
            else:
                print('No target data.')

def calcAvgSpeed():
    # dont move, then move for 1 second in a STRAIGHT line
    sleepX(1)
    textExtract = extractData()     # get initial position
    iX = float(re.search(r"X=([0-9.]+)", textExtract).group(1))
    iY = float(re.search(r"Y=([0-9.]+)", textExtract).group(1))

    while True:
        keyboard.press('w')
        sleepX(1)
        textExtract = extractData()     # call extract data right before we keyUp
        keyboard.release('w')

        fX = float(re.search(r"X=([0-9.]+)", textExtract).group(1))
        fY = float(re.search(r"Y=([0-9.]+)", textExtract).group(1))
        print("Speed: ", math.sqrt((fX - iX)**2 + (fY - iY)**2))
        iX = fX
        iY = fY

def RotateWhileForward(rtime):
    # get initial Angle
    textExtract = extractData()
    iA = float(re.search(r"A=([0-9.]+)", textExtract).group(1))
    # hold forward and left or right for a second

    keyboard.press('w')
    keyboard.press('a')
    sleepX(rtime)  # Move forward for the calculated time
    keyboard.release('a')
    keyboard.release('w')

    sleepX(0.1)

    textExtract2 = extractData()
    fA = float(re.search(r"A=([0-9.]+)", textExtract2).group(1))

    print('iA: ', iA)
    print('fA: ', fA)

# map coords are (0,0) to (1,1) (before multiplication)
# each map has the top-left corner (0,0) and the bottom right (1,1)

# player angle of 0 is parallel with the Y-axis of map coords, and
# player angle of 0 points towards negative Y of map coords (with player at (0,0) on the map)

def getAdjustPlayerAngleRad(iA, iX, iY, fX, fY):
    # If initial and final positions are the same, no rotation is needed
    if iX == fX and iY == fY:
        return 0
    
    # Calculate the target angle using atan2
    targetAngle = math.atan2(fY - iY, fX - iX)
   
    # Calculate the difference between the target angle and the initial angle
    deltaAngle = -targetAngle - iA - math.pi/2
    
    # Adjust the angle to be within the range (-pi, pi]
    rotationAngle = (deltaAngle + math.pi) % (2 * math.pi) - math.pi
    
    return rotationAngle

def rotPlayer(rtime):
    keyboard.press('a')
    sleepX(rtime)
    keyboard.release('a')

def rotatePlayerDegree(angle):
    print('Angle: ', angle)

    if Retail == True:
        if abs(angle) <= 22.5:
            AVrad = constAVrad22[1]
            print('line 0')
        elif 22.5 < abs(angle) <= 33.75:
            AVrad = line1(abs(angle))
            print('line 1')
        elif 33.75 < abs(angle) <= 45:
            AVrad = line2(abs(angle))
            print('line 2')
        elif 45 < abs(angle) <= 90:
            AVrad = line3(abs(angle))
            print('line 3')
        elif 90 < abs(angle) <= 180:
            AVrad = line4(abs(angle))
            print('line 4')
        elif abs(angle) > 180:
            AVrad = line5(abs(angle))
            print('line 5')
        else:
            print('Unknown angle: ', angle)
            AVrad = constAVrad360[1]
    else:
        AVrad = constAVradClassic[1]

    print('AVrad: ', AVrad)
    
    rotateTime = math.radians(abs(angle)) / AVrad
    print('Rotate time: ', rotateTime)

    if rotateTime > 0.01:   # error tolerance threshold
        # Rotate counter-clockwise (left)
        if angle > 0: 
            print('Rotate player: Left')
            keyboard.press('a')
            sleepX(rotateTime)  # Adjust time based on angular difference
            keyboard.release('a')
        # Rotate clockwise (right)
        elif angle < 0:    
            print('Rotate player: Right')
            keyboard.press('d')
            sleepX(rotateTime)  # Adjust time based on angular difference
            keyboard.release('d')
        else:
            print('Rotate player: None')
    else:
        print('Rotate time less than error tolerance.')

def gotoPoint(fX, fY):
    iX = iY = iA = None
    # Get initial Positions and Angles
    textExtract = extractData()   
    iX = float(re.search(r"X=([0-9.]+)", textExtract).group(1))
    iY = float(re.search(r"Y=([0-9.]+)", textExtract).group(1))
    iA = float(re.search(r"A=([0-9.]+)", textExtract).group(1))

    print('iX:', iX, 'iY:', iY)
    print('fX:', fX, 'fY:', fY)
    print('iA:', iA)

    # Calculate time to travel in a straight line towards destination
    distance = math.sqrt((fX - iX) ** 2 + (fY - iY) ** 2)
    print('distance:', distance)
    travelTime = distance / constSpeed  # Time required to travel this distance

    # Print time till arrival (in seconds)
    print(f"Time till arrival: {travelTime:.2f} seconds")

    firstIter = True   # flag for for iter of loop, to not jump on start

    # Check if player is already there
    if travelTime >= 0.9: # error tolerance threshold
        # 1st, while NOT moving, rotate player towards the destination
        rotatePlayerDegree(math.degrees(getAdjustPlayerAngleRad(iA, iX, iY, fX, fY)))   # Rotates player based on Angular difference of the destination position

        startTime = time.perf_counter() # start timer after initial rotation
        elapsedTime = 0

        prevSpeed = constSpeed  # start with our globally defined constSpeed

        # 2nd, now that we have the angle towards the destination, start moving
        keyboard.press('w')

        # While elapsed time is less than travelTime, move towards the destination
        while abs(travelTime - elapsedTime) > 0.9:   # error tolerance threshold

            # EVERY SECOND, check the Angle and make adjustments towards destination
            # EVERY SECOND, if the player is stuck then jump
            if abs(elapsedTime - round(elapsedTime)) <= 0.0001:  # error tolerance threshold for going over a integer
                print('Adjusting angle')
                textExtract = extractData() # takes about 0.25s on my machine
                pX = iX # previous x position
                pY = iY # previous y position
                iX = float(re.search(r"X=([0-9.]+)", textExtract).group(1))
                iY = float(re.search(r"Y=([0-9.]+)", textExtract).group(1))
                iA = float(re.search(r"A=([0-9.]+)", textExtract).group(1))

                # get Angle and time for a 'rotation WHILE moving'
                rotateAngle = math.degrees(getAdjustPlayerAngleRad(iA, iX, iY, fX, fY))
                rotateTime = math.radians(abs(rotateAngle)) / constAVrad360Moving[1]

                # rotate left
                if rotateAngle > 0:
                    keyboard.press('a')
                    sleepX(rotateTime)
                    keyboard.release('a')
                # rotate right
                else:
                    keyboard.press('d')
                    sleepX(rotateTime)
                    keyboard.release('d')

                # jump if stuck
                if abs(pX - iX) < 0.1 and abs(pY - iY) < 0.1 and firstIter == False:
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)

            elapsedTime = time.perf_counter() - startTime
            firstIter = False   # don't jump
            """print('speed: ', speed)
            print('dist: ', distance)
            print('tt: ', travelTime)
            print('start: ', startTime)
            print('elapsed: ', elapsedTime)
            print('tt-e: ', travelTime - elapsedTime)"""
        
        keyboard.release('w')
        print('Player arrived.')
    else:
        print('Player already arrived.')

def startPath(path):
    print('Starting path...')
    # calc the distance between current position and each point of path
    # attempt to go to the point of the shortest distance
    for i, (x, y) in enumerate(path1, start=1):
        x, y = convertImageToMapCoords(x, y)
        print('Going to waypoint: ', i)
        print('x: ', x)
        print('y: ', y)
        gotoPoint(x, y)

class BufferedFileWriter:
    def __init__(self, filename, buffer_size=5):
        self.filename = filename
        self.buffer = []
        self.buffer_size = buffer_size

    def write(self, data):
        self.buffer.append(data)
        
        # When buffer reaches the limit, flush it to the file
        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        # Write all buffered data to the file
        with open(self.filename, 'a') as file:
            file.write("\n".join(self.buffer) + "\n")
        self.buffer.clear()

def createWaypoint(textExtract):
    # Find X, Y, and A values from the text, with fallback values if not found
    x_match = re.search(r"X=([0-9.]+)", textExtract)
    y_match = re.search(r"Y=([0-9.]+)", textExtract)
    a_match = re.search(r"A=([0-9.]+)", textExtract)

    # Use the matched values if found, otherwise fallback to 'x', 'y', 'a'
    x_value = x_match.group(1) if x_match else 'x'
    y_value = y_match.group(1) if y_match else 'y'
    a_value = a_match.group(1) if a_match else 'a'

    # Write the values to the file
    with open('wayPoints.txt', 'a') as wayPoints:
        wayPoints.write(f'{x_value} {y_value} {a_value}\n')

def writePath():
    # record waypoints at 1s intervals for 10 seconds
    startTime = time.perf_counter()
    elapsedTime = 0

    while elapsedTime <= 10:       
        if abs(elapsedTime - round(elapsedTime)) <= 0.0001:  # error tolerance threshold
            print(f"Waypoint at second {round(elapsedTime)}")
            textExtract = extractData()
            createWaypoint(textExtract)
        elapsedTime = time.perf_counter() - startTime

#Main function
wayPoints = BufferedFileWriter("waypoints.txt")

# Define the window title you're looking for
window_title = "World of Warcraft"
window = pygetwindow.getWindowsWithTitle(window_title)

if window:
    # Get the first window from the list of windows found
    window = window[0]
    window.restore()  # Restore the window if minimized
    window.activate()  # Bring the window to the front

    # Wait for a moment to ensure the window is active
    sleepX(1)

    # Define the size of the screenshot region (e.g., 300x300 pixels)
    ss_w = 300
    ss_h = 300

    # Calculate the center of the window to create the bounding box
    center_x = window.left + window.width // 2
    center_y = window.top + window.height // 2

    # Define the bounding box for the screenshot
    left = center_x - ss_w // 2
    top = center_y - ss_h // 2
    right = left + ss_w
    bottom = top + ss_h

    if Retail:print('---WoW RETAIL---')
    else:print('---WoW CLASSIC---')

    # global to hold our average extract data time
    #extractDataAvgTime = extractDataTime()  # on my machine takes about 0.25s
    #print(extractDataAvgTime)

    #textExtract = extractData()
    #gotoPoint(58.175939321517, 73.954319953918)
    #rotatePlayerDegree(180)
    #rotPlayer(0.4975)
    startPath(path1)

    wayPoints.flush()

else:
    print('Window not found.')
