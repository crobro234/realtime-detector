# frame_extractor.py 또는 ytb_server.py 내부 함수로 추가 가능
import cv2
import os


def extract_frames(video_path, output_dir="frames", interval_sec=5):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frame = int(fps * interval_sec)
    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % interval_frame == 0:
            frame_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_idx += 1

    cap.release()
    print(f"✅ 총 {saved_count}개 프레임 추출 완료.")
