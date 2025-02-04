import os
import requests
from datetime import date, datetime, timedelta
from customtkinter import CTk, CTkLabel, CTkFrame

class Prayers(CTk):
    def __init__(self, pos, right):
        super().__init__()
        self.pos = pos
        self.right = right
        self.today_prayers = {}
        self.tomorrow_prayers = {}
        self.current_date = date.today()
        self.tomorrow_date = self.current_date + timedelta(days=1)
        self.addressCheck()

    def addressCheck(self):
        self.load_prayer_times(self.current_date, self.today_prayers)
        self.load_prayer_times(self.tomorrow_date, self.tomorrow_prayers)

    def load_prayer_times(self, date_obj, prayer_dict):
        date_str = date_obj.strftime("%d-%m-%Y")
        directory = os.path.dirname(__file__)
        folder = "Prayer_Logs"
        file_name = f"prayersTable_{date_str}.txt"
        address = os.path.join(directory, folder)
        file_path = os.path.join(address, file_name)

        if not os.path.exists(address):
            os.makedirs(address)

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    prayer, time_str = line.strip().split(': ')
                    prayer_dict[prayer] = self.convert_to_time(date_obj, time_str)
        else:
            self.get_prayer_times(date_obj, file_path, prayer_dict)

    def get_prayer_times(self, date_obj, file_path, prayer_dict):
        date_str = date_obj.strftime("%d-%m-%Y")
        url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?city=avcilar&country=turkey&method=13"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            timings = data['data']['timings']

            with open(file_path, 'w', encoding='utf-8') as file:
                for prayer, time_str in timings.items():
                    if prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']:
                        time_obj = self.convert_to_time(date_obj, time_str)
                        prayer_dict[prayer] = time_obj
                        file.write(f"{prayer}: {time_str}\n")

    def convert_to_time(self, date_obj, time_str):
        return datetime.strptime(f"{date_obj} {time_str}", "%Y-%m-%d %H:%M")

    def time_until_next_prayer(self):
        now = datetime.now()
        all_prayers = list(self.today_prayers.items()) + list(self.tomorrow_prayers.items())

        for prayer, time in all_prayers:
            if now < time:
                time_diff = time - now
                return f"{prayer}: {str(time_diff).split('.')[0]}"
        return "No upcoming prayers."

    def update_daily(self):
        if date.today() != self.current_date:
            self.current_date = date.today()
            self.tomorrow_date = self.current_date + timedelta(days=1)
            self.addressCheck()
            self.ui()

    def ui(self):
        self.resizable(False, False)
        self.title("Prayer Times")
        self.after(60000, self.update_daily)

        # Positioning the window
        offset = -150 if self.right else -20
        posS = f"{int(self.pos[0]) + offset}+{int(self.pos[1]) + 40}"
        self.geometry(f"200x300+{posS}")

        # Widgets
        self.prayer_frame = CTkFrame(self, corner_radius=10)
        self.prayer_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.label = CTkLabel(self.prayer_frame, text=f"📅 Prayer Times Today:\n\n{self.format_prayers(self.today_prayers)}", 
                            font=("Arial", 14), justify="left")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.next_prayer_frame = CTkFrame(self, corner_radius=10, fg_color="#3f4046")
        self.next_prayer_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        time_left = self.time_until_next_prayer()
        self.time_label = CTkLabel(self.next_prayer_frame, text=f"Next Prayer:\n{time_left}", 
                                font=("Arial", 15), text_color="#dbdbdb")
        self.time_label.grid(row=0, column=0, padx=10, pady=10)

        self.mainloop()

    def format_prayers(self, prayers):
        return '\n'.join([f"{prayer}: {time.strftime('%H:%M')}" for prayer, time in prayers.items()])

    def main(self):
        self.ui()


# if __name__ == "__main__":
#   app = Prayers((100, 100), right=False)
#   app.main()