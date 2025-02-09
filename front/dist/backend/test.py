import json

test = ```json
{
   "classification": "Somewhat Misleading",
   "summary": The article presents Michel Houellebecq's perspective on Donald Trump as a good president from a non-American viewpoint. Houellebecq argues that Trump's presidency signals a decline in U.S. global influence, which he sees as beneficial for the rest of the world. He praises Trump for his stance on trade and disengagement from global interventions, contrasting him with previous U.S. policies. However, Houellebecq also criticizes Trump's personal behavior, suggesting a more morally upright leader would be preferable. The article reflects Houellebecq's broader critique of global politics and societal values.

   "misleading_quotes": {
       "The Americans are getting off our backs. The Americans are letting us exist.": "This quote might be misleading because it simplifies complex geopolitical dynamics. While Trump's policies may have reduced U.S. interventionism, the U.S. remains a significant global power with ongoing international engagements[1][3].",
       "President Trump seems to me to be one of the best American presidents I’ve ever seen.": "This statement is misleading because it contradicts Houellebecq's own criticisms of Trump's personal behavior and the broader context of Trump's presidency, which has been controversial[3][5]."
   },
   "citations": [1, 3, 5]
}
```

parsed_data = json.loads(data)

# Extract required elements
classification = parsed_data["classification"]
summary = parsed_data["summary"]
misleading_quotes = parsed_data["misleading_quotes"]
citations = [str(citation) for citation in parsed_data["citations"]]  # Convert citations to list of strings

# Print results
print("Classification:", classification)
print("\nSummary:", summary)
print("\nMisleading Quotes:")
for quote, explanation in misleading_quotes.items():
    print(f"- \"{quote}\": {explanation}")
print("\nCitations:", citations)
