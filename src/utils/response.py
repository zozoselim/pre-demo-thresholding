
from sdks.novavision.src.helper.package import PackageHelper
from components.Thresholding.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, ThresholdingExecutor, ThresholdingResponse, ThresholdingOutputs, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = ThresholdingOutputs(outputImage=outputImage)
    normalizationResponse = ThresholdingResponse(outputs=Outputs)
    normalizationExecutor = ThresholdingExecutor(value=normalizationResponse)
    executor = ConfigExecutor(value=normalizationExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
