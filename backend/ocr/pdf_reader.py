import fitz


class PDFReader:

    # =====================================================
    # Extract Complete PDF Text
    # =====================================================

    @staticmethod
    def extract(file_path: str):

        text = ""

        document = fitz.open(file_path)

        for page in document:

            page_text = page.get_text()

            if page_text:
                text += page_text + "\n"

        document.close()

        return text.strip()

    # =====================================================
    # Extract Page-Wise Text
    # =====================================================

    @staticmethod
    def extract_pages(file_path: str):

        pages = []

        document = fitz.open(file_path)

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            page_text = page.get_text()

            pages.append(
                {
                    "page": page_number,
                    "text": page_text.strip(),
                }
            )

        document.close()

        return pages