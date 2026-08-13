from sqlalchemy.orm import Session

from repositories.product_master import ProductMasterRepository
from repositories.product_alias import ProductAliasRepository
from repositories.hsn import HSNRepository


def global_search(
    query: str,
    db: Session,
):

    return {

        "products":
            ProductMasterRepository.search(
                db,
                query,
            ),

        "aliases":
            ProductAliasRepository.search(
                db,
                query,
            ),

        "hsn":
            HSNRepository.search(
                db,
                query,
            ),

    }