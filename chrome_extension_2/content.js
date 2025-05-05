console.log("✅ content.js 실행됨");

if (!sessionStorage.getItem("yt_warned")) {
  console.log("🎬 YouTube watch 페이지 감지됨. 서버에서 감지 시각 불러오는 중...");

  fetch("http://localhost:5000/status")
    .then(response => response.json())
    .then(data => {
      if (data.nudity_detected && typeof data.timestamp === "number") {
        const delayMs = data.timestamp * 1000;
        console.log(`⚠️ ${data.timestamp}초 후 영상 정지 및 경고창 예정`);

        setTimeout(() => {
          const video = document.querySelector('video');
          if (video) {
            video.pause();
            console.log("⏸️ 영상 일시정지됨");
          } else {
            console.log("❌ 영상 요소를 찾을 수 없음");
          }
          alert("⚠️ Nudity Detected!");
          sessionStorage.setItem("yt_warned", "true");
        }, delayMs);
      } else {
        console.log("✅ 외설 없음 또는 감지 시간 없음. 처리 생략.");
      }
    })
    .catch(err => console.error("❌ 감지 정보 불러오기 실패:", err));
}
