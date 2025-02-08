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

def check_article_reliability(article_link):
    # Request payload
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant designed to fact check an article in a provided link. In your response, give a media bias/fact check reliability score of the page and a brief summary of the reliability. Be sure to cite 3 outside sources if possible and quote particular statements in the article that are misleading or untrue."},
            {"role": "user", "content": f"How reliable is this article? {article_link}"}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Debugging information
    print("Status Code:", response.status_code)
    # print("Response Text:", response.text)
    
    try:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response"}

# Example usage
article_link = "https://www.bbc.com/news/uk-61585886"
result = check_article_reliability(article_link)
print(result)