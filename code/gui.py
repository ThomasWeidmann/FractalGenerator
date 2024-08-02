from tkinter import *
import fractal_generator as fractal
import numpy as np
from datetime import datetime
import style_transfer
from os import listdir, mkdir
from os.path import isfile, join, isdir
from PIL import ImageTk, Image


def get_date_as_filename():
  filename = ""
  for c in ["-" if c == ":" else c for c in str(datetime.now())]:
    filename += c
  return "generated/" + filename + ".png"

def get_random_colors(n):
  return np.random.randint(255, size=(n,3))


class App:
  def update_mandelbrot(self):
    fractal.create_mandelbrot(self.mandelbrot_re_min, self.mandelbrot_re_max, self.mandelbrot_im_min, self.mandelbrot_im_max, self.WIDTH, self.HEIGHT, int(self.iteration_var.get()), self.mandelbrot_path, self.colors, float(self.quality_var.get()))
    self.m = PhotoImage(file = self.mandelbrot_path)
    
    self.mandelbrot_canvas.create_image(0,0, anchor=NW, image=self.m)

  def update_juliaset(self):
    fractal.create_juliaset(self.juliaset_re_min, self.juliaset_re_max, self.juliaset_im_min, self.juliaset_im_max, self.WIDTH, self.HEIGHT, int(self.iteration_var.get()), self.juliaset_path, self.julia, self.colors, float(self.quality_var.get()))
  
    self.j = PhotoImage(file = self.juliaset_path)
    self.juliaset_canvas.create_image(0,0, anchor=NW, image=self.j)
    
  def update_fractals(self):
    self.colors = get_random_colors(int(self.color_var.get()))
    
    self.update_mandelbrot()
    self.update_juliaset()
  
  def apply_styles(self, style_img_path):
    self.style = style_img_path
  
    style_transfer.style_image(self.mandelbrot_path, style_img_path, self.mandelbrot_stylized_path)
    style_transfer.style_image(self.juliaset_path, style_img_path, self.juliaset_stylized_path)
      
    self.sm = PhotoImage(file = self.mandelbrot_stylized_path)
    self.stylized_mandelbrot_canvas.create_image(0,0, anchor=NW, image=self.sm)
    
    self.sj = PhotoImage(file = self.juliaset_stylized_path)
    self.stylized_juliaset_canvas.create_image(0,0, anchor=NW, image=self.sj)

  def __init__(self, master):
    master.title("FractalGenerator")
  
    self.WIDTH = 500
    self.HEIGHT = 300
    
    self.mandelbrot_re_min = -2
    self.mandelbrot_re_max = 1
    self.mandelbrot_im_min = -1
    self.mandelbrot_im_max = 1
    
    self.juliaset_re_min = -2
    self.juliaset_re_max = 1
    self.juliaset_im_min = -1
    self.juliaset_im_max = 1
    
    self.julia = complex(0,0)

    self.ZOOM = 10

    self.mandelbrot_path = "__mycache__/mandelbrot.png"
    self.juliaset_path = "__mycache__/juliaset.png"
    self.mandelbrot_stylized_path = "__mycache__/stylized_mandelbrot.png"
    self.juliaset_stylized_path = "__mycache__/stylized_juliaset.png"
 
    canvas_frame = Frame(master)
    canvas_frame.pack(side='top')

    self.mandelbrot_canvas = Canvas(canvas_frame, width=self.WIDTH,  height=self.HEIGHT)
    self.mandelbrot_canvas.pack(side='left')
    self.mandelbrot_canvas.bind("<ButtonPress-1>",lambda event: self.click_mandelbrot(self.mandelbrot_canvas.canvasx(event.x), self.mandelbrot_canvas.canvasy(event.y)))
  
    self.juliaset_canvas = Canvas(canvas_frame, width=self.WIDTH, height=self.HEIGHT)
    self.juliaset_canvas.pack(side='left')
    self.juliaset_canvas.bind("<ButtonPress-1>",lambda event: self.click_juliaset(self.juliaset_canvas.canvasx(event.x), self.juliaset_canvas.canvasy(event.y)))
    
    self.settings_frame = Frame(master)
    self.settings_frame.pack(side='top')
    
    self.iteration_label = Label(self.settings_frame, text="Iteration: ").pack(side='left')
    self.iteration_var = StringVar()
    self.iteration_var.set("100")
    self.iteration_entry = Entry(self.settings_frame, width=5,textvariable = self.iteration_var).pack(side='left')
    
    self.color_label = Label(self.settings_frame, text="Colors: ").pack(side='left')
    self.color_var = StringVar()
    self.color_var.set("5")
    self.color_entry = Entry(self.settings_frame, width=5, textvariable=self.color_var).pack(side='left')
    
 
    self.quality_label = Label(self.settings_frame, text="Quality: ").pack(side='left')
    self.quality_var = StringVar()
    self.quality_var.set("1.0")
    self.quality_entry = Entry(self.settings_frame, width=5, textvariable=self.quality_var).pack(side='left')
    
    self.zoom_label = Label(self.settings_frame, text="Zoom: ").pack(side='left')
    self.zoom_var = StringVar()
    self.zoom_var.set("10")
    self.zoom_entry = Entry(self.settings_frame, width=5, textvariable=self.zoom_var).pack(side='left')
    
    self.zoom_mandelbrot_var = IntVar()
    self.zoom_mandelbrot_checkbutton = Checkbutton(self.settings_frame, text="Zoom mandelbrot", variable=self.zoom_mandelbrot_var).pack(side='left')
    
    self.create_juliaset_var = IntVar()
    self.create_juliaset_checkbutton = Checkbutton(self.settings_frame, text="Create juliaset", variable=self.create_juliaset_var).pack(side='left')
    
    
    
    create_fractal_button = Button(self.settings_frame, text="Create fractals", command = self.update_fractals, padx=10).pack(side='left')
    
    self.width_label = Label(self.settings_frame, text="Width: ").pack(side='left')
    self.width_var = StringVar()
    self.width_var.set("2000")
    self.width_entry = Entry(self.settings_frame, width=5, textvariable=self.width_var).pack(side='left')
    
    self.height_label = Label(self.settings_frame, text="Height: ").pack(side='left')
    self.height_var = StringVar()
    self.height_var.set("1500")
    self.height_entry = Entry(self.settings_frame, width=5, textvariable=self.height_var).pack(side='left')
    
    save_mandelbrot_button = Button(self.settings_frame, text="Save mandelbrot!",padx=10, command= lambda:fractal.create_mandelbrot(self.mandelbrot_re_min, self.mandelbrot_re_max, self.mandelbrot_im_min, self.mandelbrot_im_max, int(self.width_var.get()), int(self.height_var.get()), int(self.iteration_var.get()), get_date_as_filename(), self.colors, 1)).pack(side='left')
    save_juliaset_button = Button(self.settings_frame, text="Save juliaset!",padx=10, command= lambda:fractal.create_juliaset(self.juliaset_re_min, self.juliaset_re_max, self.juliaset_im_min, self.juliaset_im_max, int(self.width_var.get()), int(self.height_var.get()), int(self.iteration_var.get()), get_date_as_filename(), self.julia, self.colors, 1)).pack(side='left')
  
    self.update_fractals()
    
    styles_frame = Frame(master)
    styles_frame.pack(side='top')
    
    style_width = 100
    style_height = 100
    
    canvas1 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas1.pack(side='left')
    self.canvas1_img = ImageTk.PhotoImage(Image.open("../ressources/styles/monet.jpeg").resize((style_width,style_height)))
    canvas1.create_image(0,0, anchor=NW, image=self.canvas1_img)
    canvas1.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/monet.jpeg"))
    
    canvas2 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas2.pack(side='left')
    self.canvas2_img = ImageTk.PhotoImage(Image.open("../ressources/styles/starrynight.jfif").resize((style_width,style_height)))
    canvas2.create_image(0,0, anchor=NW, image=self.canvas2_img)
    canvas2.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/starrynight.jfif"))
    
    canvas3 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas3.pack(side='left')
    self.canvas3_img = ImageTk.PhotoImage(Image.open("../ressources/styles/andy.png").resize((style_width,style_height)))
    canvas3.create_image(0,0, anchor=NW, image=self.canvas3_img)
    canvas3.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/andy.png"))
    
    canvas4 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas4.pack(side='left')
    self.canvas4_img = ImageTk.PhotoImage(Image.open("../ressources/styles/dali.jpeg").resize((style_width,style_height)))
    canvas4.create_image(0,0, anchor=NW, image=self.canvas4_img)
    canvas4.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/dali.jpeg"))
    
    canvas5 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas5.pack(side='left')
    self.canvas5_img = ImageTk.PhotoImage(Image.open("../ressources/styles/frida.jpg").resize((style_width,style_height)))
    canvas5.create_image(0,0, anchor=NW, image=self.canvas5_img)
    canvas5.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/frida.jpg"))
    
    canvas6 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas6.pack(side='left')
    self.canvas6_img = ImageTk.PhotoImage(Image.open("../ressources/styles/vangogh.jpeg").resize((style_width,style_height)))
    canvas6.create_image(0,0, anchor=NW, image=self.canvas6_img)
    canvas6.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/vangogh.jpeg"))
    
    canvas7 = Canvas(styles_frame, width=style_width,  height=style_height)
    canvas7.pack(side='left')
    self.canvas7_img = ImageTk.PhotoImage(Image.open("../ressources/styles/klimt.jpg").resize((style_width,style_height)))
    canvas7.create_image(0,0, anchor=NW, image=self.canvas7_img)
    canvas7.bind("<ButtonPress-1>",lambda event: self.apply_styles("../ressources/styles/klimt.jpg"))
    
    stylized_frame = Frame(master)
    stylized_frame.pack(side='top')
    
    
    self.stylized_mandelbrot_canvas = Canvas(stylized_frame, width=self.WIDTH,  height=self.HEIGHT)
    self.stylized_mandelbrot_canvas.pack(side='left')
    
    self.stylized_juliaset_canvas = Canvas(stylized_frame, width=self.WIDTH,  height=self.HEIGHT)
    self.stylized_juliaset_canvas.pack(side='left')
    
    self.apply_styles("../ressources/styles/vangogh.jpeg")
    
    self.settings_frame2 = Frame(master)
    self.settings_frame2.pack(side='top')
    
    self.width_label2 = Label(self.settings_frame2, text="Width: ").pack(side='left')
    self.width_var2 = StringVar()
    self.width_var2.set("2000")
    self.width_entry2 = Entry(self.settings_frame2, width=5, textvariable=self.width_var2).pack(side='left')
    
    self.height_label2 = Label(self.settings_frame2, text="Height: ").pack(side='left')
    self.height_var2 = StringVar()
    self.height_var2.set("1500")
    self.height_entry2 = Entry(self.settings_frame2, width=5, textvariable=self.height_var2).pack(side='left')
    
    save_mandelbrot_button2 = Button(self.settings_frame2, text="Save stylized mandelbrot!",padx=10, command = self.click_save_stylized_mandelbrot ).pack(side='left')
    save_juliaset_button2 = Button(self.settings_frame2, text="Save stylized juliaset!",padx=10, command= self.click_save_stylized_juliaset ).pack(side='left')
  
  def click_save_stylized_mandelbrot(self):
    fractal.create_mandelbrot(self.mandelbrot_re_min, self.mandelbrot_re_max, self.mandelbrot_im_min, self.mandelbrot_im_max, int(self.width_var2.get()), int(self.height_var2.get()), int(self.iteration_var.get()), self.mandelbrot_path, self.colors, 1)
    style_transfer.style_image(self.mandelbrot_path, self.style, get_date_as_filename())
    
  def click_save_stylized_juliaset(self):
    fractal.create_juliaset(self.juliaset_re_min, self.juliaset_re_max, self.juliaset_im_min, self.juliaset_im_max, int(self.width_var2.get()), int(self.height_var2.get()), int(self.iteration_var.get()), self.juliaset_path,self.julia, self.colors, 1)
    style_transfer.style_image(self.juliaset_path, self.style, get_date_as_filename())
  
  def click_juliaset(self,x,y):
    re = self.juliaset_re_min + (x / self.WIDTH) * (self.juliaset_re_max - self.juliaset_re_min)
    im = self.juliaset_im_min + (y / self.HEIGHT) * (self.juliaset_im_max - self.juliaset_im_min)
    
    re_diff = (self.juliaset_re_max - self.juliaset_re_min) * 1 / np.sqrt(float(self.zoom_var.get()))
    im_diff = (self.juliaset_im_max - self.juliaset_im_min) * 1 / np.sqrt(float(self.zoom_var.get()))

    self.juliaset_re_min = re - re_diff/2
    self.juliaset_re_max = re + re_diff/2
    self.juliaset_im_min = im - im_diff/2
    self.juliaset_im_max = im + im_diff/2
    
    self.update_juliaset()
   
  def click_mandelbrot(self,x,y):
    re = self.mandelbrot_re_min + (x / self.WIDTH) * (self.mandelbrot_re_max - self.mandelbrot_re_min)
    im = self.mandelbrot_im_min + (y / self.HEIGHT) * (self.mandelbrot_im_max - self.mandelbrot_im_min)
    
    if self.zoom_mandelbrot_var.get() == 1:  
        re_diff = (self.mandelbrot_re_max - self.mandelbrot_re_min) * 1 / np.sqrt(float(self.zoom_var.get()))
        im_diff = (self.mandelbrot_im_max - self.mandelbrot_im_min) * 1 / np.sqrt(float(self.zoom_var.get()))

        self.mandelbrot_re_min = re - re_diff/2
        self.mandelbrot_re_max = re + re_diff/2
        self.mandelbrot_im_min = im - im_diff/2
        self.mandelbrot_im_max = im + im_diff/2

        self.update_mandelbrot()
        
    if self.create_juliaset_var.get() == 1:
        self.julia=complex(re,im)
        self.update_juliaset()
        
if not isdir("__mycache__"):
    mkdir("__mycache__")
root = Tk()
app = App(root)
root.mainloop()