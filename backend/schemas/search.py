from pydantic import BaseModel


class SearchResponse(BaseModel):

    query: str

    products: list = []

    hsn: list = []

    faq: list = []

    gst_returns: list = []

    total_results: int