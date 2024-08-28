import requests
from dotenv import load_dotenv
import os
import json
# Load environment variables from the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')


def get_esv_text(passage):
    url = 'https://api.esv.org/v3/passage/html/'

    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-footnote-body': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False,
        'include-crossrefs': True,
        'crossref-url' : True,
    }

    headers = {
        'Authorization': 'Token %s' % api_key
    }

    

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            verse = response
            return verse
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def main():
    js = get_esv_text("Genesis 1")

    if js:
        json_object = json.loads(js.text)

        json_formatted_str = json.dumps(json_object, indent=1)

        print(json_formatted_str)
    else:
        print('Failed to fetch text from API.')

if __name__ == '__main__':
    main()