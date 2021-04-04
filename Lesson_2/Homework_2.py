import requests
import bs4
import pymongo
import datetime as dt
from urllib.parse import urljoin

class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client["Magnit_promos_Moscow"]
        self.collection = self.db["Products"]

    def _get_response(self, url):
        return requests.get(url)

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, "lxml")

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find("div", attrs={"class": "сatalogue__main"})
        for prod_a in catalog.find_all("a", recursive=False):
            product_data = self._parse(prod_a)
            self._save(product_data)

    def __get_date(self, date_string) -> list:
        date_list = date_string.replace("с ", "", 1).replace("\n", "").split("до")
        result = []
        for date in date_list:
            temp_date = date.split()
            result.append(
                dt.datetime(
                    year=dt.datetime.now().year,
                    day=int(temp_date[0]),
                    month=int(temp_date[1]),
                )
            )
        return result

    def get_template(self):
        return {
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "")),
            "promo_name": lambda a: a.find("div", attrs={"class": "card-sale__name"}).text,
            "old_price": lambda a: float(
                ".".join(
                    itm for itm in a.find("div", attrs={"class": "label__price_old"}).text.split()
                )
            ),
            "new_price": lambda a: float(
                ".".join(
                    itm for itm in a.find("div", attrs={"class": "label__price_new"}).text.split()
                )
            ),
            "image_url": lambda a: urljoin(self.start_url, a.find("img").attrs.get("data-src")),
            "date_from": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[0],
            "date_to": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[1],
        }

    def _parse(self, product_a) -> dict:
        data = {}
        for key, funk in self.get_template().items():
            try:
                data[key] = funk(product_a)
            except (AttributeError, ValueError):
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)

if __name__ == "__main__":
    url = "https://magnit.ru/promo/?geo=moskva"
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()
