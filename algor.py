# 管理dp算法
import time
import random
import logging
from files import FileOperator

logging.basicConfig(filename='C:\\Users\\86180\\Desktop\\动态日程安排器\\日志.txt',level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')


class Algor():
    def __init__(self):
        #从任务难度记录里获取任务量，记录在task_num中
        self.date = time.strftime('%Y%m%d')
        self.diff_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务难度记录\\{self.date}.txt'
        self.task_num = float(FileOperator(self.diff_path).read_file())

        #每日任务地址
        every_path = f'C:\\Users\\86180\\Desktop\\动态日程安排器\\每日任务\\{self.date}.txt'

        #根据任务量设置背包容量
        self.pack_capacity = self.task_num*1.2 #任务量乘2得到背包容量

        #先获取easy,diff,vdif,fix_tasks4个分区的所有任务，整合成列表
        self.easy_lis = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\easy.txt').read_line()
        self.diff_lis = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\diff.txt').read_line()
        self.vdif_lis = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\vdif.txt').read_line()
        self.fix_tasks = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt').read_line()

        #获得固定任务列表以及剩余背包容量
        self.fix_lis= self.fixtask_lis()

        #生成计划表
        self.lis = self.givealis(greedy=True) #greedy参数为贪心算法的开关
        self.fina_lis = self.sum_twolis(self.fix_lis,self.lis)
        
        #点击确定后，先删除每日任务中的所有值
        FileOperator(every_path).delete_value(clear=True)

        #将计划表中的值填入每日任务
        FileOperator(every_path).lis_file(self.fina_lis)

    
    def shop(self):
        """从任务库里随机挑选任务，放置在一个列表里，作为任务商店（后续用商店中的任务做dp）"""

        #制定商店列表
        shop = []

        #根据任务量确定挑选多少任务
        if self.task_num < 1:
            pass
        elif 1<=self.task_num//1<=3:
            random.shuffle(self.easy_lis)
            _shop = self.easy_lis
            shop = _shop[0:random.randint(1,len(_shop))]
        elif 4<= self.task_num//1 <=6:
            random.shuffle(self.diff_lis)
            random.shuffle(self.easy_lis)
            _shop = self.diff_lis[0:2]
            _shop2 = self.easy_lis
            shop += _shop+_shop2[0:random.randint(1,len(_shop))]
        elif 7<=self.task_num//1 <=9:
            random.shuffle(self.diff_lis)
            _shop = self.diff_lis[0:2]
            _shop2 = [random.choice(self.vdif_lis)]
            shop += _shop+_shop2
        else:
            random.shuffle(self.diff_lis)
            random.shuffle(self.vdif_lis)
            _shop = self.diff_lis[0:2]
            _shop2 = self.vdif_lis[0:3]
            shop += _shop+_shop2
        
        #找到商店里任务的各个信息
        shop_dic = self.find_mes(shop)
        #将任务名，任务信息传递到生成最终商店的函数中
        final_shop = self.final_shop(shop_dic,greedy=True) #贪心算法和动态规划所用的列表是不一样的
        return final_shop


    def find_mes(self,shop):
        """找到给定shop的时长和难度信息，并生成字典"""
        path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\难度管理\\coe.txt'
        dic = {}
        for name in shop:
            with open(path,'r') as file:
                for line in file:
                    if name+'难度' in line:
                        coe = line.split(':')[1]
                        coe = coe.rstrip()
                    elif name+'最小时长' in line:
                        min_time = line.split(':')[1]
                        min_time = min_time.rstrip()
                    elif name+'最大时长' in line:
                        max_time = line.split(':')[1]
                        max_time = max_time.rstrip()
            dic[name] = {'coe':coe,'min_time':min_time,'max_time':max_time}
        return dic


    def final_shop(self,shop_dic,greedy=False):
        """传入shop字典，生成一个final_shop列表"""
        final_shop = []
        #生成动态规划所需的列表，将时长不同的同一任务视为不同的商品
        if greedy == False:  
            for name, value in shop_dic.items():
                min_time = float(value['min_time'])
                max_time = float(value['max_time'])
                time_count = min_time
                while min_time <= time_count <= max_time:
                    all_coe = time_count*float(value['coe'])
                    final_shop.append([name,time_count,all_coe])
                    if name !='冥想':
                        time_count += 0.5
                    else:
                        time_count += 0.1
        else:
            #生成贪心算法所需的列表，随机选择时长
            for name, value in shop_dic.items():
                tem_lis = []
                min_time = float(value['min_time'])
                max_time = float(value['max_time'])
                time_count = min_time
                while min_time <= time_count <= max_time:
                    all_coe = time_count*float(value['coe'])
                    tem_lis.append([name,time_count,all_coe])
                    if name !='冥想':
                        time_count += 0.5
                    else:
                        time_count += 0.1
                final_shop.append(random.choice(tem_lis))
        return final_shop


    def print_shop(self,lis):
        """测试用"""
        for i in range(len(lis)):
            print(f'{i+1}.{lis[i]}')


    def greedy(self,final_shop):
        """使用贪心算法生成计划列表"""
        #指定背包的容量
        pac = self.pack_capacity
        #这是最终要返回的列表
        task_lis = []
        #将商店里所有背包装不下的商品全部删除
        ls_lis = self.delete_m(pac,final_shop)
        #只要背包还有容量，并且商店里还有商品，就不停循环
        while pac>0 and bool(ls_lis):
            #找到背包中价值最大的商品
            x = ls_lis[0]
            for item in ls_lis:
                if float(item[2]) > x[2]:
                    x = item
                else:
                    continue
            #将价值最大的商品从商店中删除，装进背包中，背包容量减少
            del(ls_lis[ls_lis.index(x)])
            pac -= float(x[1])
            task_lis.append(x)
            #再次删除商店中所有背包装不下的商品，重复以上步骤直到背包装不下或商店清空
            ls_lis = self.delete_m(pac,ls_lis)
        return task_lis


    def delete_m(self,pac,lis):
        """删除LIS中大于Pac的值"""
        ls = []
        for item in lis:
            if float(item[1]) > pac:
                continue
            else:
                ls.append(item)
        return ls


    def givealis(self,greedy=False):
        """生成计划表"""
        #这是最后要返回的列表
        fina_lis = []
        fix_lis = FileOperator('C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt').read_line()
        if greedy:
            dic = {}
            #随机生成十张商店，并对它们使用贪心算法，将得到的最优解存储进dic中
            for i in range(1,11):
                final_shop = self.shop()
                lis = self.greedy(final_shop)
                dic[f'第{i}张列表'] = lis
            x = dic['第1张列表']
            #找出总价值最大的背包，返回
            for name,value in dic.items():
                y = 0
                m = 0
                for item in x:
                    m += item[2]
                for item in value:
                    y += item[2]
                if y > m:
                    x = dic[name]
            for item in x:
                fina_lis.append([item[0],round(float(item[1]),1)])
            return fina_lis


    def fixtask_lis(self):
        """返回一张包含固定任务的列表以及背包的剩余容量"""
        if self.task_num >= 4:
            if self.task_num//1>0:
                lis = []
                weight=0
                fix_path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\任务管理\\fix_tasks.txt'
                fix_lis = FileOperator(fix_path).read_line()
                fix_dic = self.find_mes(fix_lis)
                dif_coe = self.task_num//1
                div = dif_coe/15
                for key,value in fix_dic.items():
                    times = (float(value['max_time'])-float(value['min_time']))*div+float(value['min_time'])
                    times = round(times,1)
                    lis.append([key,times])
                return lis
            else:
                pass
        else:
            return False


    def sum_twolis(self,fix_lis:list,greedy_lis:list)-> list:
        """合并fix和贪心列表"""
        if fix_lis:
            logging.debug('start of sum_twolis')
            i = 1
            fina_fix = []
            temp_lis = []
            __fina_lis = []
            logging.debug('fix_lis:'+str(fix_lis))
            logging.debug('greedy_lis:'+str(greedy_lis))
            for fix_task in fix_lis:
                fina_fix.append(fix_task[0])
            logging.debug('fina_fix:'+str(fina_fix))
            for greedy_task in greedy_lis:
                temp_lis.append(greedy_task[0])
            logging.debug('temp_lis:'+str(temp_lis))
            for task in fina_fix:
                if task in temp_lis:
                    fix_lis[fina_fix.index(task)] = 0
                    fina_fix[fina_fix.index(task)] = 0
                    logging.debug(f'第{i}次删除后的fix_lis:'+str(fix_lis))
                    logging.debug(f'第{i}次删除后的fina_fix:'+str(fina_fix))
                    i+=1
                else:
                    continue
            while 0 in fix_lis:
                fix_lis.remove(0)
            logging.debug('最后得到的fix_lis:'+str(fix_lis))
            logging.debug('greedy_lis:'+str(greedy_lis))
            fina_lis = fix_lis+greedy_lis
            logging.debug('fina_lis:'+str(fina_lis))
            _fina_lis = self.find_coe(fina_lis)
            _fina_lis.sort(key=lambda u:(u[2]))
            logging.debug('new _fina_lis:'+str(_fina_lis))
            sortedlis = self.rthym(_fina_lis)
            logging.debug('排好序的列表:'+str(sortedlis))
            for item in sortedlis:
                __fina_lis.append(f'{item[0]}{item[1]}小时')
            logging.debug('最终列表:'+str(__fina_lis))
            logging.debug('结束\n\n')
            return __fina_lis
        else:
            __fina_lis = []
            for item in greedy_lis:
                __fina_lis.append(f'{item[0]}{item[1]}小时')
            return __fina_lis
        


    def find_coe(self,lis:list)-> list:
        """对于每一项任务，找到它的coe信息"""
        path = 'C:\\Users\\86180\\Desktop\\动态日程安排器\\难度管理\\coe.txt'
        for item in lis:
            with open(path,'r') as file:
                for line in file:
                    if item[0] + '难度' in line:
                        coe = line.split(':')[1]
                        coe = coe.rstrip()
                        all_coe = float(coe)*float(item[1])
                        item.append(all_coe)
                    else:
                        continue
        logging.debug('_fina_lis:'+str(lis))
        return lis


    def rthym(self,lis:list):
        """对给定列表进行排序"""
        new = []
        odd_num = int(len(lis)//2+len(lis)%2)
        big_lis = lis[-odd_num:]
        little_lis = lis[0:odd_num-1]
        while bool(big_lis):
            x = big_lis.pop(big_lis.index(random.choice(big_lis)))
            new.append(x)
            if bool(little_lis):
                y = little_lis.pop(little_lis.index(random.choice(little_lis)))
                new.append(y)
        return new

#logging.disable(logging.CRITICAL)