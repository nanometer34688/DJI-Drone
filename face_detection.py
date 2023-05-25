import face_recognition
import numpy as np
import cv2

class FindFaces:
    def __init__(self) -> None:
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("faces/obama.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("faces/biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
       
        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        self.known_face_names = [
            "Barack Obama",
            "Biden"
        ]

    def process_frame(self, frame):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)
            
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            print(name, (left, top), (right, bottom))
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return frame, face_names