from PIL import Image
from numpy import asarray


class ImageUtils:
    def convert_image_to_np_array(self, image_path):
        return asarray(Image.open(image_path))

    def flatten_image_array(self, image_array):
        return image_array.flatten()


image_utils = ImageUtils()
