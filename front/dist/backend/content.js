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
        console.log("text:", text);
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
    } else if (message.action === "input_text"){
        let text = message.text;
        console.log(text)
        if(text){
            (async () => {
                await getPersonalText(text, sendResponse);
            })();
            return true;
        } else{
            console.error("no input provvided");
        }
    }
});

function extractVideoId(url) {
    const regex = /(?:v=|\/)([0-9A-Za-z_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

async function getPersonalText(text, sendResponse) {
    console.log(text)
    try {
        let response = await fetch('http://127.0.0.1:5000/check_manual', {
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

        let summary = data.result.content;
        let citations = data.result.citations;

        sendResponse({
            summary: summary,
            citations: citations
        });

    } catch(error){
        console.error("Error:", error);
        sendResponse({
            summary: "Error fetching summary.",
            citations: []
        });
    }
}

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

        let classification = data.result.classification;
        let summary = data.result.summary;
        let citations = data.result.citations;
        let misleadingQuotes = data.result.misleading_quotes;

        for (let quote in misleadingQuotes) {
            highlightText(quote, misleadingQuotes[quote]);
        }

        console.log(misleadingQuotes)
        sendResponse({
            classification: classification,
            summary: summary,
            misleading_quotes: data.result.misleading_quotes,
            citations: citations
        });

    } catch (error) {
        console.error("Error:", error);
        sendResponse({
            classification: "Unknown",
            summary: "Error fetching summary.",
            citations: []
        });
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

        let classification = data.result.classification;
        let summary = data.result.summary;
        let citations = data.result.citations;
        let misleading_quotes = data.result.misleading_quotes;

        console.log("CHEKCING", misleading_quotes)

        sendResponse({
            classification: classification,
            summary: summary,
            citations: citations,
            misleading_quotes: misleading_quotes
        });

    } catch (error){
        console.error("Error:", error);
        sendResponse({ summary: "Error fetching YouTube summary." });
    }
}


function highlightText(targetText, explanation) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);

    while (walker.nextNode()) {
        let node = walker.currentNode;
        if (node.nodeValue.includes(targetText)) {
            let parent = node.parentNode;
            
            // Create highlight span
            let span = document.createElement("span");
            span.style.backgroundColor = "yellow";
            span.style.fontWeight = "bold";
            span.style.position = "relative";
            span.textContent = targetText;

            // Create tooltip box
            let tooltip = document.createElement("div");
            tooltip.textContent = explanation;
            tooltip.style.position = "absolute";
            tooltip.style.left = "105%"; // Slightly offset to the right of the element
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)";
            tooltip.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
            tooltip.style.color = "#fff";
            tooltip.style.padding = "8px";
            tooltip.style.borderRadius = "4px";
            tooltip.style.fontSize = "12px";
            tooltip.style.whiteSpace = "normal";      // Allow wrapping of text
            tooltip.style.width = "250px";           // Limit tooltip width
            tooltip.style.overflowWrap = "break-word";   // Break long words if needed
            tooltip.style.boxShadow = "0 2px 6px rgba(0, 0, 0, 0.2)";
            tooltip.style.zIndex = "1000";        
            tooltip.style.display = "none"; 

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