from tkinter import *
from tkinter.colorchooser import askcolor

class Paint(object):
    DEFAULT_PEN_SIZE = 4.0
    DEFAULT_COLOR = 'black'

    def buttons(self):
        self.app = Tk()
        pen_image = PhotoImage(file = "pen.png")
        eraser_image = PhotoImage(file = "eraser.png")
        color_image = PhotoImage(file = "color.png")
        clear_image = PhotoImage(file = "clear.png")

        self.pen_button = Button(self.app, image = pen_image, command=self.use_pen)
        self.pen_button.grid(row = 0, column = 0)

        self.eraser_button = Button(self.app, image = eraser_image, command=self.use_eraser)
        self.eraser_button.grid(row = 0, column = 1)

        self.color_button = Button(self.app, image = color_image, command=self.use_color)
        self.color_button.grid(row = 0, column = 2)
        
        self.clear_button = Button(self.app, image = clear_image, command=self.clear_canvas)
        self.clear_button.grid(row = 0, column = 3)

        self.choose_size_button = Scale(self.app, from_ = 1, to = 10, orient=HORIZONTAL)
        self.choose_size_button.grid(row = 0, column =4 )
        
        self.canvas = Canvas(self.app, bg = "white", width = 800, height = 800)
        self.canvas.grid(row = 1, columnspan = 5)
        

        self.setup()
        self.app.mainloop()

    def setup(self):
        self.pre_y = None
        self.pre_x = None
        self.line_width = self.choose_size_button.get()
        self.line_width = self.DEFAULT_PEN_SIZE
        self.color = self.DEFAULT_COLOR
        self.eraser_state = False
        self.active_button = self.pen_button

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.active_button = self.pen_button
        self.eraser_state = False
        self.update_button_state()

    def use_color(self):
        self.eraser_state = False
        color = askcolor(color = self.color)[1]
        if color:
            self.color = color
            self.update_button_state()

    def use_eraser(self):
        self.active_button = self.eraser_button
        self.eraser_state = True
        self.update_button_state()
        
    def clear_canvas(self):
        self.canvas.delete("all")

    def update_button_state(self):
        for button in [self.pen_button, self.eraser_button]:
            button.config(relief=RAISED)
        self.active_button.config(relief=SUNKEN)
    
    def paint(self, state):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_state else self.color
        if self.pre_x and self.pre_y:
            self.canvas.create_line(
                self.pre_x, self.pre_y, state.x, state.y,
                width=self.line_width, fill=paint_color, capstyle=ROUND, splinesteps=20
            )

    
        self.pre_x = state.x
        self.pre_y = state.y

    def reset(self, state):
        self.pre_x, self.pre_y = None, None

    

paint_app = Paint()
paint_app.buttons()