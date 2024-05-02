import tkinter as tk
import pyautogui
import time
import pyperclip
import pytesseract
from tkinter import messagebox

class ScreenShotter:
    def __init__(self):
        self.master = tk.Tk()
        self.master.overrideredirect(True)
        self.master.attributes("-alpha", 0.5)
        self.master.attributes("-topmost", True)
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.canvas = tk.Canvas(self.master, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.master.bind("<Button-1>", self.record_click)
        self.click_count = 0

        self.master.mainloop()

    def record_click(self, event):
        if self.click_count == 0:
            self.click_count += 1
            self.first_click = event.x_root, event.y_root
            self.draw_circle(event.x, event.y)
        elif self.click_count == 1:
            self.click_count += 1
            self.second_click = event.x_root, event.y_root
            self.draw_circle(event.x, event.y)
            self.draw_rectangle_animation(self.first_click, self.second_click)
            self.click_count = 0
        else:
            pass

    def draw_circle(self, x, y):
        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline="red", width=2)

    def draw_rectangle_animation(self, start, end):
        x1, y1 = start
        x2, y2 = end
        steps = 50 if ((x2-x1)* (y2-y1) ) >= 600000 else 100
        for i in range(steps+1):
            time.sleep(0.005)
            ratio = i / steps
            x = x1 + (x2 - x1) * ratio
            y = y1 + (y2 - y1) * ratio
            self.canvas.delete("line1")
            self.canvas.create_line(x1, y1, x, y1, fill="blue", width=2, tags="line1")
            self.canvas.create_line(x1, y1, x1, y, fill="blue", width=2, tags="line1")
            self.master.update()
        time.sleep(0.4)
        self.canvas.create_rectangle(x1, y1, x, y, outline="blue", width=2, tags="rect")
        self.master.update()
        self.canvas.create_rectangle(x1, y1, x, y, fill="white", width=2, tags="flash")
        self.master.update()
        time.sleep(0.1)
        self.canvas.delete("flash")
        self.master.update()
        self.master.after(500, self.close_app) 

        self.screenshot(start, end)
        

    def screenshot(self,start, end):
        x1, y1 = start
        x2, y2 = end
        self.ss = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        self.ss.save("screenshot.png")
        self.OCR()


    def OCR(self):
        self.text = pytesseract.image_to_string(self.ss)
        pyperclip.copy(self.text)
        print(self.text)
        
    def close_app(self):
        self.master.destroy()

if __name__ == "__main__":
    new = ScreenShotter(True)



