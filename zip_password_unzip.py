import tkinter as tk
import os
from tkinter import messagebox
from unrar import rarfile
from threading import Thread


def getPwd(dict):
    with open(dict, 'r') as f:
        for pwd in f:
            yield pwd.strip()


def slowerDecode(fp, pwd, check_file, extract_path):
    fp.extractall(extract_path, pwd=pwd)
    if os.path.exists(check_file):
        messagebox.showinfo(message="密码：" + pwd)
        messagebox.showinfo(message="程序结束")
        messagebox.showinfo(message="密码：" + pwd)
        exit(0)


def quickDecode(fp, pwd, extract_path):
    fp.extractall(extract_path, pwd=pwd)


def check(obs):
    flag = 1
    for ob in obs:
        if not ob.checkExist():
            flag = 0
            ob.showError()

    if (not flag):
        return 0
    else:
        for ob in obs:
            if not ob.check():
                flag = 0
                ob.showError()

    if (not flag):
        return 0
    else:
        for ob in obs:
            ob.right()
        return 1


def main(obs):
    extract_path = obs[0].path_input.get()
    rar_path = obs[1].path_input.get()
    txt_path = obs[2].path_input.get()
    pwds = getPwd(txt_path)
    global var1
    global var2
    if (check(obs)):
        if (var1.get() == 0 and var2.get() == 0):
            messagebox.showerror(message="选择一个选项！！！")
        elif (var1.get() == 0 and var2.get() == 1):
            fp = rarfile.RarFile(rar_path)
            check_file = fp.namelist()[0]
            for pwd in pwds:
                slowerDecode(fp, pwd, check_file, extract_path)
        elif (var1.get() == 1 and var2.get() == 0):
            fp = rarfile.RarFile(rar_path)
            for pwd in pwds:
                t = Thread(target=quickDecode, args=(fp, pwd, extract_path))
                t.start()
            exit(0)
        else:
            messagebox.showerror(message="只选择一个！！！")


class FolderPath:

    def __init__(self, y=0, error_message="Not exists!", path_input="", text=''):
        self.y = y
        self.error_message = error_message
        self.path_input = path_input
        self.text = text

    def createLabel(self):
        label = tk.Label(window, bg="white", font=("楷体", 13), width=20, text=self.text)
        cv.create_window(100, self.y, window=label)

    def createEntry(self):
        entry = tk.Entry(window, fg="blue", width="40", bg="#ffe1ff", textvariable=self.path_input)
        cv.create_window(330, self.y, window=entry)

    def show(self):
        self.createLabel()
        self.createEntry()

    def showError(self, color="red"):
        label = tk.Label(window, bg="white", fg=color, font=("楷体", 13), width="10", text=self.error_message)
        cv.create_window(530, self.y, window=label)

    def checkExist(self):
        self.error_message = 'Not exists!'
        if not os.path.exists(self.path_input.get()):
            return 0
        return 1

    def check(self):
        if not os.path.isdir(self.path_input.get()):
            self.error_message = 'Not a dir!'
            return 0
        else:
            return 1

    def right(self):
        self.error_message = "right path!"
        self.showError('#00FFFF')


class FilePath(FolderPath):
    def check(self):
        if (self.path_input.get().split('.')[-1] == self.suffix):
            return 1
        else:
            self.error_message = "Not " + self.suffix + '!'
            return 0


window = tk.Tk()
window.title('made by qiufeng')
window.geometry('600x300')
cv = tk.Canvas(window, width=600, height=300, bg='white')
cv.pack()

folderpath = FolderPath(y=140, path_input=tk.StringVar(), text="请输入解压路径")
folderpath.show()

rarpath = FilePath(y=60, path_input=tk.StringVar(), text="请输入rar路径")
rarpath.suffix = 'rar'
rarpath.show()

txtpath = FilePath(y=100, path_input=tk.StringVar(), text="请输入字典路径")
txtpath.suffix = 'txt'
txtpath.show()
obs = [folderpath, rarpath, txtpath]

# 多选框
var1 = tk.IntVar()
var2 = tk.IntVar()
ck1 = tk.Checkbutton(window, text="直接破解(无法获得密码)", variable=var1)
cv.create_window(150, 200, window=ck1)
ck2 = tk.Checkbutton(window, text="慢速(可获得密码)", variable=var2)
cv.create_window(132, 230, window=ck2)
button = tk.Button(window, text="确认", command=lambda: main(obs))
cv.create_window(90, 260, window=button)

window.mainloop()
