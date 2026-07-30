import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import math

HISTORY_FILE = "history.txt"

root = tk.Tk()
root.title("Digital Calculator")
root.geometry("420x700")
root.config(bg="#181818")
root.resizable(False, False)

expression = ""

# -----------------------
# Functions
# -----------------------

def update_time():
    now = datetime.now().strftime("%d-%m-%Y\n%I:%M:%S %p")
    time_label.config(text=now)
    root.after(1000, update_time)

def press(value):
    global expression
    expression += str(value)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def calculate():
    global expression
    try:
        result = str(eval(expression))
        save_history(expression, result)
        expression = result
        display_var.set(result)
        load_history()
    except:
        messagebox.showerror("Error", "Invalid Expression")
        expression = ""

def square():
    global expression
    try:
        value = eval(expression)
        result = value ** 2
        save_history(f"{expression}²", result)
        expression = str(result)
        display_var.set(result)
        load_history()
    except:
        messagebox.showerror("Error", "Invalid Input")

def sqrt():
    global expression
    try:
        value = eval(expression)
        result = math.sqrt(value)
        save_history(f"√({expression})", result)
        expression = str(result)
        display_var.set(result)
        load_history()
    except:
        messagebox.showerror("Error", "Invalid Input")

def percent():
    global expression
    try:
        value = eval(expression)
        result = value / 100
        save_history(f"{expression}%", result)
        expression = str(result)
        display_var.set(result)
        load_history()
    except:
        messagebox.showerror("Error", "Invalid Input")

def save_history(exp, result):
    with open(HISTORY_FILE, "a") as file:
        file.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} : {exp} = {result}\n")

def load_history():
    history_box.delete("1.0", tk.END)
    try:
        with open(HISTORY_FILE, "r") as file:
            history_box.insert(tk.END, file.read())
    except:
        pass

def clear_history():
    open(HISTORY_FILE, "w").close()
    load_history()

# -----------------------
# Time
# -----------------------

time_label = tk.Label(root,
                      font=("Arial",14),
                      bg="#181818",
                      fg="cyan")
time_label.pack(pady=10)

update_time()

# -----------------------
# Display
# -----------------------

display_var = tk.StringVar()

display = tk.Entry(root,
                   textvariable=display_var,
                   font=("Arial",28),
                   bd=0,
                   justify="right",
                   bg="#222",
                   fg="white")
display.pack(fill="x", padx=10, pady=10, ipady=20)

# -----------------------
# Buttons
# -----------------------

frame = tk.Frame(root, bg="#181818")
frame.pack()

buttons = [
('C',1,0),('⌫',1,1),('%',1,2),('/',1,3),
('7',2,0),('8',2,1),('9',2,2),('*',2,3),
('4',3,0),('5',3,1),('6',3,2),('-',3,3),
('1',4,0),('2',4,1),('3',4,2),('+',4,3),
('0',5,0),('.',5,1),('√',5,2),('=',5,3),
('x²',6,0)
]

for (text,row,col) in buttons:

    if text=="=":
        cmd=calculate
    elif text=="C":
        cmd=clear
    elif text=="⌫":
        cmd=backspace
    elif text=="√":
        cmd=sqrt
    elif text=="x²":
        cmd=square
    elif text=="%":
        cmd=percent
    else:
        cmd=lambda t=text: press(t)

    tk.Button(frame,
              text=text,
              command=cmd,
              width=8,
              height=3,
              font=("Arial",14),
              bg="#333",
              fg="white").grid(row=row,column=col,padx=3,pady=3)

# -----------------------
# History
# -----------------------

tk.Label(root,
         text="Calculation History",
         bg="#181818",
         fg="white",
         font=("Arial",14)).pack()

history_box = tk.Text(root,
                      height=8,
                      bg="#222",
                      fg="lime",
                      font=("Consolas",10))
history_box.pack(fill="x", padx=10)

load_history()

tk.Button(root,
          text="Clear History",
          command=clear_history,
          bg="red",
          fg="white",
          font=("Arial",12)).pack(pady=10)

# -----------------------
# Keyboard Support
# -----------------------

def key(event):
    k = event.keysym

    if k in "0123456789":
        press(k)

    elif event.char in "+-*/.":
        press(event.char)

    elif k=="Return":
        calculate()

    elif k=="BackSpace":
        backspace()

    elif k=="Escape":
        clear()

root.bind("<Key>", key)

root.mainloop()