import requests
from bs4 import BeautifulSoup

DOL_GRN = 'https://www.google.com/search?q=dollar+to+uah&oq=Doolar+to+u&aqs=chrome.1.69i57j0i10i512l9.14327j1j9&sourceid=chrome&ie=UTF-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

full_page = requests.get(DOL_GRN, headers=headers)

soup = BeautifulSoup(full_page.content, 'html.parser')

convert = soup.find(
    "span", {"class": "DFlfde SwHCTb", "data-precision": "2"})
print(convert.text.replace('.', ','))
# print(full_page.status_code)
# print(soup.prettify())
