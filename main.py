
def run():

    from PIL import ImageGrab
    import win32gui
    import win32com.client

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

    first_tile_position = (425, 465)
    attack_button_position = (415,740)

    methods = [OpenCV.TM_CCOEFF,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_CCORR,OpenCV.TM_CCOEFF_NORMED,OpenCV.TM_SQDIFF,OpenCV.TM_SQDIFF_NORMED]

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabetImages = []
    for a in alphabet:
        alphabetImages.append(OpenCV.imread("assets/"+a+".png",0))

    def PIL_to_OpenCV(img):
        numpy_img = numpy.array(img)
        cv_image = OpenCV.cvtColor(numpy_img, OpenCV.COLOR_RGB2GRAY)

        return cv_image

    def PIL_to_OpenCV_RGB(img):
        numpy_img = numpy.array(img)
        cv_image = OpenCV.cvtColor(numpy_img, OpenCV.COLOR_RGB2BGR)

        b = cv_image[:,:,0]
        g = cv_image[:,:,1]
        r = cv_image[:,:,2]


        return b,g,r


    def getHandleFromTitle(t, exact=False):
        toplist, windowList = [], []
        def getAllWindows(hwnd, results):
            windowList.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(getAllWindows, toplist)
        if exact:
            return[(hwnd,title) for hwnd, title in windowList if t == title]
        else:
            return [(hwnd,title) for hwnd, title in windowList if t in title.lower()]

    def switchWindow(hwnd):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    def screenshotWindow(hwnd):
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2)
        boundingBox = win32gui.GetWindowRect(hwnd)
        print("Bounding box of window:\t"+str(boundingBox))
        img = ImageGrab.grab(boundingBox)

        return (img, boundingBox)

    def getAttackPixel():
        x = attack_button_position[0] + world_pos[0]
        y = attack_button_position[1] + world_pos[0]

        bBox = (x,y,x+1,y+1)

        img = ImageGrab.grab(bBox)
        return PIL_to_OpenCV(img)


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

        def matchImages(current, images, i):
            j = 0
            letters = ""
           
            for img in images:
                result = OpenCV.matchTemplate(img,current, methods[3])
                min_v, max_v, min_loc, max_loc = OpenCV.minMaxLoc(result)
                if max_v > 0.90 and j not in positions:
                    letters+= alphabet[i]
                    positions.append(j)

                j += 1
            i += 1
            return letters
  
        b_images = getWorldLetterImages(world[0])
        g_images = getWorldLetterImages(world[1])
        r_images = getWorldLetterImages(world[2])

        positions=[]
        i = 0
        lettersCollected = ""

        for l in alphabetImages:            
            lettersCollected += matchImages(l, b_images, i)
            lettersCollected += matchImages(l, g_images, i)
            lettersCollected += matchImages(l, r_images, i)
            i += 1;
        print(lettersCollected, positions)
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

    def removeWord(word):
        i = allWords.index(word.lower()+"\n")
        del allWords[i]
        f = open("english_words_edited.txt", "w")

        for w in allWords:
            if len(w) > 3:
                f.write(w)

        f.close

    def cancelWord():
        x = 270 + world_pos[0]
        y = 225 + world_pos[1]
        bBox = (x,y,x+400,y+1)

        img = ImageGrab.grab(bBox)
        img = PIL_to_OpenCV(img)

        line = img[0]
        
        for br in line:
            x += 1
            if br > 200:
                mouse.move(x,y,duration = 0.1)
                mouse.click('left')
                break


            
    # use [string].strip() to remove \n at the end
    bookworm_handle = getHandleFromTitle("adventures")[0][0]
    ps_handle = getHandleFromTitle("powershell")[0][0]

    print(ps_handle,bookworm_handle)




    while True:
        world, world_pos = screenshotWindow(bookworm_handle)
        world = PIL_to_OpenCV_RGB(world)
    

        worldLetters, letterPositions =getLettersShown(world)
        inRound = True
        filtered_words = getFilteredWords(worldLetters)
        filtered_words.sort( key=len)

        while inRound: 

            
            worldLetters_copy = (worldLetters+" ").strip()
            longest_word = filtered_words[-1]
            print("Current Word: "+longest_word)
            pl = ""
            for l in longest_word:
                index = worldLetters_copy.find(l)
                index = letterPositions[index]
                worldLetters_copy = worldLetters_copy.replace(l," ",1)
                
                if pl == 'Q' and l=='U':
                    continue
                x,y = getCoordsFromIndex(index)

                x += first_tile_position[0]
                y += first_tile_position[1]
                #print(x,y, l, index,worldLetters_copy)

                mouse.move(world_pos[0]+x,world_pos[1]+y,duration=0.05)
                mouse.click("left")
                pl = l
                
            time.sleep(0.1)
            attack_pixel = getAttackPixel()[0][0]

            if attack_pixel > 155:
                mouse.move(attack_button_position[0],attack_button_position[1], duration=0.1)
                mouse.click('left')
                time.sleep(5)
                switchWindow(ps_handle)

                choice = input("GO? ")
                if choice == "n":
                    quit()
                while choice == " ":
                    switchWindow(bookworm_handle)
                    time.sleep(4)
                    switchWindow(ps_handle)
                    choice = input("GO? ")

                switchWindow(bookworm_handle)

                inRound = False
            else:
                print("Removed word: "+longest_word)
                removeWord(longest_word)
                del filtered_words[-1]
                cancelWord()
                time.sleep(0.1)




    


















if __name__ == '__main__':
    run() #Only runs the code if this is the master file
