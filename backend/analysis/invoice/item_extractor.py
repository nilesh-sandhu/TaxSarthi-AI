import re


class ItemExtractor:

    @staticmethod
    def extract(text: str):

        items = []

        # --------------------------------------------------
        # Example Pattern
        # Description  HSN  Qty  Rate
        # --------------------------------------------------

        pattern = re.compile(

            r"([A-Za-z0-9\s\-\(\)]+?)\s+"
            r"(\d{4,8})\s+"
            r"(\d+)\s+"
            r"([\d,]+(?:\.\d+)?)",

            re.MULTILINE,

        )

        matches = pattern.findall(text)

        for match in matches:

            description = match[0].strip()

            hsn = match[1]

            qty = int(match[2])

            rate = float(

                match[3].replace(",", "")

            )

            taxable = qty * rate

            items.append({

                "description": description,

                "hsn": hsn,

                "quantity": qty,

                "rate": rate,

                "taxable_value": taxable,

            })

        return items