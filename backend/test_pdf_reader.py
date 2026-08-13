from ocr.pdf_reader import PDFReader

text = PDFReader.extract(
    "uploads/documents/GST_Invoice_Template.pdf"
)

print(text)