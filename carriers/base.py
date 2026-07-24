from abc import ABC, abstractmethod


class CarrierBase(ABC):

    @abstractmethod
    def search_schedule(self, pol, pod):
        pass