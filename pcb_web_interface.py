"""
  Author : Balram Chaudhary
  Connect : linkedin.com/in/balram-chaudhary-855926195/
"""

import streamlit as st
from PIL import Image
import cv2
import numpy as np
import mediapipe as mp
import tempfile
import os
import mapp
import pandas as pd
import base64
PATH = os.getcwd()

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.pexels.com/photos/1105379/pexels-photo-1105379.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=428&w=700")
    }
    </style>
    """,
    unsafe_allow_html=True
)
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

new_title = '<p style="font-family:sans-serif; color:#ffffff; font-size: 42px;">PCB Component and Fault Detection</p>'
st.markdown(new_title,unsafe_allow_html=True)
# st.markdown(

#     """
#     <style>
#     [data-testid = "stSidebar"][aria-expanded="true] > div:first-child{
#         width: 350px
#     }
#     [data-testid="stSidebar"][aria-expanded="false] >div:first-child{
#         width: 350px
#         margin-left: -350px
    
#     }    
#     </style>
#     """,
#     unsafe_allow_html=True, 
# )
st.sidebar.title("Control Center")
st.sidebar.markdown("Choose an appropriate option from below for the precise PCB inspection")


@st.cache()
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = width/float(w)
        dim = (int(w*r),height)
    else:
        r = width/float(w)
        dim = (height,int(h*r))
    
    resized = cv2.resize(image,dim,interpolation=inter)

    return resized

app_mode1 = st.sidebar.selectbox("Type of PCB unit :",["Manufacturing Unit","Service Unit"])


if app_mode1 == "Servicing Unit":
    st.markdown("Sorry for the inconvinience.. This module is currently under development stage")


app_mode2 = st.sidebar.selectbox("Choose the detection mode :",["Image","Video","Camera"])
if app_mode1 == "Manufacturing Unit":
    if app_mode2 == "Image":
        # st.markdown("Please provide valid image of PCB as input for detection..")
        img_file_buffer = st.sidebar.file_uploader("Upload the PCB Image :",type=["jpg","jpeg","png"])
        
        #
        if img_file_buffer:
            
            #image = np.array(Image.open("static/abc.jpg"))
            #breakpoint()
            img_path = PATH + "/static/" + img_file_buffer.name
            with open(img_path,"wb") as f: 
                f.write(img_file_buffer.getbuffer())

            st.sidebar.text("Uploaded image is:")
            st.sidebar.image(Image.open(img_path))
            
            p = mapp.predict_label(img_path)
            prediction= p['present']

            all= ['Resistor', 'Cap3', 'Transformer', 'Transformer', 'Cap4', 'Cap1', 'Cap2', 'MOSFET', 'Mov']
            
            present = [x.split(" ")[0] for x in prediction]
            absent = [x for x in all if x not in present]
            status = '<p style="font-family:sans-serif; color:#FF0000; font-size: 35px;">Status of PCB : Defective </p>'

            if len(absent) ==0:
                absent = ["All components present"]
                global op_image_path
                status = '<p style="font-family:sans-serif; color:#00FF00; font-size: 35px;">Status of PCB : Not Defective </p>'


            st.markdown(status, unsafe_allow_html=True)


            op_image_path = os.path.join(PATH,str(p['save_dir']))
            result_image = np.array(Image.open(os.path.join(op_image_path,img_file_buffer.name)))
            
            df = pd.DataFrame({'Present components':pd.Series(present),"Absent components":pd.Series(absent)}).replace(np.nan, '', regex=True)
            df.index = np.arange(1, len(df)+1)
            st.markdown(
                """
                <style>
                .reportview-container {
                    background: url("https://marathonjetcenter.com/wp-content/uploads/2019/03/animated-lines-on-gray-background-element_4yuscfqex__F0000.png")
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.subheader("Detection Results..")
            st.table(df)
            st.image(result_image)

if app_mode2 == "Video":
    st.markdown("Go to input video")
    stframe = st.empty
    
    video_file_buffer = st.sidebar.file_uploader("Upload Video",type=["mp4","mov","avi","asf","m4v"])
    tffile = tempfile.NamedTemporaryFile(delete=False)
    tffile.write(video_file_buffer.read())

    vid = cv2.VideoCapture(tffile.name)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

if app_mode2 == "Camera":
    st.markdown("Go to connected cam")
    start_vid_detect = st.sidebar.button("Start Detection on video")
    start_img_detect = st.sidebar.button("Take snapshot and detect")

    if start_vid_detect:
        st.checkbox("Detecting..",value=True)

    if start_img_detect:
            st.sidebar.text("Snapped Image")
            st.sidebar.image(frame)
    st.title("Camera view")
    #run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while app_mode2 == "Camera":
        _, frame = camera.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')

