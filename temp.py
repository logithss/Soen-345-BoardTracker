from tkinter import *
root = Tk()

def next_image(event=None):
    canvas1.move(item, 10, 0)
    canvas1.after(100, next_image) # Call this function after 100 ms.

image1 = "startup.gif"
photo1 = PhotoImage(file=image1)
width1 = photo1.width()
height1 = photo1.height()
canvas1 = Canvas(width=1920, height=1080)
canvas1.pack(expand=1, fill=BOTH) # <--- Make your canvas expandable.
x = (width1)/2.0
y = (height1)/2.0
item = canvas1.create_image(x, y, image=photo1) # <--- Save the return value of the create_* method.
canvas1.bind('<Button-1>', next_image)
root.mainloop() 


root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
root.wm_attributes('-toolwindow', True)