import tkinter as tk
from tkinter import simpledialog,messagebox
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

def sort_printing(words,times):
    index = 0
    printing = ''
    while True:
        for ii in range(times):
            printing += f'{words[index]} , '
            index += 1
            if index >= len(words):
                return printing
        printing += '\n'

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

def add_book():
    while True:
        book_num = simpledialog.askstring('book manager','圖書編號:')
        if book_num == '' or book_num == None:
            save()
            break
        else:
            book_info[book_num] = simpledialog.askstring('book manager','書名:')
            print(book_info)

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