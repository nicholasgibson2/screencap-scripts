import cv2
from scenedetect import SceneManager, VideoManager
from scenedetect.detectors import ContentDetector


def find_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    return scene_manager.get_scene_list()


def export_frames(video_dir, video_name):
    video_path = f"{video_dir}/{video_name}"
    scenes = find_scenes(video_path)

    cap = cv2.VideoCapture(video_path)

    for i, scene in enumerate(scenes):
        cap.set(cv2.CAP_PROP_POS_MSEC, (scene[0].get_seconds() + 0.083) * 1000)
        ret_val, frame = cap.read()
        if ret_val:
            cv2.imwrite(
                f"{video_dir}/scene_{i}_frame.png",
                frame,
                [cv2.IMWRITE_PNG_COMPRESSION, 0],
            )
    cap.release()


if __name__ == "__main__":
    # video_path = "videos/ve_svideo.MP4"
    # video_path = "videos/1.MP4"
    video_dir = "../Video Essentials/LD/CLD-R7G/composite/Kramer/480i/VP50/1080p/defaults" 
    video_name = "REC_20230728_171811_655.MP4"
    export_frames(video_dir, video_name)


