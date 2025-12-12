import base64
import requests
from loguru import logger

def encode_image_by_path(image_path: str):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as error:
        logger.error(f"Error encoding image: {error}")
        raise error

def encode_image_by_url(image_url: str):
    try:
        response = requests.get(image_url)
        return base64.b64encode(response.content).decode("utf-8")
    except Exception as error:
        logger.error(f"Error encoding image by url: {error}")
        raise error
       

