
import cv2
import numpy as np
from sdks.novavision.src.base.component import Component
from components.Thresholding.src.models.PackageModel import PackageConfigs,ConfigExecutor,PackageModel,ThresholdingExecutor,ThresholdingResponse,ThresholdingOutputs,OutputImage,Images
from sdks.novavision.src.base.response import Response
from pydantic import ValidationError
from sdks.novavision.src.media.image import Image


class Thresholding(Component):
    def __init__(self, request,bootstrap):
        self.error_list = []
        try:
            super().__init__(request)
            self.request.model = PackageModel(**(self.request.data))
            self.type = self.request.get_param("configType")
            self.load_parameters()
            self.images = self.request.get_param("Images")

        except ValidationError as e:
            self.error_list.append({"error": "hata_normalization"})

    def load_parameters(self):
        if self.type == "GlobalThresholding":
            self.global_type = self.request.get_param("configGlobalType")
            if self.global_type in ["Binary_TH","BinaryINV_TH","Truncated_TH","ToZero_TH","ToZeroINV_TH",]:
                self.th_value = self.request.get_param("ThresholdValue")
            self.max_value = self.request.get_param("ConfigMaxValue")

        elif self.type == "LocalThresholding":
            self.local_type = self.request.get_param("configLocalType")
            self.max_value = self.request.get_param("ConfigMaxValue")
            self.sub_block = self.request.get_param("ConfigSubBlock")
            self.off_set = self.request.get_param("ConfigOffSet")

    @staticmethod
    def bootstrap():
        model = {"models": " "}
        return model

    def thresholding(self,image):
        if self.type == "GlobalThresholding":
            if self.global_type=="Binary_TH":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY)
            elif self.global_type=="BinaryINV_TH":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_BINARY_INV)
            elif self.global_type=="Truncated_TH":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TRUNC)
            elif self.global_type=="ToZero_TH":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO)
            elif self.global_type=="ToZeroINV_TH":
                _, th_image = cv2.threshold(image, self.th_value, self.max_value, cv2.THRESH_TOZERO_INV)
            elif self.global_type=="ConfigAuto_TH":
                pass


        elif self.type == "LocalThresholding":
            if self.local_type == "mean":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)
            elif self.local_type == "gaussian":
                th_image = cv2.adaptiveThreshold(image, self.max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,self.sub_block, self.off_set)

        return  th_image

    def run(self):
        imgs = []
        for img in self.images:
            img.value = Image.encode64(np.asarray(self.thresholding(np.array(img.value))), img.mimeType)
            imgs.append(img)

        imageList = Images(name="Images", value=imgs, type="Images")
        outputImage = OutputImage(value=imageList)
        Outputs = ThresholdingOutputs(outputImage=outputImage)
        normalizationResponse = ThresholdingResponse(outputs=Outputs)
        normalizationExecutor = ThresholdingExecutor(value=normalizationResponse)
        executor = ConfigExecutor(value=normalizationExecutor)
        packageConfigs = PackageConfigs(executor=executor)
        packageModel = PackageModel(configs=packageConfigs)
        return Response(model=packageModel).response()

