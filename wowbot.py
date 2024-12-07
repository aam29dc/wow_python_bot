import pytesseract
from PIL import Image, ImageEnhance, ImageOps, ImageGrab
import pyautogui
import pygetwindow
import time
import re
import keyboard

# Set the path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Define the window title you're looking for
window_title = "World of Warcraft"
window = pygetwindow.getWindowsWithTitle(window_title)

def updateData():
    # Capture the screenshot of the region
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    
    # Convert the screenshot to grayscale for better OCR accuracy
    screenshot = screenshot.convert('L')

    # Apply thresholding: Convert to pure black and white
    threshold = 140  # You can adjust this threshold value to optimize results
    screenshot = screenshot.point(lambda p: p > threshold and 255)  # Binarize the image

    # Enhance contrast (optional, can help if the text is not prominent enough)
    screenshot = ImageEnhance.Contrast(screenshot)
    screenshot = screenshot.enhance(2.0)  # Adjust the factor as necessary

    # Optionally, invert colors if text is white on black (for better OCR)
    screenshot = ImageOps.invert(screenshot)

    screenshot.save("screenshot.png")

    # Extract text from the screenshot using Tesseract
    extracted_text = pytesseract.image_to_string(screenshot)
    extracted_text = extracted_text.replace(" ", "")  # Remove spaces for easier regex matching

    print(extracted_text)

    # Using regular expression to match both T and C values
    match = re.search(r"T=([A-Za-z]+)", extracted_text)
    #match = re.search(r"T=([A-Za-z]+)\s*C=([A-Za-z]+)", extracted_text)

    if match:
        # If a match is found, extract values
        target_value = match.group(1)  # Value for T
        #cast_value = match.group(2)    # Value for C
        print(f"Target: {target_value}")
        #print(f"Target: {target_value}, Cast: {cast_value}")
        return target_value
        #return target_value, cast_value
    else:
        # No match found, return None
        print("No target information found.")
        return None, None

if window:
    # Get the first window from the list of windows found
    window = window[0]
    window.restore()  # Restore the window if minimized
    window.activate()  # Bring the window to the front

    # Wait for a moment to ensure the window is active
    time.sleep(1)

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

    updateData()

    #search for an enemy
    """while True:
        #cancel search by pressing x
        if keyboard.is_pressed('x'):
            break
        else:
            #update data every iteration
            data_target, data_cast = updateData()

            # Only proceed if data_target is not None
            if data_target is not None:
                # If target is E, attempt to attack
                if data_target == "E":
                    print("Attempting to attack target.")
                    pyautogui.press('1')
                    time.sleep(1)

                    # first update to check if player is casting
                    _, data_cast = updateData()

                    # check if casting, if not press A key (rotate left)
                    if data_cast == "F" or data_cast is None:
                        pyautogui.keyDown('a')
                        time.sleep(0.2)

                # otherwise search for an E
                else:
                    print("No enemy target found. Searching for a new target...")
                    pyautogui.press('tab')
                    time.sleep(1)"""

else:
    print("Window not found.")
