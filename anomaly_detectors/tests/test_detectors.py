from unittest import TestCase

import numpy as np

from ..spectral_residual import SpectralResidualDetector
from ..ttest import TTestDetector
from .mock_classes import MockPoint


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


class TTestTestCase(TestCase):

    def setUp(self) -> None:
        self.hotend_t = 220
        self.hotend_sigma = 0.5
        self.hotend_offset = 0
        self.detector = TTestDetector()
        self.detector.init(size=600, field='hotend', params={'alpha': 0.06})
        self.every = 10

    def test_detection(self):
        response_count, error_count = 0, 0
        for i in range(3600):
            # update sigma values
            is_anomaly = False
            hotend = np.random.normal(self.hotend_t + self.hotend_offset, self.hotend_sigma)
            if i % 180 in list(range(55, 63)):
                hotend *= 1.02
                is_anomaly = True
            point = MockPoint({'hotend': hotend})

            if i % self.every == 0:
                self.detector.begin_batch(None)

            self.detector.point(point)

            if i % self.every == (self.every - 1):
                should_repsonse, ret = self.detector.end_batch(None)
                if should_repsonse:
                    response_count += 1
                if should_repsonse and not ret['is_anomaly'] == is_anomaly:
                    error_count += 1

        print(f'error rate: {error_count / response_count}')
