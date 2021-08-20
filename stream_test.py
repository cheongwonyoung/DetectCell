import streamlit as st
from PIL import Image
import os
import ttss
import numpy as np
import requests
import cv2
import base64

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
        st.subheader("Cell Detection") # 소제목
        enhance_type = st.sidebar.radio("File , Folder", ["File", "Folder"])


        if enhance_type == 'File':
            image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])  # 세가지 종류 타입 이미지 업로드 가능
            if image_file is not None:

                # show input image
                img = load_image(image_file)
                st.image(img)


                if st.button("Detect Cells"):  # Detect 버튼 생성
                    # save to /tt22
                    with open(os.path.join("../../tt22", image_file.name), "wb") as f:
                        f.write(image_file.getbuffer())
                    st.success("Saved File")
                    st.success("Wait Please...")

                    # to server
                    files = open(os.path.join("../../tt22", image_file.name), 'rb')
                    upload = {'file': files}
                    ress = requests.post('http://210.115.242.180:1212/file_upload', files=upload)
                    st.write(ress.content)

                    # from server
                    res = requests.get('http://210.115.242.180:1212/csv_file_download_with_file')
                    res = res.content.decode('utf-8')
                    res = eval(res)
                    img = res['img']
                    img = base64.b64decode(img)
                    jpg_arr = np.frombuffer(img, dtype=np.uint8)
                    img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)
                    st.image(img)

        if enhance_type == 'Folder':
            multi_file = st.file_uploader("Upload Multi Image", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
            if multi_file is not None:
                if st.button("Detect Cells"):  # Detect 버튼 생성
                    for i, image_file in enumerate(multi_file):
                        bytes_data = image_file.read()
                        st.success("======================== "+ str(i+1) +" image ============================")
                        st.image(bytes_data)

                        with open(os.path.join("../../tt22", image_file.name), "wb") as f:
                            f.write(image_file.getbuffer())
                        st.success("Saved File")
                        st.success("Wait Please...")

                        files = open(os.path.join("../../tt22", image_file.name), 'rb')
                        upload = {'file': files}
                        ress = requests.post('http://210.115.242.180:1212/file_upload', files=upload)
                        st.write(ress.content)

                        res = requests.get('http://210.115.242.180:1212/csv_file_download_with_file')
                        res = res.content.decode('utf-8')
                        res = eval(res)
                        img = res['img']
                        img = base64.b64decode(img)
                        jpg_arr = np.frombuffer(img, dtype=np.uint8)
                        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

                        st.image(img)

if __name__ == '__main__':
        main()
