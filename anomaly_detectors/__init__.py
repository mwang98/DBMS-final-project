from .ttest import TTestHandler
from .spectral_residual import SpectralResidualHandler


anomaly_detector_hub = {
    'ttest': TTestHandler,
    'spectral_residual': SpectralResidualHandler,
}
