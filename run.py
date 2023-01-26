import cv2
import pickle
import numpy as np
import time
import json
import traceback
from datetime import date, datetime
import pyrebase
import requests

config = {
    "apiKey": "AIzaSyBgGx67w032_zncuZ37tFYPrm02rH1XbrY",
    "authDomain": "wise-baton-353710.firebaseapp.com",
    "databaseURL": "https://wise-baton-353710-default-rtdb.firebaseio.com",
    "projectId": "wise-baton-353710",
    "storageBucket": "wise-baton-353710.appspot.com",
    "messagingSenderId": "962857669223",
    "appId": "1:962857669223:web:3360987f13c2f1e6787ac2"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#TODO make the falsk project for the app
width, height = 107, 250
with open('CarParkPos2', 'rb') as f:
    posList = pickle.load(f)
    with open('config.json', 'rb') as config:
        data = json.load(config)
        width, height = data["width"], data["height"]
        config.close()


def empty(a):
    pass

def update_data():
    pass


def start(perview, user_token, user_id, video_location="video.webm"):
    #print("hh1")
    cap = cv2.VideoCapture(video_location)
    now = datetime.now()
    status = False
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
            #cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,color, 2)
        return [spaces, len(posList)]
    #print("hh2")
    try:
        if perview :
            cv2.namedWindow("Parameters"+str(now))
            cv2.resizeWindow("Parameters"+str(now), 640, 240)
            cv2.createTrackbar("blockSize", "Parameters"+str(now), data["blockSize"], 50, empty)
            cv2.createTrackbar("C", "Parameters"+str(now), data["C"], 50, empty)
            cv2.createTrackbar("ksize_Blur", "Parameters"+str(now), data["ksize_Blur"], 50, empty)
            #print("hh3")
        next = []
        perv = next
        max_data_check = db.child("Users").child(user_id).child("maxSizeAtDay").child(str(date.today())).get().val()
        if max_data_check is None:
            max_data_check = 0
        while True:
            status = json.loads(requests.get(url="http://127.0.0.1:1212/status").text).get("status")
            print(status)
            blockSize = data["blockSize"]
            C = data["C"]
            ksize_Blur = data["ksize_Blur"]
            # Get image frame
            success, img = cap.read()
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # img = cv2.imread('img.png')
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)
            if perview:
                blockSize = cv2.getTrackbarPos("blockSize", "Parameters"+str(now))
                C = cv2.getTrackbarPos("C", "Parameters"+str(now))
                ksize_Blur = cv2.getTrackbarPos("ksize_Blur", "Parameters"+str(now))
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
            perv = next
            next = checkSpaces()
            if next != perv:
                cv2.imwrite("static/pos.png",img=img)
                db.child("Users").child(user_id).update({"freespace":next[0],"totalplace":next[1]}, token=user_token)
                new_max_data_check = next[1]-next[0]
                if new_max_data_check > max_data_check:
                    db.child("Users").child(user_id).child("maxSizeAtDay").update({str(date.today()):new_max_data_check}, token=user_token)
                    max_data_check = new_max_data_check
            # Display Output
            #print("hh5")
            if perview :
                cv2.imshow("Image"+str(now), img)
                cv2.imshow("ImageGray"+str(now), imgThres)
                cv2.imshow("ImageBlur"+str(now), imgBlur)
            if cv2.waitKey(2) & 0xFF==ord('d'):
                break
            #time.sleep(0.5)#just for testing
            print(blockSize, C, ksize_Blur)
            if status == False:
                cap.release()
                cv2.destroyAllWindows()
                return 1
        cap.release()
        cv2.destroyAllWindows()
    except: 
        cap.release()
        cv2.destroyAllWindows()
        traceback.print_exc()
        return

#start(True,"eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNTU5YzU5MDgzZDc3YWI2NDUxOThiNTIxZmM4ZmVmZmVlZmJkNjIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2lzZS1iYXRvbi0zNTM3MTAiLCJhdWQiOiJ3aXNlLWJhdG9uLTM1MzcxMCIsImF1dGhfdGltZSI6MTY3NDQwNDU2NCwidXNlcl9pZCI6IkFBcDM1RmdOT0dQNnBkaWg2M0JQRVJ0VGlrdTEiLCJzdWIiOiJBQXAzNUZnTk9HUDZwZGloNjNCUEVSdFRpa3UxIiwiaWF0IjoxNjc0NDA0NTY0LCJleHAiOjE2NzQ0MDgxNjQsImVtYWlsIjoiYWRtaW5AbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYWRtaW5AbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.GO1SS1hZYmpaCKG89Wqz_Y_vKEyyM9oPUZaxTkGLsAXaggUVG_75WsUNPV-QLyj0wMHrVt9KawkrJk7cJfi0y5nOHEz4dugKqwcTfG4xRECokZUcQnn1txi8VVbf0_tdFXwY1VsX6G9ZFVp-Liv63odaw1f-hTtPxzwRtZ8Bz0DTuJ-IQ2cWUBoObcghYv9KXWatfj2fCP0r6vSee3RrPVyzw80p03jzSrQsevwZ22_o3tER0fy2YpMgCKE_X3GGyp0DN69FauKB6mi0NoXO2M_Kf85bHl9kMTTStC-QFoD8WOiEwvcbsDv1OUoLJcWTORZ_gRAvN6ib7tZMBWE8ZA","AAp35FgNOGP6pdih63BPERtTiku1", video_location="video.webm")