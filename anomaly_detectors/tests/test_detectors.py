from unittest import TestCase

import numpy as np
from matplotlib import pyplot as plt

from ..spectral_residual import SpectralResidualHandler


class SpectralResidualTestCase(TestCase):

    def setUp(self) -> None:
        self.data = 0.5 * np.random.random(size=3600)
        self.data += 3 * np.sin(np.linspace(0, 100, 3600)) + np.linspace(0, 5, 3600)
        self.data[1800:1800 + 100] += 3 * np.random.random(size=100)

        self.data[2500:2500 + 100] += 3 * np.random.random(size=100)

    def test_detection(self):
        O = SpectralResidualHandler.detect_anomalies(data=self.data)
