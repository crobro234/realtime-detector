# check.py (필터링 적용 버전)
import os
import sys
from nudenet import NudeDetector
import json

def run_nude_check(image_folder, result_folder="result", interval_sec=5, analysis_start_time=None):
    os.makedirs(result_folder, exist_ok=True)
    detector = NudeDetector()

    valid_ext = ['.jpg', '.jpeg', '.png']
    image_files = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in valid_ext]

    nudity_detected = False  # ✅ 외설 여부 초기화

    # ✅ 외설로 간주할 클래스 정의 (나머지는 무시됨)
    allowed_classes = [
        "FEMALE_GENITALIA_EXPOSED",
        "FEMALE_BREAST_EXPOSED",
        "MALE_GENITALIA_EXPOSED",
        "EXPOSED_BUTTOCKS",
        "EXPOSED_ANUS"
    ]

    for img_name in image_files:
        img_path = os.path.join(image_folder, img_name)
        print(f"\n🔍 [{img_name}] 처리 중...")

        results = detector.detect(img_path)
        filtered = [item for item in results if item["class"] in allowed_classes]

        if filtered:
            nudity_detected = True
            print("❗ 외설 요소 감지됨:")
            for item in filtered:
                print(f" - {item['class']} (score: {item['score']:.2f})")

            # ✅ 검열 이미지 저장
            censored_filename = f"{os.path.splitext(img_name)[0]}_censored.jpg"
            censored_path = os.path.join(result_folder, censored_filename)
            detector.censor(img_path, output_path=censored_path)

            # ✅ 타임스탬프 계산
            frame_index = int(img_name.split('_')[1].split('.')[0])
            timestamp_sec = frame_index * interval_sec

            break  # 첫 외설 감지 시 중단
        else:
            print("✅ 외설 아님 (검열 생략)")

    # ✅ 결과 저장
    with open(os.path.join(result_folder, "report.json"), "w") as f:
        json.dump({
            "nudity_detected": nudity_detected,
            "frame": img_name if nudity_detected else None,
            "timestamp": timestamp_sec if nudity_detected else None,
            "analysis_started": analysis_start_time
        }, f)

    if nudity_detected:
        print("\n⚠️ 외설 감지됨! 경고 알림이 실행됩니다.")
    else:
        print("\n✅ 깨끗한 영상입니다. 외설 없음.")

# ▶ 실행 진입점
if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "frames"
    analysis_start_time = float(sys.argv[2]) if len(sys.argv) > 2 else None
    run_nude_check(folder, analysis_start_time=analysis_start_time)
