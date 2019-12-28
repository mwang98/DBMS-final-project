import sys
from collections import deque
from typing import List

from scipy.fftpack import fft, ifft
import numpy as np

from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2


epsilon = 1e-12


class SpectralResidualHandler(Handler):

    def __init__(self, agent):
        self._agent = agent
        self._field = ''
        self._history = None
        self._size = 0
        self._n = 0
        self.q = 20
        self.z = 200

    @staticmethod
    def info():
        """
        Respond with which type of edges we want/provide and any options we have.
        """
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.BATCH
        response.info.provides = udf_pb2.STREAM

        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        response.info.options['size'].valueTypes.append(udf_pb2.INT)
        return response

    def init(self, init_req):
        """
        Given a list of options initialize this instance of the handler
        """
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
            elif opt.name == 'size':
                self._size = opt.values[0].intValue

        if self._size <= 1:
            success = False
            msg += ' must supply window size > 1'
        if self._field == '':
            success = False
            msg += ' must supply a field name'

        self._history = deque(maxlen=self._size)
        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
        return response

    def begin_batch(self, begin_req):
        pass

    def point(self, point):
        self._history.append(point.fieldsDouble[self._field])
        self._n += 1

    def end_batch(self, batch_meta):
        if self._n > self._history.maxlen:
            self._n -= self._history.maxlen
            O = self.detect_anomalies(list(self._history), q=self.q, z=self.q)
            response = udf_pb2.Response()
            response.point.time = batch_meta.tmax
            response.point.name = batch_meta.name
            response.point.group = batch_meta.group
            response.point.tags.update(batch_meta.tags)

            if np.max(O[self.q + self.z: -(self.q + self.z)]) > 1.:
                response.point.fieldsDouble["pvalue"] = 0.
            else:
                response.point.fieldsDouble["pvalue"] = 2.
            self._agent.write_response(response)

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
