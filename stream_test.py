import streamlit as st
from PIL import Image
import os
import ttss
import numpy as np
import requests
import cv2
import base64
import json

@st.cache # 변경 사항을 감지하기 위해
def load_image(img):
    im = Image.open(img)
    return im

def main():
    """Cell Detection App"""

    st.title("Cell Detection App") # 글 작성
    st.text("Build with Streamlit and OpenCV") # 글 작성

    activities = ["Detection"] # 선택지
    choice = st.sidebar.selectbox("Select Activity", activities) # 선택지 넣어 사이드 셀렉박스 만들기

    ttss.reset() # 폴더 초기화

    if choice == 'Detection': # 셀렉박스가 'Detection'일때

        # slider in sidebar
        #conf_thres = st.sidebar.slider("conf_thres", value=0.4, min_value=0.0, max_value=1.0, step=0.1)
        #iou_thres = st.sidebar.slider("iou_thres", value=0.5, min_value=0.0, max_value=1.0, step=0.1)
        #st.sidebar.write('conf = ', conf_thres)
        #st.sidebar.write('iou = ', iou_thres)

        st.subheader("Cell Detection") # 소제목
        enhance_type = st.sidebar.radio("File , Folder", ["File", "Folder"])



        if enhance_type == 'File':
            image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])  # 세가지 종류 타입 이미지 업로드 가능
            if image_file is not None:
                conf_thres = st.slider("conf_thres", value=0.4, min_value=0.0, max_value=1.0, step=0.1)
                iou_thres = st.slider("iou_thres", value=0.5, min_value=0.0, max_value=1.0, step=0.1)
                st.write('conf = ', conf_thres)
                st.write('iou = ', iou_thres)
                if st.button("Detect Cells"):  # Detect 버튼 생성
                    # show input image
                    #img = load_image(image_file)
                    #st.image(img)
                    st.success('In Progress...')
                    # save to /tt22
                    with open(os.path.join("../../tt22", image_file.name), "wb") as f:
                        f.write(image_file.getbuffer())
                    #st.success("Saved File")
                    #st.success("Wait Please...")


                    # to server(value)
                    val = {"conf":conf_thres,
                           "iou":iou_thres}
                    _ = requests.post('http://210.115.242.180:1212/data_upload', data=json.dumps(val))
                    # json.dumps is dict->str
                    # json.dumps를 안하고 val을 보내면 byte로 보내짐

                    # to server
                    files = open(os.path.join("../../tt22", image_file.name), 'rb')
                    upload = {'file': files}
                    ress = requests.post('http://210.115.242.180:1212/file_upload', files=upload)
                    # dict 구조로 파일을 보냄
                    st.write("image name : " + image_file.name +ress.content.decode('utf-8'))
                    # byte to str

                    # from server
                    res = requests.get('http://210.115.242.180:1212/csv_file_download_with_file')
                    res = res.content.decode('utf-8') # requests.models.Response - > str
                    res = eval(res)
                    img = res['img']
                    img = base64.b64decode(img) 
                    jpg_arr = np.frombuffer(img, dtype=np.uint8)
                    img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)
                    st.image(img)

        if enhance_type == 'Folder':
            multi_file = st.file_uploader("Upload Multi Image", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
            if multi_file is not None:
                conf_thres = st.slider("conf_thres", value=0.4, min_value=0.0, max_value=1.0, step=0.1)
                iou_thres = st.slider("iou_thres", value=0.5, min_value=0.0, max_value=1.0, step=0.1)
                st.write('conf = ', conf_thres)
                st.write('iou = ', iou_thres)
                if st.button("Detect Cells"):  # Detect 버튼 생성
                    t1 = ''
                    st.success('In Progress...')
                    for i, image_file in enumerate(multi_file):

                        #bytes_data = image_file.read()
                        #st.success("======================== "+ str(i+1) +" image ============================")
                        #st.image(bytes_data)

                        with open(os.path.join("../../tt22", image_file.name), "wb") as f:
                            f.write(image_file.getbuffer())
                        #st.success("Saved File")
                        #st.success("Wait Please...")

                        # to server(value)
                        val = {"conf": conf_thres,
                               "iou": iou_thres}
                        _ = requests.post('http://210.115.242.180:1212/data_upload', data=json.dumps(val))

                        # to server
                        files = open(os.path.join("../../tt22", image_file.name), 'rb')
                        upload = {'file': files}
                        ress = requests.post('http://210.115.242.180:1212/file_upload', files=upload)

                        t1 = t1 + str(i+1) + "st image name : " + image_file.name + ress.content.decode('utf-8') + '\n'

                        #st.write(ress.content.decode('utf-8'))

                        # from server
                        res = requests.get('http://210.115.242.180:1212/csv_file_download_with_file')
                        res = res.content.decode('utf-8')
                        res = eval(res)
                        img = res['img']
                        img = base64.b64decode(img)
                        jpg_arr = np.frombuffer(img, dtype=np.uint8)
                        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

                        st.image(img)
                    st.write(t1)

if __name__ == '__main__':
        main()
