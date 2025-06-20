import cv2
import pytesseract
import difflib
import os
import nltk
from nltk.corpus import words

# Download word list once
nltk.download("words")
english_vocab = set(words.words())


def extract_text_from_video(video_path, output_dir, start_time=0):
    """
    Extract text from video frames starting at specified time.

    Args:
        video_path (str): Path to the video file
        start_time (float): Start time in seconds (default: 0)
    """

    cap = cv2.VideoCapture(video_path)
    frame_interval = 0.25  # seconds between frames
    frame_num = start_time  # Start from specified time
    last_text = ""
    skip_keywords = ["music television", "new music"]
    # skip_keywords = []

    def is_new_text(text, last_text, threshold=0.9):
        ratio = difflib.SequenceMatcher(None, text.strip(), last_text.strip()).ratio()
        return ratio < threshold

    def contains_real_word(text, min_length=3, min_count=2):
        tokens = [word.lower() for word in text.split()]
        real_words = [
            word for word in tokens if word in english_vocab and len(word) >= min_length
        ]
        return len(real_words) >= min_count
        # return True

    def preprocess_frame(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    custom_config = r"--psm 6"

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_num * 1000)
        success, frame = cap.read()
        if not success:
            break

        prepped = preprocess_frame(frame)
        text = pytesseract.image_to_string(prepped, config=custom_config).strip()

        if text and is_new_text(text, last_text):
            lowered = text.lower()
            if not any(k in lowered for k in skip_keywords) and contains_real_word(
                text
            ):
                print(f'Time: {frame_num:.2f}s\n{text}\n{"-"*40}')
                cv2.imwrite(f"{output_dir}/frame_{int(frame_num*1000):07}.png", frame)
                last_text = text

        frame_num += frame_interval

    cap.release()


# Usage examples:
if __name__ == "__main__":
    video_path = "./mtv_4.mp4"
    output_dir = "./frames_with_text"
    extract_text_from_video(video_path, output_dir)
