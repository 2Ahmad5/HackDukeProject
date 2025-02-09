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
context = '''Primary Menu
SECTIONS
Search
Email
New York Post
LOG IN
Entertainment
TV
Movies
Music
Celebrities
Awards
Theater
Ticket Sales
Search
SEARCH
TRENDING NOW
Skip to main content
Massive 7.6-magnitude earthquake shakes Caribbean, tsunami...
Trump stripping the security clearances of numerous antagonists...
Trump's press secretary claps back at ‘pitiful’ Dem who...
Beloved retail stores to shut down in US after operator files for...
Trump rules out deporting Prince Harry -- while taking jab at...
Trump reveals plan to 'kill' NYC congestion pricing — here's how
More than 2M doughnut products recalled nationwide over listeria...
These twins followed different diets for 12 weeks. The results...
BREAKING NEWS
Massive 7.6 earthquake shakes Caribbean, tsunami warning issued
ENTERTAINMENT
Cancer-stricken King Charles hangs with David and Victoria Beckham at glitzy food and fashion event organized by Stanely Tucci
By Alexandra Bellusci
Published Feb. 8, 2025, 2:55 p.m. ET
59 Comments
Britain's King Charles III speaks with Helen Mirren.
AP

We wannabe a fly on the wall for this convo.

David and Victoria Beckham were pictured chatting with King Charles on Friday night during a dinner celebrating “Slow Food and Slow Fashion” at Highgrove House in Tetbury, England. 

The monarch, 76, sported a cheeky smile and a drink in his hand while looking dapper in a black suit with a matching black bowtie.

Former footballer David, 49, sported a similar look, while his Spice Girl squeeze, 50, stunned in a white dress and diamond bracelets.

8
King Charles III speaks to David Beckham and Victoria Beckham during a dinner in celebration of Slow Food.
Getty Images

The Italian-themed dinner was organized by Stanley Tucci. Queen Camilla, dressed in royal blue, and Helen Mirren, were also in attendance.

Mirren, 79, wore a dazzling emerald green dress with a matching headband.

King Charles’ night out comes almost a year after Buckingham Palace revealed that he had been diagnosed with cancer and had begun treatment.

8
King Charles III, David Beckham and Victoria Beckham.
Getty Images
8
King Charles III, David Beckham and Victoria Beckham during a dinner at Highgrove House on February 07, 2025 in Tetbury, England.
Getty Images

The cancer was discovered in January after Charles underwent a planned procedure to treat a benign enlarged prostate. 

“I would like to express my most heartfelt thanks for the many messages of support and good wishes I have received in recent days,” the British leader said in a statement at the time. “As all those who have been affected by cancer will know, such kind thoughts are the greatest comfort and encouragement.”

Palace sources confirmed to The Post in December that “his treatment has been moving in a positive direction, and as a managed condition the treatment cycle, will continue into next year.”

8
Queen Camilla (right) talks with Dame Helen Mirren (left) and David Beckham and Victoria Beckham, during a dinner in celebration of Slow Food at King Charles III’s Gloucestershire estate.
Getty Images

That same month, Charles reflected on 2024 after both he and his daughter-in-law Kate Middleton battled the disease.

“All of us go through some form of suffering at some stage in our life, be it mental or physical,” the king said in a pre-taped message at his annual Christmas address. “The degree to which we help one another — and draw support from each other, be we people of faith or of none — is a measure of our civilization as nations.”

“From a personal point of view, I offer special, heartfelt thanks to the selfless doctors and nurses who, this year, have supported me and other members of my family through the uncertainties and anxieties of illness, and have helped provide the strength, care and comfort we have needed.”

8
Hollywood star Stanley Tucci (left) watches as King Charles III and Italian mixologist, Alessandro Palazzi, mix a drink during a dinner in celebration of Slow Food at King Charles III’s Gloucestershire estate, Highgrove Gardens.
Getty Images
8
King Charles III speaks to Dame Helen Mirren.
Getty Images

Last March, the Princess of Wales, 42, announced that she had also been undergoing cancer treatment for about a month.

In September, the royal member shared that she had finished her chemotherapy treatment.

“It is a relief to now be in remission and I remain focused on recovery,” she wrote on Instagram alongside a picture of her sitting with a cancer patient at the hospital.

8
King Charles III during a dinner at Highgrove House on February 07, 2025.
Getty Images
8
David Beckham and Victoria Beckham attend a dinner in celebration of Slow Food.
Getty Images
59

What do you think? Post a comment.

“My heartfelt thanks goes to all those who have quietly walked alongside William and me as we have navigated everything,” the future Queen wrote. “We couldn’t have asked for more. The care and advice we have received throughout my time as a patient has been exceptional.”

“In my new role as Joint Patron of The Royal Marsden, my hope is, that by supporting groundbreaking research and clinical excellence, as well as promoting patient and family wellbeing, we might save many more lives, and transform the experience of all those impacted by cancer.”

FILED UNDER DAVID BECKHAM  KATE MIDDLETON  KING CHARLES III  QUEEN CAMILLA  ROYAL FAMILY  VICTORIA BECKHAM  2/8/25
MORE STORIES
PAGE SIX
Travis Kelce shares bold message amid backlash to pre-Super Bowl date night with Taylor Swift
NYPOST
Massive 7.6-magnitude earthquake shakes Caribbean, tsunami warning issued
Facebook
Twitter
Instagram
LinkedIn
Email
YouTube
SECTIONS & FEATURES
US NEWS
METRO
WORLD NEWS
SPORTS
SPORTS BETTING
BUSINESS
OPINION
ENTERTAINMENT
FASHION & BEAUTY
SHOPPING
LIFESTYLE
REAL ESTATE
MEDIA
TECH
SCIENCE
HEALTH
TRAVEL
ASTROLOGY
VIDEO
PHOTOS
VISUAL STORIES
ALEXA
COVERS
HOROSCOPES
SPORTS ODDS
PODCASTS
CROSSWORDS & GAMES
COLUMNISTS
CLASSIFIEDS
POST SPORTS+
SUBSCRIBE
ARTICLES
MANAGE
NEWSLETTERS & FEEDS
EMAIL NEWSLETTERS
RSS FEEDS
NY POST OFFICIAL STORE
HOME DELIVERY
SUBSCRIBE
MANAGE SUBSCRIPTION
DELIVERY HELP
HELP/SUPPORT
ABOUT NEW YORK POST
CUSTOMER SERVICE
APPS HELP
COMMUNITY GUIDELINES
CONTACT US
TIPS
NEWSROOM
LETTERS TO THE EDITOR
LICENSING & REPRINTS
CAREERS
VULNERABILITY DISCLOSURE PROGRAM
APPS
IPHONE APP
IPAD APP
ANDROID PHONE
ANDROID TABLET
ADVERTISE
MEDIA KIT
CONTACT
© 2025 NYP Holdings, Inc. All Rights Reserved Terms of Use Membership Terms Privacy Notice Sitemap
Your California Privacy Rights'''
result = check_article_reliability(context)