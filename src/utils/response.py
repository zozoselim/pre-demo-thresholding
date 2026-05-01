from sdks.novavision.src.helper.package import PackageHelper
from components.DemoThresholdingg.src.models.PackageModel import (
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
    OutputImageSecond,
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

    else:
        outputImage = OutputImage(value=context.image)

        outputs = ThresholdingOutputs(outputImage=outputImage)

        response = ThresholdingResponse(outputs=outputs)

    executor = ConfigExecutor(value=response)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)

    return package.build_model(context)
