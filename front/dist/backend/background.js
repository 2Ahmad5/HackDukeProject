chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "highlightText",
    title: "Highlight Text",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "highlightText" && info.selectionText) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0].id) {
        chrome.tabs.sendMessage(tabs[0].id, {
          action: "highlight",
          text: info.selectionText,
        });
      }
    });
  }
});
