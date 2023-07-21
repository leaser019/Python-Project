from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from googletrans import Translator

def clear():
    box_input.delete(1.0,END)
    box_output.delete(1.0,END)
def translate():
    box_output.delete(1.0,END)
    input = box_input.get(1.0,END)
    translator = Translator()
    result = translator.translate(input,src="vi",dest="en").text
    box_output.insert(END,result)
# Init GUI
root = Tk()
root.title("Translator")
root.geometry("900x600")
root.iconbitmap("./assets/imgs/dictionary.ico")
root.resizable(False,False)

background = Image.open("./assets/imgs/background.png")
render = ImageTk.PhotoImage(background)
img = Label(root, image=render)
img.place(x=0, y=0)

name = Label(root, text="Translator", fg="#fff", bd=0, bg="#000")

name.config(font=("ROBOTO", 30))
name.pack(pady=10) 

box_input = Text(root,width=55,height=8,font=("ROBOTO",16))
box_input.pack(pady=15)


button_frame = Frame(root).pack(side=BOTTOM)
clear_button = Button(button_frame,text="Clear Text",font=(("Arial"),10,'bold'),bg="#303030",fg="#fff",command= clear)
translate_button = Button(button_frame,text="Translate Text",font=(("Arial"),10,'bold'),bg="#303030",fg="#fff",command= translate)
clear_button.place(x=330,y=295)
translate_button.place(x=465,y=295)

box_output = Text(root, width=55,heigh=8,font=("ROBOTO",16))
box_output.pack(pady=50)



root.mainloop()
