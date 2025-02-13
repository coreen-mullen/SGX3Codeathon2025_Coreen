import requests
from bs4 import BeautifulSoup
import json
url = "https://sciencegateways.org/resources/browse"

response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to retrieve page with status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

public_resources = soup.find_all('li', class_="public")

if not public_resources:
    print("No resources found with class 'public'")
    exit()

with open("scraped_data.json", "w", encoding="utf-8") as file:
    for resource in public_resources:
        title_tag = resource.find('p', class_='title')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        description_tag = resource.find('p', class_='result-description')
        description = description_tag.get_text(strip=True) if description_tag else "No Description Found"
        
        file.write(f"Title: {title}\n")
        file.write(f"Result Description: {description}\n")
        file.write("\n")

print("Data saved to scraped_data.json")
