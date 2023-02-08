import tkinter as tk
from files import FileOperator

class Fix():
    def __init__(self):
        #初始化窗口
        self.root = tk.Toplevel()
        self.root.geometry('400x400')
        self.root.title('固定任务列表')
        self.root.resizable(0,0)

        #设置列表框
        self.fix_tasks = tk.Listbox(self.root,width=22,height=18,listvariable=None)
        self.fix_tasks.place(x=10,y=40)

        #提示标签
        self.fix_lable = tk.Label(self.root,text='固定任务')
        self.fix_lable.place(x=10,y=17)

        #设置移除按钮和退出按钮
        self.delete = tk.Button(self.root,text='删除任务',width=10,height=1,command=self.delete_op)
        self.delete.place(x=200,y=100)
        self.cancel = tk.Button(self.root,text='完成',command=self.root.destroy)
        self.cancel.place(x=350,y=350)

        self.tasks_print()


    def tasks_print(self):
        """更新任务栏"""
        fix_taskss = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt').read_line()
        for data in fix_taskss:
            self.fix_tasks.insert('end',data)


    def delete_op(self):
        """响应删除按钮"""
        fine = True #如果没有点击任何一栏，就将其设为False
        try:
            value = self.fix_tasks.get(self.fix_tasks.curselection())
        except:
            fine = False

        if fine:
            name = value
            transit = ''
            path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt'
            with open(path,'r') as file_object:
                for line in file_object:
                    if name in line:
                        continue
                    else:
                        transit += line
            file = open(path,'w')
            file.write(transit)
            file.close()
            self.fix_tasks.delete('0','end')
            self.tasks_print()
