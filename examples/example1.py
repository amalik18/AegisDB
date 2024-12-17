from aegis_db.datastore import AegisDB
from aegis_db.logger import logger
from aegis_db.exceptions import DatabaseError, EncryptionError, KeyNotFoundError
import time

def main():
    # Initialize the database
    db = AegisDB()

    try:
        # Insert values into the database
        time1 = time.time()
        db.put('a', 10)
        print(time.time() - time1)
        time.sleep(5)
        db.put('b', 10)
        db.put('c', 10)  # Duplicate value to test search
        db.put('d', 30)

        # Retrieve values from the database
        time1 = time.time()
        value_a = db.get('a')
        print(time.time() - time1)
        time.sleep(5)
        value_b = db.get('b')
        value_c = db.get('c')
        value_d = db.get('d')
        print(f"Decrypted value of 'a': {value_a}")
        print(f"Decrypted value of 'b': {value_b}")
        print(f"Decrypted value of 'c': {value_c}")
        print(f"Decrypted value of 'd': {value_d}")

        # Perform homomorphic addition
        time1 = time.time()
        db.add('a', 'b', 'sum_ab')
        print(time.time() - time1)
        time.sleep(5)
        sum_result = db.get('sum_ab')
        print(f"Decrypted sum of 'a' and 'b': {sum_result}")

        # Perform homomorphic multiplication
        time1 = time.time()
        db.multiply('a', 'b', 'product_ab')
        print(time.time() - time1)
        time.sleep(5)
        product_result = db.get('product_ab')
        print(f"Decrypted product of 'a' and 'b': {product_result}")

        # Perform search
        time1 = time.time()
        search_value = 10
        print(time.time() - time1)
        time.sleep(5)
        matching_keys = db.search(search_value)
        print(f"Keys with value {search_value}: {matching_keys}")

        # Delete a key
        time1 = time.time()
        db.delete('a')
        print(time.time() - time1)
        time.sleep(5)
        value_a_after_delete = db.get('a')
        print(f"Value of 'a' after deletion: {value_a_after_delete}")


        time1 = time.time()
        t = db.compare('b', 'c')
        print(time.time() - time1)
        print(f'Comparison Result: {t}')

        # Perform search
        search_value = 10
        time1 = time.time()
        matching_keys = db.search(search_value)
        print(time.time() - time1)
        time.sleep(5)
        print(f"Keys with value {search_value}: {matching_keys}")

    except (DatabaseError, EncryptionError, KeyNotFoundError, ValueError) as e:
        logger.error(e)

    finally:
        db.close()

if __name__ == "__main__":
    main()