from .ttest import TTestDetector
from .spectral_residual import SpectralResidualDetector


anomaly_detector_hub = {
    'ttest': TTestDetector,
    'spectral_residual': SpectralResidualDetector,
}
