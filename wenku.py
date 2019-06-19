
import tkinter as tk
from backend import fetch

window = tk.Tk()

window.title('文库下载器')

window.geometry('500x300')

l = tk.Label(window, text='在下方输入文库链接', font=('Arial', 12))
l.grid(row=0, pady=20)


link = tk.StringVar()
tk.Entry(window, textvariable=link, width=60).grid(row=1, columnspan=5)

choices = { 'word','PDF','PPT','txt'}
choose_var = tk.StringVar()
choose_var.set('word') # set the default option

tk.Label(window, text='选择文件类型', font=('Arial', 12)).grid(row=2, column=0, pady=20)
popupMenu = tk.OptionMenu(window, choose_var, *choices).grid(row=2, column=1, pady=20)

def download():
    fetch(link.get(), choose_var.get())


tk.Button(window, text='下载', command=download).grid(row=3, pady=20)

window.mainloop()