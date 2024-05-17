from PIL import Image, ImageTk
from turtle import Shape, getscreen


def resize_shape(input_path, size):
    image = Image.open(input_path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    # Returns a tkinter compatible image object, where turtle uses tkinter for its GUI
    photo_image = ImageTk.PhotoImage(image)
    return photo_image


def register_shape(photo_image: ImageTk.PhotoImage, set_name):
    shape = Shape("image", photo_image)
    getscreen()._shapes[set_name] = shape  # underpinning, not published API (so ignore warning message)
    # Taken from https://stackoverflow.com/questions/53794657/how-do-you-set-a-turtles-shape-to-a-pil-image

