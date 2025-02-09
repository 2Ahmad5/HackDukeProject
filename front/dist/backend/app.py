from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

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
            {"role": "system", "content": "You are a helpful assistant designed to fact check an article in a provided link. In your response, give a media bias/fact check reliability score of the page and a brief summary of the reliability. Be sure to cite 3 outside sources if possible and quote particular statements in the article that are misleading or untrue. Do not reword quotations from the article, cite it word for word."},
            {"role": "user", "content": f"How reliable is this article? {context}"}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Debugging information
    print("Status Code:", response.status_code)
    
    try:
        response_json = response.json()
        print(response_json['choices'][0]['message']['content'])
        return response_json['choices'][0]['message']['content']
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

@app.route('/check_reliability', methods=['POST'])
def process_article():
    data = request.json
    if 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    article_url = data['url']
    result = check_article_reliability(article_url)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)