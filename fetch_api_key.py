import requests
from bs4 import BeautifulSoup

def fetch_api():
    # Specify the URL of the API documentation page
    url = 'http://127.0.0.1:8000/api_docs'  # Replace with the actual URL

    try:
        # Send an HTTP GET request to the page
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Search for the API key (modify this based on the actual HTML structure)
            api_key = soup.find('code').get_text()
            if api_key:
                return api_key
            else:
                print('API Key not found on the page.')

        else:
            print(f'Failed to fetch the page (HTTP Status Code: {response.status_code})')

    except Exception as e:
        print(f'An error occurred: {str(e)}')
