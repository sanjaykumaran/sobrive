import dlib
import cv2
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import pandas as pd
import numpy as np
import os

col_names = []
value = []
for i in range(0,68):
    name_X = "x" + str(i)
    name_Y = "y" + str(i)
    col_names.append(name_X)
    col_names.append(name_Y)
    value.append(0)
    value.append(0)

col_names.append("type")
value.append("drunk")

df = pd.DataFrame(columns = col_names)
df.loc[0] = value

for folder in os.listdir("."):
    if folder == "drunk1" or folder == "drunk2" or folder == "drunk3" or folder == "sober":
        for files in os.listdir(folder):
            print(files)
            image = cv2.imread(os.path.join(folder,files))
            #cv2.imshow("Output", image)

            #step2: converts to gray image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            #step3: get HOG face detector and faces
            hogFaceDetector = dlib.get_frontal_face_detector()

            #landmark predictor
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            rects = hogFaceDetector(gray, 1)

            #step4: loop through each face and draw a rect around it
            feature_list=[]
            i=0
            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                # Draw on our image, all the finded cordinate points (x,y) 
                for (x, y) in shape:
                    cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
                    feature_list.append(x)
                    feature_list.append(y)

            if files.endswith("_1.png"):
                feature_list.append("Sober")
            elif files.endswith("_2.png"):
                feature_list.append("Drunk")
            elif files.endswith("_3.png"):
                feature_list.append("Drunk")
            elif files.endswith("_4.png"):
                feature_list.append("Drunk")
            
            if (len(feature_list) == 137):
                df.loc[len(df.index)] = feature_list
        

df.to_csv("fulldata.csv", sep='\t')