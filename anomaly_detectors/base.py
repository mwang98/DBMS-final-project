from abc import ABC, abstractmethod


class BaseDetector(ABC):

    @abstractmethod
    def init(self, size: int, field: str, init_req) -> str:
        pass

    @abstractmethod
    def begin_batch(self, begin_req):
        pass

    @abstractmethod
    def point(self, point):
        pass

    @abstractmethod
    def end_batch(self, batch_meta) -> (bool, dict):
        pass
