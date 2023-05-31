import os
from PIL import Image, UnidentifiedImageError
from logger import logger

from utils.utils import get_checksum


DATASET_PATH = "D:\\Github\\thesis\\dataset"


class SneakerModel:
    def __init__(self, model, sku, additional_info=None):
        self.model = model
        self.sku = sku

        self.info = additional_info

        logger.debug(f"Initializing sneaker model for {self}")

    def __repr__(self):
        return f"{self.model} ({self.sku})"

    def __str__(self):
        return self.__repr__()

    @property
    def directory_path(self):
        """
        Gets directory to current model
        :return: current's model directory
        :rtype: str
        """
        model_path = os.path.join(DATASET_PATH, self.model, self.sku)

        if not os.path.isdir(model_path):
            os.makedirs(model_path)

        return model_path

    @property
    def images(self):
        """
        Gets all images located under this model's directory
        :return: list of image names
        :rtype: list of str
        """
        return [
            os.path.join(self.directory_path, image)
            for image
            in sorted(os.listdir(self.directory_path), key=lambda x: int(x.rstrip(".jpg")))
        ]

    @property
    def next_path(self):
        """
        Gets path for next image of the current model
        :return: path where image should be saved
        :rtype: str
        """
        file_index = int(self.images[-1].split(os.path.sep)[-1].rstrip(".jpg")) + 1 if self.images else 0

        return os.path.join(self.directory_path, f"{file_index}.jpg")

    @property
    def current_path(self):
        """
        Gets current path of the latest image
        :return: current path to the latest image
        :rtype: str or None
        """
        current_path = self.images[-1]
        return current_path if os.path.isfile(current_path) else None

    @property
    def checksums(self):
        """
        Gets list of checksums of all files located in current directory
        :return: list of checksums
        :rtype: list of str
        """
        return [self._get_checksum_for_image(image=image) for image in self.images]

    def verify_latest_download(self):
        """
        Verifies whether image which was downloaded already exists in the dataset, if so its being removed
        """
        checksums = self.checksums

        if checksums[-1] in checksums[:-1]:
            logger.trace(f"Found repeated checksum: {checksums[-1]}, removing {self.current_path}...")
            os.remove(self.current_path)

    @staticmethod
    def _get_checksum_for_image(image):
        """
        Gets checksum for specified image
        :param image: path to the image
        :type image: str
        :return: image checksum
        :rtype: str
        """
        try:
            with Image.open(image) as img:
                checksum = get_checksum(img.tobytes())
        except UnidentifiedImageError:
            logger.warning(f"Found corrupted image: {image}, removing...")
            os.remove(image)
            return None

        return checksum

