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


def get_timestamps(phrase):
    """
    Given a phrase, returns all timestamps to frames of the video that may contain the phrase, ranked in order of
    likelihood

    :param phrase:
        a string with one or more words
    :return:
        numpy array of timestamps as ints, with the best results first
    """
    timestamp_counts = np.zeros(self.timestamp_num)

    words = phrase.split(" ")
    for word in words:
        timestamp_set = self.word_to_timestamps[word]
        for timestamp in timestamp_set:
            timestamp_counts[timestamp] += 1

    # clever trick - indices of array are equal to their equivalent timestamps
    timestamp_counts = np.argsort(timestamp_counts)
    # reverse array so in descending order
    timestamp_counts = timestamp_counts[::-1]

    return timestamp_counts


if __name__ == '__main__':
    video_path = r"videos\mysql.mp4"
    read_video(video_path)
