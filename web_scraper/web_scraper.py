import requests

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Website content:")
            print(response.text)
        else:
            print("Failed to retrieve the website. "
                  f"Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

url = input("Enter the URL of the website you want to scrape: ")
scrape_website(url)
