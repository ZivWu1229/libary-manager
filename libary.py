import time
import json
import tkinter as tk
from tkinter import simpledialog,messagebox
import os

borrowed_book = []
book_info = {}
win1 = tk.Tk()
win1.withdraw()
delayed_list = {}

class Select_mode():
    def __init__(self):
        self.mode_win = tk.Toplevel(win1)
        self.mode_win.title('labary manager')
        self.mode_borrow =     tk.Button(self.mode_win,text='借書',command=mode.borrow,font=('標楷體',28),width=15).grid(row=1,column=1)
        self.mode_return =     tk.Button(self.mode_win,text='還書',command=mode.return_mode,font=('標楷體',28),width=15).grid(row=2,column=1)
        self.mode_num_search = tk.Button(self.mode_win,text='查詢',command=mode.search_from_num,font=('標楷體',28),width=15).grid(row=3,column=1)
        self.mode_delay =      tk.Button(self.mode_win,text='逾期未還',command=mode.delay,font=('標楷體',28),width=15).grid(row=4,column=1)
        self.delayed_list =    tk.Button(self.mode_win,text='管理懲罰',command=mode.delayed_list,font=('標楷體',28),width=15).grid(row=5,column=1)

class Borrow_win():
    def __init__(self):
        self.borrow_book = tk.StringVar()
        self.book_num = tk.StringVar()
        self.borrow_win = tk.Toplevel(win1)
        self.info = tk.Label(self.borrow_win,textvariable=self.borrow_book).pack()
        self.book_num_entry = tk.Entry(self.borrow_win,textvariable=self.book_num).pack()
        self.new_book = tk.Button(self.borrow_win,text='新增書籍').pack()
        self.submit = tk.Button(self.borrow_win, text='取消').pack()

class Delayed_manager():
    def __init__(self):
        self.win = tk.Toplevel(win1)
        self.new_button  = tk.Button(self.win,text='新增懲罰者',command=self.new   ,font=('標楷體',28),width=15).grid(row=1,column=1)
        self.view_button = tk.Button(self.win,text='檢視懲罰者',command=self.view  ,font=('標楷體',28),width=15).grid(row=2,column=1)
        self.del_button  = tk.Button(self.win,text='刪除懲罰者',command=self.delete,font=('標楷體',28),width=15).grid(row=3,column=1)
    def new(self):
        stu_num = simpledialog.askstring('新增懲罰者','座號:')
        times = int(simpledialog.askstring('新增懲罰者','時長(天):'))*86400
        delayed_list[stu_num] += time.time()-(time.time()%86400)+times
        os.remove('user_info.json')
        with open('user_info.json','x') as file:
            file.write(js(delayed_list))
        return
    def view(self):
        printing = []
        end_time = None
        for i in delayed_list:
            if delayed_list[i] > time.time():
                end_time = time.localtime(delayed_list[i])
                printing.append(f'座號:{i},懲罰到期日:{end_time.tm_year-1911}年{end_time.tm_mon}月{end_time.tm_mday}日')
        messagebox.showinfo('檢視懲罰者',sort_printing(printing,2))
    def delete(self):
        pass

def sort_printing(words,times):
    index = 0
    printing = ''
    while True:
        for ii in range(times):
            printing += f'{words[index]}, '
            index += 1
            if index >= len(words):
                return printing
        printing += '\n'

def js(strs):
    strs = str(strs)
    returning = []
    for i in strs:
        if i == "'":
            returning.append('"')
        else:
            returning.append(i)
    return ''.join(returning)

def load_delayed_list():
    global delayed_list
    with open('delayed_list.json',encoding='utf8') as file:
        delayed_list = json.load(file)

def load_book_info():
    global book_info
    with open('book_info.json',encoding='utf8') as file:
        book_info = json.load(file)

def load_user_info():
    global delayed_list
    with open('user_info.json',encoding='utf8') as file:
        delayed_list = json.load(file)

def read_file():
    global borrowed_book
    with open('borrowed_book.json') as file:
        print(file.read())
        borrowed_book = json.load(file)

def borrow_book(book_num,stu_num):
    time_now = time.localtime(time.time())
    borrowed_book.append([book_num,stu_num,time_now.tm_year-1911,time_now.tm_mon,time_now.tm_mday,time.time()])
    os.remove('borrowed_book.json')
    with open('borrowed_book.json','x') as file:
        file.write(js(borrowed_book))

def return_book(book_num):
    global borrowed_book
    for i in borrowed_book:
        if i[0] == book_num:
                borrowed_book.remove(i)
                os.remove('borrowed_book.json')
                with open('borrowed_book.json','x') as file:
                        file.write(str(borrowed_book))
                messagebox.showinfo('還書','還書程序已完成')
                return
    messagebox.showinfo('還書','這本書未借出')

load_book_info()
read_file()
load_user_info()

class Mode():
    def borrow(self):
        book = 0
        book_num = simpledialog.askstring('借書','圖書編號:')
        stu_num = simpledialog.askstring('借書','座號:')
        try:
            stu_num = int(stu_num)
        except ValueError:
            messagebox.showinfo('借書','輸入的值必須為數字')
        else:
            for i in borrowed_book:
                if book_num == i[0]:
                    messagebox.showinfo('借書','這本書已被借閱')
                    return
            for i in borrowed_book:
                if stu_num == i[1]:
                    book += 1
            if book >= 2:
                messagebox.showinfo('借書','本使用者已借閱兩本書')
                return
            for i in book_info:
                if i == book_num:
                    if messagebox.askokcancel('借書',f'座號: {stu_num},圖書編號: {book_num},書名: {book_info[book_num]}'):
                        borrow_book(book_num,stu_num)
                        messagebox.showinfo('借書','借書程序已完成')
                        return
                    else:
                        return
            messagebox.showinfo('借書','沒有此讀書編號')

    def return_mode(self):
        book_num = simpledialog.askstring('還書','圖書編號:')
        return_book(book_num)
    def search_from_num(self):
        printing = ''
        print('')
        num = simpledialog.askstring('查詢','您的座號:')
        if num == None or num == '':
            return
        try:
            num = int(num)
        except:
            messagebox.showinfo('查詢','輸入的值必須是數字')
        else:
            if num == -1:
                for i in borrowed_book:
                    printing = printing + f'圖書編號: {i[0]}, 座號: {i[1]}, 借書時間: {i[2]}年 {i[3]}月 {i[4]}日\n'
            for i in borrowed_book:
                if i[1] == num:
                    printing = printing + f'圖書編號: {i[0]}, 座號: {i[1]}, 借書時間: {i[2]}年 {i[3]}月 {i[4]}日\n'
            messagebox.showinfo('查詢',printing)
        print('')
    def delay(self):
        printing = []
        for i in borrowed_book:
            if time.time() - i[-1] >= 1209600:
                printing.append(f'圖書編號: {i[0]}, 座號: {i[1]}, 借書時間: {i[2]}年 {i[3]}月 {i[4]}日')
        messagebox.showinfo('逾期未還',sort_printing(printing,1))
    def delayed_list(self):
        win = Delayed_manager()

mode = Mode()
select_mode = Select_mode()
win1.mainloop()