from tkinter import *

count_hour = 0
count_min = 0
count_sec = 0
saved_hour = 0
saved_min = 0
saved_sec = 0

last_count = True
running = False


# ---------------------------- MODIFY TIMER MECHANISM ------------------------------- #
def modify(value):
    global count_hour, count_min, count_sec
    if value == "hour+":
        count_hour += 1
    elif value == "first_min+":
        count_min += 1
    elif value == "second_min+":
        count_min += 10
    elif value == "first_sec+":
        count_sec += 1
    elif value == "second_sec+":
        count_sec += 10
    elif value == "hour-":
        count_hour -= 1
    elif value == "first_min-":
        count_min -= 1
    elif value == "second_min-":
        count_min -= 10
    elif value == "first_sec-":
        count_sec -= 1
    elif value == "second_sec-":
        count_sec -= 10
    if count_sec >= 60:
        count_sec -= 60
        count_min += 1
    elif count_sec < 0:
        count_sec = 0
    if count_min >= 60:
        count_min -= 60
        count_hour += 1
    elif count_min < 0:
        count_min = 0
    if count_hour == 100:
        count_hour -= 1
    elif count_hour < 0:
        count_hour = 0
    if count_hour < 10:
        count_hour_str = f"0{count_hour}"
    else:
        count_hour_str = count_hour
    if count_min < 10:
        count_min_str = f"0{count_min}"
    else:
        count_min_str = count_min
    if count_sec < 10:
        count_sec_str = f"0{count_sec}"
    else:
        count_sec_str = count_sec
    canvas.itemconfig(timer_text, text=f"{count_hour_str}:{count_min_str}:{count_sec_str}")


# ---------------------------- BUTTON'S MECHANISM ------------------------------- #
# noinspection PyGlobalUndefined
def start(count):
    global count_hour, count_min, count_sec, last_count, timer
    count_sec = count
    if last_count:
        repeat(action="save_last_count")
        last_count = False
    count_hour_str = count_hour
    count_min_str = count_min
    count_sec_str = count
    if count_sec == 0:
        if count_min > 0:
            count_min -= 1
            count_sec += 59
        else:
            if count_hour > 0:
                count_hour -= 1
                count_min += 59
                count_sec += 59
    if count_hour < 10:
        count_hour_str = f"0{count_hour}"
    if count_min < 10:
        count_min_str = f"0{count_min}"
    if count_sec < 10:
        count_sec_str = f"0{count}"
    canvas.itemconfig(timer_text, text=f"{count_hour_str}:{count_min_str}:{count_sec_str}")
    if count > 0:
        try:
            window.after_cancel(timer)
        except ValueError:
            pass
        except NameError:
            pass
        timer = window.after(1000, start, count - 1)


def reset():
    global count_sec, count_min, count_hour, last_count
    window.after_cancel(timer)
    count_sec = 0
    count_min = 0
    count_hour = 0
    last_count = True
    canvas.itemconfig(timer_text, text="00:00:00")


def pause():
    window.after_cancel(timer)


def repeat(action):
    global count_sec, count_min, count_hour, saved_sec, saved_min, saved_hour, last_count
    if action == "save_last_count":
        saved_sec = count_sec
        saved_min = count_min
        saved_hour = count_hour
    elif action == "reset":
        window.after_cancel(timer)
        count_sec = saved_sec
        count_min = saved_min
        count_hour = saved_hour
        last_count = True
        modify("fix misspellings")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Temporizador")
window.config(padx=5, pady=5, bg="white")

canvas = Canvas(width=190, height=40, bg="white", highlightthickness=0)
timer_text = canvas.create_text(95, 20, text="00:00:00", fill="black", font=("Courier", 35, "bold"))
canvas.grid(column=1, row=2, columnspan=3)

hour_button = Button(text="+1", highlightthickness=0, highlightbackground="white",
                     command=lambda: modify(value="hour+"))
first_minute_button = Button(width=3, text="+1", highlightthickness=0, highlightbackground="white",
                             command=lambda: modify(value="first_min+"))
second_minute_button = Button(width=3, text="+10", highlightthickness=0, highlightbackground="white",
                              command=lambda: modify(value="second_min+"))
first_second_button = Button(width=3, text="+1", highlightthickness=0, highlightbackground="white",
                             command=lambda: modify(value="first_sec+"))
second_second_button = Button(width=3, text="+10", highlightthickness=0, highlightbackground="white",
                              command=lambda: modify(value="second_sec+"))

hour_button.grid(column=1, row=1)
first_minute_button.grid(column=2, row=1)
second_minute_button.grid(column=2, row=0)
first_second_button.grid(column=3, row=1)
second_second_button.grid(column=3, row=0)

negative_hour_button = Button(text="-1", highlightthickness=0, highlightbackground="white",
                              command=lambda: modify(value="hour-"))
negative_first_minute_button = Button(width=3, text="-1", highlightthickness=0, highlightbackground="white",
                                      command=lambda: modify(value="first_min-"))
negative_second_minute_button = Button(width=3, text="-10", highlightthickness=0, highlightbackground="white",
                                       command=lambda: modify(value="second_min-"))
negative_first_second_button = Button(width=3, text="-1", highlightthickness=0, highlightbackground="white",
                                      command=lambda: modify(value="first_sec-"))
negative_second_second_button = Button(width=3, text="-10", highlightthickness=0, highlightbackground="white",
                                       command=lambda: modify(value="second_sec-"))

negative_hour_button.grid(column=1, row=3)
negative_first_minute_button.grid(column=2, row=3)
negative_second_minute_button.grid(column=2, row=4)
negative_first_second_button.grid(column=3, row=3)
negative_second_second_button.grid(column=3, row=4)

start_button = Button(text="Iniciar", highlightbackground="white", highlightthickness=0,
                      command=lambda: start(count=count_sec))
repeat_button = Button(text="Repetir", highlightbackground="white", highlightthickness=0,
                       command=lambda: repeat(action="reset"))
pause_button = Button(text="Pausar", highlightbackground="white", highlightthickness=0, command=pause)
reset_button = Button(text="Reiniciar", highlightbackground="white", highlightthickness=0, command=reset)

start_button.grid(column=4, row=1)
repeat_button.grid(column=4, row=3)
pause_button.grid(column=0, row=1)
reset_button.grid(column=0, row=3)

window.mainloop()
