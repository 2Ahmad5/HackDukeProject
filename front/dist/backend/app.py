from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from youtube_transcript import YouTubeTranscriptFetcher
import json
import re


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
        print("response_json:", response_json)  # Debug

        content = response_json["choices"][0]["message"]["content"]
        print("Raw content:", content)  

        # Remove JSON code block markers and clean whitespace
        cleaned = content.replace("```json", "").replace("```", "").strip()

        # First, find the summary section
        summary_start = cleaned.find('"summary":') + len('"summary":')
        summary_end = cleaned.find('"misleading_quotes":', summary_start)
        
        if summary_end == -1:  # If misleading_quotes isn't found, try finding the next field
            summary_end = cleaned.find(',"citations":', summary_start)

        if summary_start != -1 and summary_end != -1:
            # Extract the summary content
            summary_content = cleaned[summary_start:summary_end].strip()
            
            # Remove any existing quotes and commas at the end
            summary_content = summary_content.strip('," \n')
            
            # Create the properly formatted summary string with escaped quotes
            summary_string = f'"summary": "{summary_content}",'
            
            # Replace the original summary section with the properly formatted one
            cleaned = cleaned[:summary_start-len('"summary":')] + summary_string + cleaned[summary_end:]

        # Parse the cleaned JSON
        data = json.loads(cleaned)

        # Extract fields
        classification = data.get("classification", "")
        summary = data.get("summary", "")
        misleading_quotes = data.get("misleading_quotes", {})
        citations = data.get("citations", [])

        return classification, summary, misleading_quotes, citations

        # 2) Parse the remaining string as JSON
        structured_response = json.loads(content_str)
        print("structured_response:", structured_response)  # Debug

        top_level_citations = response_json.get("citations", [])
        numeric_citations = structured_response.get("citations", [])

        final_citations = []
        for idx in numeric_citations:
            if 1 <= idx <= len(top_level_citations):
                final_citations.append(top_level_citations[idx - 1])
            else:
                final_citations.append(f"Index {idx} out of range")

        # Replace the numeric array with the actual links
        structured_response["citations"] = final_citations

        classification = structured_response.get("classification", "Unknown")
        summary = structured_response.get("summary", "")
        misleading_quotes = structured_response.get("misleading_quotes", {})
        citations = structured_response.get("citations", [])

        print("testing testing testing")  # Debug

        return {
            "classification": classification,
            "summary": summary,
            "misleading_quotes": misleading_quotes,
            "citations": citations
        }

    except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as e:
        print("JSON Decode Error:", e)  # Debugging
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