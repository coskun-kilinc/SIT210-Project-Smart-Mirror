import datetime
import time
from widgets import spotify
from tkinter import Button, Entry, Frame, Label, Tk, scrolledtext, constants
class SmartMirror:
    def __init__(self, master):
        self.master = master

        # set title, and make fullscreen with a black background which will not show through the mirror
        self.master.title('Smart Mirror')
        self.master.attributes("-fullscreen", True)
        self.master.configure(background='black')
        self.master.bind("<Escape>", lambda event:self.close())

        self.setup()
        
    def close(self):
        print("Closing safely")
        self.master.destroy()

    '''
    Performs basic setup of interface, initiating grid, creating widgets and starting refresh cycle
    '''
    def setup(self):
        self.grid_setup()
        self.init_system_clock()
        self.init_spotify_widget()
        self.refresh()

    def refresh(self):
        self.get_system_time()
        self.refresh_spotify()
        
    def grid_setup(self):
        self.top_left = Label(self.master, bg='black', width=30)
        self.top_left.grid(row=0,column=0, sticky = "NW")

        self.bottom_left = Label(self.master, bg='black', width=30)
        self.bottom_left.grid(row=2,column=0, sticky = "W", padx=(10,0))

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)  
        #self.master.grid_columnconfigure(3, weight=1)  
        #self.master.grid_columnconfigure(4, weight=1)  

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=2)
        self.master.grid_rowconfigure(2, weight=2)
        #self.master.grid_rowconfigure(3, weight=2)
        #self.master.grid_rowconfigure(4, weight=2)

        self.top_left.grid_propagate(True)


    '''
    Just calls the initial calls for the functions to update the time
    '''
    def get_system_time(self):
        self.system_hour()
        self.system_min_sec()
        self.system_date()
        
    '''
    Gets the current system time and formats the hour for display
    
    '''
    def system_hour(self, hour=''):
        next_hour = time.strftime("%H")
        if (next_hour != hour):
            hour = next_hour
            self.clock_hour.config(text=hour)
        self.clock_hour.after(200, self.system_hour)

    '''
    Gets the current system time and formats the minutes and seconds for display
    If the time has changed, updates widget with current time
    '''
    def system_min_sec(self, min_sec=''):
        next_min_sec = time.strftime(":%M:%S")
        if (next_min_sec != min_sec):
            min_sec = next_min_sec
            self.clock_min_sec.config(text=min_sec)
        self.clock_min_sec.after(200, self.system_min_sec)


    '''
    Gets the current system date, updates widget with current date
    '''
    def system_date(self):
        system_date = datetime.date.today()
        self.date_frame.config(text=system_date.strftime("%A %d, %B %Y"))


    '''
    Creates the date and time widget
    '''
    def init_system_clock(self):
        self.clock_hour = Label(self.master, font = ('Bebas Neue', 125), bg='black', fg='white')
        self.clock_hour.grid(in_=self.top_left, row=0, column=0, rowspan = 2, sticky="W")

        self.clock_min_sec = Label(self.master, font = ('Bebas Neue', 50), bg='black', fg='white')
        self.clock_min_sec.grid(in_=self.top_left, row=0, column=1, columnspan = 3, sticky="W")

        self.date_frame = Label(self.master, font = ('Bebas Neue', 25), bg='black', fg='white')
        self.date_frame.grid(in_=self.top_left, row=0, column=1, columnspan = 3, sticky="S")
     
        
    '''
    Creates weather widget
    '''
    def init_web_weather(self):
        # weather widget is paired to clock widget

        #self.web_temp = Label(image=my_image, borderwidth = 0)
        #self.web_temp.image = my_image
        self.web_temp.grid(in_=self.TL, row =2, column = 1, sticky="NE")
        self.web_weather = Label(self.master, font = ('caviar dreams', 15, 'bold'), bg='black', fg='white')
        self.web_temp.grid(in_=self.TL, row =2, column = 2, sticky="NW") 

    '''
    generates cells for the spotify widget
    '''
    def init_spotify_widget(self):
        self.spotify_artist = Label(self.master, font = ('consolas', 30), bg='black', fg='white')
        self.spotify_artist.grid(in_=self.bottom_left, row=0, column=3, rowspan=2, columnspan = 3, sticky="N", padx=(10,10))

        # space for loading album art, currently WIP

        self.spotify_track = Label(self.master, font = ('consolas', 30), bg='black', fg='white')
        self.spotify_track.grid(in_=self.bottom_left, row=2, column=3, columnspan = 3, sticky="N", padx=(10,10))

        self.spotify_track_time = Label(self.master, font = ('consolas', 25), bg='black', fg='white')
        self.spotify_track_time.grid(in_=self.bottom_left, row=3, column=3, columnspan = 3, sticky="S", padx=(10,10))


    '''
    Refresh spotify data and update widget
    '''
    def refresh_spotify(self, current_track_info=''):
        next_track_info = spotify.get_current_track_info()
        track_time = f"{next_track_info['progress']}/{next_track_info['duration']}"
        if (next_track_info != current_track_info):
            current_track_info = next_track_info
            #limit track and artist name length
            artist_name = '{name: ^30}'.format(name=current_track_info['artists'])
            track_name = '{name: ^30}'.format(name=current_track_info['track'])
            self.spotify_artist.config(text=artist_name[:30])
            self.spotify_track.config(text=track_name[:30])
            self.spotify_track_time.config(text=track_time)
        self.spotify_artist.after(200, self.refresh_spotify)
        

root = Tk()
smart_gui = SmartMirror(root)
root.mainloop()