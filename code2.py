import requests
from bs4 import BeautifulSoup
import json

base_url = "https://sciencegateways.org/resources/browse"
start_index = 0  # Initial start index for pagination (this corresponds to the first page)

scraped_data = []  # Store all the data here to write it in one go at the end

while True:
    # Construct the URL for the current page with the start parameter
    url = f"{base_url}?view=intro&sortby=date&limit=25&start={start_index}"
    print(f"Scraping page: {url}")
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code: {response.status_code}")
        break
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the resources listed on the page
    public_resources = soup.find_all('li', class_="public")
    
    if not public_resources:
        print("No resources found on this page.")
        break
    
    # Scrape data from the current page
    for resource in public_resources:
        title_tag = resource.find('p', class_='title')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        description_tag = resource.find('p', class_='result-description')
        description = description_tag.get_text(strip=True) if description_tag else "No Description Found"
        
        scraped_data.append({
            'title': title,
            'description': description
        })
    
    # Check if there's a next page (based on the pagination structure)
    next_page_link = soup.find('a', {'title': 'Next'})
    if not next_page_link:
        print("No more pages to scrape.")
        break
    
    # Update start_index for the next page
    start_index += 25  # Increment by 25 for the next page

# Save all scraped data to a JSON file
with open("scraped_data.json", "w", encoding="utf-8") as file:
    json.dump(scraped_data, file, indent=4, ensure_ascii=False)

print("Data saved to scraped_data.json")
