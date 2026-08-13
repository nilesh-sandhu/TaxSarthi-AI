import pdfplumber
import pandas as pd
import re
from pathlib import Path

# -----------------------------
# File Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "HSN-Codes-for-GST-Enrolment.pdf"
CSV_PATH = BASE_DIR / "data" / "hsn_master.csv"

records = []

print("Reading PDF...")

with pdfplumber.open(PDF_PATH) as pdf:

    for page_number, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            # Remove repeated headers
            if (
                "SL NO" in line
                or "HS CODE DESCRIPTION" in line
                or "HSN CODE AND ITEM NAME" in line
            ):
                continue

            # Pattern:
            # 1 0101 Live horses
            # 15035 8452.10.11 With electronic controls

            match = re.match(
                r"^\d+\s+([0-9. ]+)\s+(.*)$",
                line
            )

            if match:

                hsn = match.group(1)

                description = match.group(2)

                hsn = hsn.replace(" ", "")

                records.append(
                    {
                        "hsn_code": hsn,
                        "description": description
                    }
                )

print("Cleaning...")

df = pd.DataFrame(records)

df.drop_duplicates(inplace=True)

df = df[df["hsn_code"].str.len() >= 4]

df.to_csv(
    CSV_PATH,
    index=False,
    encoding="utf-8"
)

print("=================================")
print("Conversion Complete")
print("Total Records :", len(df))
print("Saved :", CSV_PATH)
print("=================================")