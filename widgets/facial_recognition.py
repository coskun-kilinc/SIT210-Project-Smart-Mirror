# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

MAX_FRAMES = 15

class facial_recognition():
    def __init__(self, user: str) -> None:
        self.user = user
        # exploit previously trained model
        try:
            self.data = data = pickle.loads(open("widgets/facial_recognition_main/encodings.pickle", "rb").read())
        except:
            self.data = data = pickle.loads(open("widgets\facial_recognition_main\encodings.pickle", "rb").read())

    def identify_user(self) -> str:
        # initialise video stream with extremely low frame rate to save processing power
        video_stream = VideoStream(src=0,framerate=5).start()
        frames = 0

        # loop over frames from the video file stream until we find a face, or time out
        while frames < MAX_FRAMES:
            # grab the frame from the threaded video stream and resize it
	        # to 500px (to speedup processing)
            frame = video_stream.read()
            frame = imutils.resize(frame, width=500)

            # Detect the face boxes
            boxes = face_recognition.face_locations(frame)
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(frame, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(self.data["encodings"], encoding)
                name = "Unknown" # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = self.data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            #If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
            return currentname