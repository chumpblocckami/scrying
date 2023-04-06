from io import BytesIO

import PIL.Image
import pandas as pd
import requests
from datasets import Dataset, Features, Image, Value, Array3D
from tqdm import tqdm


class Scrying():
    def __init__(self, verbose=False):
        self.url = "https://api.scryfall.com/cards/search?q="
        self.cards = []
        self.verbose = verbose
        self.it = -1

    def add(self, url):
        self.cards.append(url)

    def __getitem__(self, idx):
        return PIL.Image.open(BytesIO(requests.get(self.cards[idx]).content))

    def __len__(self):
        return len(self.cards)

    def download_from_url(self, query):
        has_more = True
        page = 1
        while has_more:
            response = requests.get(self.url + query)
            has_more = response.json()["has_more"]
            url = response.json()["next_page"] if "next_page" in response.json() else ""
            remaining_pages = int(response.json()["total_cards"] / 175)
            for card in tqdm(response.json()["data"], desc=f"Downloading page {page}/{remaining_pages}"):
                if "image_uris" in card:
                    self.add(card["image_uris"]["art_crop"])
                else:
                    if self.verbose:
                        print(f"Cannot parse {card['name']}")
            page = page + 1
