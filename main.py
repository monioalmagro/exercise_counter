from datetime import datetime
from time import time
from math import acos, degrees

import cv2
import mediapipe as mp
import numpy as np
from conecction_db import insert_serie

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Principal:
    def __init__(self, usuario) -> None:
        #self.cap = cv2.VideoCapture("ejercicio.mp4")
        self.cap = cv2.VideoCapture(0)

        self.up = False
        self.down = False
        self.count = 0
        self.usuario = usuario

    def magic(self):
        time_1 = datetime.now()
        with mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as pose:
            while self.cap.isOpened():
                time_2 = datetime.now()
                if time_2.second - time_1.second > 60:
                    exercise = "sentadillas"
                    insert_serie(self.usuario, exercise, time_1, self.count, time_2)
                    cv2.destroyAllWindows()
                    return False
                # with mp_pose.Pose(
                #    static_image_mode=False) as pose:
                #
                #    while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks is not None:
                    x1 = int(results.pose_landmarks.landmark[24].x * width)
                    y1 = int(results.pose_landmarks.landmark[24].y * height)

                    x2 = int(results.pose_landmarks.landmark[26].x * width)
                    y2 = int(results.pose_landmarks.landmark[26].y * height)

                    x3 = int(results.pose_landmarks.landmark[28].x * width)
                    y3 = int(results.pose_landmarks.landmark[28].y * height)

                    p1 = np.array([x1, y1])
                    p2 = np.array([x2, y2])
                    p3 = np.array([x3, y3])

                    l1 = np.linalg.norm(p2 - p3)
                    l2 = np.linalg.norm(p1 - p3)
                    l3 = np.linalg.norm(p1 - p2)

                    # Calcular el ángulo
                    angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
                    if angle >= 160:
                        self.up = True
                    if self.up == True and self.down == False and angle <= 70:
                        self.down = True
                    if self.up == True and self.down == True and angle >= 160:
                        self.count += 1
                        self.up = False
                        self.down = False
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print("Current Time =", current_time)

                        print("self.count: ", self.count)
                    # Visualización
                    aux_image = np.zeros(frame.shape, np.uint8)
                    cv2.line(aux_image, (x1, y1), (x2, y2), (255, 255, 0), 20)
                    cv2.line(aux_image, (x2, y2), (x3, y3), (255, 255, 0), 20)
                    cv2.line(aux_image, (x1, y1), (x3, y3), (255, 255, 0), 5)
                    contours = np.array([[x1, y1], [x2, y2], [x3, y3]])
                    cv2.fillPoly(aux_image, pts=[contours], color=(128, 0, 250))

                    output = cv2.addWeighted(frame, 1, aux_image, 0.8, 0)

                    cv2.circle(output, (x1, y1), 6, (0, 255, 255), 4)
                    cv2.circle(output, (x2, y2), 6, (128, 0, 250), 4)
                    cv2.circle(output, (x3, y3), 6, (255, 191, 0), 4)
                    cv2.rectangle(output, (0, 0), (60, 60), (255, 255, 0), -1)
                    cv2.putText(
                        output, str(int(angle)), (x2 + 30, y2), 1, 1.5, (128, 0, 250), 2
                    )
                    cv2.putText(
                        output, str(self.count), (10, 50), 1, 3.5, (128, 0, 250), 2
                    )
                    imS1 = cv2.resize(output, (960, 540))
                    cv2.imshow("output", imS1)
                imS = cv2.resize(frame, (960, 540))
                cv2.imshow("Frame", imS)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        self.cap.release()
        cv2.destroyAllWindows()

    def calculate_angle(self, a, b, c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle >180.0:
            angle = 360-angle

        return angle 

    def mancurnas(self):
        time_1 = datetime.now()
        time_start  = time()
        self.counter = 0 
        self.stage = None
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.cap.isOpened():
                time_now = time()
                time_2 = datetime.now()
                a = time_now - time_start
                print(a)
                if a > 60:
                    exercise = "mancuernas"
                    insert_serie(self.usuario, exercise, time_1, self.counter, time_2)
                    cv2.destroyAllWindows()
                    return False
                ret, frame = self.cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, elbow, wrist)

                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                   tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )

                    # Curl counter logic
                    if angle > 160:
                        self.stage = "down"
                    if angle < 30 and self.stage =='down':
                        self.stage="up"
                        self.counter +=1
                        print(self.counter)
                except:
                    pass
                
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)

                # Rep data
                cv2.putText(image, 'Repeticiones', (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(self.counter), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

                # Stage data
                cv2.putText(image, '', (65,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, self.stage, 
                            (60,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)


                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                         )               

                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()
