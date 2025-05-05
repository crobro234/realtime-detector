chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
  if (details.url.includes("watch")) {
    console.log("🎯 URL에서 watch 감지됨 - content.js 강제 실행 시도");

    chrome.scripting.executeScript({
      target: { tabId: details.tabId },
      files: ["content.js"]
    });
  }
});