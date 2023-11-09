import numbers

from pydantic import Field, validator
from typing import List, Optional, Union, Any, Dict,Literal

from sdks.novavision.src.base.model import Package, Images, Param, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"
    class Config:
        title = "Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"
    class Config:
        title = "Image"

class ConfigOffSet(Config):
    """
        It is a fine-tuning parameter which is subtracted from mean or weighted mean
    """
    name: Literal["offset"] = "offset"
    value: int = Field(default=0, ge=-15.0, le=15.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [-15, 15]"] = "integers between [-15, 15]"
    class Config:
        title = "Offset"

class ConfigSubBlock(Config):
    """
        Size of sub-block size which is used to calculate a threshold value
    """
    @validator('value')
    def validate_odd_integer_range(cls, value):
        if value % 2:
            if value < 3 or value > 191:
                raise ValueError('Invalid value: must be an odd integer between 3 and 191 (inclusive)')
            return value
        else:
            raise ValueError('Invalid value: must be an odd integer between 3 and 191 (inclusive)')
    name: Literal["subblock"] = "subblock"
    value: int = Field(default=11, ge=3.0, le=191.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["odd integers between [3, 191]"] = "odd integers between [3, 191]"
    class Config:
        title = "SubBlock Size"

class ConfigMaxVal(Config):
    """
        Maximum value that can be assigned to pixels after thresholding
    """
    name: Literal["maxvalue"] = "maxvalue"
    value: int = Field(default=255, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"
    class Config:
        title = "Max Value"

class ConfigThresholdVal(Config):
    """
        It is used to separate between foreground and background pixels
    """
    name: Literal["thresholdvalue"] = "thresholdvalue"
    value: int = Field(default=127, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"
    class Config:
        title = "Threshold Value"

class ConfigTypeAutoThresholding(Config):
    name: Literal["auto thresholding"]="auto thresholding"
    maxVal: ConfigMaxVal
    value: Literal["auto thresholding"] ="auto thresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "AUTO_TH"

class ConfigTypeBlackeningInv(Config):
    name: Literal["blackening inv"]="blackening inv"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["blackening inv"] ="blackening inv"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "TOZERO_INV_TH"

class ConfigTypeBlackening(Config):
    name: Literal["blackening"]="blackening"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["blackening"] ="blackening"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "TOZERO_TH"


class ConfigTypeColorLikeGrey(Config):
    name: Literal["color like grey"]="color like grey"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["color like grey"] ="color like grey"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "TRUNCATED_TH"

class ConfigTypeBlackWhiteInv(Config):
    name: Literal["black white inv"]="black white inv"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["black white inv"] ="black white inv"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "BINARY_INV_TH"


class ConfigTypeBlackWhite(Config):
    name: Literal["black white"]="black white"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["black white"] ="black white"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "BINARY_TH"

class ConfigMean(Config):
    name: Literal["mean"] = "mean"
    maxVal: ConfigMaxVal
    subBlock: ConfigSubBlock
    offSet: ConfigOffSet
    value: Literal["mean"] = "mean"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Mean"

class ConfigGaussian(Config):
    name: Literal["gaussian"] = "gaussian"
    maxVal: ConfigMaxVal
    subBlock: ConfigSubBlock
    offSet: ConfigOffSet
    value: Literal["gaussian"] = "gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Gaussian"

class ConfigLocalType(Config):
    """
        Advanced approaches used for local thresholding
    """
    name: Literal["configLocalType"] = "configLocalType"
    value:Union[ConfigMean, ConfigGaussian]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Type"

class ConfigGlobalType(Config):
    """
        Simple approaches used for global thresholding
    """
    name: Literal["configGlobalType"] = "configGlobalType"
    value:Union[ConfigTypeBlackWhite,ConfigTypeBlackWhiteInv,ConfigTypeColorLikeGrey,ConfigTypeBlackening,ConfigTypeBlackeningInv,ConfigTypeAutoThresholding]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Type"

class ConfigTypeLocalThresholding(Config):
    configEdit: ConfigLocalType
    name:Literal["LocalThresholding"] = "LocalThresholding"
    value:Literal["LocalThresholding"] = "LocalThresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Local Thresholding"

class ConfigTypeGlobalThresholding(Config):
    configEdit: ConfigGlobalType
    name:Literal["GlobalThresholding"] = "GlobalThresholding"
    value:Literal["GlobalThresholding"] = "GlobalThresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Global Thresholding"


class ConfigType(Config):
    """
        Thresholding methods
    """
    name: Literal["configType"] = "configType"
    value:Union[ConfigTypeGlobalThresholding,ConfigTypeLocalThresholding]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Method"


class ThresholdingInputs(Inputs):
    inputImage: InputImage


class ThresholdingConfigs(Configs):
    configType: ConfigType


class ThresholdingOutputs(Outputs):
    outputImage: OutputImage


class ThresholdingRequest(Request):
    inputs: Optional[ThresholdingInputs]
    configs: ThresholdingConfigs
    class Config:
        schema_extra = {
            "target": "configs"
        }


class ThresholdingResponse(Response):
    outputs:ThresholdingOutputs


class ThresholdingExecutor(Config):
    name: Literal["Thresholding"] = "Thresholding"
    value: Union[ThresholdingRequest, ThresholdingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Thresholding"
        schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[ThresholdingExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name : Literal["Thresholding"] = "Thresholding"
    uID = "1221112"
