import tkinter
import base64

# 初始化gui界面和mune菜单，传递frame布局
class GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("加解密工具盒子_v1.0")
        self.init_window_name.geometry('1080x680+400+150')
        self.init_window_name.iconbitmap('./panda.ico')
        self.init_window_name.resizable(False, False)
        # 菜单栏
        self.init_window_menu = tkinter.Menu(self.init_window_name)
        self.init_caesar_menu = tkinter.Menu(self.init_window_menu, tearoff=0)
        self.init_window_menu.add_cascade(label="凯撒密码", menu=self.init_caesar_menu)
        self.init_caesar_menu.add_command(label="经典凯撒（字母表）", command=self.caesar_abc_show)
        self.init_caesar_menu.add_command(label="变异凯撒（ASCII码表）", command=self.caesar_ascii_show)
        self.init_base64_menu = tkinter.Menu(self.init_window_menu, tearoff=0)
        self.init_window_menu.add_cascade(label="base64", menu=self.init_base64_menu)
        self.init_base64_menu.add_command(label="base64", command=self.base64_show)
        '''-----可持续补充加密-----'''
        self.init_window_name.config(menu=self.init_window_menu)
        # 创建frame布局，初始化信息页面
        self.create_init_frame()
        initPage(self.init_window_frame)

    # 创建frame布局
    def create_init_frame(self):
        self.init_window_frame = tkinter.Frame(self.init_window_name)
        self.init_window_frame.pack(fill='both', expand='YES')

    '''凯撒类'''
    # 凯撒密码页面跳转
    def init_caesar_show(self, state):
        self.init_window_frame.destroy()
        self.create_init_frame()
        caesarPage(self.init_window_frame, state)
    
    # 经典凯撒（字母表）赋值state
    def caesar_abc_show(self):
        self.state = "abc"
        self.init_caesar_show(self.state)
    
    # 变异凯撒（ASCII码表）赋值state
    def caesar_ascii_show(self):
        self.state = "ascii"
        self.init_caesar_show(self.state)

    '''base类'''
    def init_base64_show(self, state):
        self.init_window_frame.destroy()
        self.create_init_frame()
        base64Page(self.init_window_frame, state)

    # base64加解密
    def base64_show(self):
        self.state = "64"
        self.init_base64_show(self.state)

# 初始化欢迎页面
class initPage():
    def __init__(self, init_window_frame):
        self.init_window_frame = init_window_frame
        # 开始界面
        self.init_window_title = tkinter.Frame(self.init_window_frame)
        tkinter.Label(self.init_window_title, text="欢迎使用", font=('Arial', 50)).pack()
        tkinter.Label(self.init_window_title, text="哦胖的加解密工具箱", font=('Arial', 50)).pack()
        tkinter.Label(self.init_window_title, text="在此特别鸣谢欧耶的大力支持", font=('Microsoft YaHei', 14), fg="grey").pack(side='right')
        self.init_window_title.pack(side='top', fill='y', pady=200)
    
# 凯撒密码
class caesarPage():
    def __init__(self, init_window_frame, state):
        self.init_window_frame = init_window_frame
        self.state = state
        # 标签
        self.init_data_label = tkinter.Label(self.init_window_frame, text="明 文")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = tkinter.Label(self.init_window_frame, text="密 文")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = tkinter.Label(self.init_window_frame, text="日 志")
        self.log_label.grid(row=12, column=0)
        # 输出文本框和滚动条的frame
        self.result_frame = tkinter.Frame(self.init_window_frame)
        self.result_frame.grid(row=1, column=12, rowspan=16, columnspan=10)
        self.result_sc = tkinter.Scrollbar(self.result_frame)
        # 文本框
        self.init_data_Text = tkinter.Text(self.init_window_frame, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = tkinter.Text(self.result_frame, width=70, height=48, yscrollcommand=self.result_sc.set)  #处理结果展示
        self.result_data_Text.pack(side='left')
        self.log_data_Text = tkinter.Text(self.init_window_frame, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 滚动条
        self.result_sc.configure(command=self.result_data_Text.yview)
        self.result_sc.pack(side='right', fill='y')
        # 按钮
        if self.state == 'abc':
            self.button = tkinter.Button(self.init_window_frame, text="凯撒暴力破解", bg="lightblue", width=11,command=self.caesar_abc_text)
        elif self.state == 'ascii':
            self.button = tkinter.Button(self.init_window_frame, text="ASCII凯撒爆破", bg="lightblue", width=11,command=self.caesar_ascii_text)
            self.var = tkinter.IntVar()
            self.var.set('1')
            tkinter.Checkbutton(self.init_window_frame, text="偏移量增加", variable=self.var, onvalue=1, offvalue=0).grid(row=5, column=11)
        self.button.grid(row=4, column=11)
        # 初始打印
        self.print_in_result("输出结果")
        self.print_in_log("")
    
    # 字母表凯撒密码暴力破解算法
    def caesar_abc_text(self):
        text = self.init_data_Text.get(1.0, 'end').strip().replace('\n', '')
        if text:
            try:
                result = ""
                for j in range(26):
                    b = ''
                    for i in text:
                        d = ord(i)
                        if d >= 65 and d <= 90:
                            temp = chr(((ord(i)-64) + j)%26 + 64)
                        elif d >= 97 and d <= 122:
                            temp = chr(((ord(i)-96) + j)%26 + 96)
                        else:
                            temp = i
                        b += temp
                    result += "第%d个输出为：%s\n"%(j,b)
                self.print_in_result(result)
                self.print_in_log("INFO:加解密成功 success\n")
            except:
                self.print_in_result("加解密失败,请联系作者o_pang@163.com，告诉他你怎么搞的...")
                self.print_in_log("ERROR:加解密失败 failed\n")
        else:
            self.print_in_log("ERROR:输入为空 failed\n")
    
    # ascii表凯撒爆破
    def caesar_ascii_text(self):
        text = self.init_data_Text.get(1.0, 'end').strip().replace('\n', '')
        state = self.var.get()
        if text:
            try:
                result = ""
                for j in range(256):
                    b = ''
                    for i in range(len(text)):
                        if state == 0:
                            b += chr((ord(text[i]) + j)%256)
                        else:
                            b += chr((ord(text[i]) + j + i)%256)
                    result += "第%d个输出为：%s\n"%(j,b)
                self.print_in_result(result)
                self.print_in_log("INFO:加解密成功 success\n")
            except:
                self.print_in_result("加解密失败,注意输入格式")
                self.print_in_log("ERROR:加解密失败 failed\n")
        else:
            self.print_in_log("ERROR:输入为空 failed\n")

    # result框内输出
    def print_in_result(self, text):
        self.result_data_Text.config(state="normal")
        self.result_data_Text.delete(1.0, 'end')
        self.result_data_Text.insert(1.0, text)
        self.result_data_Text.yview('end')
        self.result_data_Text.config(state="disabled")

    # log框内输出
    def print_in_log(self, text):
        self.log_data_Text.config(state="normal")
        self.log_data_Text.insert('end', text)
        self.log_data_Text.yview('end')
        self.log_data_Text.config(state="disabled")
        
# base64
class base64Page():
    def __init__(self, init_window_frame, state):
        self.init_window_frame = init_window_frame
        self.state = state
        # 声明三个frame
        self.init_data_frame = tkinter.Frame(self.init_window_frame, width=480, height=480)
        self.result_data_frame = tkinter.Frame(self.init_window_frame, width=500, height=650)
        self.trans_button_frame = tkinter.Frame(self.init_window_frame, width=80, height=40)
        self.log_data_frame = tkinter.Frame(self.init_window_frame, width=474, height=150)
        self.init_data_frame.grid(row=0, column=0, sticky='nw')
        self.result_data_frame.grid(row=0, column=2, rowspan=3, sticky='ne')
        self.trans_button_frame.grid(row=0, column=1)
        self.log_data_frame.grid(row=1, column=0)
        # 滚动条
        self.init_sc = tkinter.Scrollbar(self.init_data_frame)
        self.result_sc = tkinter.Scrollbar(self.result_data_frame)
        # 明文frame
        self.init_data_label = tkinter.Label(self.init_data_frame, text="明 文")
        self.init_data_Text = tkinter.Text(self.init_data_frame, font=('Microsoft YaHei', 11), width=52, height=23, yscrollcommand=self.init_sc.set)
        self.init_data_label.grid(row=0, column=0, sticky='nw')
        self.init_data_Text.grid(row=1, column=0)
        # 密文frame
        self.result_data_label = tkinter.Label(self.result_data_frame, text="密 文")
        self.result_data_Text = tkinter.Text(self.result_data_frame, font=('Microsoft YaHei', 11), width=54, height=31, yscrollcommand=self.result_sc.set)
        self.result_data_label.grid(row=0, column=0, sticky='nw')
        self.result_data_Text.grid(row=1, column=0)
        # 滚动条
        self.init_sc.configure(command=self.init_data_Text.yview, bg='white')
        self.init_sc.grid(row=1, column=1, sticky='n'+'s')
        self.result_sc.configure(command=self.result_data_Text.yview)
        self.result_sc.grid(row=1, column=1, sticky='n'+'s')
        # 按钮frame
        if self.state == '64':
            tkinter.Label(self.trans_button_frame, text='（支持多行）', fg='grey').grid(row=0, column=0)
            self.trans_button_en = tkinter.Button(self.trans_button_frame, text="BASE64编码→", bg="lightblue", width=11, command=self.base64_text_encry)
            self.trans_button_de = tkinter.Button(self.trans_button_frame, text="←BASE64解码", bg="lightblue", width=11, command=self.base64_text_decry)
            self.trans_button_en.grid(row=1, column=0)
            self.trans_button_de.grid(row=2, column=0)
        # 日志frame
        self.log_data_label = tkinter.Label(self.log_data_frame, text="日 志")
        self.log_data_Text = tkinter.Text(self.log_data_frame, font=('Microsoft YaHei', 11), width=52, height=6)
        self.log_data_label.grid(row=0, column=0, sticky='nw')
        self.log_data_Text.grid(row=1, column=0)
        # 初始打印
        self.print_in_log("")

    # base64加密
    def base64_text_encry(self):
        text = self.init_data_Text.get(1.0, 'end').strip().split('\n')
        if text != ['']:
            try:
                result = ''
                for value in text:
                    if value.strip() != '':
                        result += str(base64.b64encode(value.encode('utf-8')))[2:-1] + '\n'
                self.result_data_Text.delete(1.0, 'end')
                self.result_data_Text.insert('end', result)
                self.print_in_log("INFO:BASE64加密成功 success\n")
            except:
                self.result_data_Text.insert('end', "加密失败")
                self.print_in_log("ERROR:加密失败 failed\n")
        else:
            self.print_in_log("ERROR:输入为空 failed\n")

    # base64解密
    def base64_text_decry(self):
        text = self.result_data_Text.get(1.0, 'end').strip().split('\n')
        if text != ['']:
            try:
                result = ''
                for value in text:
                    if value.strip() != '':
                        result += base64.b64decode(value).decode('utf-8') + '\n'
                self.init_data_Text.delete(1.0, 'end')
                self.init_data_Text.insert('end', result)
                self.print_in_log("INFO:BASE64解密成功 success\n")
            except:
                self.init_data_Text.insert('end', "解密失败")
                self.print_in_log("ERROR:解密失败 failed\n")
        else:
            self.print_in_log("ERROR:输入为空 failed\n")

    # log框内输出
    def print_in_log(self, text):
        self.log_data_Text.config(state="normal")
        self.log_data_Text.insert('end', text)
        self.log_data_Text.yview('end')
        self.log_data_Text.config(state="disabled")



def gui_start():
    init_window = tkinter.Tk()
    GUI_ROOT = GUI(init_window)
    GUI_ROOT.set_init_window()

    init_window.mainloop()

if __name__ == "__main__":
    gui_start()