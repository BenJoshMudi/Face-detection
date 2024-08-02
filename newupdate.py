import cv2
import streamlit as st
import os

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier("C:/Users/mudia/Downloads/haarcascade_frontalface_default.xml")

def detect_faces(scaleFactor, minNeighbors, rectangle_color):
    cap = cv2.VideoCapture(0)  # Initialize the webcam (0 is the default webcam)
    frame_window = st.image([])  # Create a Streamlit image element to display frames
    captured_frame = None

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam

        if not ret:  # Check if the frame is captured successfully
            st.error("Failed to capture frame from webcam. Please ensure the webcam is connected.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)  # Detect faces

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), rectangle_color, 2)  # Draw rectangle around faces

        frame_window.image(frame, channels="BGR")  # Display the frame in Streamlit
        captured_frame = frame

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit the loop if 'q' is pressed
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_frame

def home():
    st.title("Face Detection App")
    st.write("Welcome to the Face Detection App!")
    st.write("""
        This application uses the Viola-Jones Algorithm to detect faces in real-time from your webcam.
        
        Use the navigation sidebar to start detecting faces or learn more about the app.
    """)

def face_detection():
    st.title("Face Detection")
    st.write("This application uses your webcam to detect faces in real-time.")
    st.write("Instructions:")
    st.write("1. Press the 'Start' button to start the face detection.")
    st.write("2. Use the sliders to adjust the detection parameters.")
    st.write("3. Use the color picker to choose the rectangle color for detected faces.")
    st.write("4. Enter the file name and press 'Save Image' to save the image with detected faces.")

    scaleFactor = st.slider('Scale Factor', 1.1, 2.0, 1.3)
    minNeighbors = st.slider('Min Neighbors', 1, 10, 5)
    rectangle_color_hex = st.color_picker('Pick a color for the rectangle', '#00FF00')
    rectangle_color = tuple(int(rectangle_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))  # Convert hex to BGR

    save_path = st.text_input('Enter the file name to save the image:', 'detected_faces.jpg')

    col1, col2 = st.columns([1, 1])
    
    with col1:
        start_button = st.button("Start", key="start_detection")
    
    with col2:
        save_button = st.button("Save Image", key="save_image")

    if start_button:
        frame = detect_faces(scaleFactor, minNeighbors, rectangle_color)
        st.image(frame, channels="BGR")

    if save_button and 'frame' in locals():
        if frame is not None:
            # Define the directory to save images
            save_directory = 'saved_images'

            # Create the directory if it doesn't exist
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # Full path to save the image
            full_save_path = os.path.join(save_directory, save_path)
            
            cv2.imwrite(full_save_path, frame)
            st.success(f'Image saved as {full_save_path}')
        else:
            st.error("No image to save. Please start the detection first.")

def about():
    st.title("About This App")
    st.write("""
        This Face Detection App uses the Viola-Jones Algorithm to detect faces in real-time from a webcam feed.
        
        The Viola-Jones Algorithm is a robust face detection method that uses Haar-like features and a cascade of classifiers to detect faces quickly and accurately.

        The app is built using Streamlit, a framework for creating interactive web applications in Python. The face detection is performed using OpenCV, an open-source computer vision library.

        Use this app to detect faces from your webcam, adjust detection parameters, choose rectangle colors, and save the detected images.
    """)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Face Detection", "About"])

    if page == "Home":
        home()
    elif page == "Face Detection":
        face_detection()
    elif page == "About":
        about()

if __name__ == '__main__':
    main()
