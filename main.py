import webbrowser
import pyautogui as py
import time
from PIL import ImageGrab

FPS_CHECKED = 1000

width, _ = py.size()  # browser must be in fullscreen mode
webbrowser.open("https://elgoog.im/dinosaur-game/")
time.sleep(1)  # wait for page to load

# calculate game field coordinates
header_loc = py.locateOnScreen('top.png')
game_field_top = header_loc.top + header_loc.height
game_field_coords = (0, game_field_top, width, game_field_top + width / 4)

# calculate obstacles check area coordinates
check_area_left = width * 5 / 32
check_area_top = width * 7 / 40
check_area_coords = (check_area_left, check_area_top, check_area_left + width / 20, check_area_top + width * 3 / 64)
check_area_left_increment = width / 5000

py.press('space')  # start game
time.sleep(2)  # wait game start animation

# game loop
while True:
    # take screenshot of game area
    screen = ImageGrab.grab(bbox=game_field_coords)
    # convert screenshot to B&W
    gray_image = screen.convert('L')
    binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
    # check if it's day now
    daytime = binary_image.getpixel((0, 0))
    # check for obstacle before dinosaur
    if any(binary_image.getpixel((x, y)) != daytime for x in range(int(check_area_coords[0]), int(check_area_coords[2]))
           for y in range(int(check_area_coords[1]), int(check_area_coords[3]))):
        py.press('space')
    # latency between iterations
    time.sleep(1 / FPS_CHECKED)
    check_area_left = min(check_area_left + check_area_left_increment, width - check_area_coords[2] + check_area_coords[0])
    check_area_coords = (check_area_left, check_area_top, check_area_left + width / 20, check_area_top + width * 3 / 64)
