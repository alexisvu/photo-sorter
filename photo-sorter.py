import os
import shutil
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# configure these parameters
SORT_DIRS = [ 'REJECT', 'KEEP', 'HIDE' ]
BASE_DIR = 'C:/Users/alexi/Pictures/Alexis_all_jpgs'

def main():
    images = sorted(os.listdir(BASE_DIR), key=len)

    for dir in SORT_DIRS:
        path = os.path.join(BASE_DIR, dir)
        if not os.path.isdir(path):
            os.mkdir(path)
        else:   # os.listdir includes directories in the image set, so they need to be removed.
            images.remove(dir)

    PhotoViewer(images).draw_viewer()

class PhotoViewer:
    def __init__(self, images):
        self.image_set = images
        self.index = 0  # can change this index depending on where in photo reel you want to start
        self.path = os.path.join(BASE_DIR, self.image_set[self.index])
        
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.panel = ''  

    def draw_viewer(self):
        image = self.get_label_image()
        self.panel = tk.Label(self.window, image=image)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        
        self.window.bind('<Up>', self.keep_photo)
        self.window.bind('<Down>', self.reject_photo)
        self.window.bind('<space>', self.hide_photo)
        self.window.bind('<Right>', self.next_photo)
        self.window.bind('<Left>', self.previous_photo)
        self.window.bind('<Return>', self.close_photo)
        
        self.window.mainloop()

    def update_photo(self):
        self.path = os.path.join(BASE_DIR, self.image_set[self.index])
        image = self.get_label_image()
        self.panel.configure(image=image)
        self.panel.image = image

    def keep_photo(self, event):
        shutil.move(self.path, os.path.join(BASE_DIR, SORT_DIRS[1]))    # 1 --> true --> keep
        self.image_set.remove(self.image_set[self.index])
        self.update_photo()

    def reject_photo(self, event):
        shutil.move(self.path, os.path.join(BASE_DIR, SORT_DIRS[0]))    # 0 --> false --> reject
        self.image_set.remove(self.image_set[self.index])
        self.update_photo()

    def next_photo(self, event):
        self.index += 1
        # If at right boundary of photo real, loop back to the beginning.
        if self.index >= len(self.image_set):
            self.index = 0

        self.update_photo()

    def previous_photo(self, event):
        self.index -= 1
        # If at left boundary of photo real, loop back to last photo.
        if self.index < 0:
            self.index = len(self.image_set) - 1

        self.update_photo()

    def hide_photo(self, event):
        shutil.move(self.path, os.path.join(BASE_DIR, SORT_DIRS[2]))    # 2 --> file descriptor for std err --> hide
        self.image_set.remove(self.image_set[self.index])
        self.update_photo()

    def close_photo(self, event):
        self.window.destroy()

    def get_label_image(self):
        image = Image.open(self.path)
        factor = 5
        resized_image = image.resize((image.width // factor, image.height // factor), Image.ANTIALIAS)

        return ImageTk.PhotoImage(resized_image)


if __name__ == "__main__":
    main()
