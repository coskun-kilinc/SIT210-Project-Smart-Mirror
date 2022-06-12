# import all the necessary packages
import datetime
import time
import requests
from widgets import player, google_calendar, weather, identity
from tkinter import Label, Tk
from PIL import ImageTk, Image
from io import BytesIO

CALENDAR_EVENTS = 10    # number of calendar events to display
WEATHER_INTERVAL = 900  # time between refreshing the weather widget in seconds
IDENTITY_CHECK_INTERVAL = 15 # time between checking identity in seconds, increase to reduce overhead from facial recognition

# sets the base text size
BASE_TEXT_SIZE= 4

class SmartMirror:
    def __init__(self, 
                 master, 
                 user: str, 
                 identifier: identity.AbstractIdentifier, 
                 player_client: player.AbstractPlayerInterface,
                 weather_interface: weather.AbstractWeatherInterface):
        self.master = master

        # set title, and make fullscreen with a black background which will not show through the mirror
        self.master.title('Smart Mirror')
        self.master.attributes("-fullscreen", True)
        self.master.configure(background='black')
        self.master.bind("<Escape>", lambda event:self.close())

        # set user
        self.user = user
        # set up indentifier (Dummy or real facial recognition)
        self.identifier = identifier
        # Weather Widget Interface, can be swapped out with different implementations i.e. for testing purposes or to change to a web based rather than local reading
        self.weather_interface = weather_interface
        # player client i.e. Spotify or dummy interface
        self.player_client = player_client
       
        self.setup()
        
    def close(self):
        print("Closing safely")
        # GPIO.cleanup()
        self.master.destroy()

    '''
    Performs basic setup of interface, initiating grid, creating widgets and starting refresh cycle
    '''
    ######################
    ##       Setup      ##
    ######################

    def setup(self):
        self.grid_setup()
        self.init_system_clock()
        self.init_spotify_widget()
        self.init_google_calendar()
        self.init_weather()
        self.init_greeting()
        self.refresh()

    def refresh(self):
        self.refresh_clock()
        self.refresh_spotify()
        self.refresh_google_calendar()
        self.refresh_weather()
        self.refresh_greeting()
        
    ######################
    ##       Grid       ##
    ######################

    def grid_setup(self):
        padx = 50
        pady = 75

        self.top_left = Label(self.master, bg='black', width=30)
        self.top_left.grid(row=0,column=0, sticky = "NW", padx=(padx,0), pady=(pady,0))

        self.top_right = Label(self.master, bg='black', width=30)
        self.top_right.grid(row=0,column=1, sticky = "NE", padx=(0,padx), pady=(pady,0))

        self.middle_middle = Label(self.master, bg='black', width=30)
        self.middle_middle.grid(row=1,column=0, sticky = "N",columnspan=2)
        
        self.bottom_left = Label(self.master, bg='black', width=30)
        self.bottom_left.grid(row=2,column=0, sticky = "SW", padx=(padx,0), pady=(0,pady))

        self.bottom_right = Label(self.master, bg='black', width=30)
        self.bottom_right.grid(row=2,column=1, sticky = "SE", padx=(0,padx), pady=(0,pady+50))

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

    ######################
    ##      Clock       ##
    ######################

    '''
    Creates the date and time widget
    '''
    def init_system_clock(self):
        self.clock_hour = Label(self.master,
                                font = ('Bebas Neue', BASE_TEXT_SIZE*16),
                                bg='black',
                                fg='white')
        self.clock_hour.grid(in_=self.top_left,
                                row=0,
                                column=0,
                                rowspan = 2,
                                sticky="W")

        self.clock_min_sec = Label(self.master,
                                   font = ('Bebas Neue', BASE_TEXT_SIZE*6),
                                   bg='black',
                                   fg='white')
        self.clock_min_sec.grid(in_=self.top_left,
                                row=0,
                                column=1,
                                columnspan = 3,
                                sticky="W")

        self.date_frame = Label(self.master,
                                font = ('Bebas Neue', BASE_TEXT_SIZE*3),
                                bg='black',
                                fg='white')
        self.date_frame.grid(in_=self.top_left,
                                row=0,
                                column=1,
                                columnspan = 3,
                                sticky="S")

    '''
    Just calls the initial calls for the functions to update the time
    '''
    def refresh_clock(self):
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
        self.t.after(24*60*60*100, self.system_min_sec)
            
    ######################
    ##     Greeting     ##
    ######################

    '''
    Initialise greeting widget
    '''
    def init_greeting(self):        
        # create greeter interface
        self.greeter = identity.GeneralGreeting()

        # create widget
        self.greeting = Label(self.master,
                                 font = ('Bebas Neue', BASE_TEXT_SIZE*9),
                                 bg='black',
                                 fg='white')
        self.greeting.grid(in_=self.middle_middle,
                            row =0,
                            column = 0,
                            columnspan = 3)


    def refresh_greeting(self):
        # get user identity
        identity = self.identifier.get_identity()
        # if identified person is intended user, greet them
        if identity == self.user:
            self.greeting.config(text=self.greeter.greeting(identity))
            # reveal calendar
            authorised = True
        else:
            # otherwise hide calendar information
            self.greeting.config(text="Unknown User\nSensitive Information Hidden")
            # hide google calendar
            authorised = False
        self.update_google_calendar(authorised=authorised)
        self.greeting.after(IDENTITY_CHECK_INTERVAL * 1000, self.refresh_greeting)
         

    
    ######################
    ##      Weather     ##
    ######################
    
    '''
    Creates weather widget
    '''
    def init_weather(self):    
        # Weather Readings
        self.weather_widget = Label(self.master,
                                 font = ('Bebas Neue', BASE_TEXT_SIZE*3),
                                 bg='black',
                                 fg='white',
                                 justify='left')
        self.weather_widget.grid(in_=self.top_right,
                            row =0,
                            column = 3,
                            sticky="NE",
                            rowspan = 3)


    def refresh_weather(self):
        # get weather information from weather object
        temperature = self.weather_interface.get_temperature()
        humidity = self.weather_interface.get_humidity()
        heat_index = self.weather_interface.calculate_heat_index(temperature=temperature, humidity=humidity, is_farenheit=False)
        # format and display information
        self.weather_widget.config(text=f"Temperature: \t{round(temperature)}°c\nHumidity: \t{round(humidity)}%\nHeat Index: \t {round(heat_index)}")
        # update temperature every 15 minutes (controlled by the WEATHER_INTERVAL constant)
        self.weather_widget.after(WEATHER_INTERVAL*1000, self.refresh_weather)
  
    ######################
    ##  Google Calendar ##
    ######################

    '''
    Creates google calendar widget
    '''
    def init_google_calendar(self):
        # weather widget is paired to clock widget

        self.google_calendar = Label(self.master, text='Google Calendar',
                                     font = ('Bebas Neue', BASE_TEXT_SIZE*5),
                                     bg='black',
                                     fg='white')
        self.google_calendar.grid(in_=self.bottom_right,
                                  row =0,
                                  column = 1,
                                  columnspan = 1,
                                  sticky="NE") 
        self.calendar_events = []
        self.calendar_widgets = []
        for i in range(CALENDAR_EVENTS):
            self.calendar_events.append(" ")
            self.calendar_widgets.append(Label(self.master,
                                        text=self.calendar_events[i],
                                        font = ('Bebas Neue', BASE_TEXT_SIZE*3),
                                        bg='black',
                                        fg='white'))
            self.calendar_widgets[i].grid(in_=self.bottom_right,
                                          row =1+i,
                                          column = 1,
                                          columnspan = 1,
                                          sticky="NE") 
        
    '''
    Refresh Google Calendar data
    '''
    def refresh_google_calendar(self):
        events = google_calendar.get_calendar_events(num_events=CALENDAR_EVENTS)
        i = 0
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_text = f"{start}: {event['summary']}" 
            self.calendar_events[i] = event_text
            i += 1
        self.calendar_widgets[0].after(10000, self.refresh_google_calendar)

    '''
    Update Google Calendar Widget
    '''
    def update_google_calendar(self, authorised: bool):
        if authorised:
            for i in range(CALENDAR_EVENTS):
                self.calendar_widgets[i].config(text=self.calendar_events[i])
        else:
            for i in range(CALENDAR_EVENTS):
                self.calendar_widgets[i].config(text="information hidden")

        
    ######################
    ##      Spotify     ##
    ######################

    '''
    generates cells for the spotify widget
    '''
    def init_spotify_widget(self):
        # Currently Playing Arist
        self.spotify_artist = Label(self.master,
                                    font = ('consolas', BASE_TEXT_SIZE*3),
                                    bg='black',
                                    fg='white')
        self.spotify_artist.grid(in_=self.bottom_left,
                                 row=0,
                                 column=0,
                                 rowspan=1,
                                 columnspan = 2,
                                 sticky="N")

        # Currently Playing Album Art
        try:
            self.img = ImageTk.PhotoImage(Image.open('images/default_album_art.png'))
        except:
            self.img = ImageTk.PhotoImage(Image.open('images\default_album_art.png'))
        self.spotify_art= Label(self.master,
                                image=self.img, border=0)
        self.spotify_art.grid(in_=self.bottom_left,
                              row=1,
                              column=0,
                              rowspan=1,
                              columnspan = 1,
                              sticky="S")

        # Currently Playing Song Title
        self.spotify_track = Label(self.master,
                                   font = ('consolas', BASE_TEXT_SIZE*3),
                                   bg='black',
                                   fg='white')
        self.spotify_track.grid(in_=self.bottom_left,
                                row=3,
                                column=0,
                                columnspan = 1,
                                sticky="N")

        # Currently Playing Progress
        self.spotify_track_time = Label(self.master,
                                        font = ('consolas', BASE_TEXT_SIZE*3),
                                        bg='black',
                                        fg='white')
        self.spotify_track_time.grid(in_=self.bottom_left,
                                     row=4,
                                     column=0,
                                     columnspan = 1,
                                     sticky="S")

    '''
    Refresh spotify data and update widget
    '''
    def refresh_spotify(self, current_track_info=''):
        # get new track info

        next_track_info = self.player_client.get_current_track_info()
        # convert track time into string from track info
        track_time = f"{next_track_info['progress']}/{next_track_info['duration']}"
        # check if track info has changed
        if (next_track_info != current_track_info):
            # update all track info
            current_track_info = next_track_info
            #limit track and artist name length
            artist_name = '{name: ^20}'.format(name=current_track_info['artists'])
            track_name = '{name: ^20}'.format(name=current_track_info['track'])
            self.spotify_artist.config(text=artist_name[:20])
            self.spotify_track.config(text=track_name[:20])
            self.spotify_track_time.config(text=track_time)
            # Update Album Art 
            # if track has art (returns None if no playback information)
            if current_track_info['image'] != None:
                response = requests.get(current_track_info['image']['url'])
                image_bytes = BytesIO(response.content)
                # must store reference to 
                self.spotify_album_art=ImageTk.PhotoImage(Image.open(image_bytes))
            # if track doesn't have art (nothing playing or no art uploaded) display placeholder image
            else:
                self.spotify_album_art=self.img 
            
        # call again after 200 ms
        self.spotify_art.config(image=self.spotify_album_art)
        self.spotify_artist.after(200, self.refresh_spotify)


######################
##       Main       ##
######################

if __name__=="__main__":
    root = Tk()
    user = "Josh"
    identifier = identity.FacialRecognition(user)
    player_client = player.SpotifyClient()
    weather_interface = weather.ThingSpeakWeather()
    smart_gui = SmartMirror(root, 
                            user=user,
                            identifier=identifier,
                            player_client=player_client,
                            weather_interface=weather_interface)
    root.mainloop() 