from PIL import ImageGrab
import win32gui

def run():
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
        img = ImageGrab.grab(boundingBox)

        return img
    
    handle = getHandleFromTitle("gvim")
    image = screenshotWindow(getHandleFromTitle("gvim"))
    image.show()

        





























if __name__ == '__main__':
    run() #Only runs the code if this is the master file