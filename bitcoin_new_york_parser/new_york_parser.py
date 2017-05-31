import time

import pandas as pd
from bs4 import BeautifulSoup
import requests
# from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor as Pool
import json

from numpy import unicode


def get_object_page(url):
    """Return BeautifulSoup object by given url.
    """
    try:
        html_page = requests.get(url)
    except Exception:
        time.sleep(3)
        try:
            html_page = requests.get(url)
        except Exception:
            return ""

    return BeautifulSoup(html_page.content, 'html.parser')


def read_html(html_file):
    with open(html_file) as fp:
        return BeautifulSoup(fp, 'html.parser')


def parse_article_page(href):
    print(href)
    page = get_object_page(href)
    try:
        name = page.find("h1", {"class": "headline"}).text
        total_text = ""
        texts = page.find_all("div", {"class": "story-body"})
        for text in texts:
            datas = text.find_all("p")[:-4]
            for data in datas:
                try:
                    print(type(data.text))
                    total_text += (data.text + "\n")
                except ValueError:
                    pass
                except AttributeError:
                    pass
    except AttributeError:
        name = ""
        total_text = ""
    return {
        "name": name,
        "text": total_text,
    }


def main():
    a = read_html("Bitcoin - The New York Times.html")
    links = a.find_all("a", {"class": "story-link"})
    links = [href.attrs["href"] for href in links]
    print(len(links))
    # for link in links:
    #     a = parse_article_page(link)
    #     print(a['name'])
    #     print(a["text"])
    #     with open("new_york_articles.json", "a") as myfile:
    #         myfile.write(json.dumps(a))
    pool = Pool(100)
    results = pool.map(parse_article_page, links)
    results = [res for res in results]
    result = json.dumps(results)
    with open("new_york_articles.json", "a") as myfile:
        myfile.write(result)
    for result in results:
        print(result["name"])
        print(result["text"])


if __name__ == '__main__':
    # main()
    sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
             {'account': 'Alpha Co', 'Jan': 200, 'Feb': 210, 'Mar': 215},
             {'account': 'Blue Inc', 'Jan': 50, 'Feb': 90, 'Mar': 95}]
    df = pd.DataFrame(sales)
    print(df)
