from carriers.base import CarrierBase


class MSCSchedule(CarrierBase):

    def search_schedule(
        self,
        pol,
        pod,
        container_type="40HC"
    ):

        return [
    {
        "Vessel": "MSC DEMO",
        "Voyage": "001E",
        "ETD": "28-Jul-2026",
        "ETA": "03-Aug-2026",
        "POL": pol,
        "POD": pod,
        "Container": container_type,
    }
         ]