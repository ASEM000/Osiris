# Copyright 2023 serket authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from serket._src.nn.activation import (
    ELU,
    GELU,
    GLU,
    AdaptiveLeakyReLU,
    AdaptiveReLU,
    AdaptiveSigmoid,
    AdaptiveTanh,
    CeLU,
    HardShrink,
    HardSigmoid,
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
    SquarePlus,
    Swish,
    Tanh,
    TanhShrink,
    ThresholdedReLU,
)
from serket._src.nn.attention import MultiHeadAttention
from serket._src.nn.convolution import (
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
    DepthwiseFFTConv1D,
    DepthwiseFFTConv2D,
    DepthwiseFFTConv3D,
    FFTConv1D,
    FFTConv1DTranspose,
    FFTConv2D,
    FFTConv2DTranspose,
    FFTConv3D,
    FFTConv3DTranspose,
    SeparableConv1D,
    SeparableConv2D,
    SeparableConv3D,
    SeparableFFTConv1D,
    SeparableFFTConv2D,
    SeparableFFTConv3D,
    SpectralConv1D,
    SpectralConv2D,
    SpectralConv3D,
    conv_nd,
    conv_nd_transpose,
    depthwise_conv_nd,
    depthwise_fft_conv_nd,
    fft_conv_nd,
    fft_conv_nd_transpose,
    local_conv_nd,
    separable_conv_nd,
    separable_fft_conv_nd,
    spectral_conv_nd,
)
from serket._src.nn.dropout import (
    Dropout,
    Dropout1D,
    Dropout2D,
    Dropout3D,
    RandomCutout1D,
    RandomCutout2D,
    RandomCutout3D,
    dropout_nd,
    random_cutout_nd,
)
from serket._src.nn.linear import FNN, MLP, Embedding, GeneralLinear, Identity, Linear
from serket._src.nn.normalization import (
    BatchNorm,
    GroupNorm,
    InstanceNorm,
    LayerNorm,
    WeightNormWrapper,
)
from serket._src.nn.pooling import (
    AdaptiveAvgPool1D,
    AdaptiveAvgPool2D,
    AdaptiveAvgPool3D,
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
from serket._src.nn.recurrent import (
    ConvGRU1DCell,
    ConvGRU2DCell,
    ConvGRU3DCell,
    ConvLSTM1DCell,
    ConvLSTM2DCell,
    ConvLSTM3DCell,
    DenseCell,
    FFTConvGRU1DCell,
    FFTConvGRU2DCell,
    FFTConvGRU3DCell,
    FFTConvLSTM1DCell,
    FFTConvLSTM2DCell,
    FFTConvLSTM3DCell,
    GRUCell,
    LSTMCell,
    RNNCell,
    ScanRNN,
    SimpleRNNCell,
    scan_rnn,
)
from serket._src.nn.reshape import (
    CenterCrop1D,
    CenterCrop2D,
    CenterCrop3D,
    Crop1D,
    Crop2D,
    Crop3D,
    Flatten,
    Pad1D,
    Pad2D,
    Pad3D,
    RandomCrop1D,
    RandomCrop2D,
    RandomCrop3D,
    RandomZoom1D,
    RandomZoom2D,
    RandomZoom3D,
    Resize1D,
    Resize2D,
    Resize3D,
    Unflatten,
    Upsample1D,
    Upsample2D,
    Upsample3D,
    Zoom1D,
    Zoom2D,
    Zoom3D,
)

__all__ = [
    # activation
    "ELU",
    "GELU",
    "GLU",
    "AdaptiveLeakyReLU",
    "AdaptiveReLU",
    "AdaptiveSigmoid",
    "AdaptiveTanh",
    "CeLU",
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
    "SeLU",
    "Sigmoid",
    "Snake",
    "SoftPlus",
    "SoftShrink",
    "SoftSign",
    "SquarePlus",
    "Swish",
    "Tanh",
    "TanhShrink",
    "ThresholdedReLU",
    # attention
    "MultiHeadAttention",
    # convolution
    "Conv1D",
    "Conv1DLocal",
    "Conv1DTranspose",
    "Conv2D",
    "Conv2DLocal",
    "Conv2DTranspose",
    "Conv3D",
    "Conv3DLocal",
    "Conv3DTranspose",
    "DepthwiseConv1D",
    "DepthwiseConv2D",
    "DepthwiseConv3D",
    "DepthwiseFFTConv1D",
    "DepthwiseFFTConv2D",
    "DepthwiseFFTConv3D",
    "FFTConv1D",
    "FFTConv1DTranspose",
    "FFTConv2D",
    "FFTConv2DTranspose",
    "FFTConv3D",
    "FFTConv3DTranspose",
    "SeparableConv1D",
    "SeparableConv2D",
    "SeparableConv3D",
    "SeparableFFTConv1D",
    "SeparableFFTConv2D",
    "SeparableFFTConv3D",
    "SpectralConv1D",
    "SpectralConv2D",
    "SpectralConv3D",
    # functional form
    "conv_nd",
    "depthwise_conv_nd",
    "depthwise_fft_conv_nd",
    "fft_conv_nd",
    "local_conv_nd",
    "separable_conv_nd",
    "separable_fft_conv_nd",
    "conv_nd_transpose",
    "fft_conv_nd_transpose",
    "spectral_conv_nd",
    # dropout
    "Dropout",
    "Dropout1D",
    "Dropout2D",
    "Dropout3D",
    "RandomCutout1D",
    "RandomCutout2D",
    "RandomCutout3D",
    "dropout_nd",
    "random_cutout_nd",
    # linear
    "FNN",
    "MLP",
    "Embedding",
    "GeneralLinear",
    "Identity",
    "Linear",
    # norms
    "BatchNorm",
    "GroupNorm",
    "InstanceNorm",
    "LayerNorm",
    "WeightNormWrapper",
    # pooling
    "AdaptiveAvgPool1D",
    "AdaptiveAvgPool2D",
    "AdaptiveAvgPool3D",
    "AdaptiveMaxPool1D",
    "AdaptiveMaxPool2D",
    "AdaptiveMaxPool3D",
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
    "MaxPool1D",
    "MaxPool2D",
    "MaxPool3D",
    # rnn
    "ConvGRU1DCell",
    "ConvGRU2DCell",
    "ConvGRU3DCell",
    "ConvLSTM1DCell",
    "ConvLSTM2DCell",
    "ConvLSTM3DCell",
    "DenseCell",
    "FFTConvGRU1DCell",
    "FFTConvGRU2DCell",
    "FFTConvGRU3DCell",
    "FFTConvLSTM1DCell",
    "FFTConvLSTM2DCell",
    "FFTConvLSTM3DCell",
    "GRUCell",
    "LSTMCell",
    "RNNCell",
    "ScanRNN",
    "SimpleRNNCell",
    "scan_rnn",
    # reshape
    "CenterCrop1D",
    "CenterCrop2D",
    "CenterCrop3D",
    "Crop1D",
    "Crop2D",
    "Crop3D",
    "Flatten",
    "Pad1D",
    "Pad2D",
    "Pad3D",
    "RandomCrop1D",
    "RandomCrop2D",
    "RandomCrop3D",
    "RandomZoom1D",
    "RandomZoom2D",
    "RandomZoom3D",
    "Resize1D",
    "Resize2D",
    "Resize3D",
    "Unflatten",
    "Upsample1D",
    "Upsample2D",
    "Upsample3D",
    "Zoom1D",
    "Zoom2D",
    "Zoom3D",
]
