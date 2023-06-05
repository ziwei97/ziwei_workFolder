import os
import tkinter
from tkinter import *
from tkmacosx import Button
from tkinter import Entry
from PIL import ImageTk,Image
from tkinter import messagebox
import download_request
import download_whole_dynamodb_table
import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# def execute_pycharm_function():
#     # 在这里编写你想要执行的PyCharm函数的代码
#     guid = e1.get()
#     subject=""
#     wound=""
#     try:
#         attrs = ["PseudoColor", "Mask"]
#         table = dynamodb.Table("BURN_Master_ImageCollections")
#         download_request.simple_download(table,guid,attrs,"/Users/ziweishi/Desktop/Simple")
#         subject = download_request.get_attribute(table,guid,"SubjectID")
#         wound = download_request.get_attribute(table,guid,"Wound")
#     except:
#         attrs = ["PseudoColor", "Mask","FinalTruth"]
#         table = dynamodb.Table("DFU_Master_ImageCollections")
#         download_request.simple_download(table, guid, attrs, "/Users/ziweishi/Desktop/Simple")
#         subject = download_request.get_attribute(table, guid, "SubjectID")
#         wound = download_request.get_attribute(table, guid, "Wound")



# 创建主窗口
root = Tk()
root.title("输入查询ImgCollGUID")
root.geometry('600x400')


canvas = tkinter.Canvas(root, width=600, height=400, bd=0, highlightthickness=0)
imgpath = '/Users/ziweishi/Desktop/WechatIMG12.jpeg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas.create_image(600, 400, image=photo)
canvas.pack()

btn = tkinter.Button(text='点我！') # 定义一个按钮
btn.config(width=10, height=5)
btn.pack() # 打包到父部件

en = Entry()
en.config(bg='yellow')
en.pack()





#
# def msgbox(collection_info):
#     messagebox.showinfo("结果",collection_info)


# 创建按钮
# param = "DFU"
# guid= "25e532e4-36cb-42d6-9e19-19cb285827e3"
# button = Button(root, text="执行PyCharm函数", command=lambda:execute_pycharm_function())

# Button(root,text="查询图片",command=lambda :execute_pycharm_function()).pack

# e1 = Entry(root)



# 运行主循环
root.mainloop()
