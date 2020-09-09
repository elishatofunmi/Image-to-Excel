import cv2
import pytesseract
import numpy as np
import os, sys
import pandas as pd


def engageData(out):
    DictData = {}
    for k in out:
        try:
            listData = k.strip(' ').split(' / ')
            DictData[listData[0]] = listData[1]
        except:
            DictData[listData[0]] = 'nil'

        
    return DictData


def FrameData(cate):
    Name, description = [], []
    for k in cate.keys():
        Name.append(k)
        description.append(cate[k])
        
    DictFrame = {'Name':Name, 'description':description}
    frame = pd.DataFrame(DictFrame)
    return frame


def main(image, directory):
    os.getcwd()
    os.chdir(directory)

    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)


    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)

    out = []
    for k in out_below.split('-'):
        out.append(k.replace('\n', ''))

    DictData = engageData(out)

    
    frame = FrameData(DictData)
    print(frame.head())
    fileName = image.split('.')[0] + '.xlsx'
    frame.to_excel(fileName)
    return


if __name__ == '__main__':
    image = 'menu.jpg'
    directory = '/home/odemakinde/Desktop/Image to Excel/Image-to-Excel/test images/'
    main(image, directory)