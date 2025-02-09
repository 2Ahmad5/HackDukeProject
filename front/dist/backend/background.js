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