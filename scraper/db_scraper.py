import re

from utils.csv_reader import read_csv

from .scraper import Scraper
from .exceptions import InvalidItem, ScrapUnsuccessful
from .sneaker_model import SneakerModel


class DBScrapper(Scraper):
    def __init__(self, csv_file_path, force_skip=False, workers=1):
        super().__init__(force_skip=force_skip, workers=workers)

        self.items = read_csv(path=csv_file_path)

    def __repr__(self):
        return "DBScrapper"

    def __str__(self):
        return self.__repr__()

    def _scrap_item(self, model):
        """
        Scraps one item from database, downloads its picture(s) into correct folder in dataset
        :param model: scraped sneaker model
        :type model: SneakerModel
        :return: scraped sneaker model
        :rtype: SneakerModel
        """
        images = self._get_images(item=model.info)

        if not self._force_skip or len(images) != len(model.images):
            self._download_images(model=model, images=images)

        return model

    def _get_model(self, item):
        """
        Creates SneakerModel object based on given database record
        :param item: single item record from database
        :type item: dict
        :return: scraped sneaker model
        :rtype: SneakerModel
        """
        model = self._get_sneaker_model(product_name=item["shoes_name"])
        sku = self._get_sku(sku=item["shoes_sku"])

        return SneakerModel(model=model, sku=sku, additional_info=item)

    @staticmethod
    def _get_images(item):
        """
        Gets all images from the database for specified item
        :param item: single item record from database
        :type item: dict
        :return: list of image urls
        :rtype: list of str
        """
        images = [item["shoes_image"]]

        if item["stockx_360"] == "true":
            images.extend(re.split(r",(?=https?:)", item["stockx_360_images"]))

        return images
