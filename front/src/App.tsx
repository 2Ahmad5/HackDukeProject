import { useState} from "react";
import logo from './logo.png';

function App() {
  // const [urls, setUrls] = useState<string[]>([]);
  // const [highlightText, setHighlightText] = useState("");
  // const [extractedText, setExtractedText] = useState("Click the button to extract text.");
  // const [summary, setSummary] = useState("Click button to get page summary");
  // const [ytSummary, setYtSummary] = useState("Click button to get video summary");
  const [activeTab, setActiveTab] = useState("home")
  const [inputText, setInputText] = useState("");
  const [inputData, setInputData] = useState({
    summary: "",
    citations: [],
  });
  const [articleData, setArticleData] = useState({
    classification: "",
    summary: "",
    citations: [],
    misleadingQuotes: {} as Record<string, string>,
  });
  const [videoData, setVideoData] = useState({
    classification: "",
    summary: "",
    citations: [],
    misleadingQuotes: {} as Record<string, string>,
  });
  // const [outputText, setOutputText] = useState("");

  const handleSubmitInput = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      console.log("TEXKJNFKBF:", inputText)
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(
          tabs[0].id,
          
          { action: "input_text", text: inputText },
          (response) => {
            if (chrome.runtime.lastError) {
              console.error("Error:", chrome.runtime.lastError);
              // Optionally, you can display an error message
              setInputData({
                summary: "Error fetching summary.",
                citations: [],
              });
            } else {
              // Assume that the response returns an object with
              // a summary and citations property
              setInputData({
                summary: response?.summary || "No summary found.",
                citations: response?.citations || [],
              });
            }
            // Open the new tab to display the results
            setActiveTab("input");
          }
        );
      }
    });
  };

    const handleSummarizeArticle = () => {
      setActiveTab("article");
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]?.id) {
          chrome.tabs.sendMessage(
            tabs[0].id,
            { action: "summarize" },
            (response) => {
              console.log("respoesinesofns", response)
              if (chrome.runtime.lastError) {
                console.error("Error:", chrome.runtime.lastError);
                setArticleData({
                  classification: "Error",
                  summary: "Error fetching summary.",
                  citations: [],
                  misleadingQuotes: {},
                });
              } else {
                
                setArticleData({
                  classification: response?.classification || "Unknown",
                  summary: response?.summary || "No summary found.",
                  citations: response?.citations || [],
                  misleadingQuotes: response?.misleading_quotes || {},
                });
              }
            }
          );
        }
      });
    };


  const handleSummarizeVideo = () => {
    setActiveTab("video");
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(
          tabs[0].id,
          { action: "youtube_summary" },
          (response) => {
            if (chrome.runtime.lastError) {
              console.error("Error:", chrome.runtime.lastError);
              setVideoData({
                classification: "Error",
                summary: "Error fetching video summary.",
                citations: [],
                misleadingQuotes: {},
              });
            } else {
              setVideoData({
                classification: response?.classification || "Unknown",
                summary: response?.summary || "No summary found.",
                citations: response?.citations || [],
                misleadingQuotes: response?.misleading_quotes || {},
              });
            }
          }
        );
      }
    });
  };


  return (
 
<div className="extension-container">
      {/* Header with logo and product info */}
      <header className="header">
        <img src={logo} alt="Logo" className="logo" />;
        <div className="product-info">
          <h1 className="product-name">TruthGuard</h1>
          <p className="product-description">
            TruthGuard is an extension that allows users to input questions, analyze articles, and analyze youtube videos for reliability and up-to-date fact checking.
          </p>
        </div>
      </header>

      {/* Home Tab */}
      {activeTab === "home" && (
        <div className="home-tab">
          <div className="input-section">
            <input
              type="text"
              placeholder="Enter text or URL here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="text-input"
            />
            <button onClick={handleSubmitInput} className="submit-button">
              Submit
            </button>
          </div>
          <div className="action-buttons">
            <button
              onClick={handleSummarizeArticle}
              className="action-button"
            >
              Check Article
            </button>
            <button
              onClick={handleSummarizeVideo}
              className="action-button"
            >
              Check YouTube Video
            </button>
          </div>
        </div>
      )}

            {/* Input Summary Tab */}
            {activeTab === "input" && (
        <div className="result-tab">
          <button onClick={() => setActiveTab("home")} className="back-button">
            ← Back
          </button>
          <h2>Input Summary</h2>
          <div className="result-content">
            <div className="result-section">
              <h3>Summary</h3>
              <p>{inputData.summary}</p>
            </div>
            <div className="result-section">
              <h3>Citations</h3>
              {inputData.citations.length > 0 ? (
                <div className="citation-cards">
                  {inputData.citations.map((citation, index) => (
                    <div key={index} className="citation-card">
                      <span role="img" aria-label="citation">
                        🔗
                      </span>{" "}
                      {citation}
                    </div>
                  ))}
                </div>
              ) : (
                <p>(No citations available)</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Article Summary Tab */}
      {activeTab === "article" && (
        <div className="result-tab">
          <button
            onClick={() => setActiveTab("home")}
            className="back-button"
          >
            ← Back
          </button>
          <h2>Article Summary</h2>
          <div className="result-content">
            <div className="result-section">
              <h3>Classification</h3>
              <p>{articleData.classification}</p>
            </div>
            <div className="result-section">
              <h3>Summary</h3>
              <p>{articleData.summary}</p>
            </div>
            <div className="result-section">
              <h3>Misleading Quotes</h3>
              {Object.keys(articleData.misleadingQuotes).length > 0 ? (
                <ul>
                  {(Object.entries(
                    articleData.misleadingQuotes
                  ) as [string, string][]).map(
                    ([timestamp, explanation], index) => (
                      <li key={index}>
                        <strong>{timestamp}</strong>: {explanation}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>(No misleading quotes identified)</p>
              )}
            </div>
            <div className="result-section">
              
              <h3>Citations</h3>
              {articleData.citations.length > 0 ? (
                <div className="citation-cards">
                  {articleData.citations.map((citation, index) => (
                    <div key={index} className="citation-card">
                      <span role="img" aria-label="citation">
                        🔗
                      </span>{" "}
                      {citation}
                    </div>
                  ))}
                </div>
              ) : (
                <p>(No citations available)</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Video Summary Tab */}
      {activeTab === "video" && (
        <div className="result-tab">
          <button
            onClick={() => setActiveTab("home")}
            className="back-button"
          >
            ← Back
          </button>
          <h2>Video Summary</h2>
          <div className="result-content">
            <div className="result-section">
              <h3>Classification</h3>
              <p>{videoData.classification}</p>
            </div>
            <div className="result-section">
              <h3>Summary</h3>
              <p>{videoData.summary}</p>
            </div>
            <div className="result-section">
              <h3>Misleading Quotes</h3>
              {Object.keys(videoData.misleadingQuotes).length > 0 ? (
                <ul>
                  {(Object.entries(
                    videoData.misleadingQuotes
                  ) as [string, string][]).map(
                    ([timestamp, explanation], index) => (
                      <li key={index}>
                        <strong>{timestamp}</strong>: {explanation}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>(No misleading quotes identified)</p>
              )}
            </div>
            <div className="result-section">
              <h3>Citations</h3>
              {videoData.citations.length > 0 ? (
                <div className="citation-cards">
                  {videoData.citations.map((citation, index) => (
                    <div key={index} className="citation-card">
                      <span role="img" aria-label="citation">
                        🔗
                      </span>{" "}
                      {citation}
                    </div>
                  ))}
                </div>
              ) : (
                <p>(No citations available)</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
