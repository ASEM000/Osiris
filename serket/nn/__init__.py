from . import blocks
from .activation import (
    ELU,
    GELU,
    GLU,
    SILU,
    AdaptiveLeakyReLU,
    AdaptiveReLU,
    AdaptiveSigmoid,
    AdaptiveTanh,
    CeLU,
    HardShrink,
    HardSigmoid,
    HardSILU,
    HardSwish,
    HardTanh,
    LeakyReLU,
    LogSigmoid,
    LogSoftmax,
    Mish,
    PReLU,
    ReLU,
    ReLU6,
    SeLU,
    Sigmoid,
    Snake,
    SoftPlus,
    SoftShrink,
    SoftSign,
    Swish,
    Tanh,
    TanhShrink,
    ThresholdedReLU,
)
from .blocks import UNetBlock, VGG16Block, VGG19Block
from .blur import AvgBlur2D, Filter2D, GaussianBlur2D
from .containers import Lambda, Sequential
from .contrast import AdjustContrast2D, RandomContrast2D
from .convolution import (  # Conv1DSemiLocal,; Conv2DSemiLocal,; Conv3DSemiLocal,
    Conv1D,
    Conv1DLocal,
    Conv1DTranspose,
    Conv2D,
    Conv2DLocal,
    Conv2DTranspose,
    Conv3D,
    Conv3DLocal,
    Conv3DTranspose,
    DepthwiseConv1D,
    DepthwiseConv2D,
    DepthwiseConv3D,
    SeparableConv1D,
    SeparableConv2D,
    SeparableConv3D,
)
from .crop import Crop1D, Crop2D, Crop3D, RandomCrop1D, RandomCrop2D, RandomCrop3D
from .cutout import RandomCutout1D, RandomCutout2D
from .dropout import Dropout, Dropout1D, Dropout2D, Dropout3D
from .fft_convolution import (
    DepthwiseFFTConv1D,
    DepthwiseFFTConv2D,
    DepthwiseFFTConv3D,
    FFTConv1D,
    FFTConv1DTranspose,
    FFTConv2D,
    FFTConv2DTranspose,
    FFTConv3D,
    FFTConv3DTranspose,
    SeparableFFTConv1D,
    SeparableFFTConv2D,
    SeparableFFTConv3D,
)
from .flatten import Flatten, Unflatten
from .flip import FlipLeftRight2D, FlipUpDown2D
from .fully_connected import FNN, PFNN
from .laplace import Laplace2D
from .linear import Bilinear, GeneralLinear, Identity, Linear, Multilinear
from .normalization import GroupNorm, InstanceNorm, LayerNorm
from .padding import Pad1D, Pad2D, Pad3D
from .pooling import (
    AdaptiveAvgPool1D,
    AdaptiveAvgPool2D,
    AdaptiveAvgPool3D,
    AdaptiveConcatPool1D,
    AdaptiveConcatPool2D,
    AdaptiveConcatPool3D,
    AdaptiveMaxPool1D,
    AdaptiveMaxPool2D,
    AdaptiveMaxPool3D,
    AvgPool1D,
    AvgPool2D,
    AvgPool3D,
    GlobalAvgPool1D,
    GlobalAvgPool2D,
    GlobalAvgPool3D,
    GlobalMaxPool1D,
    GlobalMaxPool2D,
    GlobalMaxPool3D,
    LPPool1D,
    LPPool2D,
    LPPool3D,
    MaxPool1D,
    MaxPool2D,
    MaxPool3D,
)
from .preprocessing import HistogramEqualization2D, PixelShuffle2D
from .random_transform import RandomApply, RandomZoom2D
from .recurrent import (
    ConvGRU1DCell,
    ConvGRU2DCell,
    ConvGRU3DCell,
    ConvLSTM1DCell,
    ConvLSTM2DCell,
    ConvLSTM3DCell,
    FFTConvGRU1DCell,
    FFTConvGRU2DCell,
    FFTConvGRU3DCell,
    FFTConvLSTM1DCell,
    FFTConvLSTM2DCell,
    FFTConvLSTM3DCell,
    GRUCell,
    LSTMCell,
    ScanRNN,
    SeparableConvGRU1DCell,
    SeparableConvGRU2DCell,
    SeparableConvGRU3DCell,
    SeparableConvLSTM1DCell,
    SeparableConvLSTM2DCell,
    SeparableConvLSTM3DCell,
    SeparableFFTConvGRU1DCell,
    SeparableFFTConvGRU2DCell,
    SeparableFFTConvGRU3DCell,
    SeparableFFTConvLSTM1DCell,
    SeparableFFTConvLSTM2DCell,
    SeparableFFTConvLSTM3DCell,
    SimpleRNNCell,
)
from .resize import (
    Repeat1D,
    Repeat2D,
    Repeat3D,
    Resize1D,
    Resize2D,
    Resize3D,
    Upsample1D,
    Upsample2D,
    Upsample3D,
)

__all__ = (
    "blocks",
    # Fully connected
    "FNN",
    "PFNN",
    # Linear
    "Linear",
    "Bilinear",
    "Identity",
    "Multilinear",
    "GeneralLinear",
    # Dropout
    "Dropout",
    "Dropout1D",
    "Dropout2D",
    "Dropout3D",
    # containers
    "Sequential",
    "Lambda",
    # Pooling
    "MaxPool1D",
    "MaxPool2D",
    "MaxPool3D",
    "AvgPool1D",
    "AvgPool2D",
    "AvgPool3D",
    "GlobalAvgPool1D",
    "GlobalAvgPool2D",
    "GlobalAvgPool3D",
    "GlobalMaxPool1D",
    "GlobalMaxPool2D",
    "GlobalMaxPool3D",
    "LPPool1D",
    "LPPool2D",
    "LPPool3D",
    "AdaptiveAvgPool1D",
    "AdaptiveAvgPool2D",
    "AdaptiveAvgPool3D",
    "AdaptiveMaxPool1D",
    "AdaptiveMaxPool2D",
    "AdaptiveMaxPool3D",
    "AdaptiveConcatPool1D",
    "AdaptiveConcatPool2D",
    "AdaptiveConcatPool3D",
    # Convolution
    "Conv1D",
    "Conv2D",
    "Conv3D",
    "Conv1DTranspose",
    "Conv2DTranspose",
    "Conv3DTranspose",
    "DepthwiseConv1D",
    "DepthwiseConv2D",
    "DepthwiseConv3D",
    "SeparableConv1D",
    "SeparableConv2D",
    "SeparableConv3D",
    "Conv1DLocal",
    "Conv2DLocal",
    "Conv3DLocal",
    # FFT Convolution
    "FFTConv1D",
    "FFTConv2D",
    "FFTConv3D",
    "Conv1DSemiLocal",
    "Conv2DSemiLocal",
    "Conv3DSemiLocal",
    "DepthwiseFFTConv1D",
    "DepthwiseFFTConv2D",
    "DepthwiseFFTConv3D",
    "FFTConv1DTranspose",
    "FFTConv2DTranspose",
    "FFTConv3DTranspose",
    "SeparableFFTConv1D",
    "SeparableFFTConv2D",
    "SeparableFFTConv3D",
    # Flattening
    "Flatten",
    "Unflatten",
    "Repeat1D",
    "Repeat2D",
    "Repeat3D",
    # Normalization
    "LayerNorm",
    "InstanceNorm",
    "GroupNorm",
    # Blur
    "AvgBlur2D",
    "GaussianBlur2D",
    "Filter2D",
    # Resize
    "Laplace2D",
    "FlipLeftRight2D",
    "FlipUpDown2D",
    "Resize1D",
    "Resize2D",
    "Resize3D",
    "Upsample1D",
    "Upsample2D",
    "Upsample3D",
    "Pad1D",
    "Pad2D",
    "Pad3D",
    # blocks
    "VGG16Block",
    "VGG19Block",
    "UNetBlock",
    # Crop
    "Crop1D",
    "Crop2D",
    "Crop3D",
    # Random Transform
    "RandomCrop1D",
    "RandomCrop2D",
    "RandomCrop3D",
    "RandomCutout1D",
    "RandomCutout2D",
    "RandomZoom2D",
    "RandomApply",
    # Preprocessing
    "HistogramEqualization2D",
    "PixelShuffle2D",
    # Activations
    "AdaptiveLeakyReLU",
    "AdaptiveReLU",
    "AdaptiveSigmoid",
    "AdaptiveTanh",
    "CeLU",
    "ELU",
    "GELU",
    "GLU",
    "HardSILU",
    "HardShrink",
    "HardSigmoid",
    "HardSwish",
    "HardTanh",
    "LeakyReLU",
    "LogSigmoid",
    "LogSoftmax",
    "Mish",
    "PReLU",
    "ReLU",
    "ReLU6",
    "SILU",
    "SeLU",
    "Sigmoid",
    "SoftPlus",
    "SoftShrink",
    "SoftSign",
    "Swish",
    "Snake",
    "Tanh",
    "TanhShrink",
    "ThresholdedReLU",
    # Contrast
    "AdjustContrast2D",
    "RandomContrast2D",
    # RNN
    "LSTMCell",
    "GRUCell",
    "SimpleRNNCell",
    "ScanRNN",
    "ConvLSTM1DCell",
    "ConvLSTM2DCell",
    "ConvLSTM3DCell",
    "SeparableConvLSTM1DCell",
    "SeparableConvLSTM2DCell",
    "SeparableConvLSTM3DCell",
    "ConvGRU1DCell",
    "ConvGRU2DCell",
    "ConvGRU3DCell",
    "SeparableConvGRU1DCell",
    "SeparableConvGRU2DCell",
    "SeparableConvGRU3DCell",
    "FFTConvGRU1DCell",
    "FFTConvGRU2DCell",
    "FFTConvGRU3DCell",
    "FFTConvLSTM1DCell",
    "FFTConvLSTM2DCell",
    "FFTConvLSTM3DCell",
    "SeparableFFTConvGRU1DCell",
    "SeparableFFTConvGRU2DCell",
    "SeparableFFTConvGRU3DCell",
    "SeparableFFTConvLSTM1DCell",
    "SeparableFFTConvLSTM2DCell",
    "SeparableFFTConvLSTM3DCell",
)
