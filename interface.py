import tkinter as tk
import tensorflow as tf
import numpy as np
import PIL
import cv2
import matplotlib.pyplot as plt


class Paint():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Number Predictor")
        self.root.configure(background='#566573')
        self.root.resizable(width=False, height=False)
        
        self.canvas = tk.Canvas(self.root, bg='white', width=500, height=500)
        self.canvas.grid(row=0, columnspan=3, pady=10, padx=10)

        self.predict_button = tk.Button(self.root, bg='#4CAF50', text='Predict', width=25, height=2, bd=0, command=self.predict)
        self.predict_button.grid(row=1, column=0, pady=10)

        self.clear_button = tk.Button(self.root, bg='#F44336', text='Clear', width=25, height=2, bd=0, command=self.clear)
        self.clear_button.grid(row=1, column=2, pady=10)

        self.display_label = tk.Label(self.root, bg='#566573', text='  ', font=("Helvetica", 20))
        self.display_label.grid(row=1, column=1, pady=(0, 10))

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 40
        self.color = 'black'
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.model = tf.keras.models.load_model('mnist_model')

    def paint(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill='black', capstyle='round')
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear(self):
        self.canvas.delete("all")
        self.display_label.config(text='  ')

    def predict(self):
        self.canvas.postscript(file='image.eps') 
        
        image = PIL.Image.open('image.eps') 
        image.save('image.png', 'png') 
        
        image = cv2.imread('image.png',0)
        image = cv2.bitwise_not(image)
        image = cv2.resize(image, (28, 28))
        image = image.reshape(-1, 28, 28, 1)
        image = tf.keras.utils.normalize(image)
        prediction = self.model.predict(image)
        prediction = np.argmax(prediction, axis=1)[0]
        self.display_label.config(text=str(prediction))


Paint()