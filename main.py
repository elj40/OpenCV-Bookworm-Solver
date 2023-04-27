
def run():

    from PIL import ImageGrab
    import win32gui

    from ctypes import windll
    import numpy
    import cv2 as OpenCV
    import mouse

    import time

    import re

    user32 = windll.user32
    user32.SetProcessDPIAware()
    
    wordsFile = open("english_words_edited.txt", "r")
    allWords = wordsFile.readlines()
    wordsFile.close()

    first_tile_position = (420, 460)
    attack_button_postion = (415,740)

    methods = [OpenCV.TM_CCOEFF,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_CCORR,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_SQDIFF,OpenCV.TM_SQDIFF_NORMED]

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabetImages = []
    for a in alphabet:
        alphabetImages.append(OpenCV.imread("assets/"+a+".png",0))
    def PIL_to_OpenCV(img):
        numpy_img = numpy.array(img)
        cv_image = OpenCV.cvtColor(numpy_img, OpenCV.COLOR_RGB2GRAY)
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
        time.sleep(0.2)
        boundingBox = win32gui.GetWindowRect(hwnd)
        print("Bounding box of window:\t"+str(boundingBox))
        img = ImageGrab.grab(boundingBox)

        return (img, boundingBox)

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
        positions=[]
        i = 0
        j=0
        lettersCollected = ""
        for l in alphabetImages:            
            for sL in screenLetters:
                result = OpenCV.matchTemplate(sL, l,methods[3])
                min_v, max_v, min_loc, max_loc = OpenCV.minMaxLoc(result)
                if max_v > 0.93:
                    lettersCollected += alphabet[i]
                    positions.append(j)

                j += 1
            i += 1
            j = 0
        print(lettersCollected)
        return lettersCollected,positions
    

    def getFilteredWords(screenLetters):
        f_words = []
        for word in allWords:
            w = word.strip().upper()
            if isWordValid(w,screenLetters):
                f_words.append(w)

        return f_words

    def isWordValid(word,letters) :
        for l in word:
            v1 = re.findall(l,word)
            v2 = re.findall(l,letters)


            if len(v1) > len(v2):
               return False

        return True

    def getCoordsFromIndex(i):
        y = i % 4
        x = (i-y) / 4
        return (int(x*64),int(y*64))

            
    # use [string].strip() to remove \n at the end
    handle = getHandleFromTitle("adventures")[0][0]
    world, world_pos = screenshotWindow(handle)

    world = PIL_to_OpenCV(world)
    

    worldLetters, letterPositions =getLettersShown(world)
    worldLetters_copy = (worldLetters+" ").strip()
    

    filtered_words = getFilteredWords(worldLetters)
    filtered_words.sort( key=len)

    print(len(filtered_words),len(allWords))
    print(filtered_words[-10:])
    
    longest_word = filtered_words[-1]
    

    mouse.move(world_pos[0], world_pos[1])
    
    for l in longest_word:
        index = worldLetters_copy.find(l)
        index = letterPositions[index]
        worldLetters_copy = worldLetters_copy.replace(l," ",1)
        
        x,y = getCoordsFromIndex(index)

        x += first_tile_position[0]
        y += first_tile_position[1]
        print(x,y, l, index,worldLetters_copy)

        mouse.move(world_pos[0]+x,world_pos[1]+y,duration=0.2)
        mouse.click("left")
        #time.sleep(0.2)


























if __name__ == '__main__':
    run() #Only runs the code if this is the master file
