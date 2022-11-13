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
import pickle
from PIL import Image
import streamlit as st

col_names = []
value = []
for i in range(0,68):
    name_X = "x" + str(i)
    name_Y = "y" + str(i)
    col_names.append(name_X)
    col_names.append(name_Y)
    value.append(0)
    value.append(0)

df = pd.DataFrame(columns = col_names)
df.loc[0] = value

#@st.cache(allow_output_mutation=True)
st.write("""
         # Soberive
         """
         )
filename = st.file_uploader("Please upload a face scan photo", type=["jpg", "png"])
if filename != None:
    image = Image.open(filename)
    st.image(image, use_column_width=True)
    print(filename)
    filename = "image.jpg" + "_new.png"
    print(filename)
    image.save(filename)
    print("after .save")
    image = cv2.imread(filename)
    print("after .imread")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hogFaceDetector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    rects = hogFaceDetector(gray, 1)
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

    #print(feature_list)
    if (len(feature_list) == 136):
        df.loc[len(df.index)] = feature_list
        df = df.iloc[1: , :]
        filename = "finalized_model.sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        y_pred = loaded_model.predict(df)
        print(y_pred[0])
        if(y_pred[0] == 0):
            st.write("## Sober ##")
        else:
            st.write("# Drunk #")
    else:
        print("Error encountered in image parsing!")

#import glob
#jpg_test = glob.glob('image.jpg')
#png_test = glob.glob('test.png')

#if (len(jpg_test)==0 and len(png_test)==1):
#    filename = "test.png"
#else:
#    filename = "test.jpg"


#image_show = Image.open(filename)
#st.image(image_show, use_column_width=True)


