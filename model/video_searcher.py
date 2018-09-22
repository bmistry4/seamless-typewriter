import math
import re
import string
from collections import defaultdict

import cv2
import numpy as np
from pytesseract import pytesseract


class VideoSearcher:
    """This class provides the data structures used to index and search for text in a video"""

    def __init__(self, video_path):
        self.video_path = video_path  # File path to video
        self.word_to_timestamps = defaultdict(set)  # word -> set of ts values (ints)
        self.timestamp_to_sentence = {}  # Keep track of full text relating to a timestamp

        self.timestamp_num = 0  # initial value of total number of timestamps
        self.video_length = 0   # initial value of length of video in seconds

        self.populate_timestamp_structures(3)

    def populate_timestamp_structures(self, sampling_rate):
        """
        For all frames in the video withing the sampling rate, get the text from the video and update the timestamp
        dicts
        :param sampling_rate:
            The rate (seconds) at which to process a frame
        :return:
            None
        """
        cap = cv2.VideoCapture(self.video_path)
        # frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        previous_timestamp = 0  # Last added timestamp to the timestamp dicts
        regex = re.compile('[%s]' % re.escape(string.punctuation))

        while cap.isOpened():
            frame_exists, frame = cap.read()

            if not frame_exists:
                self.video_length = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                break

            # Timestamp in ms for the frame relative to the start of the video
            current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            # Convert to seconds 0.d.p
            current_timestamp = math.floor(current_timestamp / 1000)

            time_diff = current_timestamp - previous_timestamp
            # Only process if within the given sampling rate
            if time_diff >= sampling_rate:

                text = self.apply_ocr(frame)
                self.timestamp_to_sentence[current_timestamp] = text.lower()

                # Split on new line and white spaces
                words = re.split("\n|\\s", text)

                # Populate the word-timestamp dicts
                for w in words:
                    w = regex.sub('', w.lower())
                    if w != "":
                        self.word_to_timestamps[w].add(current_timestamp)

                previous_timestamp = current_timestamp

        self.timestamp_num = current_timestamp

        cap.release()
        cv2.destroyAllWindows()

    def timestamp_index_to_seconds(self, index):
        """
        Converts a timestamp index to its corresponding time in the video in seconds

        :param index:
            integer representing the timestamp index
        :return:
            integer representing the seconds in the video specified by the timestamp index
        """
        return math.floor(self.video_length * index / self.timestamp_num)

    @staticmethod
    def apply_ocr(image):
        """
        Given a frame, apply ocr and return the text
        :param image:
            Frame
        :return:
            Extracted text from the image
        """
        text = pytesseract.image_to_string(image)
        return text

    def get_timestamps(self, phrase):
        """
        Given a phrase, returns all timestamps to frames of the video that may contain the phrase, ranked in order of
        likelihood

        :param phrase:
            a string with one or more words
        :return:
            numpy array of timestamps as ints, with the best results first
        """
        timestamp_counts = np.zeros(self.timestamp_num)
        timestamp_set = set()

        words = phrase.split()
        for word in words:
            timestamp_set = self.word_to_timestamps[word]
            for timestamp in timestamp_set:
                timestamp_counts[timestamp] += 1

        num_results = len(timestamp_set)
        if num_results == 0:
            return None

        # clever trick - indices of array are equal to their equivalent timestamps
        timestamp_counts = np.argsort(timestamp_counts)
        # reverse array so in descending order
        timestamp_counts = timestamp_counts[::-1]

        # don't include timestamps that had no results
        timestamp_counts = timestamp_counts[:num_results]

        return timestamp_counts

    def get_text(self, timestamp):
        """
        Return text found at the given timestamp
        :param timestamp: one of the possible occurance/s (in seconds) of the searched term
        :return: the string of text relating to the value
        """
        return self.timestamp_to_sentence[timestamp]
