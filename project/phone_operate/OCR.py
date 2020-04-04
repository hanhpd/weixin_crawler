# Turn pictures into text and pixel location information
from aip import AipOcr
from configs.auth import APP_ID, API_KEY, SECRET_KEY
from phone_operate.config import OCR_NO_WORDS
from PIL import Image
from tools.utils import logging
logger = logging.getLogger(__name__)

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


class OCR():
    @staticmethod
    def get_file_content(filePath):
        """
        :param filePath: File address
        :return: Read image file
        """
        with open(filePath, 'rb') as fp:
            return fp.read()

    @staticmethod
    def pre_process_img(pic_file_name, quality=50, crop=None):
        """
        :param pic_file_name:Picture name to be compressed
        :param quality:Mass percentage
        :param crop:(left, top, right, bottom)Crop absolute coordinates of top left and bottom right
        :return: Compress the image and return the name of the compressed image only
        """
        im = Image.open(pic_file_name)
        rgb_im = im.convert('RGB')
        if crop:
            rgb_im = rgb_im.crop(crop)
        rgb_im.save(pic_file_name+'.jpg', optimize=True, quality=quality)
        return pic_file_name+'.jpg'

    @staticmethod
    def ocr(pic_file_name, location=False, quality=50, crop=None):
        """
        Call the API to return the cor result based on the image file name containing the path
        :param pic_file_name:Image file name based on include path
        :param location:Need to identify location information Need location information True means required
        :return:
        Have location information
        [{'location': {'height': 59,'left': 38,'top': 827,'width': 432},
          'words': 'Net Chen Susu: [link]'},
         {'location': {'height': 56,'left': 212,'top': 955,'width': 206},
          'words': 'Service notification'},...]
        No location
        [{'words': 'WeChat'},
         {'words': 'Address book'},
         {'words': 'Find'},
         {'words': 'I'}],...
        ]
        """
        compressed_image = OCR.pre_process_img(pic_file_name,quality=quality,crop=crop)
        image = OCR.get_file_content(compressed_image)
        # With location
        if location:
            try:
                result = client.general(image)
            except Exception as e:
                logging.error("Request with location information OCR failed Please check the number of times the network or API is available")
                exit()
            # Calculate the true coordinates before words cropping
            if crop:
                for words in result['words_result']:
                    words['location']['left'] += crop[0]
                    words['location']['top'] += crop[1]
        # Without location
        else:
            try:
                result = client.basicGeneral(image)
            except Exception as e:
                logging.error("Request Non-location information OCR failed Please check the number of times the network or API is available")
                exit()
        if result['words_result_num'] != 0:
            return result['words_result']
        else:
            return OCR_NO_WORDS

