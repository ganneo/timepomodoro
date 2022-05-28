import math
from datetime import datetime
from tkinter import *

from update_sheets import add_to_raw_data

start_sec = datetime.now()


def start_timer():
    global start_sec
    start_sec = datetime.now()
    time_left_text.config(text=f"{datetime.now()}")


def end_timer():
    time_passed_array = str(datetime.now() - start_sec).split(":")
    activity = activity_name.get()
    add_to_raw_data(activity, str(start_sec), str(datetime.now()))
    time_left_text.config(text=f"{time_passed_array[0]}:{time_passed_array[1]}:"
                               f"{math.floor(float(time_passed_array[2]))}")


window = Tk()
window.title("Pomodoro 2")
window.config(padx=100, pady=50)

option_word = Label(text="What activity")
option_word.grid(column=1, row=1)
activity_name = StringVar()
activity_name.set("math")
options = OptionMenu(window, activity_name,
                     *["Lint Code", "Math Alone", "Playing Games", "Math With Dad", "Basketball", "Chat", "Coding",
                       "Writing", "Tennis", "Chinese", "Physics", "Music"])
options.grid(column=2, row=1)

start_btn = Button(text="Start", command=start_timer)
start_btn.grid(column=1, row=3)
end_btn = Button(text="End", command=end_timer)
end_btn.grid(column=2, row=3)

time_left_text = Label(text="00:00")
time_left_text.grid(column=1, row=4)

window.mainloop()
