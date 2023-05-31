from logger import log_input_and_output, logger
from utils.request import download_image

from .exceptions import MethodNotImplemented, InvalidItem, ScrapUnsuccessful


class Scraper:
    def __init__(self, force_skip=False):
        self._force_skip = force_skip

        self.items = None

        self.valid = []

    def __str__(self):
        return "Scraper"

    @property
    def unique(self):
        """
        Gets unique items from valid list
        :return: unique items
        :rtype: dict[str, scraper.sneaker_model.SneakerModel]
        """
        return {str(model): model for model in self.valid}

    def scrap(self):
        """
        Scraps all given items and saves their data into the dataset
        """
        for item in self.items:
            try:
                model = self._scrap_item(item=item)
                self.valid.append(model)

            except ScrapUnsuccessful:
                continue

    @log_input_and_output
    def _get_model(self, product_name):
        """
        Based on product's name gets sneaker model name
        :param product_name: product name e.g. Jordan 1 Low Fragment x Travis Scott
        :type product_name: str
        :return: formatted sneaker model name e.g. jordan_1_low
        :rtype: str
        """
        endings = ["low", "high", "mid"]
        beginnings = ["nike", "jordan", "air"]

        name_split = product_name.lower().split(" ")

        if name_split[0] not in beginnings:
            raise InvalidItem(msg=f"{name_split[0].capitalize()} models are not supported yet")
        
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

    def _scrap_item(self, item):
        """
        Scraps item and saves its data
        :param item:
        :raises MethodNotImplemented: when this method is not implemented in initialized class
        """
        raise MethodNotImplemented(f"Method _generate_route is not implemented in {self.__str__}")
