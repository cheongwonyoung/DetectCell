#Server
import subprocess 
from flask import Flask, request # 서버 구현을 위한 falsk 객체 import
import jsonpickle
import cv2
import pymysql
import sys
import json
import os
import base64
from werkzeug.utils import secure_filename
import detect


app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.

@app.route('/file_upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        global temp
        temp = 'tt33/'
        f = request.files['file']
        temp = temp + f.filename
        fname = secure_filename(f.filename)
        path = os.path.join('tt22/', fname)
        f.save(path)

        #os.system('python detect.py --weights ./runs/exp6_yolov4-csp-results/weights/best_yolov4-csp-results.pt --img 2448 --conf 0.4 --source tt22/ --device 2') # detect
        data = subprocess.check_output(['python', 'detect.py', '--weights', './runs/exp6_yolov4-csp-results/weights/best_yolov4-csp-results.pt', '--img', '2448', '--conf', '0.4', '--source', 'tt22/', '--device', '2' ]) 
        
        input_FilePath = 'tt22'
        if os.path.exists(input_FilePath):
            for file in os.scandir(input_FilePath):
                os.remove(file.path)

        return data
       
@app.route('/csv_file_download_with_file')
def csv_file_download_with_file():
    file_name = temp
    data={}
    
    img = cv2.imread(file_name,cv2.IMREAD_COLOR)
    img_str = base64.b64encode(cv2.imencode('.jpg',img)[1]).decode()
    img_dict = {'img':img_str}
    img_dict = json.dumps(img_dict)
    
    output_FilePath = 'tt33'
    if os.path.exists(output_FilePath):
        for file in os.scandir(output_FilePath):
            os.remove(file.path)

    return img_dict

if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0', port=1212)
