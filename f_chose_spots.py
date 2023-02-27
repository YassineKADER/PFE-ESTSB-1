import cv2
import pickle
import json
import requests

def start_chosing(videolocation="video.webm"):
    width, height = 0, 0

    try:
        with open('CarParkPos2', 'rb') as f:
            posList = pickle.load(f)
            f.close()
        with open('config.json', 'rb') as config:
            data = json.load(config)
            width, height = data["width"], data["height"]
            config.close()

    except:
        posList = []


    def empty(a):
        pass


    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)
    cv2.createTrackbar("height", "Parameters", height, 1000, empty)
    cv2.createTrackbar("width", "Parameters", width, 1000, empty)


    def mouseClick(events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            posList.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList.pop(i)

        with open('CarParkPos2', 'wb') as f:
            pickle.dump(posList, f)

    def getImage():
        cap = cv2.VideoCapture(videolocation)
        ret, img = cap.read()
        return img

    while True:
        status =json.loads(requests.get(url="http://127.0.0.1:1212/status").text).get("status")
        print(status)
        if status==False:
            cv2.destroyAllWindows()
            return
        height = cv2.getTrackbarPos("height", "Parameters")
        width = cv2.getTrackbarPos("width", "Parameters")
        if height != data["height"] or width != data["width"]:
            data["height"] = height
            data["width"] = width
            with open("config.json", 'w') as config:
                json.dump(data, config)
                config.close()

        img = getImage()
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Chose Spots", img)
        cv2.setMouseCallback("Chose Spots", mouseClick)
        cv2.waitKey(1)

#start_chosing()