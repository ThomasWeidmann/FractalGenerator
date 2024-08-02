from PIL import Image, ImageDraw
import numpy as np

def create_mandelbrot(re_min, re_max, im_min, im_max, real_width, real_height, iterations, path, colors,quality):
    width = int(real_width * np.sqrt(quality))
    height = int(real_height * np.sqrt(quality))
    
    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, width):
        for y in range(0, height):
            c = complex(re_min + (x / width) * (re_max - re_min), im_min + (y / height) * (im_max - im_min))
            m = mandelbrot(c, iterations)

            fp_entry = m / iterations * (len(colors) - 1)
       
            rounded_entry = int(fp_entry)
            weight_next_color = fp_entry - rounded_entry
            color = weight_average(colors[rounded_entry], 1-weight_next_color, colors[rounded_entry+1], weight_next_color)
            draw.point([x, y], color)
    im.resize((real_width, real_height)).save(path, 'PNG')
    
def create_juliaset(re_min, re_max, im_min, im_max, real_width, real_height, iterations, path,julia, colors, quality):
    width = int(real_width * np.sqrt(quality))
    height = int(real_height * np.sqrt(quality))

    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, width):
        for y in range(0, height):
            c = complex(re_min + (x / width) * (re_max - re_min), im_min + (y / height) * (im_max - im_min))
            m = mandelbrot(julia, iterations,c)

            fp_entry = m / iterations * (len(colors) - 1)
       
            rounded_entry = int(fp_entry)
            weight_next_color = fp_entry - rounded_entry
            color = weight_average(colors[rounded_entry], 1-weight_next_color, colors[rounded_entry+1], weight_next_color)
            draw.point([x, y], color)
    im.resize((real_width, real_height)).save(path, 'PNG')



def mandelbrot(c, max_iteration, julia=0):
    z = julia
    n = 0
    while abs(z) <= 2 and n < max_iteration-1:
        z = z*z + c
        n += 1
    return n

#list1 und list2 müssten 3 tupel sein
def weight_average(list1, weight_list1, list2, weight_list2):
    return (int(list1[0]*weight_list1 + list2[0] *weight_list2),int(list1[1]*weight_list1 + list2[1] *weight_list2),int(list1[2]*weight_list1 + list2[2] *weight_list2))
