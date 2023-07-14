import os
import numpy as np
import cv2 as cv 
from dotenv import load_dotenv

load_dotenv()

URI_CAM = os.getenv('URI_CAM')

# load yolo
net = cv.dnn.readNet("models\yolov3\yolov3.cfg","models\yolov3\yolov3.weights")
clasees = []
with open("coco.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# print(classes)
layer_name = net.getLayerNames()
output_layer = [layer_name[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# webcam
# cap = cv.VideoCapture(0)
# uri_cam = "rtsp://admin:Adminsds1@172.16.112.137/Streaming/Channels/102"
# uri_cam = 'rtsp://admin:l4bhcmlt9@192.168.9.250:8554/Streaming/Channels/102'
cap = cv.VideoCapture(URI_CAM)

#check camera is opened successfully
if(cap.isOpened() == False):
    print("Error opening camera")

#read video until finish
while(cap.isOpened()):
    #capture frame by frame
    ret, frame = cap.read()
    # frame = cv.resize(frame, (500, 500))
    if ret == True:
        # img = cv.resize(frame, None, fx=0.4, fy=0.4)
        img = frame
        height, width, channel = img.shape

        # Detect Objects
        blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layer)
        # print(outs)

        # Showing Information on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detection
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # cv.circle(img, (center_x, center_y), 10, (0, 255, 0), 2 )
                    # Reactangle Cordinate
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    boxes.append([x, y, w, h])
                    
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # print(len(boxes))
        # number_object_detection = len(boxes)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # print(indexes)

        font = cv.FONT_HERSHEY_PLAIN
        count_person = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                # print(label)
                color = colors[i]
                # print(label)
                if label == 'person':
                    count_person.append(label)
                    # cv.putText(img, str(len(count_person)), (x, y + 30), font, 3, color, 3)
                    cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                print("Number of person: {person} person".format(person=len(count_person)))
                # cv.imshow("IMG", img)
                    # print(len(count_person))
        #press Q to logout
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

#release video capture object
cap.release()
#close all frames
cv.destroyAllWindows()

