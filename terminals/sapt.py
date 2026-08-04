import json
import re
import requests
from bs4 import BeautifulSoup


class SAPTTerminal:

    BASE_URL = "https://www.sapt.com.pk"

    ENQUIRY_URL = BASE_URL + "/Enquiries"
    DETAILS_URL = BASE_URL + "/Enquiries/ContainerDetails"
    HISTORY_URL = BASE_URL + "/Enquiries/ContainerHistory"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
        })

    # ==================================================
    # GET PAGE
    # ==================================================

    def get_page(self, url):

        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    # ==================================================
    # CONTAINER HISTORY
    # ==================================================

    def get_container_history(self, container):

        container = str(container).strip().upper()

        params = {
            "cntrNum": container,
            "BL": "_1",
            "method": "",
            "pTId": "SAPT",
        }

        response = self.session.get(
            self.HISTORY_URL,
            params=params,
            timeout=30
        )

        print("History Status:", response.status_code)

        response.raise_for_status()

        return response.text

    # ==================================================
    # PARSE HISTORY JSON
    # ==================================================

    def parse_history_json(self, html):

        match = re.search(
            r'var\s+data\s*=\s*(\{.*?\});',
            html,
            re.DOTALL
        )

        if not match:
            return []

        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            return []

        encoded_json = data.get("_jsonArray")

        if not encoded_json:
            return []

        try:
            rows = json.loads(encoded_json)
        except json.JSONDecodeError:
            return []

        if not rows:
            return []

        # SAPT returns this when no container is found:
        #
        # [{"container_no": "N/A", "formatter": "yes"}]

        first = rows[0]

        container_value = (
            first.get("CONTAINER NO")
            or first.get("container_no")
        )

        if container_value is None:
            return []

        if str(container_value).strip().upper() in (
            "N/A",
            "NA",
            ""
        ):
            return []

        return rows

    # ==================================================
    # SEARCH CONTAINER / GET PID
    # ==================================================

    def search_container(self, container_no):

        container_no = str(
            container_no
        ).strip().upper()

        html = self.get_container_history(
            container_no
        )

        rows = self.parse_history_json(
            html
        )

        if not rows:
            return None

        for row in rows:

            returned_container = (
                row.get("CONTAINER NO")
                or row.get("container_no")
            )

            if not returned_container:
                continue

            returned_container = str(
                returned_container
            ).strip().upper()

            if returned_container == container_no:

                return row.get("pid")

        return None

    # ==================================================
    # CONTAINER DETAILS
    # ==================================================

    def get_container_details(self, pid):

        params = {
            "cntrPK": str(pid),
            "method": "C",
            "BU": "SAPT",
        }

        response = self.session.post(
            self.DETAILS_URL,
            data=params,
            timeout=30
        )

        print("Details Status:", response.status_code)

        response.raise_for_status()

        return response.text

    # ==================================================
    # PARSE CONTAINER DETAILS
    # ==================================================

    def parse_container_details(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        table = soup.find(
            "table",
            id="tblcntr"
        )

        if not table:
            return {}

        details = {}

        rows = table.find_all("tr")

        for row in rows:

            cells = row.find_all("td")

            if len(cells) < 4:
                continue

            # SAPT table is arranged:
            #
            # Label | Value | Empty | Label | Value

            pairs = [
                (cells[0], cells[1]),
                (cells[3], cells[4])
            ]

            for label_cell, value_cell in pairs:

                label = label_cell.get_text(
                    " ",
                    strip=True
                )

                value = value_cell.get_text(
                    " ",
                    strip=True
                )

                if label:
                    details[label] = value

        return details

    # ==================================================
    # COMPLETE CONTAINER INFO
    # ==================================================

    def get_container_info(self, container):

        container = str(
            container
        ).strip().upper()

        # ------------------------------------------------
        # STEP 1: HISTORY
        # ------------------------------------------------

        history_html = self.get_container_history(
            container
        )

        if not history_html:

            raise Exception(
                f"No history response for {container}"
            )

        # ------------------------------------------------
        # STEP 2: PARSE HISTORY
        # ------------------------------------------------

        rows = self.parse_history_json(
            history_html
        )

        if not rows:

            return None

        # ------------------------------------------------
        # STEP 3: PID
        # ------------------------------------------------

        row = rows[0]

        pid = row.get("pid")

        if not pid:

            return None

        # ------------------------------------------------
        # STEP 4: DETAILS
        # ------------------------------------------------

        details_html = self.get_container_details(
            pid
        )

        if not details_html:

            raise Exception(
                f"No details response for PID {pid}"
            )

        # ------------------------------------------------
        # STEP 5: PARSE DETAILS
        # ------------------------------------------------

        details = self.parse_container_details(
            details_html
        )

        if not details:

            raise Exception(
                f"Could not parse details for {container}"
            )

        # ------------------------------------------------
        # ADD PID
        # ------------------------------------------------

        details["pid"] = pid

        # ------------------------------------------------
        # ENSURE CONTAINER NUMBER
        # ------------------------------------------------

        if not details.get("Container No."):

            details["Container No."] = container

        return details