from collections import deque
from typing import List

from scipy.fftpack import fft, ifft
import numpy as np

from .base import BaseDetector


epsilon = 1e-12


class SpectralResidualDetector(BaseDetector):

    def init(self, size: int, field: str, params: dict) -> str:
        self.size = size
        self._history = deque(maxlen=self.size)
        self.field = field
        self.n = 0
        ret = ''
        self.q = params.get('q')
        self.z = params.get('z')
        if self.q is None:
            ret += 'should supply detector param: q'

        if self.z is None:
            ret += 'should supply detector param: z'

        return ret

    def begin_batch(self, begin_req):
        pass

    def point(self, point):
        self._history.append(point.fieldsDouble[self.field])
        self.n += 1

    def end_batch(self, batch_meta):
        if self.n > self._history.maxlen:
            self.n -= self._history.maxlen
            O = self.detect_anomalies(list(self._history), q=self.q, z=self.q)
            is_anomaly = (np.max(O[self.q + self.z: -(self.q + self.z)]) > 1)
            return True, {'is_anomaly': is_anomaly}
        else:
            return False, {}

    @staticmethod
    def detect_anomalies(data: List[float], q=20, z=20):
        fft_result = fft(data)
        A = np.abs(fft_result)
        P = np.angle(fft_result)
        L = np.log(A + epsilon)

        AL = np.convolve(L, np.ones([q]) / q, mode='same')
        R = L - AL
        S = np.abs(
            ifft(
                np.exp(R + P * np.complex(0, 1))
            )
        )
        S_bar = np.convolve(S, np.ones([z]) / z, mode='same')
        O = np.abs((S - S_bar) / (S_bar + epsilon))
        return O
