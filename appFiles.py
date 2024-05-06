import os
import tkinter as tk
import prayer
import SS
import pyperclip



class SquareGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.current_directory = os.getcwd()
        logo = "logo.png"
        file_path = os.path.join(self.current_directory, logo)
        self.leftpos = "+{}+{}".format(
            0, 
            self.winfo_screenheight()//2 - 25 
            )
        
        self.rightpos = "+{}+{}".format(
            self.winfo_screenwidth() - 50, 
            self.winfo_screenheight()//2 - 25 
            )
        
        self.geometry(self.rightpos)
        self.right = True
        
        self.image = tk.PhotoImage(file=file_path)
        self.image = self.image.subsample(10, 10) 
        self.square = tk.Label(self, width=50, height=50,bg="black",image=self.image)
        self.square.pack()



        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Option 1", command=self.option1)
        self.menu.add_command(label="Option 2", command=self.option2)
        self.menu.add_command(label="Prayers", command=self.prayers)
        self.menu.add_command(label="Ocr", command=self.ocr)
        self.menu.add_command(label="Switch Sides", command=self.switchside)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=exit)

        self.bind("<Button-1>", self.show_menu)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def option1(self):
         print("Option 1 selected")

    def option2(self):
        print("Option 2 selected")

    def prayers(self):
        pra = prayer.Prayers(self.geometry().split('+')[1:] , self.right)
        pra.main()

    def ocr(self):
        ss = SS.ScreenShotter()


    
    def switchside(self):
        if self.right : self.geometry(self.leftpos) 
        else : self.geometry(self.rightpos) 
        self.right = False if self.right == True else True