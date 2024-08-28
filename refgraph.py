import requests
from dotenv import load_dotenv
import os
import json
import re
import csv
import sqlite3
# Load environment variables from the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

def update_data(list):
    


def parse_passage(passage):
    #passage is a str
    print(passage)
    exp = 'href="[^"]+"'
    raws = re.findall(exp, passage)
    refs = []
    for raw in raws:
        raw = raw.lstrip('href="')
        raw = raw.rstrip('/"')
        individuals = raw.split('; ')
        refs += individuals
    
    splitrefs = []
    for ref in refs:
        temp,v = ref.split(':')
        a = temp.split(' ')
        if(len(a) == 3):
            a = [a[0] + ' ' + a[1], a[2]]
        splitrefs.append((a[0], a[1], v))
        
    return splitrefs

def get_esv_text(passage):
    url = 'https://api.esv.org/v3/passage/html/'

    params = {
        'q': passage,
        'include-headings': False,
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

    with open('Bible.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='')
        for row in spamreader:
            book = row[2]
            numchaps = row[3]
            for i in range(numchaps):
                chap = str(i+1)
                js = get_esv_text(book + " " + chap)

                if js:
                    #update data things

                    parsedlist = parse_passage(str(js.json()['passages'][0]))
                    update_data(parsedlist)
                    #print(parsedlist)
                else:
                    print('Failed to fetch text from API.')

if __name__ == '__main__':
    main()