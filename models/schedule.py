from dataclasses import dataclass


@dataclass
class Schedule:

    vessel: str
    voyage: str
    etd: str
    eta: str
    pol: str
    pod: str
    container: str