import tkinter as tk
from tkinter import messagebox
from customtkinter import *

class PomodoroTimer:
    def __init__(self):
        self.root = CTk()
        self.root.title('Pomodoro')

        self.SHORT_BREAK = 5 * 60
        self.LONG_BREAK = 20 * 60
        self.SESSION = 25 * 60
        self.SESS_COUNTER = 0
        self.is_break = False
        self.paused = False
        self.remaining_time = None
        self.job = None

        self.main_label = tk.Frame(self.root)
        self.main_label.pack(expand=True)

        self.time_label = tk.Label(self.main_label, text='00:00', font=('Arial', 24))
        self.time_label.pack(pady=10)

        self.cnt_label = tk.Label(self.main_label, text='Streak: 0', font=('Arial', 12))
        self.cnt_label.pack()

        self.button_frame = tk.Frame(self.main_label)
        self.button_frame.pack(padx=50)

        self.start_btn = tk.Button(self.button_frame, text="Start", command=self.start, bg="#4CAF50", activebackground="#45a049", padx=10)
        self.start_btn.pack(side='left', fill="x", expand=True)
        self.reset_btn = tk.Button(self.button_frame, text="Reset", command=self.stop_count, bg="#f44336", activebackground="#d32f2f", padx=10)
        self.reset_btn.pack(side='left', fill="x", expand=True)

        self.move_window_btn = tk.Button(self.button_frame, text="Snap", command=self.move_window, bg="#2196F3", activebackground="#0b7dda", padx=10)
        self.move_window_btn.pack(side='right', fill="x", expand=True)

    def count(self, timer=None):
        if self.paused:
            if timer is not None:
                self.remaining_time = timer
            return

        if timer is None:
            timer = self.remaining_time

        if timer <= -1:
            self.is_break = not self.is_break
            prompt_message = "Ready for a break ?" if self.is_break else "Ready for a new session ?"
            prompt_answer = messagebox.askquestion("Session Ended !", prompt_message, icon='question')

            if prompt_answer == 'yes':
                if self.is_break and self.SESS_COUNTER % 4 == 0:
                    self.count(self.LONG_BREAK)
                else:
                    self.SESS_COUNTER += 1
                    self.count(self.SHORT_BREAK if self.is_break else self.SESSION)
            else:
                self.stop_count()
            return

        m, s = divmod(timer, 60)
        self.time_label.configure(text='{:02d}:{:02d}'.format(m, s))
        self.cnt_label.configure(text='BREAK!' if self.is_break else 'Streak: {}'.format(self.SESS_COUNTER))
        self.job = self.root.after(1000, self.count, timer - 1)

    def stop_count(self):
        if self.job:
            self.root.after_cancel(self.job)
        self.time_label.configure(text='{:02d}:{:02d}'.format(0, 0))
        self.SESS_COUNTER = 0
        self.is_break = False
        self.cnt_label.configure(text='Streak: {}'.format(0))
        self.start_btn.configure(text="Start", command=self.start, bg="#4CAF50", activebackground="#45a049")

    def pause_count(self):
        self.paused = not self.paused
        if self.paused:
            self.start_btn.configure(text="Continue", command=self.continue_count, bg="#FFD700", activebackground="#FFC107")
        else:
            self.start_btn.configure(text="Pause", command=self.pause_count, bg="#f44336", activebackground="#d32f2f")

    def start(self):
        self.SESS_COUNTER += 1
        self.start_btn.configure(text="Pause", command=self.pause_count, bg="#f44336", activebackground="#d32f2f")
        self.count(self.SESSION)

    def continue_count(self):
        self.paused = False
        self.start_btn.configure(text="Pause", command=self.pause_count, bg="#f44336", activebackground="#d32f2f")
        self.count()

    def move_window(self):
        screen_width = self.root.winfo_screenwidth()
        window_width = self.root.winfo_width()

        current_x = self.root.winfo_x()

        if current_x >= screen_width - window_width - 10:
            self.root.geometry(f'+0+0')
        else:
            self.root.geometry(f'+{screen_width - window_width}+0')


    def main(self):
        self.root.mainloop() 

if __name__ == "__main__":
    pomodoro_timer = PomodoroTimer()
    pomodoro_timer.main()
