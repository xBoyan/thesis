import numpy as np
import threading

from logger import log_input_and_output, logger
from utils.request import download_image

from .exceptions import MethodNotImplemented, InvalidItem


class Scraper:
    def __init__(self, force_skip, workers):
        self._force_skip = force_skip
        self._workers = workers

        self.items = None

        self._valid_models = None
        self._unique_models = None

    def __str__(self):
        return "Scraper"

    @property
    def valid_models(self):
        """
        Creates list of valid sneaker models from given items
        :return: list of valid models
        :rtype:
        """
        if self._valid_models is None:
            valid_models = []
            for item in self.items:
                try:
                    valid_models.append(self._get_model(item=item))
                except InvalidItem:
                    continue

            self._valid_models = sorted(valid_models, key=lambda x: str(x))

        return self._valid_models

    @property
    def unique_models(self):
        """
        Creates list of unique sneaker models from valid items
        :return: dict containing valid and unique models
        """
        if self._unique_models is None:
            unique_models = {str(model): model for model in self.valid_models}

            self._unique_models = list(unique_models.values())

        return self._unique_models

    def scrap(self):
        """
        Scraps all given items and saves their data into the dataset
        """
        valid_models_split = np.array_split(self.valid_models, self._workers)
        for valid_models in valid_models_split:
            if self._workers == 1:
                self._scrap(valid_models=valid_models)
            else:
                threading.Thread(target=self._scrap, kwargs={"valid_models": valid_models}).start()

    def _scrap(self, valid_models):
        """
        Scraps all given part of items and saves their data into the dataset
        :param valid_models: list of scraped sneaker models
        :type valid_models: list of SneakerModel
        """
        for model in valid_models:
            self._scrap_item(model=model)

    @log_input_and_output
    def _get_sneaker_model(self, product_name):
        """
        Based on product's name gets sneaker model name
        :param product_name: product name e.g. Jordan 1 Low Fragment x Travis Scott
        :type product_name: str
        :return: formatted sneaker model name e.g. jordan_1_low
        :rtype: str
        """
        endings = ["low", "high", "mid"]
        beginnings = ["nike", "jordan", "air"]
        negative_kws = ["blazer", "ebernon", "kyrie", "court"]

        name_split = product_name.lower().split(" ")

        if name_split[0] not in beginnings:
            raise InvalidItem(msg=f"{product_name} models are not supported yet")

        for negative_kw in negative_kws:
            if negative_kw in product_name.lower():
                raise InvalidItem(msg=f"{product_name} models are not supported yet")
        
        end_index = None
        for ending in endings:
            try:
                end_index = name_split.index(ending)
            except ValueError:
                continue
                
        if end_index is None:
            raise InvalidItem(msg=f"Couldn't determine product ending: {product_name}")

        if name_split[0] == "air":
            name_split[0] = "nike_air"

        elif name_split[0] == "jordan":
            name_split[0] = "nike_jordan"
        
        return "_".join(name_split[:end_index + 1])

    @log_input_and_output
    def _get_sku(self, sku):
        """
        Gets product variant aka SKU, due to 2 SKUs being available on some products, additional handling is needed
        :param sku: product sku e.g. 315122-111/CW2288-111 or CW2288-111
        :type sku: str
        :return: single product SKU
        :rtype: str
        """
        if "/" in sku:
            return sku.split("/")[-1]

        return sku

    @staticmethod
    def _download_images(model, images):
        """
        Downloads all images given in database for selected item
        :param model: sneaker model
        :type model: SneakerModel
        :param images: list of image urls
        :type images: list of str
        """
        logger.debug(f"Downloading {len(images)} images for {model}...")
        for image in images:
            download_url = image.split("?")[0]
            download_url += "?fit=fill&bg=FFFFFF&w=300&h=214&auto=format,compress&trim=color&q=90&dpr=2"

            download_image(save_path=model.next_path, download_url=download_url)

            model.verify_latest_download()

    def _scrap_item(self, model):
        """
        Scraps given model and saves its data
        :param model: scraped sneaker model
        :type model: SneakerModel
        :raises MethodNotImplemented: when this method is not implemented in initialized class
        """
        raise MethodNotImplemented(f"Method _scrap_item is not implemented in {self.__str__}")

    def _get_model(self, item):
        """
        Gets sneaker model based on given item
        :param item:
        :raises MethodNotImplemented: when this method is not implemented in initialized class
        """
        raise MethodNotImplemented(f"Method _get_model is not implemented in {self.__str__}")
