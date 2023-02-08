import time

class FileOperator():

    def __init__(self,path):
        self.path = path

    def exit_judgment(self):
        """判断给定的文件是否存在或路径是否正确"""
        try:
            with open(self.path) as file_object:
                return True
        except FileNotFoundError:
            return False

    def creat_setfile(self):
        """创建任务量设置文档"""
        if self.exit_judgment():
            pass
        else:
            file = open(self.path,'w')
            file.write('0')
            file.close()

    def creat_everydaytask(self):
        """创建每日任务文档"""
        if self.exit_judgment():
            pass
        else:
            file = open(self.path,'w')
            file.write('')
            file.close()

    def change_file(self,contents):
        """改变某文档的内容"""
        try:
            with open(self.path,'w') as file_object:
                file_object.write(str(contents))
        except FileNotFoundError:
            print('没找到文件')

    def read_file(self):
        """读取文件"""
        with open(self.path,'r') as file_object:
            contents = file_object.read()
            return contents

    def read_line(self):
        """逐行读取,返回列表"""
        data = []
        with open(self.path) as file_object:
            for line in file_object:
                data.append(line.rstrip()) #注意，该函数会自动删除每一行的\n，非常重要！
        return data

    def delete_value(self,value=0,clear=False):
        """删除文档中的指定值"""
        transit = ''
        if clear == False:
            with open(self.path,'r') as file:
                for line in file:
                    if line == value+'\n':
                        continue
                    else:
                        transit += line
            files = open(self.path,'w')
            files.write(transit)
            files.close()
        else:
            #删除所有值
            files = open(self.path,'w')
            files.write(transit)
            files.close

    def lis_file(self,lis):
        """将列表中的值填入file"""
        file = open(self.path,'a')
        for item in lis:
            file.write(item+'\n')
        file.close()

    def creat_programming(self):
        """创建当天的进行中文档"""
        if self.exit_judgment():
            pass
        else:
            file = open(self.path,'w')
            file.close()

    def creat_done(self):
        """创建当天的已完成文档"""
        if self.exit_judgment():
            pass
        else:
            file = open(self.path,'w')
            file.close()

    def creat_sign(self):
        """每月创建一次签到文档"""
        if self.exit_judgment():
            pass
        else:
            file = open(self.path,'w')
            file.close()