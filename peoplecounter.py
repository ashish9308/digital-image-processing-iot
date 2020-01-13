#AI-IOT using ubidots

from imutils.object_detection import non_max_suppression                     
import numpy as np
import imutils
import cv2
import requests
import time
import argparse
import pybase64
import base64

URL_EDUCATIONAL = "http://things.ubidots.com"  
URL_INDUSTRIAL = "http://industrial.api.ubidots.com"  
INDUSTRIAL_USER = True
TOKEN = "Your token"
DEVICE = "Your device name"
VARIABLE = "Your variable name"

HOGCV = cv2.HOGDescriptor()                    
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detector(image):
    image = imutils.resize(image, width=min(400, image.shape[1]))
    clone = image.copy()

    (rects, weights) = HOGCV.detectMultiScale(image, winStride=(8, 8),
                                              padding=(32, 32), scale=1.05)

 
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    result = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    return result

def localDetect(image_path):
    result = []
    image = cv2.imread(image_path)
    if len(image) <= 0:
        print("[ERROR] could not read your local image")
        return result
    print("[INFO] Detecting people")
    result = detector(image)

    # shows the result
    for (xA, yA, xB, yB) in result:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (result, image)


def convert_to_base64(image):
    image = imutils.resize(image, width=400)
    img_str = cv2.imencode('.png', image)[1].tostring()
    b64 = base64.b64encode(img_str)
    return b64.decode('utf-8')


def detectPeople(args):
    image_path = args["image"]
   
    if image_path != None:
        print("[INFO] Image path provided, attempting to read image")
        (result, image) = localDetect(image_path)
        print("[INFO] sending results")
        # Converts the image to base 64 and adds it to the context
        b64 = convert_to_base64(image)
        context = {"image": b64}

        # Sends the result
        req = sendToUbidots(TOKEN, DEVICE, VARIABLE,
                            len(result), context=context)
        if req.status_code >= 400:
            print("[ERROR] Could not send data to Ubidots")
            return req


def buildPayload(variable, value, context):
    return {variable: {"value": value, "context": context}}


def sendToUbidots(token, device, variable, value, context={}, industrial=True):
    # Builds the endpoint
    url = URL_INDUSTRIAL if industrial else URL_EDUCATIONAL
    url = "{}/api/v1.6/devices/{}".format(url, device)

    payload = buildPayload(variable, value, context)
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    attempts = 0
    status = 400

    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    return req


def argsParser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default=None,
                    help="")
    args = vars(ap.parse_args())

    return args


def main():
    args = argsParser()
    detectPeople(args)


main()