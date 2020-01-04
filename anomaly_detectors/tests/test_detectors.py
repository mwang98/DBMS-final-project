from unittest import TestCase

import numpy as np

from ..spectral_residual import SpectralResidualDetector


class SpectralResidualTestCase(TestCase):

    def setUp(self) -> None:
        hotend_anomalies = [
            (0, 0.5, 0),  # normal sigma
            (3700, 3.0, -1.5),  # at one hour the hotend goes bad
            (3800, 0.5, 0),  # 5 minutes later recovers
        ]
        self.data = []
        hotend_t = 220
        hotend_sigma = 0
        hotend_offset = 0
        for i in range(60 * 60 * 10):
            # update sigma values
            if len(hotend_anomalies) > 0 and i == hotend_anomalies[0][0]:
                hotend_sigma = hotend_anomalies[0][1]
                hotend_offset = hotend_anomalies[0][2]
                hotend_anomalies = hotend_anomalies[1:]
            hotend = np.random.normal(hotend_t + hotend_offset, hotend_sigma)
            self.data.append(hotend)

    def test_detection(self):
        for i in range(0, len(self.data), 3600):
            q, z = 5, 5
            O = SpectralResidualDetector.detect_anomalies(
                data=self.data[i: i + 3600],
                q=q,
                z=z,
            )
            print(np.max(O[q + z: -(q + z)]))
