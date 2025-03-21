"""

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.msdvetmanual.com/dog-owners')

soup = BeautifulSoup(r.content, 'html.parser')
contents = soup.find('div', class_='Section_leftContent__vp_sT')
links = [a['href'] for a in contents.find_all('a', href=True)]

with open('output.txt', 'w') as file:
    print(links, file=file)
"""

import requests
from bs4 import BeautifulSoup

# Fetch the page
r = requests.get('https://www.msdvetmanual.com/dog-owners')

# Parse the content
soup = BeautifulSoup(r.content, 'html.parser')

# Find the container
contents = soup.find('div', class_='Section_leftContent__vp_sT')
print(contents.prettify())

# Check if contents is found
if contents:
    links = [a['href'] for a in contents.find_all('a', href=True)]
else:
    links = ["No content found"]

# Write to file
with open('output.txt', 'w') as file:
    print(links, file=file)