from scipy import stats
import math

from .base import BaseDetector


class TTestDetector(BaseDetector):
    """
    Keep a rolling window of historically normal data
    When a new window arrives use a two-sided t-test to determine
    if the new window is statistically significantly different.
    """
    def init(self, size: int, field: str, params: dict) -> str:
        self.size = size
        self.history = MovingStats(size)
        self.field = field
        self.alpha = params.get('alpha')

        ret = ''
        if self.alpha is None:
            ret += 'should supply detector param: alpha'
        return ret

    def begin_batch(self, begin_req):
        # create new window for batch
        self.batch = MovingStats(-1)

    def point(self, point):
        self.batch.update(point.fieldsDouble[self.field])

    def end_batch(self, batch_meta):
        pvalue = 1.0
        should_response = False
        response = {}
        if self.history.n != 0:
            # Perform Welch's t test
            t, pvalue = stats.ttest_ind_from_stats(
                self.history.mean, self.history.stddev(), self.history.n,
                self.batch.mean, self.batch.stddev(), self.batch.n,
                equal_var=False,
            )
            response = {
                'pvalue': pvalue,
                't': t,
                'is_anomaly': pvalue < self.alpha,
            }
            should_response = True

        # Update historical stats with batch, but only if it was normal.
        if pvalue > self.alpha:
            for value in self.batch._window:
                self.history.update(value)

        return should_response, response


class MovingStats:
    """
    Calculate the moving mean and variance of a window.
    Uses Welford's Algorithm.
    """
    def __init__(self, size):
        """
        Create new MovingStats object.
        Size can be -1, infinite size or > 1 meaning static size
        """
        self.size = size
        if not (self.size == -1 or self.size > 1):
            raise Exception("size must be -1 or > 1")

        self._window = []
        self.n = 0.0
        self.mean = 0.0
        self._s = 0.0

    def stddev(self):
        """
        Return the standard deviation
        """
        if self.n == 1:
            return 0.0
        return math.sqrt(self._s / (self.n - 1))

    def update(self, value):

        # update stats for new value
        self.n += 1.0
        diff = (value - self.mean)
        self.mean += diff / self.n
        self._s += diff * (value - self.mean)

        if self.n == self.size + 1:
            # update stats for removing old value
            old = self._window.pop(0)
            oldM = (self.n * self.mean - old) / (self.n - 1)
            self._s -= (old - self.mean) * (old - oldM)
            self.mean = oldM
            self.n -= 1

        self._window.append(value)
