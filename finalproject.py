import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import Label  
from PIL import Image, ImageTk
import os

#  to define a simple advertisment 
ads = {
    'young_male_happy':r'C:\Users\BIT\ad_young_male_happy.jpg',
    'young_female_happy':r'C:\Users\BIT\ad_young_female_happy.jpg',
    'adult_male_sad':r'C:\Users\BIT\ad_adult_male_sad.jpg',
    'adult_female_sad':r'C:\Users\BIT\ad_adult_female_sad.jpg',
    'default':r'C:\Users\BIT\ad_default.png'
}

#  to select an ad based on demographic &  emotion
def select_ad(demographic, emotion):
    key = f"{demographic['age_group']}_{demographic['gender']}_{emotion}"
    print(f"Key: {key}")
    return ads.get(key, ads['default'])

#  to get demographic information
def get_demographic_info(analysis):
    # Access the first dictionary in the list returned by DeepFace.analyze
    result = analysis[0] if isinstance(analysis, list) else analysis

    age = result['age']
    gender = result['gender']
    
    age_group = 'young' if age < 30 else 'adult'
    gender = 'male' if gender == 'Man' else 'female'
    
    return {'age_group': age_group, 'gender': gender}

# Initialize the camera
cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        try:
            # Analyze the frame using DeepFace
            analysis = DeepFace.analyze(frame, actions=['age', 'gender', 'emotion'], enforce_detection=False)
            print(f"Analysis: {analysis}")
            demographic_info = get_demographic_info(analysis)
            dominant_emotion = analysis[0]['dominant_emotion'] if isinstance(analysis, list) else analysis['dominant_emotion']
            print(f"Demographics: {demographic_info}, Emotion: {dominant_emotion}")  # Debugging line

            # Select the appropriate ad
            selected_ad = select_ad(demographic_info, dominant_emotion)
            print(f"Selected Ad: {selected_ad}")
            # Display the selected ad
            if os.path.exists(selected_ad):
                ad_image = cv2.imread(selected_ad)
                if ad_image is not None:
                    ad_image = cv2.resize(ad_image, (frame.shape[1], frame.shape[0]))
                    ad_image_rgb = cv2.cvtColor(ad_image, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(ad_image_rgb)
                    imgtk = ImageTk.PhotoImage(image=img)
                    ad_label.imgtk = imgtk
                    ad_label.configure(image=imgtk)
                else:
                    ad_label.config(text=f"Error loading image {selected_ad}.")
            else:
                ad_label.config(text=f"Advertisement image {selected_ad} not found.")
        except Exception as e:
            print(f" There is an error  in analyzing frame: {e}")
    
    # Update the camera feed in the Tkinter window
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    
    root.after(10, update_frame)

root = tk.Tk()
root.title("Advertisement Display System")

title_label = Label(root, text="Ad Display System", font=("Georgia", 24))
title_label.pack(side=tk.TOP, pady=10)

# Create Labels to show the camera feed and the advertisement
camera_label = Label(root)
camera_label.pack(side=tk.LEFT, padx=10, pady=10)
ad_label = Label(root)
ad_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Start updating the frames
update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the camera when the GUI is closed
cap.release()
