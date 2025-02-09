// chrome.runtime.sendMessage({ action: "getUrls" }, response => {
//     console.log("kjfvndknv")
//     const urlList = document.getElementById("urlList");
//     if (response.urls.length === 0) {
//         urlList.innerHTML = "<li>No URLs found</li>";
//     } else {
//         response.urls.forEach(url => {
//             let li = document.createElement("li");
//             let a = document.createElement("a");
//             a.href = url;
//             a.textContent = url;
//             a.target = "_blank";
//             li.appendChild(a);
//             urlList.appendChild(li);
//         });
//     }
// });

chrome.runtime.sendMessage({ action: "getUrl" }, response => {
    console.log("Popup received current page URL:", response.url); // Debugging log
    const urlList = document.getElementById("urlList");

    if (!response || !response.url) {
        urlList.innerHTML = "<li>No URL found</li>";
        console.log("No URL received in popup.");
        return;
    }

    let li = document.createElement("li");
    let a = document.createElement("a");
    a.href = response.url;
    a.textContent = response.url;
    a.target = "_blank";
    li.appendChild(a);
    urlList.appendChild(li);

    console.log("Current page URL displayed in popup.");
});

document.getElementById("highlightButton").addEventListener("click", () => {
    let userText = document.getElementById("highlightInput").value.trim();
    


    if (userText) {
       
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, { action: "highlight", text: userText });
        });
    }
});

document.getElementById("summarizeArticle").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "summarize" }, (response) => {
            if (chrome.runtime.lastError) {
                console.error("Error:", chrome.runtime.lastError);
                document.getElementById("summary").textContent = chrome.runtime.lastError;
                return;
            }

            if (response && response.summary) {
                document.getElementById("summary").textContent = response.summary;
            } else {
                document.getElementById("summary").textContent = "No summary found.";
            }
        });
    });
});

document.getElementById("summarizeVideo").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "youtube_summary" }, (response) => {
            console.log("Testong out")
            if (chrome.runtime.lastError) {
                console.error("Error:", chrome.runtime.lastError);
                document.getElementById("ytsummary").textContent = chrome.runtime.lastError;
                return;
            }

            if (response && response.summary) {
                document.getElementById("ytsummary").textContent = response.summary;
            } else {
                document.getElementById("ytsummary").textContent = "No summary found.";
            }
        });
    });
});

document.getElementById("extractTextButton").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "extractText" }, (response) => {
            if (response && response.text) {
                document.getElementById("pageText").textContent = response.text;
            } else {
                document.getElementById("pageText").textContent = "No text found.";
            }
        });
    });
});

