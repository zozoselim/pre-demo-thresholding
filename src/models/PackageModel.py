from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class InputImageSecond(Input):
    name: Literal["inputImageSecond"] = "inputImageSecond"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Image"


class OutputImageSecond(Output):
    name: Literal["outputImageSecond"] = "outputImageSecond"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Output Image"


class ConfigOffSet(Config):
    """
    Fine-tunes the threshold level for adaptive methods.
    A constant value subtracted from the calculated mean.
    - Positive values reduce noise (background becomes cleaner).
    - Negative values detect fainter details.
    """
    name: Literal["offset"] = "offset"
    value: int = Field(default=0, ge=-15.0, le=15.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [-15, 15]"] = "integers between [-15, 15]"

    class Config:
        title = "Offset"
        json_schema_extra = {
            "shortDescription": "Sensitivity Constant"
        }


class ConfigSubBlock(Config):
    """
    The size of the pixel neighborhood area used to calculate the local threshold.
    - Smaller blocks: Focus on fine details (good for high frequency variance).
    - Larger blocks: Focus on general shading (good for gradual lighting changes).
    Must be an odd integer.
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
        json_schema_extra = {
            "shortDescription": "Neighborhood Area Size"
        }


class ConfigMaxVal(Config):
    """
    The pixel intensity value assigned to pixels that pass the threshold.
    Usually 255 (White) to create a binary mask.
    """
    name: Literal["maxvalue"] = "maxvalue"
    value: int = Field(default=255, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"

    class Config:
        title = "Max Value"
        json_schema_extra = {
            "shortDescription": "Active Pixel Color"
        }


class ConfigThresholdVal(Config):
    """
    The specific cutoff value (0-255) for Global Thresholding.
    Pixels brighter than this value become the Max Value; darker ones become 0 (or vice versa).
    """
    name: Literal["thresholdvalue"] = "thresholdvalue"
    value: int = Field(default=127, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"

    class Config:
        title = "Threshold Value"
        json_schema_extra = {
            "shortDescription": "Cutoff Point"
        }



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
    Selects the algorithm for calculating the dynamic threshold.
    - Mean: Uses the average of the neighborhood.
    - Gaussian: Uses a weighted average (better for preserving edges).
    """
    name: Literal["configLocalType"] = "configLocalType"
    value:Union[ConfigMean, ConfigGaussian]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"
        json_schema_extra = {
            "shortDescription": "Adaptive Algorithm"
        }


class ConfigGlobalType(Config):
    """
    Selects the logic for applying the threshold.
    - Binary: Standard black/white separation.
    - Auto (Otsu): Automatically finds the best separation value.
    - ToZero: Keeps pixels above threshold, darkens the rest.
    """
    name: Literal["configGlobalType"] = "configGlobalType"
    value:Union[ConfigTypeBlackWhite,ConfigTypeBlackWhiteInv,ConfigTypeColorLikeGrey,ConfigTypeBlackening,ConfigTypeBlackeningInv,ConfigTypeAutoThresholding]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"
        json_schema_extra = {
            "shortDescription": "Separation Logic"
        }


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
    Selects the thresholding strategy:
    - Global: Uses a single cutoff value for the entire image (fast, good for uniform lighting).
    - Local: Calculates different thresholds for small regions (slower, essential for shadows/uneven lighting).
    """
    name: Literal["configType"] = "configType"
    value:Union[ConfigTypeGlobalThresholding,ConfigTypeLocalThresholding]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Method"
        json_schema_extra = {
            "shortDescription": "Segmentation Strategy"
        }


class ThresholdingInputs(Inputs):
    inputImage: InputImage

class DemoSecondInputs(Inputs):
    inputImage: InputImage
    inputImageSecond: InputImageSecond


class ThresholdingConfigs(Configs):
    configType: ConfigType


class ThresholdingOutputs(Outputs):
    outputImage: OutputImage

class DemoSecondOutputs(Outputs):
    outputImage: OutputImage
    outputImageSecond: OutputImageSecond

class ThresholdingRequest(Request):
    inputs: ThresholdingInputs
    configs: ThresholdingConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class DemoSecondRequest(Request):
    inputs: DemoSecondInputs
    configs: ThresholdingConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DemoSecondResponse(Response):
    outputs: DemoSecondOutputs


class ThresholdingResponse(Response):
    outputs:ThresholdingOutputs


class ThresholdingExecutor(Config):
    name: Literal["Thresholding"] = "Thresholding"
    value: Union[ThresholdingRequest, ThresholdingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Thresholding"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class DemoSecondExecutor(Config):
    name: Literal["DemoSecondExecutor"] = "DemoSecondExecutor"
    value: Union[DemoSecondRequest, DemoSecondResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Demo Second Executor"
        json_schema_extra = {
            "target": {
                "value": 1
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[ThresholdingExecutor, DemoSecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name : Literal["DemoThresholding"] = "DemoThresholding"
