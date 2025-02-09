// Function to extract URLs from Google search results
const currentUrl = window.location.href;



// Send the URL to the background script
chrome.runtime.sendMessage({ url: currentUrl });
console.log("Current page URL sent:", currentUrl);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "highlight") {
        highlightText(message.text);
    } else if (message.action === "summarize") {
        text = extractPageText();
        (async () => {
            await summarizeText(text, sendResponse);
        })();

        return true;
    }else if (message.action === "youtube_summary"){
        let text = extractVideoId(currentUrl);
        
        if (text) {
            (async () => {
                await getYoutube(text, sendResponse);
            })();
            return true;
        } else {
            console.error("Invalid YouTube URL");
        }
    }
});

function extractVideoId(url) {
    const regex = /(?:v=|\/)([0-9A-Za-z_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

// function highlightText(targetText) {
//     const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    
//     while (walker.nextNode()) {
//         let node = walker.currentNode;
//         if (node.nodeValue.includes(targetText)) {
//             const span = document.createElement("span");
//             span.style.backgroundColor = "yellow";
//             span.style.fontWeight = "bold";
//             span.textContent = targetText;

//             const newText = node.nodeValue.split(targetText);
//             const parent = node.parentNode;

//             if (parent) {
//                 parent.replaceChild(document.createTextNode(newText[0]), node);
//                 parent.insertBefore(span, node.nextSibling);
//                 parent.insertBefore(document.createTextNode(newText[1]), span.nextSibling);
//             }
//         }
//     }
    
// }

async function summarizeText(text, sendResponse){
    try {
        let response = await fetch('http://127.0.0.1:5000/check_reliability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: text })
        });
        if(!response.ok){
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        let data = await response.json();
        console.log("Reliability Check Result:", data);

        sendResponse({ summary: data.result })

    } catch (error) {
        console.error("Error:", error);
        sendResponse({ summary: "Error fetching summary." });

    }
}

async function getYoutube(url, sendResponse) {
    try{
        let response = await fetch('http://127.0.0.1:5000/get_youtube', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ video_id: url })
        });
        if(!response.ok){
            throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        let data = await response.json();
        console.log("Youtube Summary:", data);
        sendResponse({ summary: data.result })

    } catch (error){
        console.error("Error:", error);
        sendResponse({ summary: "Error fetching YouTube summary." });
    }
}


function highlightText(targetText) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);

    while (walker.nextNode()) {
        let node = walker.currentNode;
        if (node.nodeValue.includes(targetText)) {
            let parent = node.parentNode;
            
            // Create highlight span
            let span = document.createElement("span");
            span.style.backgroundColor = "yellow";
            span.style.fontWeight = "bold";
            span.style.position = "relative"; // Needed for tooltip positioning
            span.textContent = targetText;

            // Create tooltip box
            let tooltip = document.createElement("div");
            tooltip.textContent = "Highlighted";
            tooltip.style.position = "absolute";
            tooltip.style.left = "100%"; // Position to the right of the highlight
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)"; // Center it vertically
            tooltip.style.backgroundColor = "black";
            tooltip.style.color = "white";
            tooltip.style.padding = "5px";
            tooltip.style.borderRadius = "5px";
            tooltip.style.fontSize = "12px";
            tooltip.style.whiteSpace = "nowrap";
            tooltip.style.display = "none"; // Initially hidden

            // Show tooltip on hover
            span.addEventListener("mouseenter", () => { tooltip.style.display = "block"; });
            span.addEventListener("mouseleave", () => { tooltip.style.display = "none"; });

            span.appendChild(tooltip);

            // Replace text with highlighted span
            let newText = node.nodeValue.split(targetText);
            parent.replaceChild(document.createTextNode(newText[0]), node);
            parent.insertBefore(span, node.nextSibling);
            parent.insertBefore(document.createTextNode(newText[1]), span.nextSibling);

            console.log("Highlighted first occurrence:", targetText); // Debugging log
            break;
        }
    }
}


function extractPageText() {
    let bodyText = document.body.innerText || document.body.textContent;
    return bodyText.trim();
}

// Listen for a message from popup.js to send extracted text
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "extractText") {
        let pageText = extractPageText();
        console.log("Extracted Page Text:", pageText); // Debugging log
        sendResponse({ text: pageText });
    }
});

// highlightText("Ye");

console.log("Highlighting complete!");