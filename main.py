import os

import numpy as np
import cv2
from PIL import Image
from pytesseract import pytesseract


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def apply_ocr(image):
    text = pytesseract.image_to_string(image)
    return text


if __name__ == '__main__':
    video_path = r"videos\mysql.mp4"
    read_video(video_path)
