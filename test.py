import json
from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv
import os
import requests

from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text content from paragraphs
    paragraphs = soup.find_all('p')
    text_content = ' '.join([p.get_text() for p in paragraphs])
    return text_content

# Load the JSON file
with open('gdp_articles.json', 'r') as file:
    data = json.load(file)

top_stories = data['topStories']
story_content = {}
for story in top_stories:
    url = story['link']
    text = extract_text_from_url(url)
    story_content[f"{story['title']}_{story['source']}"] = text
    
breakpoint()

url = 'https://www2.deloitte.com/us/en/insights/economy/global-economic-outlook-2025.html'
text = extract_text_from_url(url)
breakpoint()
print(text)