import tensorflow_hub as hub
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2


def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img
    
model = hub.load('../ressources/magenta_arbitrary-image-stylization-v1-256_2')    

def style_image(path_content_image, path_style_image, path_stylized_image):

    

    content_image = load_image(path_content_image)
    style_image = load_image(path_style_image)

    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]




    cv2.imwrite(path_stylized_image, cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB))
