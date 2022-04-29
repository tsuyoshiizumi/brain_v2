import tkinter as tk 
from functools import partial

def outputWords(num):
    root.v = root.v+num
    txtBox.delete(0,tk.END)
    txtBox.insert(tk.END, root.v)
def plus():
    root.v1= int(root.v)
    root.v=''
    txtBox.delete(0,tk.END)
def ik():
    root.v=root.v1 + int(root.v)
    root.v=root.v2 - int(root.v)
    root.v=root.v3 * int(root.v)
    root.v=root.v4 / int(root.v)
    txtBox.delete(0,tk.END)
    txtBox.insert(tk.END, root.v)
def negative():
    root.v2= int(root.v)
    root.v=''
    txtBox.delete(0,tk.END)
def times():
    root.v3= int(root.v)
    root.v=''
    txtBox.delete(0,tk.END)
def divide():
    root.v4= int(root.v)
    root.v=''
    txtBox.delete(0,tk.END)

root = tk.Tk()
root.title("Hello World")
root.geometry("400x200")

root.v=''
root.v1=0

label = tk.Label(root, text="こんにちは")
label.pack()
button = tk.Button(text='1', width=1,command=partial(outputWords, '1'))
button.place(x=80, y=80)
button2 = tk.Button(text='2', width=1,command=partial(outputWords, '2'))
button2.place(x=95, y=80)
button3 = tk.Button(text='3', width=1,command=partial(outputWords, '3'))
button3.place(x=110, y=80)
buttonpuls = tk.Button(text='+', width=1,command=partial(plus))
buttonpuls.place(x=125, y=80)
buttonik = tk.Button(text='=', width=1,command=partial(ik))
buttonik.place(x=140, y=80)
button4 = tk.Button(text='4', width=1,command=partial(outputWords, '4'))
button4.place(x=80, y=105)
button5 = tk.Button(text='5', width=1,command=partial(outputWords, '5'))
button5.place(x=95, y=105)
button6 = tk.Button(text='6', width=1,command=partial(outputWords, '6'))
button6.place(x=110, y=105)
button7 = tk.Button(text='7', width=1,command=partial(outputWords, '7'))
button7.place(x=80, y=130)
button8 = tk.Button(text='8', width=1,command=partial(outputWords, '8'))
button8.place(x=95, y=130)
button9 = tk.Button(text='9', width=1,command=partial(outputWords, '9'))
button9.place(x=110, y=130)
buttonnegative = tk.Button(text='-', width=1,command=partial(negative))
buttonnegative.place(x=125, y=105)
buttontimes = tk.Button(text='*', width=1,command=partial(times))
buttontimes.place(x=125, y=130)
buttondivide = tk.Button(text='/', width=1,command=partial(divide))
buttondivide.place(x=125, y=155)
txtBox = tk.Entry()
txtBox.configure(state='normal', width=50)
txtBox.pack()

root.mainloop()