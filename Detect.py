# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 10:28:15 2021

@author: Iyad, Laith, Yaman
"""

import json
import jpegio as jio
import re
from PIL import Image
from PIL.ExifTags import TAGS

imagefile = 'D:/Multimedia/Assignment3/Multimedia Final/Original/2.jpg'
AppDBfile = 'AppsDB.json'
SourcesDBfile = 'SourcesDB.json'

jpeg1 = jio.read(imagefile)  
QTableY = jpeg1.quant_tables[0]
QTableC = jpeg1.quant_tables[1]
print("Image File: {}".format(imagefile))
print("Quantization Tables for the image:")
print ("Luminance Quantization Table:\n{}\n\nChrominance Quantization Table:\n{}".format(QTableY,QTableC))


def readExif (filename):
    image = Image.open(filename) 
    exifdata = image.getexif()
    print("\nExtracting EXIF Data from the image...")
    for tag_id in exifdata:
        tag = TAGS.get(tag_id)  # get the tag name from tag id
        data = exifdata.get(tag_id)
        if (tag == "Make" or tag == "Model" or tag=="Software"):
            print(f"{tag:25}: {data}")
        
          

DCdetected = False
with open(AppDBfile, "r") as file:
    data = json.load(file)
    if type(data) is dict:
        data = [data]   
    for record in data:
        Ycompared = record['QTableY']==QTableY
        Ccompared = record['QTableC']==QTableC
        if ((Ycompared.sum()/64) == 1.0 and (Ccompared.sum()/64==1.0)):
            print("Checking...{} with Qualty factor:{}, QT Similarity: %{}".format(record['Application'], record['Quality Factor'], (Ycompared.sum()/64*100)))
            print("\nDouble Compression detected...\nImage modified using {} with Qualty factor:{}, Similarity: %100\n".format(record['Application'], record['Quality Factor']))
            DCdetected=True
            #break
        else: 
            print("Checking...{} with Qualty factor:{}, QTL Similarity: %{}".format(record['Application'], record['Quality Factor'], (Ycompared.sum()/64*100)))

#if DCdetected==False:
print ("\nChecking image source...")
with open(SourcesDBfile, "r") as file:
    data = json.load(file)
    if type(data) is dict:
        data = [data]
    OriginalImage = False
    for record in data:
        #print(record['QTableY'])  
        Ycompared = record['QTableY']==QTableY
        Ccompared = record['QTableC']==QTableC
        if ((Ycompared.sum()/64) == 1.0 and (Ccompared.sum()/64==1.0)):
            print("Checking...{} Model number:{}, QT Similarity: %{}".format(record['Source'], record['Model'], (Ycompared.sum()/64*100)))
            print("\nOriginal image taken from {} Model number: {}\n".format(record['Source'], record['Model']))
            OriginalImage=True
            break
        else: 
            print("Checking...{} Model number:{}, QT Similarity: %{}".format(record['Source'], record['Model'], (Ycompared.sum()/64*100)))
            
    
if(DCdetected==True and OriginalImage==True):
    print("Warning: This could be a false postive result.")
    
readExif(imagefile)
    
if (OriginalImage == False and DCdetected==False):
    print ("\nQT Not found in database...\n Do you want to add it as original image source or image edit application?")
    print("1. Add this QT to Image editing software database.")
    print("2. Add this QT to Image Sources database.")
    print("3. Do not add QT to database.")
    MenuChoice = int(input("\nEnter your choice number:"))
    if MenuChoice==1:       
        filename = 'AppsDB.json'
        app=input("Enter Application Name:")
        qf= int(input("Enter Quality Factor:"))
        entry = {'QTableY':QTableY.tolist(),'QTableC':QTableC.tolist(),
                 'Application':app, "Quality Factor": qf}
        with open(filename, "r+") as file:
            data = json.load(file)
            if type(data) is dict:
                data = [data]
            data.append(entry)
            file.seek(0)
            json.dump(data, file)
            file.close()
            print("Added Successfuly")
        
        with open(filename, "r+") as f:
            text = f.read()
            text = re.sub('},', '},\n', text)
            f.seek(0)
            f.write(text)
            f.truncate()
            
    elif MenuChoice==2:
        filename = 'SourcesDB.json'
        source=input("Enter image soucre name or device name:")
        model= input("Enter Model name:")
        entry = {'QTableY':QTableY.tolist(),'QTableC':QTableC.tolist(),
                 'Source':source, "Model": model}
        with open(filename, "r+") as file:
            data = json.load(file)
            if type(data) is dict:
                data = [data]
            data.append(entry)
            file.seek(0)
            json.dump(data, file)
            file.close()
            print("Added Successfuly")
        
        with open(filename, "r+") as f:
            text = f.read()
            text = re.sub('},', '},\n', text)
            f.seek(0)
            f.write(text)
            f.truncate()
    else:
        print("Canceled")



            
    
