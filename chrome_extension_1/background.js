chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.includes("youtube.com/watch")) {
    console.log("유튜브 영상 URL 감지:", changeInfo.url);

    fetch("http://127.0.0.1:5000/receive-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: changeInfo.url })
    })
    .then(res => res.json())
    .then(data => {
      console.log("서버 응답:", data);
    })
    .catch(err => {
      console.error("서버 전송 실패:", err);
    });
  }
});
