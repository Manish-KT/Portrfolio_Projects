import pyautogui
from PIL import ImageGrab
import time


def hitKey(key):
    pyautogui.keyDown(key)
    return


def Check_Objects(pix):
    # check for Birds
    for i in range(250, 400):
        for j in range(510, 620):
            if pix[i, j] < 90:
                hitKey("down")
                time.sleep(0.1)
                pyautogui.keyUp("down")
                return

    # check for Cactus
    for i in range(250, 400):
        for j in range(620, 730):
            if pix[i, j] < 90:
                hitKey("up")
                return
    return


if __name__ == "__main__":
    print("Starting the game...")
    time.sleep(2)
    # k = 0 # for saving images
    while True:
        img = ImageGrab.grab().convert('L')
        data = img.load()

        Check_Objects(data)
        """
        for i in range(250, 400):
            for j in range(510, 620):
                data[i, j] = 0

        for i in range(250, 400):
            for j in range(620, 730):
                data[i, j] = 171

        # img.save(f"images/img_{k}.png")
        k += 1
        # img.show()
        # break
        """
