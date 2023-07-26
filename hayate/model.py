from abc import ABCMeta, abstractmethod

class Model(metaclass = ABCMeta):
    def __init__(self) -> None:
        self.room = {}

    @abstractmethod
    def setup(self, room_id: str):
        pass