import math
import tkinter
import matplotlib
from tkinter import *
import matplotlib.pyplot as plt 
import numpy as np


app = tkinter.Tk()
app.geometry("400x630+100+100")
app.title("Calculator")
app.resizable(0, 0)
app.config(bg = "grey")


entry = tkinter.Entry(app, font=("arial", 20, "bold"), bg="black", fg="white", bd=10, width=20)
entry.pack()
entry.grid(row=0, column=0, columnspan=8)


operator_list = ["+", "-", ".", "%", "/"]
operations = ["+", "-", "%", "/", "*"]


def split_operation(expression):
     text_list = []
     start_index = 0
     for i, char in enumerate(expression):
          if char in operations:
               text_list.append(expression[start_index:i])
               start_index = i+1
     text_list.append(expression[start_index:])
     return text_list

               
def check_expression(expression, value):
     if len(expression)>0 and expression[-1] in operator_list and expression[-1] == value:
          return False
     splitted_operations = split_operation(expression)
     if len(splitted_operations)>0 and "." in splitted_operations[-1] and (value == "." and value in operator_list):
          return False
     return True
     
          
def plot_quadratic(a, b, c):
    x = np.linspace(-10, 10, 400) 
    y = a * x**2 + b * x + c  
    plt.plot(x, y, label=f"y = {a}x^2 + {b}x + {c}")
    
    zero = b**2 - 4 * a * c
    if zero > 0:
        x1 = (-b + np.sqrt(zero)) / (2 * a)
        x2 = (-b - np.sqrt(zero)) / (2 * a)
        plt.scatter([x1, x2], [0, 0], color="red", label="Roots")
        
    plt.axhline(0, color="black", linewidth=2, linestyle="-", label="x-axis")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show() 

def open_plot_window_quad():
    plot_window = tkinter.Toplevel()
    plot_window.title("Quadratic equation")
    plot_window.geometry("400x300")
    
    a_label = tkinter.Label(plot_window, text="a:")
    a_label.pack()
    a_entry = tkinter.Entry(plot_window)
    a_entry.pack()
    
    b_label = tkinter.Label(plot_window, text="b:")
    b_label.pack()
    b_entry = tkinter.Entry(plot_window)
    b_entry.pack()
    
    c_label = tkinter.Label(plot_window, text="c:")
    c_label.pack()
    c_entry = tkinter.Entry(plot_window)
    c_entry.pack()
    
    plot_button = tkinter.Button(plot_window, text="Print graph", command=lambda: plot_quadratic(float(a_entry.get()), float(b_entry.get()), float(c_entry.get())))
    plot_button.pack()


def open_plot_window_trig():
    plot_window = tkinter.Toplevel()
    plot_window.title("Trigonometry plot")
    plot_window.geometry("400x300")

    label = tkinter.Label(plot_window, text="Choose function:")
    label.pack()

    functions = ["Sinus", "Cosinus", "Tangens", "Cotangens"]
    chosen_function = tkinter.StringVar(value=functions[0])

    function_menu = tkinter.OptionMenu(plot_window, chosen_function, *functions)
    function_menu.pack()

    value_entry = tkinter.Entry(plot_window)
    value_entry.pack()
    value_label = tkinter.Label(plot_window, text="Value:")
    value_label.pack()

    draw_button = tkinter.Button(plot_window, text="Draw plot", command=lambda: draw_plot(chosen_function.get(), value_entry.get()))
    draw_button.pack()




def draw_plot(chosen_function, value_entry):
    try:
        value = float(value_entry)
    except ValueError:
        value = 1.0

    if chosen_function == "Sinus":
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(value * x)
        plt.plot(x, y)
        plt.title(f"Sinus({value}x)")
    elif chosen_function == "Cosinus":
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.cos(value * x)
        plt.plot(x, y)
        plt.title(f"Cosinus({value}x)")
    elif chosen_function == "Tangens":
        x = np.linspace(0, 2 * np.pi, 400)
        y = np.tan(value * x)
        plt.ylim(-10, 10)
        plt.plot(x, y)
        plt.title(f"Tangens({value}x)")
    elif chosen_function == "Cotangens":
        x = np.linspace(0, 2 * np.pi, 400)
        y = 1 / np.tan(value * x)
        plt.ylim(-10, 10)  
        plt.plot(x, y)
        plt.title(f"Cotangens({value}x")
    plt.axhline(0, color="black", linewidth=2, linestyle="-", label="x-axis")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()



def button_click(value):
    e = entry.get()
    ans = ""
    if not check_expression(e, value):
         return
     
    try:
          
          if value == "C":
               entry.delete(0, "end")
               return
        
          if value == "<-":
               e = e[0:len(e) - 1] 
               entry.delete(0, "end")
               entry.insert(0, e)
               return
     
          elif value == "√":
               ans = math.sqrt(eval(e))
     
          elif value == "π":
               ans = math.pi
     
          elif value == "2π":
               ans = 2 * math.pi

          elif value == "deg":
               ans = math.degrees(eval(e))

          elif value =="cosφ":
               ans = math.cos(math.radians(eval(e)))

          elif value == "sinφ":
               ans = math.sin(math.radians(eval(e)))

          elif value ==  "tgφ":
               ans = math.tan(math.radians(eval(e)))

          elif value == "ctgφ":
               ans = 1/math.tan(math.radians(eval(e)))

          elif value == chr(8731):
               ans = eval(e) ** (1 / 3)

          elif value == "x\u02b8":
               entry.insert("end", "**")
               return
     
          elif value == "x\u00B3":
               ans = eval(e) ** 3

          elif value == "x\u00B2":
               ans = eval(e) ** 2
          
          elif value == "ln":
               ans = math.log2(eval(e))

          elif value == "log":
               ans = math.log10(eval(e))

          elif value == "rad":
               ans = math.radians(eval(e))

          elif value == "e":
               ans = math.e

          elif value == "x!":
               ans = math.factorial(eval(e))
          
          elif value == chr(247):
               ans = entry.insert("end", "/")
               return
          elif value == "=":
               ans = eval(e)
               expression = str(ans)
               
          else:
            entry.insert("end", value)
            return

          entry.delete(0, "end")
          entry.insert(0, ans)
          
    except SyntaxError:
        pass



     
button_2pi = tkinter.Button(app, width=10, height=4, bd=2, text="2π", bg="#808080", fg="white", command= lambda: button_click("2π")) 
button_2pi.grid(row=1, column=0, pady=1)
button_pi = tkinter.Button(app, width=10, height=4, bd=2, text="π", bg="#808080", fg="white", command= lambda: button_click("π")) 
button_pi.grid(row=1, column=1, pady=1)
button_e = tkinter.Button(app, width=10, height=4, bd=2, text="e", bg="#808080", fg="white", command= lambda: button_click("e")) 
button_e.grid(row=1, column=2, pady=1)
button_back = tkinter.Button(app, width=10, height=4, bd=2, text="<-", bg="#808080", fg="white", command= lambda: button_click("<-")) 
button_back.grid(row=1, column=3, pady=1)
button_C= tkinter.Button(app, width=10, height=4, bd=2, text="C", bg="#808080", fg="white", command= lambda: button_click("C")) 
button_C.grid(row=1, column=4, pady=1)
button_x2 = tkinter.Button(app, width=10, height=4, bd=2, text="x\u00B2", bg="#808080", fg="white", command= lambda: button_click("x\u00B2")) 
button_x2.grid(row=2, column=0, pady=1)
button_x3 = tkinter.Button(app, width=10, height=4, bd=2, text="x\u00B3", bg="#808080", fg="white", command= lambda: button_click("x\u00B3")) 
button_x3.grid(row=2, column=1, pady=1)
button_xy = tkinter.Button(app, width=10, height=4, bd=2, text="x\u02b8", bg="#808080", fg="white", command= lambda: button_click("x\u02b8")) 
button_xy.grid(row=2, column=2, pady=1)
button_sqrt = tkinter.Button(app, width=10, height=4, bd=2, text="√", bg="#808080", fg="white", command= lambda: button_click("√")) 
button_sqrt.grid(row=2, column=3, pady=1)
button_sqrt3 = tkinter.Button(app, width=10, height=4, bd=2, text=chr(8731), bg="#808080", fg="white", command= lambda: button_click(chr(8731))) 
button_sqrt3.grid(row=2, column=4, pady=1)
button_0 = tkinter.Button(app, width=10, height=4, bd=2, text="0", bg="#808080", fg="white", command= lambda: button_click("0")) 
button_0.grid(row=7, column=2, pady=1)
button_1 = tkinter.Button(app, width=10, height=4, bd=2, text="1", bg="#808080", fg="white", command= lambda: button_click("1")) 
button_1.grid(row=6, column=1, pady=1)
button_2 = tkinter.Button(app, width=10, height=4, bd=2, text="2", bg="#808080", fg="white", command= lambda: button_click("2")) 
button_2.grid(row=6, column=2, pady=1)
button_3 = tkinter.Button(app, width=10, height=4, bd=2, text="3", bg="#808080", fg="white", command= lambda: button_click("3")) 
button_3.grid(row=6, column=3, pady=1)
button_4 = tkinter.Button(app, width=10, height=4, bd=2, text="4", bg="#808080", fg="white", command= lambda: button_click("4")) 
button_4.grid(row=5, column=1, pady=1)
button_5 = tkinter.Button(app, width=10, height=4, bd=2, text="5", bg="#808080", fg="white", command= lambda: button_click("5")) 
button_5.grid(row=5, column=2, pady=1)
button_6 = tkinter.Button(app, width=10, height=4, bd=2, text="6", bg="#808080", fg="white", command= lambda: button_click("6")) 
button_6.grid(row=5, column=3, pady=1)
button_7 = tkinter.Button(app, width=10, height=4, bd=2, text="7", bg="#808080", fg="white", command= lambda: button_click("7")) 
button_7.grid(row=4, column=1, pady=1)
button_8 = tkinter.Button(app, width=10, height=4, bd=2, text="8", bg="#808080", fg="white", command= lambda: button_click("8")) 
button_8.grid(row=4, column=2, pady=1)
button_9 = tkinter.Button(app, width=10, height=4, bd=2, text="9", bg="#808080", fg="white", command= lambda: button_click("9")) 
button_9.grid(row=4, column=3, pady=1)
button_plus = tkinter.Button(app, width=10, height=4, bd=2, text="+", bg="#808080", fg="white", command= lambda: button_click("+")) 
button_plus.grid(row=5, column=4, pady=1)
button_minus = tkinter.Button(app, width=10, height=4, bd=2, text="-", bg="#808080", fg="white", command= lambda: button_click("-")) 
button_minus.grid(row=6, column=4, pady=1)
button_divide = tkinter.Button(app, width=10, height=4, bd=2, text=chr(247), bg="#808080", fg="white", command= lambda: button_click("/")) 
button_divide.grid(row=3, column=4, pady=1)
button_multiply = tkinter.Button(app, width=10, height=4, bd=2, text="*", bg="#808080", fg="white", command= lambda: button_click("*")) 
button_multiply.grid(row=4, column=4, pady=1)
button_equalize = tkinter.Button(app, width=10, height=4, bd=2, text="=", bg="orange", fg="white", command= lambda: button_click("=")) 
button_equalize.grid(row=7, column=4, pady=1)
button_dot = tkinter.Button(app, width=10, height=4, bd=2, text=".", bg="#808080", fg="white", command= lambda: button_click(".")) 
button_dot.grid(row=7, column=3, pady=1)
button_ln = tkinter.Button(app, width=10, height=4, bd=2, text="ln", bg="#808080", fg="white", command= lambda: button_click("ln")) 
button_ln.grid(row=3, column=0, pady=1)
button_log = tkinter.Button(app, width=10, height=4, bd=2, text="log", bg="#808080", fg="white", command= lambda: button_click("log")) 
button_log.grid(row=3, column=1, pady=1)
button_factorial = tkinter.Button(app, width=10, height=4, bd=2, text="x!", bg="#808080", fg="white", command= lambda: button_click("x!")) 
button_factorial.grid(row=3, column=2, pady=1)
button_radians = tkinter.Button(app, width=10, height=4, bd=2, text="rad", bg="#808080", fg="white", command= lambda: button_click("rad")) 
button_radians.grid(row=3, column=3, pady=1)
button_degrees = tkinter.Button(app, width=10, height=4, bd=2, text="deg", bg="#808080", fg="white", command= lambda: button_click("deg")) 
button_degrees.grid(row=7, column=1, pady=1)
button_cos = tkinter.Button(app, width=10, height=4, bd=2, text="cosφ", bg="#808080", fg="white", command= lambda: button_click("cosφ")) 
button_cos.grid(row=4, column=0, pady=1)
button_sin = tkinter.Button(app, width=10, height=4, bd=2, text="sinφ", bg="#808080", fg="white", command= lambda: button_click("sinφ")) 
button_sin.grid(row=5, column=0, pady=1)
button_tg = tkinter.Button(app, width=10, height=4, bd=2, text="tgφ", bg="#808080", fg="white", command= lambda: button_click("tgφ")) 
button_tg.grid(row=6, column=0, pady=1)
button_ctg = tkinter.Button(app, width=10, height=4, bd=2, text="ctgφ", bg="#808080", fg="white", command= lambda: button_click("ctgφ")) 
button_ctg.grid(row=7, column=0, pady=1)
plot_button = tkinter.Button(app, width=10, height=3, bd=2, text ="■", bg="#808080", fg="white", command=open_plot_window_quad)
plot_button.grid(row=8, column=1, pady=1)
plot_button = tkinter.Button(app, width=10, height=3, bd=2, text ="△", bg="#808080", fg="white", command=open_plot_window_trig)
plot_button.grid(row=8, column=3, pady=1)



app.mainloop()