import customtkinter as ctk
from PIL import Image, ImageTk
import pywinstyles

window = ctk.CTk()
window.geometry('600x400')
window.wm_attributes("-topmost", True)
#window.wm_attributes("-disabled", True)
window.config(bg = '#000001')
window.wm_attributes("-transparentcolor", "#000001")

global buttonY, buttonYDir, animating
buttonY = 0.1
buttonYDir = 1
animating = False
def animateUp():
    global buttonY
    
    print(buttonY)
    if (buttonY-100) <= 0.0001:
        buttonY = 1
        print("here: " + str(buttonY))
        roundedbutton.place(relx=0.5, y=buttonY, anchor='s')
        return

    buttonY -= 5
    roundedbutton.place(relx=0.5, y=buttonY, anchor='s')
    window.after(200, animateUp)

def click():
    animateUp()

img = ctk.CTkImage(Image.open("button.png"),size=[200, 200])
roundedbutton = ctk.CTkButton(window, text="", image=img, fg_color='transparent', 
                              bg_color="#000001", width = 200, height = 200, 
                              border_width=0, hover = None, command=click, anchor='sw')
roundedbutton.place(relx=0.5, y=200, anchor='s')
pywinstyles.set_opacity(roundedbutton, color="#000001")

window.mainloop()