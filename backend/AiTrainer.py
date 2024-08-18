import cv2
import PoseModule as pm
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Define ideal angles and thresholds
ideal_angles = {
    "knee": 90,  # Ideal knee angle
    "hip": 90,   # Ideal hip angle
    "back": 180  # Ideal back angle
}

# Set to either 'beginner' or 'pro' to choose the appropriate thresholds
mode = 'beginner'  # or 'pro'

def get_thresholds(mode):
    if mode == 'beginner':
        return {
            'HIP_KNEE_VERT': {
                'NORMAL': (0, 32),
                'TRANS': (35, 65),
                'PASS': (70, 95)
            },
            'HIP_THRESH': [10, 50],
            'ANKLE_THRESH': 45,
            'KNEE_THRESH': [50, 70, 95],
            'OFFSET_THRESH': 35.0,
            'INACTIVE_THRESH': 15.0,
            'CNT_FRAME_THRESH': 50
        }
    elif mode == 'pro':
        return {
            'HIP_KNEE_VERT': {
                'NORMAL': (0, 32),
                'TRANS': (35, 65),
                'PASS': (80, 95)
            },
            'HIP_THRESH': [15, 50],
            'ANKLE_THRESH': 30,
            'KNEE_THRESH': [50, 80, 95],
            'OFFSET_THRESH': 35.0,
            'INACTIVE_THRESH': 15.0,
            'CNT_FRAME_THRESH': 50
        }

class SquatEvaluator:
    def __init__(self, mode='beginner'):
        self.thresholds = get_thresholds(mode)
        self.state_tracker = {
            'state_seq': []
        }

    def _get_state(self, knee_angle):
        knee = None
        if self.thresholds['HIP_KNEE_VERT']['NORMAL'][0] <= knee_angle <= self.thresholds['HIP_KNEE_VERT']['NORMAL'][1]:
            knee = 1
        elif self.thresholds['HIP_KNEE_VERT']['TRANS'][0] <= knee_angle <= self.thresholds['HIP_KNEE_VERT']['TRANS'][1]:
            knee = 2
        elif self.thresholds['HIP_KNEE_VERT']['PASS'][0] <= knee_angle <= self.thresholds['HIP_KNEE_VERT']['PASS'][1]:
            knee = 3
        return f's{knee}' if knee else None

    def _update_state_sequence(self, state):
        if state == 's2':
            if (('s3' not in self.state_tracker['state_seq']) and 
                (self.state_tracker['state_seq'].count('s2') == 0)) or \
               (('s3' in self.state_tracker['state_seq']) and 
                (self.state_tracker['state_seq'].count('s2') == 1)):
                self.state_tracker['state_seq'].append(state)
        elif state == 's3':
            if (state not in self.state_tracker['state_seq']) and 's2' in self.state_tracker['state_seq']:
                self.state_tracker['state_seq'].append(state)

    def evaluate_squat(self, knee_angle):
        state = self._get_state(knee_angle)
        if state:
            self._update_state_sequence(state)
        
        feedback = "Squat Needs Improvement"
        color = (255, 0, 0)  # red
        
        if 's2' in self.state_tracker['state_seq'] and 's3' in self.state_tracker['state_seq']:
            feedback = "Good Squat! Keep it up!"
            color = (0, 255, 0)  # green
        elif 's2' in self.state_tracker['state_seq']:
            feedback = "Descending phase good, but focus on reaching a deeper squat."
        elif 's3' in self.state_tracker['state_seq']:
            feedback = "Ascending phase good, but focus on starting from a deeper squat."
        
        return feedback, color

def draw_text(img, text, position, font_size=20, color=(255, 255, 255), box_color=(0, 0, 0)):
    # Create an image with PIL to use custom font
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    try:
        # Load the custom font
        font = ImageFont.truetype("Outfit.ttf", font_size)
    except IOError:
        # Fallback to default font if custom font is not found
        font = ImageFont.load_default()
    
    # Calculate text size using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    box_width = text_width + 20
    box_height = text_height + 10

    # Draw box
    draw.rectangle([position[0] - 10, position[1] - 10, position[0] + box_width, position[1] + box_height], fill=box_color)
    draw.text(position, text, font=font, fill=color)
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img

def process_video(video_source):
    # Open video file or webcam
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    # Define output image folder
    frames_folder = "frames"
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    frame_number = 0
    detector = pm.poseDetector()
    evaluator = SquatEvaluator(mode=mode)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break  # End of video

        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if lmList:
            # Right Hip and Knee
            hip_angle = detector.findAngle(img, 11, 23, 25)
            knee_angle = detector.findAngle(img, 23, 25, 27)
            back_angle = detector.findAngle(img, 11, 12, 24)  # Adjust as needed

            feedback, color = evaluator.evaluate_squat(knee_angle)

            # Display feedback in a box
            y0, dy = 30, 40
            img = draw_text(img, feedback, (20, y0), font_size=20, color=color, box_color=(0, 0, 0))

        # Save the frame as an image
        output_file = os.path.join(frames_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(output_file, img)

        frame_number += 1

    cap.release()

def create_video_from_images():
    path = 'frames/'  # Folder containing the images
    out_path = 'processedREAL/'  # Save the video in the 'processed' folder
    out_video_name = 'PV.mp4'  # Output video name
    out_video_full_path = os.path.join(out_path, out_video_name)

    # Ensure the output directory exists
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # Get a list of image filenames from the 'frames' folder
    pre_imgs = os.listdir(path)

    # Sort the filenames if necessary (e.g., if they need to be in a specific order)
    pre_imgs.sort()

    # Initialize a list to store the full paths of images
    img = []

    # Construct full paths for each image and append to the list
    for filename in pre_imgs:
        img_path = os.path.join(path, filename)
        img.append(img_path)

    # Check if there are any images to process
    if not img:
        raise ValueError("No images found in the specified directory.")

    # Read the first image to get the size for the video
    frame = cv2.imread(img[0])
    if frame is None:
        raise ValueError("Error reading the first image. Check the image files.")
    size = (frame.shape[1], frame.shape[0])  # (width, height)

    # Define the codec and create a VideoWriter object
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, 24, size)  # FPS: 24

    # Write each image to the video
    for i in range(len(img)): 
        frame = cv2.imread(img[i])
        if frame is None:
            print(f"Warning: Skipping image {img[i]}")
            continue
        video.write(frame)
        print('Frame ', i+1, ' of ', len(img))

    # Release the video writer object
    video.release()
    print('Output video saved to ', out_video_full_path)

def main(filepath="video.mp4"):
    video_source = filepath  # Change this to 0 for webcam feed
    process_video(video_source)
    create_video_from_images()

if __name__ == "__main__":
    main()
