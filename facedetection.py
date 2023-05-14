import cv2
import tkinter as tk
import pygame
from PIL import Image, ImageTk


class QuarrelDetectionApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Quarrel Detection App")

        # Open the video source
        self.cap = cv2.VideoCapture(video_source)

        # Create a canvas for displaying frames
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Load the pre-trained Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Initialize the quarrel flag and the alert sound
        self.quarrel_flag = False
        pygame.mixer.init()
        self.alert_sound = pygame.mixer.Sound('alert.wav')

        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the frame
            faces = self.detect_faces(rgb_frame)

            # Draw rectangles around the detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Check for quarrel-like situation
            if len(faces) >= 2:
                self.quarrel_flag = True
            else:
                self.quarrel_flag = False

            # Play alert sound if quarrel-like situation is detected
            if self.quarrel_flag:
                self.alert_sound.play()
                self.quarrel_flag = False

            # Convert the frame to PIL Image format
            img = Image.fromarray(rgb_frame)

            # Create Tkinter-compatible image
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the canvas image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk

        # Keep updating the frame
        self.window.after(10, self.update)

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        return faces


# Create the Tkinter window
window = tk.Tk()

# Create the QuarrelDetectionApp instance
app = QuarrelDetectionApp(window)

# Run the Tkinter event loop
window.mainloop()
