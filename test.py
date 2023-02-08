import tkinter as tk

root = tk.Tk()
root.geometry('300x300')

s = ['a','b','c']
for item in s:
    canvas = tk.Canvas(root,background='green',tag=item)
    canvas.pack()



root.mainloop()