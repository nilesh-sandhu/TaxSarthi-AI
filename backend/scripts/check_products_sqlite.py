import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "taxsarthi.db",
)


def main():
    if not os.path.exists(DB_PATH):
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM product_master")
        total = cur.fetchone()[0]
    except Exception as e:
        print("Error reading product_master:", e)
        conn.close()
        return

    print(f"product_master rows = {total}")

    try:
        cur.execute(
            "SELECT product_name, hsn_code, gst_rate FROM product_master LIMIT 20"
        )
        rows = cur.fetchall()

        if not rows:
            print("No product rows found.")
        else:
            for r in rows:
                print(f"product_name={r[0]!r}, hsn_code={r[1]!r}, gst_rate={r[2]!r}")

    except Exception as e:
        print("Error querying products:", e)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
