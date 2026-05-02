   
import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoThresholdingg.src.utils.response import build_response
from components.DemoThresholdingg.src.models.PackageModel import PackageModel


class DemoSecondExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.type = self.request.get_param("configType")
        self.images = self.request.get_param("inputImage")
        self.load_parameters()

    def load_parameters(self):
        if self.type == "GlobalThresholding":
            self.global_type = self.request.get_param("configGlobalType")
            if self.global_type in ["black white","black white inv","color like grey","blackening","blackening inv"]:
                self.th_value = self.request.get_param("thresholdvalue")
            self.max_value = self.request.get_param("maxvalue")

        elif self.type == "LocalThresholding":
            self.local_type = self.request.get_param("configLocalType")
            self.max_value = self.request.get_param("maxvalue")
            self.sub_block = self.request.get_param("subblock")
            self.off_set = self.request.get_param("offset")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def thresholding(self, image):
        image = np.asarray(image).astype(np.uint8)

        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if self.type == "GlobalThresholding":
            if self.global_type == "black white":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY)
            elif self.global_type == "black white inv":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY_INV)
            elif self.global_type == "color like grey":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TRUNC)
            elif self.global_type == "blackening":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO)
            elif self.global_type == "blackening inv":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO_INV)
            elif self.global_type == "auto thresholding":
                _, th_image = cv2.threshold(image, 0, self.max_value, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        elif self.type == "LocalThresholding":
            if self.local_type == "mean":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)
            elif self.local_type == "gaussian":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)

        return th_image

    def run(self):
        frames = Image.get_frame(img=self.images, redis_db=self.redis_db)

        if not isinstance(frames, list):
            frames = [frames]

        img1 = frames[0]
        img2 = frames[1] if len(frames) > 1 else frames[0]

        img1.value = self.thresholding(img1.value)
        img2.value = self.thresholding(img2.value)

        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageSecond = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
