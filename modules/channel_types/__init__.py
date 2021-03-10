from .image import ImageModel
from .geo import GeoModel

channel_type_dict = {
    "numeric":None,
    "image":ImageModel,
    "geo":GeoModel
}