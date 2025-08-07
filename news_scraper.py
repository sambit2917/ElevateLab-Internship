from bs4 import BeautifulSoup
import requests

url = 'https://www.bbc.com/news'

# to get the html from the page
page = requests.get(url)
html = page.text

# Using BeautifulSoup to parse the html
soup = BeautifulSoup(html,'html.parser')

# Finding all headline tags
headlines = soup.find_all('h2')
# print(headlines)

# Extract and clean the text from all the headline tags
titles = [headline.get_text(strip=True) for headline in headlines]
# print(titles)

# Save to a file
with open('headlines.txt','w') as file:
    for title in titles:
        file.write(title+'\n')
print("Headlines saved to headlines.txt")