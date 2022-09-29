from datetime import datetime
from math import acos, degrees

import cv2
import mediapipe as mp
import numpy as np
from conecction_db import insert_serie

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Principal:
    def __init__(self, usuario) -> None:
        self.cap = cv2.VideoCapture("ejercicio.mp4")
        # self.cap = cv2.VideoCapture(0)

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
                print(time_2.second - time_1.second)
                if time_2.second - time_1.second > 10:
                    # cliente, inicio, cantidad, fin
                    insert_serie(self.usuario, time_1, self.count, time_2)
                    cv2.destroyAllWindows()
                    return False
                    # break
                # with mp_pose.Pose(
                #    static_image_mode=False) as pose:
                #
                #    while True:
                ret, frame = self.cap.read()
                if not ret:  # if ret == False:
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
