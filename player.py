import os
import time
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
from mutagen.mp3 import MP3

root = Tk()
root.title('Music Player')
root.geometry("500x400")
# Initialize Pygame Mixer
pygame.mixer.init()

def play_time():
    if stopped:
        return
    
    current_time = pygame.mixer.music.get_pos() / 1000
    new_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    global song_length
    song = f'/Users/teja1208/Desktop/Music_player/audio/{song}.mp3'
    song_mut = MP3(song)
    song_length = song_mut.info.length
    song_duration = time.strftime('%M:%S', time.gmtime(song_length))
    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed:{new_current_time} of {song_duration}')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {song_duration}')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    
    status_bar.after(1000, play_time)

# Function to add a single song
def add_songs():
    song = filedialog.askopenfilename(initialdir='/Users/teja1208/Desktop/Music_player/audio/', title="Select a Song", filetypes=(("mp3 Files","*.mp3"),))
    song = song.replace("/Users/teja1208/Desktop/Music_player/audio/", "")
    song = song.replace(".mp3","")
    song_box.insert(END, song)

# Function to play a song
def play():
    song = song_box.get(ACTIVE)
    song = f'/Users/teja1208/Desktop/Music_player/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)

global stopped
stopped=False

# Function to stop playing
def stop():
    status_bar.config(text='')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)
    status_bar.config(text='')
    global stopped
    stopped = True 
    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)

global paused
paused = False

# Function to pause or unpause
def pause(is_paused):
    global paused
    paused = is_paused
    if paused == True:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

# Function to add multiple songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='/Users/teja1208/Desktop/Music_player/audio/', title="Select a Song", filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song = song.replace("/Users/teja1208/Desktop/Music_player/audio/", "")
        song = song.replace(".mp3","")
        song_box.insert(END, song)

# Function to play the next song
def next_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'/Users/teja1208/Desktop/Music_player/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

# Function to play the previous song
def previous_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]-1
    song = song_box.get(next_one) 
    song = f'/Users/teja1208/Desktop/Music_player/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

# Function to delete the selected song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Function to delete all songs
def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

# Function to slide the slider
def slide(x):
    song = song_box.get(ACTIVE)
    song = f'/Users/teja1208/Desktop/Music_player/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Function to adjust the volume
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)

# Create frames and widgets
master_frame = Frame(root)
master_frame.pack(pady=20)
    
song_box = Listbox(master_frame, bg="black", fg="white", width=60, selectbackground="grey", selectforeground="white")
song_box.grid(row=0, column=0)

back_button = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/back.png')
forward_button = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/next.png')
play_button = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/play.png')
pause_button = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/pause.png')
stop_button = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/stop.png')

vol0 = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/vol0.png')
vol1 = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/vol1.png')
vol2 = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/vol2.png')
vol3 = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/vol3.png')
vol4 = PhotoImage(file='/Users/teja1208/Desktop/Music_player/images/vol4.png')

control_frame = Frame(master_frame)
control_frame.grid(row=1, column=0, pady=20)

volume_meter = Label(master_frame, image=vol0)
volume_meter.grid(row=1, column=1, padx=10)

volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)

back_btn = Button(control_frame, image=back_button, borderwidth=0, command=previous_song)
frwd_btn = Button(control_frame, image=forward_button, borderwidth=0, command=next_song)
play_btn = Button(control_frame, image=play_button, borderwidth=0, command=play)
pause_btn = Button(control_frame, image=pause_button, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(control_frame, image=stop_button, borderwidth=0, command=stop)

back_btn.grid(row=0, column=0, padx=10)
frwd_btn.grid(row=0, column=4, padx=10)
play_btn.grid(row=0, column=1, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=0, column=3, padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song)
add_song.add_command(label="Add a song to Playlist", command=add_songs)
add_song.add_command(label="Add songs to Playlist", command=add_many_songs)

remove_song = Menu()
my_menu.add_cascade(label="Delete Songs", menu=remove_song)
remove_song.add_command(label="Delete a song from Playlist", command=delete_song)
remove_song.add_command(label="Delete all song from Playlist", command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=0, command=volume, length=125)
volume_slider.pack(pady=10)

root.mainloop()
