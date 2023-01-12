import cv2
import pickle
import numpy as np
import time
import json

cap = cv2.VideoCapture('video.webm')
width, height = 107, 250
with open('CarParkPos2', 'rb') as f:
    posList = pickle.load(f)
    with open('config.json', 'rb') as config:
        data = json.load(config)
        width, height = data["width"], data["height"]
        config.close()


def empty(a):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("blockSize", "Parameters", data["blockSize"], 50, empty)
cv2.createTrackbar("C", "Parameters", data["C"], 50, empty)
cv2.createTrackbar("ksize_Blur", "Parameters", data["ksize_Blur"], 50, empty)


def checkSpaces():
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)
            thic = 5
            spaces += 1

        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)
    return [spaces, len(posList)]

try:
    while True:

        # Get image frame
        success, img = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # img = cv2.imread('img.png')
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)

        blockSize = cv2.getTrackbarPos("blockSize", "Parameters")
        C = cv2.getTrackbarPos("C", "Parameters")
        ksize_Blur = cv2.getTrackbarPos("ksize_Blur", "Parameters")
        if blockSize != data["blockSize"] or C != data["C"] or ksize_Blur !=data["ksize_Blur"]:
            data["blockSize"] = blockSize
            data["C"] = C
            data["ksize_Blur"] = ksize_Blur
            with open("config.json", 'w') as config:
                json.dump(data, config)
                config.close()
        if blockSize % 2 == 0: blockSize += 1
        if ksize_Blur % 2 == 0: ksize_Blur += 1
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, blockSize, C)
        imgThres = cv2.medianBlur(imgThres, ksize_Blur)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)

        print(checkSpaces())
        # Display Output

        cv2.imshow("Image", img)
        cv2.imshow("ImageGray", imgThres)
        cv2.imshow("ImageBlur", imgBlur)
        key = cv2.waitKey(1)
        time.sleep(0.5)#just for testing
        print(blockSize, C, ksize_Blur)
        if key == ord('r'):
            pass
except:
    print("The programme is finished")