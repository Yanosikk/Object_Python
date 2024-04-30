from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import simpledialog
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

class Paint(object):
    DEFAULT_PEN_SIZE = 4.0
    DEFAULT_COLOR = 'black'
    
    
    
    def save(self):
     file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
     if file_path:
        image = Image.new("RGB", (self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 0, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()], fill="white")

        items = self.canvas.find_all()
        for item in items:
            coords = self.canvas.coords(item)
            if self.canvas.type(item) == "line":
                draw.line(coords, fill=self.color, width=self.line_width)
            elif self.canvas.type(item) == "rectangle":
                draw.rectangle(coords, outline=self.color, width=self.line_width)
            elif self.canvas.type(item) == "oval":
                draw.ellipse(coords, outline=self.color, width=self.line_width)
            elif self.canvas.type(item) == "polygon":
                draw.polygon(coords, outline=self.color, fill="white", width=self.line_width)
            elif self.canvas.type(item) == "text":
                text = self.canvas.itemcget(item, "text")
                font = self.canvas.itemcget(item, "font")
                fill = self.canvas.itemcget(item, "fill")
                draw.text(coords[:2], text, font=font, fill=fill)

        image.save(file_path)

    def open(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            image = Image.open(file_path)
            self.canvas.delete("all")
            self.canvas.config(width=image.width, height=image.height)
            image_tk = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=NW, image = image_tk)
            self.canvas.image = image_tk
            
    

    def buttons(self):
        self.app = Tk()
        pen_image = PhotoImage(file="pen.png")
        eraser_image = PhotoImage(file="eraser.png")
        color_image = PhotoImage(file="color.png")
        clear_image = PhotoImage(file="clear.png")
        circle_image = PhotoImage(file="circle.png")
        square_image = PhotoImage(file="square.png")
        triangle_image = PhotoImage(file="triangle.png")
        text_image = PhotoImage(file="text.png")

        self.circle_button = Button(self.app, image=circle_image, command=self.start_circle_drawing)
        self.circle_button.grid(row=0, column=5)
        self.square_button = Button(self.app, image=square_image, command=self.start_square_drawing)
        self.square_button.grid(row=0, column=6)
        self.triangle_button = Button(self.app, image=triangle_image, command=self.start_triangle_drawing)
        self.triangle_button.grid(row=0, column=7)
        self.text_button = Button(self.app, image=text_image, command=self.start_text)
        self.text_button.grid(row=0, column=8)
        self.pen_button = Button(self.app, image=pen_image, command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.eraser_button = Button(self.app, image=eraser_image, command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1)

        self.color_button = Button(self.app, image=color_image, command=self.use_color)
        self.color_button.grid(row=0, column=2)

        self.clear_button = Button(self.app, image=clear_image, command=self.clear_canvas)
        self.clear_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.app, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.canvas = Canvas(self.app, bg="white", width=800, height=800)
        self.canvas.grid(row=1, columnspan=11)
        
        self.save_button = Button(self.app, text="Save", command=self.save)
        self.save_button.grid(row=0, column=9)

        self.open_button = Button(self.app, text="Open", command=self.open)
        self.open_button.grid(row=0, column=10)

        self.setup()
        self.app.mainloop()

    def setup(self):
        self.pre_y = None
        self.pre_x = None
        self.line_width = self.choose_size_button.get()
        self.line_width = self.DEFAULT_PEN_SIZE
        self.color = self.DEFAULT_COLOR
        self.eraser_state = False
        self.active_button = None
        self.point1 = None
        self.point2 = None
        self.point3 = None
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_text = False

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.active_button = self.pen_button
        self.eraser_state = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_text = False
        self.update_button_state()

    def use_color(self):
        self.eraser_state = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_text = False
        color = askcolor(color=self.color)[1]
        if color:
            self.color = color
            self.update_button_state()

    def use_eraser(self):
        self.active_button = self.eraser_button
        self.eraser_state = True
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_text = False
        self.update_button_state()

    def clear_canvas(self):
        self.canvas.delete("all")

    def update_button_state(self):
        for button in [self.pen_button, self.eraser_button, self.circle_button, self.square_button, self.triangle_button, self.text_button]:
            if button == self.active_button:
                button.config(relief=SUNKEN)
            else:
                button.config(relief=RAISED)

    def active_click(self, event):
        if self.drawing_circle:
            if self.point1 is None:
                self.point1 = (event.x, event.y)
            elif self.point2 is None:
                self.point2 = (event.x, event.y)
                self.draw_circle_between_points()
                self.point1 = None
                self.point2 = None
        elif self.drawing_square:
            if self.point1 is None:
                self.point1 = (event.x, event.y)
            elif self.point2 is None:
                self.point2 = (event.x, event.y)
                self.draw_square_between_points()
                self.point1 = None
                self.point2 = None
        elif self.drawing_triangle:
            if self.point1 is None:
                self.point1 = (event.x, event.y)
            elif self.point2 is None:
                self.point2 = (event.x, event.y)
            elif self.point3 is None:
                self.point3 = (event.x, event.y)
                self.draw_triangle_between_points()
                self.point1 = None
                self.point2 = None
                self.point3 = None
                
        elif self.drawing_text:
            self.create_text_at_point(event.x, event.y)

    def draw_circle_between_points(self):
        if self.point1 and self.point2:
            x1, y1 = self.point1
            x2, y2 = self.point2
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = ((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2
            outline_width = self.choose_size_button.get()
            self.canvas.create_oval(center_x - radius - outline_width, center_y - radius - outline_width,
                                    center_x + radius + outline_width, center_y + radius + outline_width,
                                    outline="black", width=outline_width)
            self.canvas.create_oval(center_x - radius, center_y - radius,
                                    center_x + radius, center_y + radius,
                                    outline=self.color, fill="white", width=2)

    def start_circle_drawing(self):
        self.active_button = self.circle_button
        self.drawing_circle = True
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_text = False
        self.canvas.bind("<Button-1>", self.active_click)
        self.update_button_state()

    def draw_square_between_points(self):
        if self.point1 and self.point2:
            x1, y1 = self.point1
            x2, y2 = self.point2
            outline_width = self.choose_size_button.get()
            self.canvas.create_rectangle(x1 - outline_width, y1 - outline_width,
                                         x2 + outline_width, y2 + outline_width,
                                         outline="black", width=outline_width)
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.color, fill="white", width=2)

    def start_square_drawing(self):
        self.active_button = self.square_button
        self.drawing_square = True
        self.drawing_circle = False
        self.drawing_triangle = False
        self.drawing_text = False
        self.canvas.bind("<Button-1>", self.active_click)
        self.update_button_state()

    def draw_triangle_between_points(self):
        if self.point1 and self.point2 and self.point3:
            outline_width = self.choose_size_button.get()
            self.canvas.create_polygon(self.point1[0], self.point1[1],
                                       self.point2[0], self.point2[1],
                                       self.point3[0], self.point3[1],
                                       outline="black", width=outline_width)
            self.canvas.create_polygon(self.point1[0], self.point1[1],
                                       self.point2[0], self.point2[1],
                                       self.point3[0], self.point3[1],
                                       outline=self.color, fill="white", width=2)

    def start_triangle_drawing(self):
        self.active_button = self.triangle_button
        self.drawing_triangle = True
        self.drawing_square = False
        self.drawing_circle = False
        self.drawing_text = False
        self.canvas.bind("<Button-1>", self.active_click)
        self.update_button_state()

    def start_text(self):
        self.active_button = self.text_button
        self.drawing_text = True
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.canvas.bind("<Button-1>", self.active_click)
        self.update_button_state()

    def create_text_at_point(self, x, y):
        text = simpledialog.askstring("Input", "Enter text:")
        if text:
            self.canvas.create_text(x, y, text=text, font=("Arial", 12), fill=self.color)

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
