import { useState, useEffect } from "react";

function App() {
  const [urls, setUrls] = useState<string[]>([]);
  const [, setSelectedText] = useState("");
  const [highlightText, setHighlightText] = useState("");
  const [extractedText, setExtractedText] = useState(
    "Click the button to extract text."
  );
  const [summary, setSummary] = useState("Click button to get page summary");
  const [ytSummary, setYtSummary] = useState(
    "Click button to get video summary"
  );

  // Fetch URLs from content script
  useEffect(() => {
    if (chrome.runtime) {
      chrome.runtime.sendMessage(
        { action: "getUrl" },
        (response: { url?: string }) => {
          console.log("Popup received current page URL:", response?.url); // Debugging log
          if (response?.url) {
            setUrls([response.url]);
          }
        }
      );
    }
  }, []);

  useEffect(() => {
    chrome.storage.local.get(["selectedText"], (result) => {
      if (result.selectedText) {
        setSelectedText(result.selectedText);
        setHighlightText(result.selectedText); // Use selectedText as input
        // Clear the storage after retrieving
        chrome.storage.local.remove("selectedText");
      }
    });

    chrome.storage.onChanged.addListener((changes) => {
      if (changes.selectedText) {
        setSelectedText(changes.selectedText.newValue);
        setHighlightText(changes.selectedText.newValue); // Use selectedText as input
      }
    });
  }, []);

  // Handle highlight text
  const handleHighlight = () => {
    if (highlightText.trim()) {
      chrome.tabs.query(
        { active: true, currentWindow: true },
        (tabs: chrome.tabs.Tab[]) => {
          if (tabs[0].id) {
            chrome.tabs.sendMessage(tabs[0].id, {
              action: "highlight",
              text: highlightText,
            });
          }
        }
      );
    }
  };

  // Handle text extraction
  const handleExtractText = () => {
    chrome.tabs.query(
      { active: true, currentWindow: true },
      (tabs: chrome.tabs.Tab[]) => {
        if (tabs[0].id) {
          chrome.tabs.sendMessage(
            tabs[0].id,
            { action: "extractText" },
            (response: { text?: string }) => {
              setExtractedText(response?.text || "No text found.");
            }
          );
        }
      }
    );
  };

  // Handle article summarization
  const handleSummarizeArticle = () => {
    chrome.tabs.query(
      { active: true, currentWindow: true },
      (tabs: chrome.tabs.Tab[]) => {
        if (tabs[0].id) {
          chrome.tabs.sendMessage(
            tabs[0].id,
            { action: "summarize" },
            (response: { summary?: string }) => {
              if (chrome.runtime.lastError) {
                console.error("Error:", chrome.runtime.lastError);
                setSummary("Error fetching summary.");
              } else {
                setSummary(response?.summary || "No summary found.");
              }
            }
          );
        }
      }
    );
  };

  // Handle YouTube video summarization
  const handleSummarizeVideo = () => {
    chrome.tabs.query(
      { active: true, currentWindow: true },
      (tabs: chrome.tabs.Tab[]) => {
        if (tabs[0].id) {
          chrome.tabs.sendMessage(
            tabs[0].id,
            { action: "youtube_summary" },
            (response: { summary?: string }) => {
              if (chrome.runtime.lastError) {
                console.error("Error:", chrome.runtime.lastError);
                setYtSummary("Error fetching video summary.");
              } else {
                setYtSummary(response?.summary || "No summary found.");
              }
            }
          );
        }
      }
    );
  };

  return (
    <div>
      <h1>Test Element</h1>
      <div
        style={{
          fontFamily: "Arial, sans-serif",
          padding: "10px",
          width: "300px",
        }}
      >
        <h2>Extracted URLs</h2>
        <ul>
          {urls.length === 0 ? (
            <li>No URLs found</li>
          ) : (
            urls.map((url, index) => (
              <li key={index}>
                <a href={url} target="_blank" rel="noopener noreferrer">
                  {url}
                </a>
              </li>
            ))
          )}
        </ul>

        <input
          type="text"
          placeholder="Enter text to highlight"
          value={highlightText}
          onChange={(e) => setHighlightText(e.target.value)}
          style={{ width: "100%", padding: "5px", marginBottom: "10px" }}
        />
        <button
          onClick={handleHighlight}
          style={{ width: "100%", padding: "10px" }}
        >
          Highlight
        </button>

        <h2>Extract Page Text</h2>
        <button
          onClick={handleExtractText}
          style={{ width: "100%", padding: "10px" }}
        >
          Extract Text
        </button>
        <pre>{extractedText}</pre>

        <button
          onClick={handleSummarizeArticle}
          style={{ width: "100%", padding: "10px" }}
        >
          Click button to get summary
        </button>
        <pre>{summary}</pre>

        <button
          onClick={handleSummarizeVideo}
          style={{ width: "100%", padding: "10px" }}
        >
          Click button to get video summary
        </button>
        <pre>{ytSummary}</pre>
      </div>
    </div>
  );
}

export default App;
