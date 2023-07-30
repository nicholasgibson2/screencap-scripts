import cv2
import subprocess
from scenedetect import SceneManager, VideoManager
from scenedetect.detectors import ContentDetector


def extract_subclip_ffmpeg(video_path, start_time, end_time, output_path):
    command = [
        "ffmpeg",
        "-ss",
        str(start_time),
        "-i",
        video_path,
        "-t",
        str(end_time - start_time),
        "-map",
        "0:v",
        "-map",
        "0:a",
        "-c",
        "copy",
        "-y",
        output_path,
    ]
    subprocess.check_output(command)


def find_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    return scene_manager.get_scene_list()


def trim_scenes(video_path, front_clips_to_remove, end_clips_to_remove, output_path):
    scenes = find_scenes(video_path)

    start_time = scenes[front_clips_to_remove][0].get_seconds()
    end_time = scenes[-end_clips_to_remove - 1][1].get_seconds()

    extract_subclip_ffmpeg(video_path, start_time, end_time, output_path)

    cap = cv2.VideoCapture(output_path)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frames / fps
    cap.release()

    print(f"Output written to {output_path}, duration: {duration} seconds")


if __name__ == "__main__":
    video_path = "videos/ve_svideo.MP4"
    output_path = "output.MP4"

    front_clips_to_remove = int(input("Enter the number of front clips to remove: "))
    end_clips_to_remove = int(input("Enter the number of end clips to remove: "))

    trim_scenes(video_path, front_clips_to_remove, end_clips_to_remove, output_path)
