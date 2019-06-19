
import tkinter as tk

window = tk.Tk()

window.title('文库下载器')

window.geometry('500x300')

l = tk.Label(window, text='在下方输入文库链接', font=('Arial', 12))
l.grid(row=0, pady=20)


tk.Entry(window,text = '', width=60).grid(row=1)

def download():
    print('hello')


tk.Button(window, text='下载', command=download).grid(row=2, pady=20)

window.mainloop()