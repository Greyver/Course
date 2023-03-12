import requests
import locale
from flask import Flask, render_template, request
from bs4 import BeautifulSoup


locale.setlocale(locale.LC_ALL, '')


app = Flask("__name__")


usd = {"grn": 'https://www.google.com/search?q=dollar+to+uah&oq=Doolar+to+u&aqs=chrome.1.69i57j0i10i512l9.14327j1j9&sourceid=chrome&ie=aUTF-8',
       "eur": 'https://www.google.com/search?q=usd+to+eur&oq=usd+to+eur&aqs=chrome..69i57j0i512l9.3688j1j9&sourceid=chrome&ie=UTF-8'
       }

grn = {"usd": 'https://www.google.com/search?q=grn+to+usd&oq=grn+t&aqs=chrome.1.69i57j0i512l9.4118j1j9&sourceid=chrome&ie=UTF-8',
       "eur": 'https://www.google.com/search?q=grn+to+euro&oq=grn+to+eur&aqs=chrome.0.0i512j69i57j0i512j0i22i30l7.8054j1j9&sourceid=chrome&ie=UTF-8'
       }

eur = {"usd": 'https://www.google.com/search?q=euro+to+usd&sxsrf=AJOqlzV7AF2cz_umoMmpvfkLuVL14gnknA%3A1678042736982&ei=cOYEZKnOO5W43AP17re4Cw&oq=euro+t&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgBMgQIABBDMgQIABBDMgUIABCABDIICAAQgAQQsQMyBQguEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BgizARCFBDoMCAAQ6gIQtAIQQxgBOg0IABCPARDqAhC0AhgCOg4ILhCABBCxAxDHARDRAzoGCAAQChBDOgcIABCxAxBDOgsILhCABBDHARCvAUoECEEYAFD1TViyc2CqhgFoBHABeACAAckBiAGSCZIBBTAuNi4xmAEAoAEBsAERwAEB2gEECAEYB9oBBggCEAEYCg&sclient=gws-wiz-serp',
       "grn": 'https://www.google.com/search?q=eur+to+grn&oq=eur+to+grn&aqs=chrome..69i57j0i390l2.5553j1j9&sourceid=chrome&ie=UTF-8'
       }


def converts(val1, val2):
    if val1 != val2:
        if val1 == "usd":
            val = usd[val2]
        elif val1 == "grn":
            val = grn[val2]
        elif val1 == "eur":
            val = eur[val2]
    else:
        val = 0
    return val


def facespalm(val):
    if val == 0:
        return "Нет смысла"
    # получается при помощи my User Agent, защита от ботов
    print('меня вызвали')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    full_page = requests.get(val, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')
    # выборка нужного тега и информации
    convert = soup.find(
        "span", {"class": "DFlfde SwHCTb", "data-precision": "2"})
    if convert == None:
        convert = soup.find(
            "span", {"class": "DFlfde SwHCTb", "data-precision": "3"})
    print(convert)
    value = convert.text.replace(
        '.', locale.localeconv()['decimal_point'])
    return value


@app.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        from_currency = request.form['from']
        to_currency = request.form['to']
        currency = facespalm(converts(from_currency, to_currency))
        if request.form["number"] != '':
            number = float(request.form["number"])
            result = number * \
                locale.atof(currency.replace(
                    '.', locale.localeconv()['decimal_point'])) / 1000
            return render_template("index.html", from_currency=currency, result=result)
        else:
            return render_template("index.html", from_currency=facespalm(converts(from_currency, to_currency)))
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
