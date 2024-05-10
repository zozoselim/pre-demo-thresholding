
import cv2
import sys
import numpy as np
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from components.Thresholding.src.models.PackageModel import PackageConfigs,ConfigExecutor,PackageModel,ThresholdingExecutor,ThresholdingResponse,ThresholdingOutputs,OutputImage
from sdks.novavision.src.base.response import Response
from pydantic import ValidationError
from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.redis import RedisPubSubManager
from sdks.novavision.src.base.app import App


class Thresholding(Component):
    def __init__(self, request,bootstrap):
        self.error_list = []
        try:
            super().__init__(request)
            self.request.model = PackageModel(**(self.request.data))
            self.type = self.request.get_param("configType")
            #self.images = self.request.get_param("Images")
            if App.get_app_mode() == 'runtime':
                self.r = RedisPubSubManager()
                self.images = self.request.get_param("inputImage")
                self.images["value"] = self.r.redis_stream_get_frame_range(self.images["value"])
            elif App.get_app_mode() == 'api':
                self.images = self.request.get_param("inputImage")
            self.islist = Image.is_list(self.images)
            self.load_parameters()

        except ValidationError as e:
            self.error_list.append({"error": "hata_normalization"})

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
    def bootstrap():
        model = {"models": " "}
        return model

    def thresholding(self,image):
        image = np.asarray(image).astype(np.uint8)

        if len(image.shape)==3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if self.type == "GlobalThresholding":
            if self.global_type=="black white":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY)
            elif self.global_type=="black white inv":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY_INV)
            elif self.global_type=="color like grey":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TRUNC)
            elif self.global_type=="blackening":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO)
            elif self.global_type=="blackening inv":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO_INV)
            elif self.global_type=="auto thresholding":
                _, th_image = cv2.threshold(image,0, self.max_value, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        elif self.type == "LocalThresholding":
            if self.local_type == "mean":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)
            elif self.local_type == "gaussian":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)

        return th_image

    def run(self):
        image = []
        if (self.islist):
            for img in self.images:
                img = Image.get_image(img)
                img.value = Image.encode64(np.asarray(self.thresholding(np.array(img.value))), img.mimeType)
                image.append(img)
        else:
            img = Image.get_image(self.images)
            img.value = Image.encode64(np.asarray(self.thresholding(np.array(img.value))), img.mimeType)
            if App.get_app_mode() == 'runtime':
                self.r.redis_stream_set_frame(img.value, self.request.model.uID)
                img.value = f'redis_{self.request.model.uID}_outputImage'
            image = img

        outputImage = OutputImage(value=image)
        Outputs = ThresholdingOutputs(outputImage=outputImage)
        normalizationResponse = ThresholdingResponse(outputs=Outputs)
        normalizationExecutor = ThresholdingExecutor(value=normalizationResponse)
        executor = ConfigExecutor(value=normalizationExecutor)
        packageConfigs = PackageConfigs(executor=executor)
        packageModel = PackageModel(configs=packageConfigs)
        Response(model=packageModel).response()


if "__main__" == __name__:
    r = RedisPubSubManager()._subscribe(room_id=sys.argv[1])