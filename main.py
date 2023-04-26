
def run():

    from PIL import ImageGrab
    import win32gui

    from ctypes import windll
    import numpy
    import cv2 as OpenCV
    import mouse

    import time

    user32 = windll.user32
    user32.SetProcessDPIAware()


    methods = [OpenCV.TM_CCOEFF,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_CCORR,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_SQDIFF,OpenCV.TM_SQDIFF_NORMED]

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabetImages = []
    for a in alphabet:
        alphabetImages.append(OpenCV.imread("assets/"+a+".png",0))
    def PIL_to_OpenCV(img):
        numpy_img = numpy.array(img)
        cv_image = OpenCV.cvtColor(numpy_img, OpenCV.COLOR_RGB2BGR)
        return cv_image

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
        time.sleep(0.5)
        boundingBox = win32gui.GetWindowRect(hwnd)
        print("Bounding box of window:\t"+str(boundingBox))
        img = ImageGrab.grab(boundingBox)

        return img

    def getLettersShown(world, letterImg=0):
        
        def getWorldLetterImages(world):
            images = []
            for i in range(4):
                x = 380 + 64*i
                index = 0
                for j in range(4):
                    y = 420 + 64*j
                    images.append(world[y:y+64, x:x+64])
    
                    index += 1
            return images

        screenLetters = getWorldLetterImages(world)
        i = 0
        lettersCollected = ""
        for l in alphabetImages:            
            for sL in screenLetters:
                result = OpenCV.matchTemplate(sL, l,methods[3])
                min_v, max_v, min_loc, max_loc = OpenCV.minMaxLoc(result)
                print(max_v)
                if max_v > 0.95:
                    lettersCollected += alphabet[i]
            i += 1

        return lettersCollected


    
    world = OpenCV.imread("assets/tempScreen.png", 0)
    d = OpenCV.imread("assets/D.png", 0)

    height, width = d.shape
    print(len(alphabetImages))
    print(getLettersShown(world))
    
           
    world2 = world.copy()

    result = OpenCV.matchTemplate(world2, d, methods[1])
    (yPosList, xPosList) = numpy.where(result >= 0.97)
    print(xPosList)
        
    #location = max_location
    #bottom_right = (location[0]+width,location[1]+height)
    #OpenCV.rectangle(world2, location, bottom_right, 255, 5)
    OpenCV.imshow("Match", world2)
    OpenCV.waitKey(0)
    OpenCV.destroyAllWindows()


























if __name__ == '__main__':
    run() #Only runs the code if this is the master file
