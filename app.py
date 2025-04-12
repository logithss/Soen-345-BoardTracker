import customtkinter as ctk
from PIL import Image, ImageTk
import pywinstyles
from pynput import keyboard
from pynput.keyboard import Key, Controller
import random
from functools import partial
import subprocess
import os

global myKeyboard
myKeyboard = Controller()

global buttonY, buttonYDir, animating
buttonY = 0.1
buttonYDir = 1
animating = False

global buttons, buttonImages
buttons=[]
buttonImages = ["buttonKeyboard.png","buttonCalculator.png","buttonBrush.png","buttonEraser.png","buttonExplorer.png","buttonCancel.png"]
global buttonsPos, buttonsShown
buttonsShown = True
buttonsPos=[(0.23, 0.87), (0.35, 0.8), (0.5, 0.77), (0.65, 0.8), (0.77, 0.87), (0.5, 0.90)]

window = ctk.CTk()


window.geometry('1020x768+1920+0')
window.overrideredirect(True)
#indow.wm_attributes('-fullscreen','true')
window.wm_attributes("-topmost", True)
#window.wm_attributes("-disabled", True)
window.config(bg = '#000001')
window.wm_attributes("-transparentcolor", "#000001")

def getButtonPos(index, time):
    originPos = (0.5, 1.1)
    selectedPos = buttonsPos[index]

    return (originPos[0] + (selectedPos[0]-originPos[0]) * time, originPos[1] + (selectedPos[1]-originPos[1]) * time )

def on_press(key, injected):
    if str(key) == "'q'":
        window.destroy()
    if str(key) == "'b'":
        startAnimUp()

global buttonTime
buttonTime = 0
global buttonTimeDelta
buttonTimeDelta = 0

def startAnimUp():
    global buttonTime, buttonTimeDelta, buttonsShown
    if buttonTimeDelta == 0 and buttonsShown == False:
        buttonTime = 0
        buttonTimeDelta = 0.04
        buttonsShown = True
        animateButton()

def startAnimDown():
    global buttonTime, buttonTimeDelta, buttonsShown
    if buttonTimeDelta == 0 and buttonsShown == True:
        buttonTime = 1
        buttonTimeDelta = -0.04
        buttonsShown = False
        animateButton()

def animateButton():
    global buttonTime, buttonTimeDelta
    if(buttonTime > 1 or buttonTime < 0):
        buttonTimeDelta = 0
        return
    
    for i in range(len(buttons)):
        actualTime = buttonTime * (1 + buttonTimeDelta *i)
        if actualTime > 1:
            actualTime = 1
        if actualTime < 0:
            actualTime = 0
        pos = getButtonPos(i, actualTime)
        buttons[i].place(relx=pos[0], rely=pos[1], anchor='center')
    
    buttonTime += buttonTimeDelta
    window.after(10, animateButton)

def buttonCommand(command):
    global buttonTime, buttonTimeDelta, myKeyboard
    if(buttonTime < 0.9 and buttonTime > 0.1):
        return
    if str(command) == '0':
        freevkPath = 'C:\\Users\\Yasser\\Documents\\Soen357\\assets\\FreeVK.exe'
        print(freevkPath)
        subprocess.call([freevkPath])
    elif str(command) == '1':
        subprocess.call(['c:\windows\system32\calc.exe'])
    elif str(command) == '2':
        window.focus_set()
        myKeyboard.press('b')
        myKeyboard.release('b')
    elif str(command) == '3':
        window.focus_set()
        myKeyboard.press('e')
        myKeyboard.release('e')
    elif str(command) == '4':
        subprocess.call(['C:\windows/explorer.exe'])
    elif str(command) == '5':
        print("hide")
    else:
        return
    startAnimDown()


for i in range(6):
    buttonSize = [100, 100] if i!=5 else [80, 80]
    img = ctk.CTkImage(Image.open("assets/"+buttonImages[i]),size=buttonSize)
    action_with_arg = partial(buttonCommand, i)
    button = ctk.CTkButton(window, text="", image=img, fg_color='transparent', 
                                bg_color="#000001", width = buttonSize[0], height = buttonSize[1],
                                border_width=0, hover = None, command= action_with_arg, anchor='center')
    buttonPos = getButtonPos(i, 1)
    button.place(relx=buttonPos[0], rely=buttonPos[1], anchor='center')
    buttons.append(button)

listener = keyboard.Listener(on_press=on_press)
listener.start()

window.mainloop()