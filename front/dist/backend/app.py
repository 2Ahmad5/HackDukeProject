from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from youtube_transcript import YouTubeTranscriptFetcher
import json
import re


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

def check_video_reliability(context):
    # Request payload
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": 
                    "You are a helpful assistant designed to analyze the reliability of a given video transcript and provide structured output. "
                    "Follow this format **exactly**, without any additional text or explanation:\n\n"
                    "0. **Classification**: Assign a classification to the video transcript out of Highly Reliable, Somewhat Reliable, Somewhat Misleading, and Unreliable.\n\n"
                    "1. **Summary**: Provide a one-paragraph summary of the video's content. Make sure to make the summary a STRING\n\n"
                    "2. **Misleading Quotes**: Extract several (a lot if necessary) quotes from the video that are potentially misleading or unreliable. Present this as a dictionary where:\n"
                    "   - The **key** is the time and exact quote from the video.\n"
                    "   - The **value** is an explanation of why this quote was flagged, citing evidence where possible.\n\n"
                    "3. **Citations**: Provide an array of sources that support your explanations for why certain quotes may be misleading.\n\n"
                    "Your response **must** be structured **strictly** as follows:\n"
                    "```\n"
                    "{\n"
                    '   "classification": "<Reliability Classification>",\n'
                    '   "summary": "<Summary of the video>",\n'
                    '   "misleading_quotes": {\n'
                    '       "<Time in the video FORMATTED IN MINUTES:SECONDS (convert to minutes if you have to)> <Quote 1>": "<Explanation of why this quote is misleading>",\n'
                    '       "<Time in the video formatted IN MINUTES:SECONDS (convert to minutes if you have to)> <Quote 2>": "<Explanation of why this quote is misleading>"\n'
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
        response_json = response.json()
        print(response_json)
        content = response_json["choices"][0]["message"]["content"]
        citations = response_json.get('citations', [])
        print("Raw content:", content)

        cleaned = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned)

        print(data)

        # Extract fields
        classification = data.get("classification", "")
        summary = data.get("summary", "")
        misleading_quotes = data.get("misleading_quotes", {})
        

        return {
            "classification": classification,
            "summary": summary,
            "misleading_quotes": misleading_quotes,
            "citations": citations
        }

    except (requests.exceptions.JSONDecodeError, json.JSONDecodeError) as e:
        print("JSON Decode Error:", e)  # Debugging
        return {"error": "Invalid JSON response"}
    
def check_manual_text(context):
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": 
                    "You are a helpful assistant designed to answer the prompt inputted to you with a complete degree of accuracy."
                
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
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        citations = response_json.get('citations', [])
        
        print("Content:", content)
        print("Citations:", citations)

        
        return {"content": content, "citations": citations} 
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

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
                    "1. **Summary**: Provide a one-paragraph summary of the article's content. Make sure to make the summary a STRING\n\n"
                    "2. **Misleading Quotes**: Extract several (a lot if necessary) quotes from the article that are potentially misleading or unreliable. Present this as a dictionary where:\n"
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
        response_json = response.json()
        print(response_json)
        content = response_json["choices"][0]["message"]["content"]
        citations = response_json.get('citations', [])
        # print("Raw content:", content)

        cleaned = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned)

        # print(data)

        # Extract fields
        classification = data.get("classification", "")
        summary = data.get("summary", "")
        misleading_quotes = data.get("misleading_quotes", {})
        

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

@app.route('/check_manual', methods=['POST'])
def check_manual():
    data = request.json
    print(data)
    if 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    article_url = data['url']
    result = check_manual_text(article_url)

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
    res = check_video_reliability(result.get_transcript())
    return jsonify({"result": res})

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