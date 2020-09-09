import cv2
import pytesseract
import numpy as np
import os, sys
import pandas as pd



def DumCategory(data): #function that creates key based category
    KeyCategory = {}
    count = 0
    for k in data:
        if k.isupper():
            KeyCategory[k] = count
            count += 1
        else:
            count += 1
    return KeyCategory



#Create dummy categories
def createDummyCategory(Categories, gauge):
    DummyCategory = []
    start, stop = 0, 0
    try:
        for k in Categories.values():
            start = k
            mm = list(Categories.values()).index(k)+1
            stop = list(Categories.values())[mm]
            for f in range(start, stop):
                DummyCategory.append(list(Categories.keys())[mm-1])
    except IndexError:
        start = k
        mm = list(Categories.values()).index(k)+1
        stop = gauge
        for f in range(start, stop):
            DummyCategory.append(list(Categories.keys())[mm-1])
        
    return DummyCategory




#re-shape data into matching extracted dummy based categories
def CutData(data, data_keys):
    try:
        first = list(data_keys.keys())[0]
        index= data.index(first)
        out = data[index:]
    except IndexError:
        out = data
    
    return out


#validate data dimension
def confirmDimension(a,b):
    if len(a) == len(b):
        return True
    else:
        return False
    

#extract prices from data using CheckIntNum
def CheckIntNum(data):
    indexes = []
    CountTrue = 0
    dataSplit = data.split(' ')
    jint = 0
    for j in dataSplit:
        try:
            jint = float(j)
            CountTrue+= 1
            indexes.append(dataSplit.index(j))
        except ValueError:
            pass
    return CountTrue, indexes


#concatenate descritions and Names present in the data
def concatName(data, start, stop):
    #start and stop are both starting and ending indexes
    outString = ''
    for f in data[start:stop]:
        outString = outString + f + ' '
        
    return outString

#extract prices, name, description and category
def ExtractDetails(InputData,dummyCategory):
    Categories = {}#Name as key, dummyCategory and price as a tuple
    for i, j in zip(InputData, dummyCategory):
        dataSplit = i.split(' ')
        if CheckIntNum(i)[0] >0:
            valOne, valTwo = CheckIntNum(i)
            start = 0
            for th in range(valOne):
                description = InputData[InputData.index(i) - 1]
                if CheckIntNum(description)[0] >0:
                    description = 'Nil'
                else:
                    pass
                stop = valTwo[th]
                Name = concatName(dataSplit, start, stop)
                price = dataSplit[stop]
                Categories[Name] = (j, price, description)
                start = stop+1
    return Categories

#convert data into a dataframe
def FrameData(cate):
    keys, Name, price, description = [], [], [],[]
    for k in cate.keys():
        keys.append(k)
        Name.append(cate[k][0])
        price.append(cate[k][1])
        description.append(cate[k][2])
        
    DictFrame = {'Categories':Name, 'Name':keys, 'Description':description, 'price':price}
    frame = pd.DataFrame(DictFrame)
    return frame



def main(directory , image):
    #load image into directory and convert to black and white

    os.chdir(directory)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)
    #cv2.imshow('image', gray)

    #extract text in image using pytesseract
    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)

    #split extracted text by new lines
    splitByNewLines = out_below.split('\n')

    #create a dummy Key category
    KeyCategory = DumCategory(splitByNewLines) # create key based categories
    gauge = len(splitByNewLines)
    dummyCategory = createDummyCategory(KeyCategory, gauge) #create dummy based categories

    InputData = CutData(splitByNewLines, KeyCategory) #re-shape data into matching extracted dummy based categories

    out = confirmDimension(InputData, dummyCategory) #confirm data dimension


    Categories = ExtractDetails(InputData,dummyCategory) #extract prices, name, description and category

    
    frame = FrameData(Categories)
    print(frame.head())
    frame_name = image.split('.')[0] +'.xlsx'
    frame.to_excel(frame_name)
    return 



if __name__ == '__main__':
    directory = '/home/odemakinde/Desktop/Image to Excel/Image-to-Excel/test images/'
    image = 'menu2.jpg' #save image as 'imagename' + '.xlsx'
    main(directory, image)




