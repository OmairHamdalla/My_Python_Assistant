import os
import requests 
import bs4 
from datetime import date
from customtkinter import *

class Prayers(CTk):
    def __init__(self,pos,right):
        super().__init__()
        self.addressCheck()
        self.pos = pos
        self.right = right
    
    def addressCheck(self):
        today = date.today().strftime("%d,%m,%Y")
        directory = os.path.dirname(__file__)
        folder = "Prayer_Logs"
        fileName = f"prayersTable_{today}.txt"
        address = os.path.join(directory, folder)
        self.filePath = os.path.join(address, fileName)

        if not os.path.exists(address):
            os.makedirs(address)

        if os.path.exists(self.filePath):
            print("found")
            with open(self.filePath, 'r', encoding='utf-8') as file:
                self.Text = file.read()
        else:
            self.scrape()

    def scrape(self):
            print("scraped")
            query = "Prayer Times Istanbul"
            url = "https://google.com/search?q=" + query 

            request_result = requests.get(url) 
            soup = bs4.BeautifulSoup(request_result.text, "html.parser") 

            times = soup.findAll("span", class_='r0bn4c rQMQod')

            fajr = times[0].text
            duhur = times[2].text
            asr = times[3].text
            maghrib = times[4].text
            ishaa = times[5].text
            
            self.Text = f'Fajr: {fajr}\nDuhur: {duhur}\nAsr: {asr}\nMaghrib: {maghrib}\nIshaa: {ishaa}'

            with open(self.filePath, 'w', encoding='utf-8') as file:
                file.write(self.Text)

    def ui(self):
        self.root = CTk()
        self.root.resizable(False, False)
        self.root.title("Prayer Times")
        self.root.attributes('-alpha', 1)

        x, y = self.root.winfo_pointerxy()

        print(self.pos)

        offset = -150  if self.right else -20
        
        posS = str(int(self.pos[0]) + offset) + "+" + str(int(self.pos[1]) + 40)
        
        print(posS)

        self.root.geometry(f"200x200+{posS}")
        
        self.root.columnconfigure((1,2,4,5), weight=1)
        self.root.columnconfigure(3, weight=2)
        self.root.rowconfigure((1,2,4,7,8) ,weight=2)
        self.root.rowconfigure((3,5,6) ,weight=1)
        self.label =  CTkLabel(self.root,text=f"Prayer Times Today: \n\n{self.Text}" , font=("Arial", 14) ).grid(row=3,column=3)

    def main(self):
        self.ui()
        self.root.mainloop()

