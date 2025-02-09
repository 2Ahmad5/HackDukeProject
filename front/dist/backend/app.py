from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from youtube_transcript import YouTubeTranscriptFetcher
import json


app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Set your API key
api_key = os.getenv("PERPLEXITY_API_KEY")

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

# Request headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def check_article_reliability(context):
    # Request payload
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": 
                    "You are a helpful assistant designed to analyze the reliability of a given article and provide structured output. "
                    "Follow this format **exactly**, without any additional text or explanation:\n\n"
                    "0. **Classification**: Assign a classification to the article out of Highly Reliable, Somewhat Reliable, Somewhat Misleading, and Unreliable.\n\n"
                    "1. **Summary**: Provide a one-paragraph summary of the article's content.\n\n"
                    "2. **Misleading Quotes**: Extract quotes from the article that are potentially misleading or unreliable. Present this as a dictionary where:\n"
                    "   - The **key** is the exact quote from the article.\n"
                    "   - The **value** is an explanation of why this quote was flagged, citing evidence where possible.\n\n"
                    "3. **Citations**: Provide an array of sources that support your explanations for why certain quotes may be misleading.\n\n"
                    "Your response **must** be structured **strictly** as follows:\n"
                    "```\n"
                    "{\n"
                    '   "classification": "<Reliability Classification>",\n'
                    '   "summary": "<Summary of the article>",\n'
                    '   "misleading_quotes": {\n'
                    '       "<Quote 1>": "<Explanation of why this quote is misleading>",\n'
                    '       "<Quote 2>": "<Explanation of why this quote is misleading>"\n'
                    "   },\n"
                    "}\n"
                    "```\n"
                    "If there are no misleading quotes, return an empty dictionary for 'misleading_quotes'. If no citations are available, return an empty list for 'citations'.\n"
                    "Do not include any other text or commentary outside of this format."
                
            },
            {
                "role": "user",
                "content": f"Analyze the reliability of this article and structure your response as instructed: {context}"
            }
        ],
        "return_citations": True
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Debugging information
    print("Status Code:", response.status_code)

    try:
        # Parse JSON response
        response_json = response.json()

        print("response_json:", response_json)  # Debugging
        
        # Extract structured content
        content = response_json['choices'][0]['message']['content']
        
        print("content:", content)  # Debugging
        
        # Directly use content as a dictionary, no need for json.loads()
        structured_response = content

        print("structured_response:", structured_response)  # Debugging

        # Ensure correct keys exist in response
        classification = structured_response.get("classification", "Unknown")
        summary = structured_response.get("summary", "")
        misleading_quotes = structured_response.get("misleading_quotes", {})
        citations = structured_response.get("citations", [])

        print("testing testing testing")  # Debugging

        return {
            "classification": classification,
            "summary": summary,
            "misleading_quotes": misleading_quotes,
            "citations": citations
        }
    
    except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as e:
        print("JSON Decode Error:", e)  # Debugging error message
        return {"error": "Invalid JSON response"}


@app.route('/check_reliability', methods=['POST'])
def process_article():
    data = request.json
    if 'url' not in data:
        print("ooofuygcjsdb")
        return jsonify({"error": "Missing 'url' field"}), 400

    article_url = data['url']
    result = check_article_reliability(article_url)

    print(result)
   
    return jsonify({"result": result})

@app.route('/get_youtube', methods=['POST'])
def process_youtube():
    data = request.json

    if 'video_id' not in data:
        return jsonify({"error": "Missing 'video_id' field"}), 400

    video_id = data['video_id']
    result = YouTubeTranscriptFetcher(video_id)
    print(result.get_transcript())
    return jsonify({"result": result.get_transcript()})

if __name__ == '__main__':
    app.run(debug=True)