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
    name: Literal["ConfigOffSet"] = "ConfigOffSet"
    value: int = Field(ge=-15.0, le=15.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [-15, 15]"] = "integers between [-15, 15]"
    class Config:
        title = "Off Set"

class ConfigSubBlock(Config):
    name: Literal["ConfigSubBlock"] = "ConfigSubBlock"
    value: int = Field(ge=3.0, le=191.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [3, 191]"] = "integers between [3, 191]"
    class Config:
        title = "Sub Block Size"

class ConfigMaxVal(Config):
    name: Literal["ConfigMaxValue"] = "ConfigMaxValue"
    value: int = Field(ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"
    class Config:
        title = "Max Value"

class ConfigThresholdVal(Config):
    name: Literal["ThresholdValue"] = "ThresholdValue"
    value: int = Field(ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"
    class Config:
        title = "Threshold Value"

class ConfigAuto_TH(Config):
    name: Literal["ConfigAuto_TH"]="ConfigAuto_TH"
    maxVal: ConfigMaxVal
    value: Literal["ConfigAuto_TH"] ="ConfigAuto_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Auto-TH"

class ConfigToZeroINV_TH(Config):
    name: Literal["ToZero-INV_TH"]="ToZeroINV_TH"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["ToZeroINV_TH"] ="ToZeroINV_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "ToZero-INV-TH"

class ConfigToZero_TH(Config):
    name: Literal["ToZero_TH"]="ToZero_TH"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["ToZero_TH"] ="ToZero_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "ToZero-TH"

class ConfigTruncated_TH(Config):
    name: Literal["Truncated_TH"]="Truncated_TH"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["Truncated_TH"] ="Truncated_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Truncated-TH"

class ConfigBinaryINV_TH(Config):
    name: Literal["BinaryINV_TH"]="BinaryINV_TH"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["BinaryINV_TH"] ="BinaryINV_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Binary-INV-TH"

class ConfigBinary_TH(Config):
    name: Literal["Binary_TH"]="Binary_TH"
    thresholdVal: ConfigThresholdVal
    maxVal: ConfigMaxVal
    value: Literal["Binary_TH"] ="Binary_TH"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Binary-TH"


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
    name: Literal["configLocalType"] = "configLocalType"
    value:Union[ConfigMean, ConfigGaussian]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Type"

class ConfigGlobalType(Config):
    name: Literal["configGlobalType"] = "configGlobalType"
    value:Union[ConfigBinary_TH,ConfigBinaryINV_TH,ConfigTruncated_TH,ConfigToZero_TH,ConfigToZeroINV_TH,ConfigAuto_TH]
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
        The image
    """
    name: Literal["configType"] = "configType"
    value:Union[ConfigTypeGlobalThresholding,ConfigTypeLocalThresholding]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"


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
