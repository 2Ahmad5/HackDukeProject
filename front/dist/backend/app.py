from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from youtube_transcript import YouTubeTranscriptFetcher


app = Flask(__name__)

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
            {"role": "system", "content": "You are a helpful assistant designed to answer questions about a provided reading in user content, along with providing output in a rigorous format so that it can be passed into a front-end. Follow these instructions exactly, without any additional text whatsover: First, give a 1 paragraph summary, followed by a newline. Second, quote statements from the article in user content (and only from user content) verbatim that may be false or misleading. After each quote, explain why you chose to include that quote, and always cite evidence to support your explanation. Seperate all of these with new lines. If there are no misleading quotes in the entire article, say so."},
            {"role": "user", "content": f"{context}"}


        ],
        "return_citations": True
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Debugging information
    print("Status Code:", response.status_code)
    
    try:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        citations = response_json.get('citations', [])
        

        # print("Content:", content)
        # print("Citations:", citations)
        
        return {"content": content, "citations": citations}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

@app.route('/check_article_reliability', methods=['POST'])
def process_article():
    data = request.json
    if 'url' not in data:
        print("ooofuygcjsdb")
        return jsonify({"error": "Missing 'url' field"}), 400

    article_url = data['url']
    result = check_article_reliability(article_url)
   
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

def check_video_reliability(transcript):
    # Request payload
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant designed to answer questions about a provided video transcript, along with providing output in a rigorous format so that it can be passed into a front-end. Follow these instructions exactly, without any additional text whatsoever: First, give a 1 paragraph summary, followed by a newline. Second, quote statements (starting and ending at timestamps) from the transcript verbatim that may be false or misleading. After each quote, explain why you chose to include that quote, and always cite evidence to support your explanation. Separate all of these with new lines. If there are no misleading quotes in the entire transcript, only print N/A after the summary and nothing else."},
            {"role": "user", "content": f"{transcript}"}
        ],
        "return_citations": True
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Debugging information
    print("Status Code:", response.status_code)
    
    try:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        citations = response_json.get('citations', [])
        
        print("Content:", content)
        print("Citations:", citations)
        
        return {"content": content, "citations": citations}  # Return both content and citations
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

@app.route('/check_video_reliability', methods=['POST'])
def process_video():
    data = request.json
    if 'transcript' not in data:
        return jsonify({"error": "Missing 'transcript' field"}), 400

    transcript = data['transcript']
    result = check_video_reliability(transcript)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)