import requests
import os
from dotenv import load_dotenv

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
        
        print("Content:", content)
        print("Citations:", citations)
        
        return {"content": content, "citations": citations}  # Return both content and citations
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

# Example usage
context = "The moon is made of cheese."
result = check_article_reliability(context)
# print(result)