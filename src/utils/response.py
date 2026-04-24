from sdks.novavision.src.helper.package import PackageHelper
from src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    ThresholdingExecutor,
    ThresholdingResponse,
    ThresholdingOutputs,
    OutputImage,
    DemoSecondExecutor,
    DemoSecondResponse,
    DemoSecondOutputs,
    OutputImageSecond
)


def build_response(context):
    if hasattr(context, "imageSecond"):
        outputImage = OutputImage(value=context.image)
        outputImageSecond = OutputImageSecond(value=context.imageSecond)

        outputs = DemoSecondOutputs(
            outputImage=outputImage,
            outputImageSecond=outputImageSecond
        )

        response = DemoSecondResponse(outputs=outputs)
        selectedExecutor = DemoSecondExecutor(value=response)

    else:
        outputImage = OutputImage(value=context.image)

        outputs = ThresholdingOutputs(outputImage=outputImage)

        response = ThresholdingResponse(outputs=outputs)
        selectedExecutor = ThresholdingExecutor(value=response)

    executor = ConfigExecutor(value=selectedExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)

    return packageModel