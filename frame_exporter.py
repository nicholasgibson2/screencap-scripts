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


def export_frames(video_path):
    scenes = find_scenes(video_path)

    cap = cv2.VideoCapture(video_path)

    for i, scene in enumerate(scenes):
        cap.set(cv2.CAP_PROP_POS_MSEC, (scene[0].get_seconds() + 0.083) * 1000)
        ret_val, frame = cap.read()
        if ret_val:
            cv2.imwrite(
                f"output_images/scene_{i}_frame.png",
                frame,
                [cv2.IMWRITE_PNG_COMPRESSION, 0],
            )
    cap.release()


if __name__ == "__main__":
    # video_path = "../videos/ve_svideo.MP4"
    video_path = "../videos/okinawa_ld.MP4"
    # video_path = "../videos/okinawa_muse.MP4"
    export_frames(video_path)
