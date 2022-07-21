import tkinter as tk
from tkinter import Variable, simpledialog,messagebox
import json
import os
import webbrowser

book_info = {}

def html(title,body):
    html = f'''<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
</head>
<body>
'''
    for i in body:
        html += f'<p>{i}</p>\n'
    html += '''</body>
</html>'''
    try:
        os.remove('index.html')
    except:
        pass
    with open('index.html','x') as file:
        file.write(html)
    webbrowser.open('index.html')

def load_book_info():
    global book_info
    with open('book_info.json',encoding='utf8') as file:
        book_info = json.load(file)

def js(strs):
    strs = str(strs)
    returning = []
    for i in strs:
        if i == "'":
            returning.append('"')
        else:
            returning.append(i)
    return ''.join(returning)

def save():
    os.remove('book_info.json')
    with open('book_info.json','x',encoding='utf8') as file:
        file.write(js(book_info))

class Adding_book():
    def __init__(self):
        self.win = tk.Toplevel(win1)
        self.win.geometry('300x90')
        self.section = tk.StringVar()
        self.number  = tk.StringVar()
        self.name    = tk.StringVar(value='')
        self.book_number = tk.Label(self.win,font=('標楷體',16),text='圖書編號:').place(x=0,y=0)
        self.section_box = tk.Entry(self.win,show=None,width=2,font=('標楷體',16),textvariable=self.section).place(x=110,y=0)
        self.number_box  = tk.Entry(self.win,show=None,width=5,font=('標楷體',16),textvariable=self. number).place(x=135,y=0)
        self.book_name   = tk.Label(self.win,font=('標楷體',16),text='書名:').place(x=0,y=30)
        self.name_box    = tk.Entry(self.win,show=None,width=20,font=('標楷體',16),textvariable=self.  name).place(x=60,y=30)
        self.submit_box  = tk.Button(self.win,text='新增',font=('標楷體',16),command=self.submit).place(x=0,y=60)
        self.sort_book()

    def sort_book(self):
        book_nums = []
        for i in book_info:
            book_nums.append(int(i))
        self.number .set(max(book_nums) %100+1)
        self.section.set(max(book_nums)//100)
        print(type(self.number.get()))
        if int(self.number.get()) < 10:
            print(True)
            self.number.set('0'+self.number.get())
    def submit(self):
        try:
            self.number.set(int(self.number.get()))
            self.section.set(int(self.section.get()))            
        except :
            messagebox.showerror('錯誤',"輸入的不是數字")
            self.sort_book()
            return
        finally:
            print(self.section.get()+self.number.get())
        if self.name.get() == '':
            messagebox.showerror('錯誤','名字不能為空')
            self.sort_book()
            return
        if len(self.section.get()) > 1 or len(self.number.get()) > 2:
            messagebox.showerror('錯誤','您輸入的數字過大')
            self.sort_book()
            return
        if len(self.number.get()) == 1:
            book_number = self.section.get()+"0"+self.number.get()
        elif int(self.number.get()) == 0:
            book_number = self.section.get()+"00"
        else:
            book_number = self.section.get()+self.number.get()
        for i in book_info:
            if i == book_number:
                if not messagebox.askokcancel('新增書籍','本編號已存在書籍\n確認覆蓋?'):
                    self.sort_book()
                    return
        if messagebox.askokcancel('新增書籍',f'編號: {book_number} , 書名: {self.name.get()}\n確認新增?'):
            book_info[book_number] = self.name.get()
            save()
        self.sort_book()

def add_book():
    add_win = Adding_book()

def del_book():
    while True:
        book_num = simpledialog.askstring('book manager','圖書編號:')
        if book_num == '' or book_num == None:
            save()
            break
        else:
            if book_info[book_num] != None:
                del book_info[book_num]
                print(book_info)

def view_book():
    printing_str = []
    for i in book_info:
        printing_str.append(f'圖書編號: {i}, 書名: {book_info[i]}')
    html('book manager',printing_str)

load_book_info()

win1 = tk.Tk()
win1.title('book manager')

add_button = tk.Button(win1,text='增加書籍',font=('標楷體',24),width=15,command=add_book).pack()
del_button = tk.Button(win1,text='刪除書籍',font=('標楷體',24),width=15,command=del_book).pack()
view_button = tk.Button(win1,text='檢視書籍',font=('標楷體',24),width=15,command=view_book).pack()

win1.mainloop()