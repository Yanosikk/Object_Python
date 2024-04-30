import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
import tkinter
from tkinter import filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


app = tkinter.Tk()
app.geometry("800x600")
app.title("Graph")
app.resizable(0, 0)
app.config(bg = "white")
x = None
y = None

main_frame = tkinter.Frame(app, bg = "white")
main_frame.pack(fill=tkinter.BOTH, expand = True)

plot_frame = tkinter.Frame(main_frame, bg="white")
plot_frame.pack(fill=tkinter.BOTH, expand = True)

def fwhm_calculation(x, y):
    max_value_index = np.argmax(y)
    max_x = x[max_value_index]
    max_y = y[max_value_index]
    half_max_value = max_y/2
    indices_above_half_max = np.where(y > half_max_value)[0]
    fwhm = np.abs(x[indices_above_half_max[0]] - x[indices_above_half_max[-1]])
    return fwhm

def choose_file():
    global x, y
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            df = pd.read_csv(file_path, header = None, names = ["x", "y"], delim_whitespace = True)
            print(f"File opened successfully: {file_path}")

            x = df["x"]
            y = df["y"]
            
        except Exception as exc:
            print(f"Issue with file opening: {exc}")
    else:
        print("No file chosen")

def generate_graph():
    global x, y
    if x is not None and y is not None:
       
        plt.figure()
        plt.plot(x, y)
        plt.xlabel("X AXIS")
        plt.ylabel("Y AXIS")
        plt.title("Graph")

        
        max_value_index = y.idxmax()
        max_x = x[max_value_index]
        max_y = y[max_value_index]
        plt.axhline(max_y, color='red', linestyle='-', label=f'Max Value ({max_x}, {max_y})')
        plt.text(max_x, max_y, f'Max Value  ({max_y})', color='red', verticalalignment='bottom')
        min_value_index = y.idxmin()
        min_x = x[min_value_index]
        min_y = y[min_value_index]
        plt.axhline(min_y, color='blue', linestyle='-', label=f'Min Value ({min_x}, {min_y})')
        plt.text(min_x, min_y, f'Min Value  ({min_y})', color='blue', verticalalignment='bottom')
        
        fwhm = fwhm_calculation(x, y)
        plt.axvline(x=max_x - fwhm/2, color='green', linestyle='--')
        plt.axvline(x=max_x + fwhm/2, color='green', linestyle='--')
        plt.text(max_x - fwhm/2, max_y, f'x1 ({max_x - fwhm/2:.2f})', color='green', verticalalignment='top', horizontalalignment = 'right')
        plt.text(max_x + fwhm/2, max_y, f'x2 ({max_x + fwhm/2:.2f})', color='green', verticalalignment='top', horizontalalignment = 'left')


        canvas = FigureCanvasTkAgg(plt.gcf(), master = plot_frame)
        canvas.get_tk_widget().pack(fill = tkinter.BOTH, expand = True)
        canvas.draw()
    else:
        print("There is no data available")

button_open = tkinter.Button(app, width = 10, height = 5, bd = 1, text= "open", bg = "green", command = choose_file)
button_open.pack(side = tkinter.LEFT)
button_generate = tkinter.Button(app, width = 10, height = 5, bd = 1, text= "generate", bg = "red", command = generate_graph)
button_generate.pack(side = tkinter.RIGHT)

app.mainloop()
