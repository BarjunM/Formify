import cv2
import mediapipe as mp
import time
import math

class poseDetector:
    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.static_image_mode,
                                     model_complexity=self.model_complexity,
                                     smooth_landmarks=self.smooth_landmarks,
                                     enable_segmentation=self.enable_segmentation,
                                     smooth_segmentation=self.smooth_segmentation,
                                     min_detection_confidence=self.min_detection_confidence,
                                     min_tracking_confidence=self.min_tracking_confidence)

        # Define orange color in BGR format
        self.orange_color = (0, 69, 255)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                # The default landmark drawing color is blue; cannot change here
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    # Draw joints in orange color
                    cv2.circle(img, (cx, cy), 5, self.orange_color, cv2.FILLED)  # Orange color for circles
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if draw:
            # Draw lines in default color (usually blue)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)  # Default color for lines
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)  # Default color for lines
            # Draw joints in orange color
            cv2.circle(img, (x1, y1), 10, self.orange_color, cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, self.orange_color, 2)
            cv2.circle(img, (x2, y2), 10, self.orange_color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, self.orange_color, 2)
            cv2.circle(img, (x3, y3), 10, self.orange_color, cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, self.orange_color, 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, self.orange_color, 2)
        return angle
