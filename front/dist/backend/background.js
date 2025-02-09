
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

// let storedUrls = [];

// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     if (message.urls) {
//         storedUrls = message.urls;
//         console.log("Received URLs in background.js:", storedUrls);
//     }
//     else{
//         console.log("jdklnfdkvn")
//     }
// });

// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//     if (request.action === "getUrls") {
//         console.log("Popup requested URLs, sending:", storedUrls);
//         sendResponse({ urls: storedUrls });
//     }
  

let currentPageUrl = "";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.url) {
        currentPageUrl = message.url;
        console.log("Stored current page URL:", currentPageUrl); // Debugging log
    }

    if (message.action === "getUrl") {
        console.log("Popup requested current URL:", currentPageUrl); // Debugging log
        sendResponse({ url: currentPageUrl });
    }

    return true; // Keeps sendResponse() alive for async requests
});


