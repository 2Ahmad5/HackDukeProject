# HackDukeProject: TruthGuard Chrome Extension
This project is a Chrome extension designed to assess the reliability of online articles and YouTube videos.  It leverages the Perplexity AI API to analyze content and provide summaries, classifications, and citations.

<div align="center">
<img src="https://github.com/2Ahmad5/HackDukeProject/blob/main/front/public/image-1739131814003.png?raw=true" alt="image-1739131814003.png" />
</div>


## Features
* **Article Reliability Check:** Analyzes articles to determine their reliability, providing a classification (Highly Reliable, Somewhat Reliable, Somewhat Misleading, Unreliable), a summary, and citations.
* **YouTube Video Reliability Check:** Analyzes YouTube video transcripts (obtained via the `youtube-transcript-api`) to provide a similar reliability assessment, including summaries and citations.  Identifies potentially misleading quotes with explanations and timestamps.
* **Text Input Analysis:** Allows users to input text directly for reliability analysis.
* **Highlighting:** Highlights potentially misleading quotes within the article or video for the user.
* **Context Menu Integration:** Right-click context menu option to highlight selected text.
* **User Interface:** Clean and intuitive user interface built with React, TypeScript, and Vite.  Includes a history of previously analyzed content.

## Usage
1. Install the Chrome extension (see Installation section below).
2. Navigate to an article or YouTube video.
3. Use the extension's interface to submit the article URL or YouTube video ID for analysis.  Alternatively, you can input text directly.
4. View the results, including classification, summary, misleading quotes (with explanations), and citations.

## Installation
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the `front` directory: `cd front`
3. Install dependencies: `npm install`
4. Build the project: `npm run build`
5. Load the unpacked extension in Chrome:
    * Open Chrome extensions page (`chrome://extensions`).
    * Enable "Developer mode" in the top right corner.
    * Click "Load unpacked".
    * Select the `front/dist` directory.

## Technologies Used
* **Frontend:**
    * **React:** JavaScript library for building user interfaces.
    * **TypeScript:** Superset of JavaScript that adds static typing.
    * **Vite:** Fast build tool for frontend development.
    * **React Router DOM:** Routing library for React applications.
    * **Styled Components:** CSS-in-JS library for styling React components.
    * **Bootstrap:**  CSS framework for responsive design.


* **Backend:**
    * **Python (Flask):**  Framework for building web applications.
    * **Perplexity AI API:** API for accessing large language models for text analysis and summarization.
    * **requests:** Python library for making HTTP requests.
    * **dotenv:** Python library for loading environment variables from a `.env` file.
    * **youtube-transcript-api:** Python library for retrieving YouTube video transcripts.

* **Other:**
    * **Chrome Extension API:** Used for interacting with the Chrome browser.

## API Documentation
The backend Flask application provides several API endpoints:

* `/check_reliability`: POST request to analyze an article URL.
    * **Request Body:** `{"url": "<article_url>"}`
    * **Response:**  `{"result": {"classification": "...", "summary": "...", "misleading_quotes": {...}, "citations": [...]}}`
* `/check_manual`: POST request to analyze text input.
    * **Request Body:** `{"url": "<text>"}`
    * **Response:** `{"result": {"content": "...", "citations": [...]}}`
* `/get_youtube`: POST request to analyze a YouTube video ID.
    * **Request Body:** `{"video_id": "<video_id>"}`
    * **Response:**  `{"result": {"classification": "...", "summary": "...", "misleading_quotes": {...}, "citations": [...]}}`
* `/check_video_reliability`: POST request to analyze a provided YouTube video transcript.
    * **Request Body:** `{"transcript": ["<timestamp> <text>", ... ]}`
    * **Response:** `{"result": {"content": "...", "citations": [...]}}`

## Dependencies
The project uses several npm packages (listed in `front/package.json`) and Python libraries (listed in `requirements.txt` if you create one, otherwise just list them here).  Make sure to install them before running the project.

*README.md was made with [Etchr](https://etchr.dev)*