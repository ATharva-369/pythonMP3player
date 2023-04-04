import tkinter as tk
import customtkinter as ck
from pygame import mixer
from mutagen.mp3 import MP3
import os
import sys
import time
from PIL import Image, ImageTk

#basic definitions
ck.set_appearance_mode("dark")
m= ck.CTk()
m.geometry('1920x1080')
current_scale = 0
when_slide = 0
mixer.init()
mx = mixer.music
slided = False
song_length = 0;

#importing images
play_button = ImageTk.PhotoImage(Image.open("images/play-button.png"), Image.ANTIALIAS, width=50, height=50)
pause_button = ImageTk.PhotoImage(Image.open("images/pause-button.png"), Image.ANTIALIAS, width=50, height=50)
quit_button = ImageTk.PhotoImage(Image.open("images/quit-button.png"), Image.ANTIALIAS, width=50, height=50)
bgimg = ImageTk.PhotoImage(Image.open("images/wallpaper.jpg"), Image.ANTIALIAS)
# getting mp3 files
files= []
for x in os.listdir():
    if x.endswith(".mp3"):
        files.append(x)


# play function
def Play():
    mx.load(clicked.get())
    audio = MP3(clicked.get())
    global song_length 
    song_length = int(audio.info.length)
    my_slider.config(to=song_length)
    mx.play(start = int(my_slider.get()))
    vol.set(100)
#pause function
def Pause():
    mx.pause()

#slider function

def slider(self):
    global slided
    global song_length
    slided = True
    slider_label.config(text=f'{int(my_slider.get())} of {song_length}')
    global currenttime
    currenttime = int(my_slider.get())
    global when_slide
    when_slide = currenttime
    mx.play(start = currenttime)

def current_scale():
    global song_length
    if not slided:
        global currenttime
        currenttime = mx.get_pos() /1000
        # print(currenttime)
        converted_currenttime = time.strftime('%M:%S', time.gmtime(currenttime))
        scale_var.set(currenttime)
        slider_label.config(text=f'{int(my_slider.get())} of {song_length}')
    if slided:
        global when_slide
        currenttime = (mx.get_pos()/ 1000) +(when_slide)
        # print(when_slide)
        converted_currenttime = time.strftime('%M:%S', time.gmtime(currenttime))
        scale_var.set(currenttime)
        slider_label.config(text=f'{int(my_slider.get())} of {song_length}')
    m.after(1000, current_scale)


def change_vol(self):
    mx.set_volume(vol.get()/100)

def starting(self):
    my_slider.set(0)
    mx.stop()

m.title('MP3 Player')

#styles
s = tk.ttk.Style()
s.configure('volume_scale.Vertical.TScale', background='black')
s.configure('progress_scale.Horizontal.TScale', background='black')
helv36 = tk.font.Font(family='Helvetica', size=15)

limg= tk.Label(m, image=bgimg)
limg.place(x = 0, y = 0)


clicked = tk.StringVar()
if len(files) > 0:
    clicked.set(files[0])
else:
    tk.messagebox.showerror("Error", "No mp3 files in current directory")

scale_var = tk.IntVar()

drop = tk.OptionMenu(m,clicked, *files, command= starting)
drop.config( bg='black', fg='white', width=200, height=5,font=helv36)
drop["menu"].config( bg='green', fg='black')
drop.pack()
my_slider = tk.ttk.Scale( m, variable = scale_var, 
           from_ = 1, to = 100, 
           orient = tk.HORIZONTAL,
           command = slider,
           style="progress_scale.Horizontal.TScale",
           length=300)
my_slider.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER, )

slider_label = tk.Label(m, text="0", width = 10, height =3,foreground='white',background='black')
slider_label.place(relx = 0.5, rely = 0.45, anchor = tk.CENTER)

vol = tk.ttk.Scale(
    from_ = 0,
    to = 100,
    orient = tk.VERTICAL ,
    ####################
    command=change_vol,
    ####################
    style='volume_scale.Vertical.TScale',
    length=300
    
)
vol.place(relx = 0.95, rely = 0.8, anchor = tk.CENTER, )

play_button = ck.CTkButton(master=m, text='' , image=play_button, command = Play, width=50, height=50, fg_color="#1A1110", hover=False)
play_button.image = play_button
play_button.place(relx = 0.2, rely = 0.6, anchor = tk.CENTER)

pause_button = ck.CTkButton(master=m, text='' , image=pause_button, command = Pause, width=50, height=50, fg_color="#1A1110", hover=False)
pause_button.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

close_button = ck.CTkButton(master=m, text='' , image=quit_button, command = sys.exit, width=50, height=50, fg_color="#1A1110", hover=False)
close_button.place(relx = 0.8, rely = 0.6, anchor = tk.CENTER)

m.after(1000, current_scale)
m.mainloop()
