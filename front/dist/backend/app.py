from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from youtube_transcript import YouTubeTranscriptFetcher


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
            {"role": "system", "content": "You are a helpful assistant designed to answer questions about a provided reading, along with providing output in a rigorous format so that it can be passed into a front-end. Follow these instructions exactly, without any additional text whatsover: First assign a classification to the article out of Highly Reliable, Somewhat Reliable, Somewhat Misleading, and Unreliable. Second, in a new line, give a 1 paragraph summary, followed by a newline. Third, quote statements from the article verbatim that may be false or misleading. After each quote, explain why you chose to include that quote, and always cite evidence to support your explanation. Seperate all of these with new lines. If there are no misleading quotes in the entire article, only print N/A after the summary and nothing else."},
            {"role": "user", "content": f"How reliable is this article? {context}"}
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

@app.route('/check_reliability', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)