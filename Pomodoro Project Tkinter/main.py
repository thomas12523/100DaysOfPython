from math import *
from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps=0
timer=None
# ---------------------------- TIMER RESET ------------------------------- # 
def reseter():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text,text="00:00")
    tittle_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps=0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    work_sec=WORK_MIN*60
    short_break_sec= SHORT_BREAK_MIN*60
    long_break_sec= LONG_BREAK_MIN*60

    reps+=1
    if reps %2==0:
        check_marks.config(text="✔"*(reps//2))
    if reps%8==0:
        tittle_label.configure(text="Long Break",fg=RED)
        count_down(long_break_sec)
    elif reps%2==0:
        tittle_label.configure(text="Break",fg=PINK)
        count_down(short_break_sec)
    else:
        tittle_label.configure(text="Work",fg=GREEN)
        count_down(work_sec)
    
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min=floor(count/60)
    count_sec=count%60
    if count_sec==0:
        count_sec="00"
    elif int(count_sec)<10:
        count_sec=f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count >0:
        global timer
        timer= window.after(1000,count_down,count-1)
    else:
        start_timer()



# ---------------------------- UI SETUP ------------------------------- # ✔

window= Tk()
window.title("Pomodoro")
window.config(padx=100,pady=50,bg=YELLOW)


tittle_label=Label(text="Timer",font=(FONT_NAME,35,"bold"),foreground=GREEN,highlightthickness=0,bg=YELLOW)
tittle_label.grid(column=1,row=0)

canvas=Canvas(width=200, height=224,bg=YELLOW,highlightthickness=0)
tomato_img=PhotoImage(file="Pomodoro Project Tkinter/tomato.png")
canvas.create_image(100,112,image=tomato_img)
canvas.grid(column=1,row=1)

timer_text=canvas.create_text(100,130,text="00:00",fill="white",font=(FONT_NAME,25,"bold"))

start_buttom=Button(text="Start",highlightthickness=0,command=start_timer)
start_buttom.grid(column=0,row=2)

reset_buttom=Button(text="Reset",highlightthickness=0,command=reseter)
reset_buttom.grid(column=2,row=2)

check_marks= Label(text="",fg=GREEN,bg=YELLOW)
check_marks.grid(column=1,row=3)

window.mainloop()