
def run():

    from PIL import ImageGrab
    import win32gui

    from ctypes import windll
    import numpy
    import cv2 as openCV

    user32 = windll.user32
    user32.SetProcessDPIAware()

    def getHandleFromTitle(t, exact=False):
        toplist, windowList = [], []
        def getAllWindows(hwnd, results):
            windowList.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(getAllWindows, toplist)
        if exact:
            return[(hwnd,title) for hwnd, title in windowList if t == title]
        else:
            return [(hwnd,title) for hwnd, title in windowList if t in title.lower()]


    def screenshotWindow(hwnd):
        win32gui.SetForegroundWindow(hwnd)
        boundingBox = win32gui.GetWindowRect(hwnd)
        print("Bounding box of window:\t"+str(boundingBox))
        img = ImageGrab.grab(boundingBox)

        return img
    
    handle = getHandleFromTitle("avast")[0][0]
    image = screenshotWindow(handle)
    image.show()

        





























if __name__ == '__main__':
    run() #Only runs the code if this is the master file
