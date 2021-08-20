import os

def reset():
    input_FilePath = '../../tt22'
    if os.path.exists(input_FilePath):
        for file in os.scandir(input_FilePath):
            os.remove(file.path)

    output_FilePath = '../../tt33'
    if os.path.exists(output_FilePath):
        for file in os.scandir(output_FilePath):
            os.remove(file.path)