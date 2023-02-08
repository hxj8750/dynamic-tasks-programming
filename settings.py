import tkinter as tk
import time
from files import FileOperator
from algor import Algor

class Setting():

    def __init__(self):
        #设置弹出窗口
        self.setting_window = tk.Toplevel()
        self.setting_window.title('设置任务量')
        self.setting_window.geometry('456x123')
        self.setting_window.resizable(0,0) #不可更改窗口大小

        #显示任务量
        self.diffcult_lable = tk.Label(self.setting_window,text='难度：')
        self.diffcult_lable.pack()

        #点击确定键
        self.confirm_button = tk.Button(self.setting_window,text='确定',command=self.confirm_asked)
        self.confirm_button.place(x=362,y=80)

        #点击取消键
        self.cancel_button = tk.Button(self.setting_window,text='取消',command=self.setting_window.destroy)
        self.cancel_button.place(x=410,y=80)

        #设置难度scale
        self.set_scale = tk.Scale(self.setting_window,label='任务量设置',from_=0,to=10,orient=tk.HORIZONTAL,
                            length=300,showvalue=1,tickinterval=1,resolution=0.1,command=self.diffcult_scale)
        self.set_scale.place(x=50,y=30)

        #获取任务量设置保存文件的路径
        self.date = time.strftime('%Y%m%d')
        self.path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务难度记录\\{self.date}.txt'

        #每次打开窗口，检测保存的任务量的值
        self.detect_difnum()

    def confirm_asked(self):
        """点击确认，保存设定的值，关闭设置窗口"""
        #获取scale的值
        dif = self.set_scale.get()
        #将新的scale值保存下来
        files = FileOperator(self.path)
        files.change_file(dif)
        
        fi = Algor()
        self.setting_window.destroy()

    def diffcult_scale(self,num):
        """更新任务量提示标签"""
        if float(num)//1 == 0:
            self.diffcult_lable.config(text=f'难度:{num},无任务')
        elif 1<=float(num)//1<=3:
            #只有easy任务，总时数4h
            self.diffcult_lable.config(text=f'难度:{num},轻松') 
        elif 4<=float(num)//1<=6:
            #至少一个，最多2个diff任务，总时数6h
            self.diffcult_lable.config(text=f'难度:{num},较困难')
        elif 7<=float(num)//1<=9:
            #包含两个diff和一个vdif任务，总时数8h
            self.diffcult_lable.config(text=f'难度:{num},困难')
        else:
            #包含3个vdif和2个diff任务，总时数10H
            self.diffcult_lable.config(text=f'难度:{num},非常困难')

    def detect_difnum(self):
        """每次打开任务量设置页面，则检测该日期下最新的设定值"""
        files = FileOperator(self.path)
        new_dif = files.read_file()
        self.set_scale.set(float(new_dif))