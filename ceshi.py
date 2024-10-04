from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import pyautogui
import tkinter as tk
from tkinter import ttk

page = ChromiumPage()
ac = Actions(page)

# connect = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').text
# title = page.ele('xpath://*[@id="dc-normal-body"]/div[3]/div[1]/div[1]/div[2]/h1').text
# img = page.ele('xpath://*[@id="ArticleContent"]/div[2]/div').eles('tag:img')
# print(img)
# imgList = img.get.links()
# print(imgList)


mainWindow = tk.Tk()
mainWindow.title('自动化')
mainWindow.geometry('600x800')


releaseType = tk.StringVar(value='0')
label = tk.Label(mainWindow, text="发布平台")
label.pack()
radio_button1 = tk.Radiobutton(mainWindow, text='发布平台',variable=releaseType,value='0',anchor='nw',padx=20, pady=20, justify=LEFT)
radio_button1.pack()
radio_button2 = tk.Radiobutton(mainWindow, text='公众号',variable=releaseType,value='1',anchor='nw',padx=20, pady=20, justify=LEFT)
radio_button2.pack()

publishType = tk.StringVar(value='0')
radio_button1 = tk.Radiobutton(mainWindow, text='头条',variable=publishType,value='0',anchor='w',padx=20, pady=20)
radio_button1.pack(side=tk.LEFT)
radio_button2 = tk.Radiobutton(mainWindow, text='公众号',variable=publishType,value='1',anchor='w',padx=20, pady=20)
radio_button2.pack(side=tk.LEFT)
radio_button3 = tk.Radiobutton(mainWindow, text='百家号',variable=publishType,value='2',anchor='w',padx=20, pady=20)
radio_button3.pack(side=tk.LEFT)


button = tk.Button(mainWindow, text="点击我")
button.pack()

mainWindow.mainloop()