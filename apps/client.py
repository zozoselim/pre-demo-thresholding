import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))
import cv2
import numpy as np
import json
from components.Thresholding.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, \
    ThresholdingExecutor, ThresholdingRequest, ThresholdingConfigs, ThresholdingInputs, ConfigType, \
    ConfigTypeGlobalThresholding, ConfigGlobalType, ConfigTypeBlackWhite, ConfigThresholdVal, ConfigMaxVal, InputImage, \
    ConfigTypeLocalThresholding, ConfigLocalType, ConfigMean, ConfigSubBlock, ConfigOffSet, ConfigTypeBlackWhiteInv, \
    ConfigTypeColorLikeGrey, ConfigTypeBlackening, ConfigTypeBlackeningInv, ConfigTypeAutoThresholding, ConfigGaussian

from sdks.novavision.src.base.model import Image, Images, Request
from sdks.novavision.src.media.image import Image as image



# ENDPOINT_URL = "http://10.5.0.3:80/api"
ENDPOINT_URL = "http://127.0.0.1:8000/api"

def infer():
    image_list = Image(name="DemoImage", uID="001", mimeType="image/jpg", encoding="base64",
                       value=image.encode64(np.asarray(
                           cv2.imread("/opt/project/components/Thresholding/resources/einstein.jpg")).astype(
                           np.float32), 'image/jpg'), type="Image")
    imageList = Images(name="Images", value=[image_list], type="Images")
    inputImage = InputImage(value=imageList)

    subBlock = ConfigSubBlock(value=11)
    offSet = ConfigOffSet(value=4)
    maxVal = ConfigMaxVal(value=255)
    thresholdVal = ConfigThresholdVal(value=100)

    configMean = ConfigMean(maxVal=maxVal,subBlock=subBlock,offSet=offSet)
    configGaussian = ConfigGaussian(maxVal=maxVal,subBlock=subBlock,offSet=offSet)

    configTypeBlackWhite = ConfigTypeBlackWhite(thresholdVal=thresholdVal, maxVal=maxVal)
    configTypeBlackWhiteInv = ConfigTypeBlackWhiteInv(thresholdVal=thresholdVal, maxVal=maxVal)
    configTypeColorLikeGrey = ConfigTypeColorLikeGrey(thresholdVal=thresholdVal, maxVal=maxVal)
    configTypeBlackening = ConfigTypeBlackening(thresholdVal=thresholdVal, maxVal=maxVal)
    configTypeBlackeningInv = ConfigTypeBlackeningInv(thresholdVal=thresholdVal, maxVal=maxVal)
    configTypeAutoThresholding = ConfigTypeAutoThresholding(maxVal=maxVal)

    configGlobalType = ConfigGlobalType(value=configTypeColorLikeGrey)
    configLocalType = ConfigLocalType(value=configGaussian)

    configTypeGlobalThresholding = ConfigTypeGlobalThresholding(configEdit=configGlobalType)
    configTypeLocalThresholding = ConfigTypeLocalThresholding(configEdit=configLocalType)

    configType = ConfigType(value=configTypeLocalThresholding)
    thresholdingInputs = ThresholdingInputs(inputImage=inputImage)
    thresholdingConfigs = ThresholdingConfigs(configType=configType)
    thresholdingRequest = ThresholdingRequest(inputs=thresholdingInputs, configs=thresholdingConfigs)
    thresholdingExecutor = ThresholdingExecutor(value=thresholdingRequest)
    executor = ConfigExecutor(value=thresholdingExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    request = PackageModel(configs=packageConfigs, name="Thresholding")
    request_json = json.loads(request.json())
    response = requests.post(ENDPOINT_URL, json = request_json)
    print(response.raise_for_status())
    print(response.json())

if __name__ =="__main__":
    infer()

