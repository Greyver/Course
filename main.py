import requests
import locale
from flask import Flask, render_template, request
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_ALL, '')


app = Flask("__name__")


@app.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        from_currency = request.form['from']
        to_currency = request.form['to']
        print(f'Конвертировать из {from_currency} в {to_currency}')
        print({from_currency})
        print(request.form)
        print("Строкой выше")
        # Добавьте код для конвертации валюты здесь
    return render_template("prob.html")


@app.route("/about")
def about():
    return "<h1> Кто я </h1>"


DOL_GRN = 'https://www.google.com/search?q=dollar+to+uah&oq=Doolar+to+u&aqs=chrome.1.69i57j0i10i512l9.14327j1j9&sourceid=chrome&ie=UTF-8'
# получается при помощи my User Agent, защита от ботов
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

full_page = requests.get(DOL_GRN, headers=headers)

soup = BeautifulSoup(full_page.content, 'html.parser')
# выборка нужного тега и информации
convert = soup.find(
    "span", {"class": "DFlfde SwHCTb", "data-precision": "2"})
print(convert.text.replace('.', locale.localeconv()['decimal_point']))

if __name__ == "__main__":
    app.run()
