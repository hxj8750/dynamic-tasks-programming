import tkinter as tk
import time
from tkinter import messagebox
from tkinter import ttk
from files import FileOperator
from fix_op import Fix

class Tasks():
    def __init__(self):
        #初始化窗口
        self.root = tk.Toplevel()
        self.root.geometry('562x512')
        self.root.title('任务管理')
        self.root.resizable(0,0)

        #设置菜单
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label='添加任务',command=self.add_tasks)
        self.menubar.add_command(label='固定任务一览',command=self.see_fix)
        self.root.config(menu=self.menubar)

        #添加三个任务框
        self.easy_tasks = tk.Listbox(self.root,width=22,height=18,listvariable=None)
        self.easy_tasks.place(x=10,y=60)
        self.diff_tasks = tk.Listbox(self.root,width=22,height=18,listvariable=None)
        self.diff_tasks.place(x=200,y=60)
        self.vdif_tasks = tk.Listbox(self.root,width=22,height=18,listvariable=None)
        self.vdif_tasks.place(x=390,y=60)

        #为任务框添加label
        self.easy_lable = tk.Label(self.root,text='容易:')
        self.easy_lable.place(x=10,y=30)
        self.diff_lable = tk.Label(self.root,text='困难:')
        self.diff_lable.place(x=200,y=30)
        self.vdif_lable = tk.Label(self.root,text='非常困难:')
        self.vdif_lable.place(x=390,y=30)    

        #创建删除和添加进固定任务按钮以及更改按钮
        self.add_to_fix = tk.Button(self.root,text='添加进固定任务',width=13,height=1,command=self.add_tofix)
        self.add_to_fix.place(x=10,y=400)
        self.delete = tk.Button(self.root,text='删除任务',width=10,height=1,command=self.delete_op)
        self.delete.place(x=150,y=400)
        self.change_button = tk.Button(self.root,text='修改',command=self.change_asked)
        self.change_button.place(x=290,y=400)

        #创建完成按钮
        self.cancel = tk.Button(self.root,text='完成',command=self.root.destroy)
        self.cancel.place(x=500,y=450)

        self.tasks_print()


    def tasks_print(self):
        """显示已有的任务"""
        easy_taskss = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\easy.txt').read_line()
        for data in easy_taskss:
            self.easy_tasks.insert('end',data)
        diff_taskss = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\diff.txt').read_line()
        for data in diff_taskss:
            self.diff_tasks.insert('end',data)
        vdif_taskss = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\vdif.txt').read_line()
        for data in vdif_taskss:
            self.vdif_tasks.insert('end',data)


    def delete_op(self):
        """响应删除按钮"""
        dic = {}
        fine = True #如果没有点击任何一栏，就将其设为False
        try:
            value = self.easy_tasks.get(self.easy_tasks.curselection())
            dic = {'easy':value}
        except:
            try:
                value = self.diff_tasks.get(self.diff_tasks.curselection())
                dic = {'diff':value}
            except:
                try:
                    value = self.vdif_tasks.get(self.vdif_tasks.curselection())
                    dic = {'vdif':value}
                except:
                    fine = False
        if fine:
            if value.count('\n') >= 2:
                pass
            else:
                transit = ''
                for name,value in dic.items():
                    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\{name}.txt'
                    with open(path,'r') as file_object:
                        for line in file_object:
                            if value in line:
                                continue
                            else:
                                transit += line
                file = open(path,'w')
                file.write(transit)
                file.close()
                self.easy_tasks.delete('0','end')
                self.diff_tasks.delete('0','end')
                self.vdif_tasks.delete('0','end')
                self.tasks_print()

                #删除难度管理中的相应值
                transit2 = ''
                new_path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\难度管理\\coe.txt'
                for name,value in dic.items():
                    with open(new_path,'r') as file:
                        for line in file:
                            if value in line:
                                continue
                            else:
                                transit2 += line
                file2 = open(new_path,'w')
                file2.write(transit2)
                file2.close()

                #删除固定任务中的相应值
                transit3 = ''
                new_path2 = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt'
                for name,value in dic.items():
                    with open(new_path2,'r') as file:
                        for line in file:
                            if value in line:
                                continue
                            else:
                                transit3 += line
                file3 = open(new_path2,'w')
                file3.write(transit3)
                file3.close()
    

    def diff_judge(self,coe,max_time,min_time):
        """判断一个任务的难度，返回相应的path和平均难度"""
        #计算平均难度
        ave_time = (float(max_time)+float(min_time))/2
        ave_diff = ave_time*float(coe)

        #根据平均难度分类
        if 1<= ave_diff <=4:
            path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\easy.txt'
        elif 4< ave_diff <= 7:
            path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\diff.txt'
        elif 7< ave_diff <= 10:
            path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\vdif.txt'
        else:
            path = False

        return path,ave_diff

    
    def add_tasks(self):
        """响应添加"""

        def judge_null():
            """判断4个输入框是否填写完整"""
            if name_entry.get()!=''and coe_entry.get()!=''and max_time.get()!=''and min_time.get()!='':
                add_button.config(state='normal')
            else:
                add_button.config(state='disable')
            adding_window.after(500,judge_null)
    

        def adding_tasks():
            """将任务添加进任务管理文档中,同时更新"""
            dic =  {'任务名':name_entry.get(),
                    '难度系数':coe_entry.get(),
                    '最大时长':max_time.get(),
                    '最小时长':min_time.get()}
            
            path,ave_diff = self.diff_judge(dic['难度系数'],dic['最大时长'],dic['最小时长'])
            if path != False:
                #输入后清空输入栏
                name_entry.delete('0','end')
                coe_entry.delete('0','end')
                max_time.delete('0','end')
                min_time.delete('0','end')

                #添加
                file = open(path,'a')
                file.write(dic['任务名']+'\n') #添加任务会自动添加换行符，但是在更新时，read_line函数会删除换行符
                file.close()

                #添加进whole
                file2 = open('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\whole.txt','a')
                file2.write(dic['任务名']+'\n')
                file2.close()

                #将任务的难度信息添加进难度管理文档中
                new_path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\难度管理\\coe.txt'
                file = open(new_path,'a')
                file.write(dic['任务名']+'\n'
                            +dic['任务名']+'难度'+':'+dic['难度系数']+'\n'
                            +dic['任务名']+'最小时长'+':'+dic['最小时长']+'\n'
                            +dic['任务名']+'最大时长'+':'+dic['最大时长']+'\n')
                file.close()

                #更新任务栏
                self.easy_tasks.delete('0','end')
                self.diff_tasks.delete('0','end')
                self.vdif_tasks.delete('0','end')
                self.tasks_print()

            else:
                error_lable = tk.Label(adding_window,text=f'平均难度为{ave_diff},平均难度不应小于1或大于10',bg='Red')
                error_lable.place(x=10,y=80)
                error_lable.after(2000,error_lable.destroy)


        #创建窗口
        adding_window = tk.Toplevel()
        adding_window.title('添加任务')
        adding_window.geometry('456x123')
        adding_window.resizable(0,0) #不可更改窗口大小

        #创建任务名输入框
        name_entry = tk.Entry(adding_window,width=15,show=None)
        name_entry.place(x=10,y=30)
        
        #创建难度系数输入框
        coe_entry = tk.Entry(adding_window,width=10,show=None)
        coe_entry.place(x=150,y=30)

        #时长输入框
        max_time = tk.Entry(adding_window,width=10,show=None)
        max_time.place(x=240,y=30)
        min_time = tk.Entry(adding_window,width=10,show=None)
        min_time.place(x=330,y=30)

        #创建添加和退出按钮
        add_button = tk.Button(adding_window,text='添加',command=adding_tasks)
        add_button.place(x=350,y=75)
        quit_button = tk.Button(adding_window,text='退出',command=adding_window.destroy)
        quit_button.place(x=400,y=75)

        #创建提示标签
        name_lable = tk.Label(adding_window,text='任务名:')
        name_lable.place(x=10,y=7)
        coe_lable = tk.Label(adding_window,text='难度系数:')
        coe_lable.place(x=150,y=7)
        max_lable = tk.Label(adding_window,text='最大时长:')
        max_lable.place(x=240,y=7)
        min_lable = tk.Label(adding_window,text='最小时长:')
        min_lable.place(x=330,y=7)

        #每隔0.5秒判断一次是否完整填写
        judge_null()


    def add_tofix(self):
        """响应添加进固定任务按钮"""
        fine = True #如果没有点击任何一栏，就将其设为False
        try:
            value = self.easy_tasks.get(self.easy_tasks.curselection())
        except:
            try:
                value = self.diff_tasks.get(self.diff_tasks.curselection())
            except:
                try:
                    value = self.vdif_tasks.get(self.vdif_tasks.curselection())
                except:
                    fine = False

        if fine:
            file = open('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt','a')
            file.write(value+'\n') #从那三个任务框里get到的都是不带\n的
            file.close()

    
    def see_fix(self):
        """打开固定任务列表"""
        fix_win = Fix()


    def change_asked(self):
        """响应修改按钮"""

        def getvalue(value):
            """填入初始值"""
            dics = {'任务名':value}
            with open(diffmana_path,'r') as file:
                for line in file:
                    #注意，下面获取的值最右边都带有\n,为了避免发生错误，要先统一去掉\n
                    if value+'难度' in line:
                        难度 = line.split(':')[1]
                        难度=难度.rstrip()
                        dics['难度'] = 难度
                    if value+'最小时长' in line:
                        最小时长 = line.split(':')[1]
                        最小时长 = 最小时长.rstrip()
                        dics['最小时长'] = 最小时长
                    if value+'最大时长' in line:
                        最大时长 = line.split(':')[1]
                        最大时长 = 最大时长.rstrip()
                        dics['最大时长'] = 最大时长
            return dics


        def judge_null():
            """判断4个输入框是否填写完整"""
            if name_entry.get()!=''and coe_entry.get()!=''and max_time.get()!=''and min_time.get()!='':
                change_button.config(state='normal')
            else:
                change_button.config(state='disable')
            change_window.after(500,judge_null)


        def put_change():
            """点击修改以后"""
            my_dic = {}
            my_dic['任务名'] = name_entry.get()
            my_dic['难度'] = coe_entry.get()
            my_dic['最小时长'] = min_time.get()
            my_dic['最大时长'] = max_time.get()
            
            #先找到更改后添加进哪个任务框
            _newpath,ave = self.diff_judge(my_dic['难度'],my_dic['最大时长'],my_dic['最小时长'])

            #如果难度符合要求
            if _newpath != False:
                
                #清空4个框
                name_entry.delete('0','end')
                coe_entry.delete('0','end')
                max_time.delete('0','end')
                min_time.delete('0','end')

                #首先删除main中的信息
                transit_main = ''
                with open(main_path,'r') as file:
                    for line in file:
                        if value in line:
                            continue
                        else:
                            transit_main += line
                file1 = open(main_path,'w')
                file1.write(transit_main)
                file1.close()

                #再将新的值添加进_newpath中
                f_file = open(_newpath,'a')
                f_file.write(my_dic['任务名']+'\n')
                f_file.close()

                #更改任务管理中的信息
                transit_mana = ''
                with open(diffmana_path,'r') as file:
                    for line in file:
                        if line == value+'\n':
                            transit_mana += my_dic['任务名'] + '\n'
                        elif value+'难度' in line:
                            transit_mana += my_dic['任务名']+'难度'+':'+my_dic['难度'] + '\n'
                        elif value+'最小时长' in line:
                            transit_mana += my_dic['任务名']+'最小时长'+':'+my_dic['最小时长'] + '\n'
                        elif value+'最大时长' in line:
                            transit_mana += my_dic['任务名']+'最大时长'+':'+my_dic['最大时长'] + '\n'
                        else:
                            transit_mana += line
                file2 = open(diffmana_path,'w')
                file2.write(transit_mana)
                file2.close()

                #更改固定任务中的信息
                transit_fix = ''
                with open(fix_path,'r') as file:
                    for line in file:
                        if value in line:
                            transit_fix += my_dic['任务名']+'\n'
                        else:
                            transit_fix += line
                file3 = open(fix_path,'w')
                file3.write(transit_fix)
                file3.close()

                #更新任务框
                self.easy_tasks.delete('0','end')
                self.diff_tasks.delete('0','end')
                self.vdif_tasks.delete('0','end')
                self.tasks_print()
            else:
                #如果难度不符合规范
                error_lable = tk.Label(change_window,text=f'平均难度为{ave},平均难度不应小于1或大于10',bg='Red')
                error_lable.place(x=10,y=80)
                error_lable.after(2000,error_lable.destroy)


        #先判断修改哪一个
        dic = {}
        fine = True #如果没有点击任何一栏，就将其设为False
        try:
            value = self.easy_tasks.get(self.easy_tasks.curselection())
            dic = {'easy':value}
        except:
            try:
                value = self.diff_tasks.get(self.diff_tasks.curselection())
                dic = {'diff':value}
            except:
                try:
                    value = self.vdif_tasks.get(self.vdif_tasks.curselection())
                    dic = {'vdif':value}
                except:
                    fine = False
        if fine:
            #主路径
            for name,value in dic.items():
                main_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\{name}.txt'
            #难度管理路径
            diffmana_path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\难度管理\\coe.txt'
            #固定任务路径
            fix_path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt'

            #创建窗口
            change_window = tk.Toplevel()
            change_window.title('更改任务')
            change_window.geometry('456x123')
            change_window.resizable(0,0) #不可更改窗口大小

            #创建任务名输入框
            name_entry = tk.Entry(change_window,width=15,show=None)
            name_entry.place(x=10,y=30)
            
            #创建难度系数输入框
            coe_entry = tk.Entry(change_window,width=10,show=None)
            coe_entry.place(x=150,y=30)

            #时长输入框
            max_time = tk.Entry(change_window,width=10,show=None)
            max_time.place(x=240,y=30)
            min_time = tk.Entry(change_window,width=10,show=None)
            min_time.place(x=330,y=30)

            #创建修改和退出按钮
            change_button = tk.Button(change_window,text='更改',command=put_change)
            change_button.place(x=350,y=75)
            quit_button = tk.Button(change_window,text='退出',command=change_window.destroy)
            quit_button.place(x=400,y=75)

            #创建提示标签
            name_lable = tk.Label(change_window,text='任务名:')
            name_lable.place(x=10,y=7)
            coe_lable = tk.Label(change_window,text='难度系数:')
            coe_lable.place(x=150,y=7)
            max_lable = tk.Label(change_window,text='最大时长:')
            max_lable.place(x=240,y=7)
            min_lable = tk.Label(change_window,text='最小时长:')
            min_lable.place(x=330,y=7)

            #获取所选值的信息
            dictionary = getvalue(value)

            #将信息填入四个框中，作为初始值
            name_entry.insert('0',dictionary['任务名'])
            coe_entry.insert('0',dictionary['难度'])
            max_time.insert('0',dictionary['最大时长'])
            min_time.insert('0',dictionary['最小时长'])

            judge_null()