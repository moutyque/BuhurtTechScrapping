# This is a sample Python script.
from dataclasses import dataclass

import requests as requests
from bs4 import BeautifulSoup, Tag
import re


@dataclass()
class Item:
    name: str = ""
    url: str = ""
    weight: str = ""
    length: str = ""


found_items = list()


def process(url):
    r = requests.get(url)
    r.raise_for_status()
    # Parsing the HTML
    page = BeautifulSoup(r.content, 'html.parser')
    # print(page)

    links = {link['href'] for link in page.find_all('a') if
             link['href'].startswith("https://www.buhurttech.com/product-page")}
    # print(links)
    for link in links:
        r = requests.get(link)
        r.raise_for_status()
        page = BeautifulSoup(r.content, 'html.parser')
        infos: list[Tag] = page.find_all("li")
        infos = [item for item in infos if str(item.contents[0]).startswith("<") == False]
        item = Item()
        for info in infos:
            fetchWeight(info, item)
            fetchLength(info, item)

        item.url = link
        found_items.append(item)


def fetch(info, reg):
    return re.search(reg, str(info.getText()), re.IGNORECASE)


def fetchLength(info, item):
    x = fetch(info, "Total\sLength(.*)cm")
    if x:
        item.length = x.group(1).strip()
        return
    x = fetch(info, "Total Length(.*)cm")
    if x:
        item.length = x.group(1).strip()
        return


def fetchWeight(info, item):
    x = fetch(info, "Total Weight\s(.*)\skg")
    if x:
        item.weight += x.group(1)
        return
    x = fetch(info, "Total Weight (.*) kg")
    if x:
        item.weight += x.group(1)
        return

    x = fetch(info, "Weight\s(.*)\skg")
    if x and item.weight == '':
        item.weight += x.group(1)
        return
    x = fetch(info, "Weight (.*) kg")
    if x and item.weight == '':
        item.weight += x.group(1)
        return


if __name__ == '__main__':
    base_uri = "https://www.buhurttech.com"
    process(f'{base_uri}/two-handed-axes?page=10')
    process(f'{base_uri}/halberds?page=10')
    process(f'{base_uri}/poleaxes?page=10')
    print(*found_items, sep="\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
