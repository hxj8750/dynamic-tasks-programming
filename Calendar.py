# -*- coding: utf-8 -*- 
#上一行声名编码方式为utf-8，一般代码中含有中文就需要这样声名。python3.0以后的默认编码方式为utf-8，现在这么写只是为了方便移植
import calendar
import tkinter as tk
import logging
import tkinter.font as tkFont
from tkinter import ttk
from files import FileOperator
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')

#创建datetime对象，处理时间
datetime = calendar.datetime.datetime
#创建timedelta对象，处理时间加减
timedelta = calendar.datetime.timedelta

class Calendar:
    def __init__(s, point = None):#s即self,不一定非要写self，这个可以自定义
        #运行代码则自动打开一个叫master的弹窗
        s.master = tk.Toplevel()
        #隐藏弹窗,但是为什么要写这行代码？而且为什么运行后弹窗并没有被隐藏？暂时搁置吧
        s.master.withdraw()
        #将master的属性设置为topmost，置顶，这样生成出来的时候就是在最顶上了。
        s.master.attributes('-topmost' ,True)
        #calendar.SUNDAY返回星期天的代号，6，fwday=6，可能是后面想把它当作每周的第一天吧
        fwday = calendar.SUNDAY
        #获取当前年份,datetime.now().year是datetime类中的一个函数
        year = datetime.now().year
        #获取当前月份
        month = datetime.now().month
        #locale代表什么？
        locale = None
        #背景颜色（应该是弹窗的）
        sel_bg = '#ecffc4'
        #字体颜色
        sel_fg = '#05640e'
        #获取当前年月的第一天
        s._date = datetime(year, month, 1)        #每月第一日
        s._selection = None                       #设置为未选中日期
        #在master上再创建一个框架
        s.G_Frame = ttk.Frame(s.master)
        #将textcalendar实例化，赋予s._cal
        s._cal = s.__get_calendar(locale, fwday)
        #自定义左右箭头，风格为ttk风格
        s.__setup_styles()        # 创建自定义样式
        #一些小部件
        s.__place_widgets()       # pack/grid 小部件
        s.__config_calendar()     # 调整日历列和安装标记
        # 配置画布和正确的绑定，以选择日期。将日历画出来。
        s.__setup_selection(sel_bg, sel_fg)
        # 存储项ID，用于稍后插入。
        s._items = [s._calendar.insert('', 'end', values='') for _ in range(6)]
        # 在当前空日历中插入日期
        s._update()
        s.G_Frame.pack(expand = 1, fill = 'both')
        s.master.overrideredirect(1)
        s.master.update_idletasks()
        width, height = s.master.winfo_reqwidth(), s.master.winfo_reqheight()
        s.height=height
        s._sign(year,month)
        if point:
            x, y = point[0], point[1]
        else: 
            x, y = (s.master.winfo_screenwidth() - width)/2, (s.master.winfo_screenheight() - height)/2
        s.master.geometry('%dx%d+%d+%d' % (width, height, x, y)) #窗口位置居中
        s.master.after(300, s._main_judge)
        s.master.deiconify()
        s.master.focus_set() #将焦点聚焦在master上
        s.master.wait_window() #这里应该使用wait_window挂起窗口，如果使用mainloop,可能会导致主程序很多错误

    def __get_calendar(s, locale, fwday):
        #如果locale的值为none,这里locale被初始化为none
        if locale is None:
            #TextCalendar是一个类，可生成纯文本日历
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(s, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            s._canvas['background'] = value
        elif item == 'selectforeground':
            s._canvas.itemconfigure(s._canvas.text, item=value)
        else:
            s.G_Frame.__setitem__(s, item, value)

    def __getitem__(s, item):
        if item in ('year', 'month'):
            return getattr(s._date, item)
        elif item == 'selectbackground':
            return s._canvas['background']
        elif item == 'selectforeground':
            return s._canvas.itemcget(s._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(s, item)})
            return r[item]

    def __setup_styles(s):
        # 自定义TTK风格
        #将ttk.Style实例化，参数就是一个窗口
        style = ttk.Style(s.master)

        #创建左右箭头，日期旁边的
        arrow_layout = lambda dir: (
        [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        #自定义左右箭头
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(s):
        # 标头框架及其小部件
        Input_judgment_num = s.master.register(s.Input_judgment) # 需要将函数包装一下，必要的
        #最顶上的日期栏
        hframe = ttk.Frame(s.G_Frame)
        #中间的日历本体
        gframe = ttk.Frame(s.G_Frame)

        #最下面的确定，取消
        bframe = ttk.Frame(s.G_Frame)
        hframe.pack(in_=s.G_Frame, side='top', pady=5, anchor='center')
        #fill=tk.X,当窗口大小发生变化时，widgets在X方向改变
        gframe.pack(in_=s.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=s.G_Frame, side='bottom', pady=5)

        #将已经自定义后的左右箭头实例化，并连接command函数
        lbtn = ttk.Button(hframe, style='L.TButton', command=s._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=s._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)

        #在这里创建一个名为CB_year的全局变量，且CB_year是一个combobox，即一个可以拉下来查看的栏，其值为当前年到11年前之间的所有年，倒序排列
        s.CB_year = ttk.Combobox(hframe, width = 5, values = [str(year) for year in range(datetime.now().year, datetime.now().year-11,-1)], validate = 'key', validatecommand = (Input_judgment_num, '%P'))
        #默认值为当前年
        s.CB_year.current(0)
        s.CB_year.grid(in_=hframe, column=1, row=0)
        #下面两条语句的意思，选中某个对应年份的值，便调动update函数，更新到对应年份的日历
        s.CB_year.bind('<KeyPress>', lambda event:s._update(event, True))#将前面的event作为参数传入Update函数中
        s.CB_year.bind("<<ComboboxSelected>>", s._update)
        tk.Label(hframe, text = '年', justify = 'left').grid(in_=hframe, column=2, row=0, padx=(0,5))

        #和上面一样的逻辑
        s.CB_month = ttk.Combobox(hframe, width = 3, values = ['%02d' % month for month in range(1,13)], state = 'readonly')
        s.CB_month.current(datetime.now().month - 1)
        s.CB_month.grid(in_=hframe, column=3, row=0)
        s.CB_month.bind("<<ComboboxSelected>>", s._update)
        tk.Label(hframe, text = '月', justify = 'left').grid(in_=hframe, column=4, row=0)

        # 日历部件
        s._calendar = ttk.Treeview(gframe, show='', selectmode='none', height=7)
        s._calendar.pack(expand=1, fill='both', side='bottom', padx=5)
        ttk.Button(bframe, text = "确 定", width = 6, command = lambda: s._exit(True)).grid(row = 0, column = 0, sticky = 'ns', padx = 20)
        ttk.Button(bframe, text = "取 消", width = 6, command = s._exit).grid(row = 0, column = 1, sticky = 'ne', padx = 20)
        #添加边框
        tk.Frame(s.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 0, relwidth = 1, relheigh = 2/200)
        tk.Frame(s.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 198/200, relwidth = 1, relheigh = 2/200)
        tk.Frame(s.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 0, rely = 0, relwidth = 2/200, relheigh = 1)
        tk.Frame(s.G_Frame, bg = '#565656').place(x = 0, y = 0, relx = 198/200, rely = 0, relwidth = 2/200, relheigh = 1)
    
    def __config_calendar(s):
        # cols = s._cal.formatweekheader(3).split()
        cols = ['日','一','二','三','四','五','六']
        s._calendar['columns'] = cols
        s._calendar.tag_configure('header', background='grey90')
        s._calendar.insert('', 'end', values=cols, tag='header')
        # 调整其列宽
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            s._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                anchor='center')

    def __setup_selection(s, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            s._selection = None

        s._font = tkFont.Font()
        #将s._calendar的值画在canvas上
        s._canvas = canvas = tk.Canvas(s._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
        #点击日历则遗忘画布
        canvas.bind('<Button-1>', __canvas_forget)
        s._calendar.bind('<Configure>', __canvas_forget)
        s._calendar.bind('<Button-1>', s._pressed)

    def _build_calendar(s):
        year, month = s._date.year, s._date.month
        header = s._cal.formatmonthname(year, month, 0)
        # 更新日历显示的日期
        cal = s._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(s._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            s._calendar.item(item, values=fmt_week)

    def _show_select(s, text, bbox):
        x, y, width, height = bbox
        textw = s._font.measure(text)
        canvas = s._canvas
        canvas.configure(width = width, height = height)
        canvas.coords(canvas.text, (width - textw)/2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=s._calendar, x=x, y=y)

    def _pressed(s, evt = None, item = None, column = None, widget = None):
        """在日历的某个地方点击。"""
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)
        if not column or not item in s._items:
            # 在工作日行中单击或仅在列外单击。
            return
        item_values = widget.item(item)['values']
        if not len(item_values): # 这个月的行是空的。
            return
        text = item_values[int(column[1]) - 1]
        if not text: 
            return
        bbox = widget.bbox(item, column)
        if not bbox: # 日历尚不可见
            s.master.after(20, lambda : s._pressed(item = item, column = column, widget = widget))
            return
        text = '%02d' % text
        s._selection = (text, item, column)
        s._show_select(text, bbox)

    def _prev_month(s):
        """更新日历以显示前一个月。"""
        s._canvas.place_forget()
        s._selection = None

        sign_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\签到记录\\{datetime.now().year}_{datetime.now().month}.txt').read_line()
        for i in range(len(sign_lis)):
            eval('canvas'+str(i)).place_forget()
        s._date = s._date - timedelta(days=1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

        try:
            s._sign(s._date.year,s._date.month)
        except:
            pass

    def _next_month(s):
        """更新日历以显示下一个月。"""
        s._canvas.place_forget()
        s._selection = None

        sign_lis = FileOperator(f'C:\\Users\\86180\\Desktop\\动态日程安排器\\签到记录\\{datetime.now().year}_{datetime.now().month}.txt').read_line()
        for i in range(len(sign_lis)):
            eval('canvas'+str(i)).place_forget()

        year, month = s._date.year, s._date.month
        s._date = s._date + timedelta(
        days=calendar.monthrange(year, month)[1] + 1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

        try:
            s._sign(s._date.year,s._date.month)
        except:
            pass

    def _update(s, event = None, key = None):
        """刷新界面"""
        if key and event.keysym != 'Return': return
        year = int(s.CB_year.get())
        month = int(s.CB_month.get())
        if year == 0 or year > 9999: return
        s._canvas.place_forget()
        s._date = datetime(year, month, 1)
        s._build_calendar() # 重建日历
        #s._sign(s.path)
        if year == datetime.now().year and month == datetime.now().month:
            day = datetime.now().day
            #自动选择当前日
            for _item, day_list in enumerate(s._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day)+1)
                    s.master.after(100, lambda :s._pressed(item = item, column = column, widget = s._calendar))
        #s._sign(s.path)

    def _exit(s, confirm = False):
        if not confirm: s._selection = None
        s.master.destroy()

    def _main_judge(s):
        """判断窗口是否在最顶层"""
        try:
            if s.master.focus_displayof() == None or 'toplevel' not in str(s.master.focus_displayof()):pass # s._exit()
            else: s.master.after(10, s._main_judge)
        except:
            s.master.after(10, s._main_judge)

    def selection(s):
        """返回表示当前选定日期的日期时间。"""
        if not s._selection: return None
        year, month = s._date.year, s._date.month
        return str(datetime(year, month, int(s._selection[0])))[:10]

    def Input_judgment(s, content):
        """输入判断"""
        if content.isdigit() or content == "":
            return True
        else:
            return False

    def _sign(s,year,month):
        """从签到文件中获取本月信息，并将以签到的年份可视化"""
        count = 0
        path=f'C:\\Users\\86180\\Desktop\\动态日程安排器\\签到记录\\{year}_{month}.txt'
        sign_lis = FileOperator(path).read_line()
        for i in range(len(sign_lis)):
            sign_lis[i]=int(sign_lis[i])
        year = datetime.now().year
        month = datetime.now().month
        for day in sign_lis:
            for _item, day_list in enumerate(s._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day)+1)
                    s.drawline(item=item,column=column,widget=s._calendar,count=count)
                    count += 1
    
    def drawline(s,item,column,widget,count):
        """绘制签到信息"""
        bbox = widget.bbox(item,column)
        if not bbox: # 日历尚不可见
            s.master.after(20, lambda : s.drawline(item = item, column = column, widget = widget,count=count))
            return
        x,y,width,height = bbox
        item_value = widget.item(item)['values']
        text = item_value[int(column[1]) - 1]
        text = '%02d' % text
        globals()['canvas'+str(count)] = canvas = tk.Canvas(s._calendar,bg='white', borderwidth=0, highlightthickness=0)
        canvas.configure(width=width,height=height)
        canvas.text = canvas.create_text(0, 0, fill='black', anchor='w')
        canvas.create_line(0,0,20,20,fill='red',width=2)
        textw = s._font.measure(text)
        canvas.configure(width = width, height = height)
        canvas.coords(canvas.text, (width - textw)/2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=s._calendar, x=x, y=y)

#logging.disable(logging.CRITICAL)