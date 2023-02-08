import tkinter as tk
import time
import winsound
import threading
import calendar
from tkinter import ttk
from random import choice
from random import randint
from settings import Setting
from files import FileOperator
from taskarrange import Tasks
from Calendar import Calendar

datetime=calendar.datetime.datetime

def gettime():
    """时间函数，获取当前时间，系统每隔一秒调用一次该函数，在程序内的上方不断更新时间"""
    tim.set(time.strftime("%H:%M:%S"))
    root.after(1000,gettime)


def begin_command():
    """begin按钮调用的函数，目前未完成，功能是变换该按钮的text，并且开始抽取任务以及结束任务
        目前该函数是通过begin这个变量的初始值来判断，但后续不可能这么做，后续要把用来判断的变量
        存储进一个文档中，好实现关闭程序后再次打开依然能接着做任务的功能。"""
    global n
    global tasks_left
    if begin.get() == '开始':
        if bool(_task_lis):
            if n < 200:
                rand_lable.config(text=choice(lis),fg='black')
                n += 1
                root.after(10,begin_command)
                
            else:
                tt_task = _task_lis.pop(0)
                rand_lable.config(text=tt_task,fg='red')
                f = open(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt','w')
                f.write(tt_task)
                f.close()
                judge_label_()
                FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\每日任务\\{date}.txt').delete_value(value=tt_task)
                begin.set('完成')
        else:
            rand_lable.config(text='今日已无任务！',fg='red')
    elif begin.get() == '完成':
        file_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt').read_line()
        f = open(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt','w')
        f.write('')
        f.close()
        rand_lable.config(text='')
        task = file_lis[0]
        done = open(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\已完成\\{date}.txt','a')
        done.write(task+'\n')
        done.close()
        judge_label_()
        judge_isdone()
        begin.set('开始')
        tasks_left = len(_task_lis)
        tasks_lable.config(text=f'还剩下{tasks_left}个任务')
        n = 0


def time_confirm():
    """该函数是用来解锁“生成报告”按钮的，当日期为星期天晚上十点到星期一晚上十点之间时，
        解锁“生成报告”按钮，目前还在测试功能当中"""
    if int(time.strftime("%S"))%2==0:
        toolsmenu.entryconfig('生成本周报告',state='normal')
    else:
        toolsmenu.entryconfig('生成本周报告',state='disable')
    root.after(1000,time_confirm) # 每0.5秒执行一次


def setting_wins():
    """打开设置窗口，调用设置类"""
    set_win = Setting()


def creat_settingfile():
    """检测或创建新的任务量设置文件"""
    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务难度记录\\{date}.txt'
    files = FileOperator(path)
    files.creat_setfile()


def creat_everydaytask():
    """检测或创建新的任务列表文件"""
    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\每日任务\\{date}.txt'
    files = FileOperator(path)
    files.creat_everydaytask()


def creat_programming():
    """创建当天的进行中文件"""
    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt'
    files = FileOperator(path)
    files.creat_programming()


def creat_sign():
    """每个月创建一次签到文件"""
    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\签到记录\\{datetime.now().year}_{datetime.now().month}.txt'
    files = FileOperator(path)
    files.creat_sign()


def judge_isdone():
    """判断是否完成今天的全部任务，若完成，则将今天的日期放入签到文件中"""
    sign_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\签到记录\\{datetime.now().year}_{datetime.now().month}.txt'
    if _task_lis:
        pass
    else:
        today = [str(datetime.now().day)]
        FileOperator(sign_path).lis_file(today)


def creat_done():
    """创建完成文件"""
    path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\已完成\\{date}.txt'
    files = FileOperator(path)
    files.creat_done()


def tasks_arr():
    """点击任务管理后调用Tasks类"""
    tasks = Tasks()


def set_calendar(event):
    """点击日期，响应"""
    calendar = Calendar()


def judge_programming():
    """每次运行程序，先判断是否有还在进行中的任务，没有就pass"""
    pro_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt').read_line()
    done_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\已完成\\{date}.txt').read_line()
    if bool(pro_lis):
        rand_lable.config(text=pro_lis[0])
        judge_label_()
        begin.set('完成')
    if bool(done_lis):
        judge_label_()
    else:
        pass


def creat_label():
    """根据已完成和进行中的情况，创建若干label"""
    done_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\已完成\\{date}.txt'
    doing_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt'
    done_filelis = FileOperator(done_path).read_line()
    doing_filelis = FileOperator(doing_path).read_line()
    if done_filelis:
        done_task = len(done_filelis)
        if not doing_filelis:
            doing_task = 0
        else:
            doing_task = 1
        label_num = done_task+doing_task
        for i in range(label_num):
            globals()['_label'+str(i+1)] = label = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
            label.place(x=-5,y=10+i*20)
    else:
        global _label1
        _label1 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
        _label1.place(x=-5,y=10)
        


def more_thread(thread):
    """创建多线程"""
    if thread == 'dida' and bool(_task_lis):
        if begin.get() == '开始':
            sound = threading.Thread(target=lambda :[playbgm(bgm='dida')])
            sound.start()
        else:
            sound = threading.Thread(target=lambda :[playbgm(bgm='shua')])
            sound.start()


def playbgm(bgm:str)-> None: #建议符
    """管理bgm"""
    if bgm == 'dida':
        winsound.PlaySound('C:\\Users\\86180\\Desktop\\动态日程安排器\\音效\\滴答8.wav',winsound.SND_FILENAME)
        winsound.PlaySound('C:\\Users\\86180\\Desktop\\动态日程安排器\\音效\\选取成功.wav',winsound.SND_FILENAME)
    elif bgm == 'shua':
        winsound.PlaySound('C:\\Users\\86180\\Desktop\\动态日程安排器\\音效\\完成任务3.wav',winsound.SND_FILENAME)


def judge_label_():
    """判断应使用哪一个label"""
    done_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\已完成\\{date}.txt'
    doing_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\进行中\\{date}.txt'
    done_filelis = FileOperator(done_path).read_line()
    doing_filelis = FileOperator(doing_path).read_line()
    creat_label()
    if doing_filelis:
        if not done_filelis:
            _label1.config(text=f'进行中:{doing_filelis[0]}',fg='red')
        else:
            for i in range(len(done_filelis)):
                eval('_label'+str(i+1)).config(text=f'已完成:{done_filelis[i]}',fg='grey')
            eval('_label'+str(len(done_filelis)+1)).config(text=f'进行中:{doing_filelis[0]}',fg='red')
    else:
        if done_filelis:
            for i in range(len(done_filelis)):
                eval('_label'+str(i+1)).config(text=f'已完成:{done_filelis[i]}',fg='grey')


if __name__ == '__main__':
    
    root = tk.Tk() #创建窗口
    root.geometry('512x512') #设置窗口大小
    root.title('动态日程安排器') #设置窗口名称
    root.resizable(0,0)

    #变量初始化
    n = 0
    date = time.strftime('%Y%m%d')
    creat_programming()
    creat_everydaytask()
    creat_done()
    _task_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\每日任务\\{date}.txt').read_line()
    ff = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\whole.txt')
    lis = ff.read_line()
    tim = tk.StringVar() #将当前时间作为一个变量，该变量的值由gettime函数确定，并每隔一秒更新一次
    tasks_left = len(_task_lis) #还剩下多少任务？目前是测试阶段，先给一个确定值3，后续需要检测文档内的任务数量
    begin = tk.StringVar() #用来测试开始按钮的，初始值为“开始”，按一次变一次。
   
    #rand_task = tk.StringVar()

    time_lable = tk.Label(root,textvariable = tim) #创建日期标签
    time_lable.pack()
    time_lable.bind('<Button-1>',set_calendar)

    strtim_lable = tk.Label(root,text='日期:') 
    strtim_lable.place(x=200,y=0)

    tasks_lable = tk.Label(root, text = f'还剩下{tasks_left}个任务') # 创建剩余任务提示栏
    tasks_lable.place(x=200,y=40)

    taskspick_lable = tk.Label(root,text='任务抽签框') # 顾名思义，提示下面的文本框为任务抽签框
    taskspick_lable.place(x=85,y=70)

    taskslist_lable = tk.Label(root,text='任务栏') # 同上
    taskslist_lable.place(x=339,y=70)

    tasks_pick = tk.Frame(root,borderwidth=2,height=350,width=200,bg='lightblue') 
    tasks_pick.pack(side = tk.LEFT)

    tasks_list = tk.Frame(root,borderwidth=2,height=350,width=200,bg='lightgreen')
    tasks_list.pack(side=tk.RIGHT)

    begin_button = tk.Button(root, textvariable=begin,width=10,height=2,command=lambda:[more_thread(thread='dida'),begin_command()]) #创建开始按钮，其文本是一个变量，就是上面说过的begin
    begin_button.place(x=212,y=400)
    begin.set('开始') #将begin初始化为开始。

    #创建随机抽取动画标签
    rand_lable = tk.Label(tasks_pick,height=8,width=20,bg='lightblue',font=("Arial Blod",18),wraplength=150,justify='center')
    rand_lable.place(x=-25,y=10)

    #创建任务状态标签
    tasks_lable1 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable1.place(x=-5,y=10)

    tasks_lable2 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable2.place(x=-5,y=30)


    tasks_lable3 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable3.place(x=-5,y=50)

    tasks_lable4 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable4.place(x=-5,y=70)


    tasks_lable5 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable5.place(x=-5,y=90)


    tasks_lable6 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable6.place(x=-5,y=110)

    tasks_lable7 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable7.place(x=-5,y=130)

    tasks_lable8 = tk.Label(tasks_list,bg='lightgreen',font=("Arial Blod",8))
    tasks_lable8.place(x=-5,y=150)


    #创建母菜单栏
    menubar = tk.Menu(root)

    #在母菜单栏上创建工具子菜单栏
    toolsmenu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='文件',menu=toolsmenu)
    #在工具菜单栏上创建两个报告管理菜单栏
    toolsmenu.add_command(label='生成本周报告')
    toolsmenu.add_command(label='查看过往报告')
    toolsmenu.add_separator()
    toolsmenu.add_command(label='退出',command=root.quit)

    #在母菜单栏上创建任务管理子菜单栏
    tasksmenu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='任务设置',menu=tasksmenu)
    #在任务管理菜单栏上创建两个任务菜单栏
    tasksmenu.add_command(label='任务管理',command=tasks_arr)
    tasksmenu.add_command(label='设置次日任务量',command=setting_wins)

    #在母菜单栏上创建一个子菜单栏
    menubar.add_command(label='编辑算法')

    #将母菜单栏放置在窗口上
    root.config(menu=menubar)

    #运行函数
    #time_confirm() #判断是否满足条件，若满足条件，则隐藏“生成本周报告”按钮，否则放置该按钮。
    gettime() #调用gettime函数，系统会根据最后一行的指令多次调用该函数
    creat_settingfile()
    judge_programming()
    
    root.mainloop()