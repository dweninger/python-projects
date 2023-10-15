import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "http://quotes.toscrape.com/"

# Send HTTP GET request to URL
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse HTML content of webpage using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find and print all content within HTML
    page_text = soup.get_text()
    print(page_text.encode("utf-8").decode("utf-8"))
else:
    print("Failed to retrieve the webpage. "
          "Status code:", response.status_code)
