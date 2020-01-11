import sys
import json

import numpy as np

from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2

from anomaly_detectors import anomaly_detector_hub


class CustomHandler(Handler):

    def __init__(self, agent):
        self._agent = agent
        self.detector = None

    def info(self):
        """
        Respond with which type of edges we want/provide and any options we have.
        """
        response = udf_pb2.Response()
        # We will consume batch edges aka windows of data.
        response.info.wants = udf_pb2.BATCH
        # We will produce single points of data aka stream.
        response.info.provides = udf_pb2.STREAM

        # Here we can define options for the UDF.
        # Define which field we should process
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)

        # Since we will be computing a moving average let's make the size configurable.
        # Define an option 'size' that takes one integer argument.
        response.info.options['size'].valueTypes.append(udf_pb2.INT)
        response.info.options['detector_type'].valueTypes.append(udf_pb2.STRING)
        response.info.options['detector_params'].valueTypes.append(udf_pb2.STRING)
        print('info', file=sys.stderr)
        return response

    def init(self, init_req):
        """
        Given a list of options initialize this instance of the handler
        """
        success = True
        msg = ''
        field, size, detector_type, detector_params = None, None, None, None
        for opt in init_req.options:
            if opt.name == 'field':
                field = opt.values[0].stringValue
            elif opt.name == 'size':
                size = opt.values[0].intValue
            elif opt.name == 'detector_type':
                detector_type = opt.values[0].stringValue
            elif opt.name == 'detector_params':
                detector_params = opt.values[0].stringValue
                detector_params = json.loads(detector_params)

        if size is None:
            success = False
            msg += ' must supply window size > 1'
        if field is None:
            success = False
            msg += ' must supply a field name'
        if detector_type is None:
            success = False
            msg += ' must supply a detector type'
        else:
            try:
                self.detector = anomaly_detector_hub[detector_type]()
                msg += self.detector.init(size=size, field=field, params=detector_params)
            except KeyError:
                success = False
                msg += ' invalid detector type'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
        print('init', file=sys.stderr)
        return response

    def begin_batch(self, begin_req):
        self.detector.begin_batch(begin_req)

    def point(self, point):
        self.detector.point(point)

    def end_batch(self, batch_meta):
        print('end_batch', file=sys.stderr)
        should_response, ret = self.detector.end_batch(batch_meta)

        if should_response != 0:
            # Send response point back to Kapacitor
            response = udf_pb2.Response()
            response.point.time = batch_meta.tmax
            response.point.name = batch_meta.name
            response.point.group = batch_meta.group
            response.point.tags.update(batch_meta.tags)
            for key, value in ret.items():
                if isinstance(value, int):
                    response.point.fieldsInt[key] = value
                elif isinstance(value, float):
                    response.point.fieldsDouble[key] = value
                elif isinstance(value, (bool, np.bool_)):
                    response.point.fieldsInt[key] = int(value)
                else:
                    print(f'invalid value key:{key}, value: {value}, type: {type(value)}', file=sys.stderr)
            self._agent.write_response(response)
