from seed.seed_categories import seed_categories
from seed.seed_hsn import seed_hsn
from seed.seed_gst_slabs import seed_gst_slabs
from seed.seed_products import seed_products
from seed.seed_product_alias import seed_product_alias


def run():

    print("=" * 60)
    print("🚀 TaxSarthi AI Database Seeding")
    print("=" * 60)

    print("\n[1/5] Seeding Categories...")
    seed_categories()

    print("\n[2/5] Seeding HSN Master...")
    seed_hsn()

    print("\n[3/5] Seeding GST Slabs...")
    seed_gst_slabs()

    print("\n[4/5] Seeding Products...")
    seed_products()

    print("\n[5/5] Seeding Product Aliases...")
    seed_product_alias()

    print("\n" + "=" * 60)
    print("✅ Database Seeding Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    run()