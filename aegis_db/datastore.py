import sqlite3
from threading import RLock
from config import Config
from exceptions import DatabaseError, EncryptionError, KeyNotFoundError
from encryption import AegisEncryptorContext
from logger import logger
from concrete import fhe
from typing import Optional
import numpy as np


class AegisDB:
    """
    A NoSQL key-value store that supports fully homomorphic encryption.
    """
    def __init__(self):
        self.lock = RLock()
        self.connection = sqlite3.connect(Config.DATABASE_FILE, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_table()
        self.HE_context = AegisEncryptorContext()

    def _create_table(self):
        with self.lock:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value BLOB NOT NULL
                )
            ''')
            self.connection.commit()
            logger.info("Database table initialized.")

    def put(self, key: str, value: int):
        with self.lock:
            if not isinstance(value, int):
                raise ValueError("Value must be an integer.")
            try:
                encrypted_value = self.HE_context.encryptor_circuit.encrypt(np.array([value]))
                # Serialize the encrypted value
                encrypted_blob = self.HE_context.serialize(encrypted_value)
                logger.info(f'Encrypted value: {encrypted_blob}')

                self.cursor.execute('''
                    INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)
                ''', (key, encrypted_blob))
                self.connection.commit()
                logger.info(f"Inserted key '{key}' with encrypted value.")
            except Exception as e:
                logger.exception(f"Failed to put value into database")
                raise DatabaseError("Failed to put value into database.") from e

    def get(self, key: str) -> Optional[int]:
        with self.lock:
            self.cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
            row = self.cursor.fetchone()
            if row:
                encrypted_blob = row[0]
                try:
                    # Deserialize the encrypted value
                    encrypted_value = self.HE_context.deserialize(encrypted_blob)
                    # encrypted_value = self.HE_context.encryptor_circuit.deserialize_ciphertext(encrypted_blob)
                    decrypted_value = self.HE_context.encryptor_circuit.decrypt(encrypted_value)
                    logger.info(f"Retrieved and decrypted value for key '{key}'.")
                    return int(decrypted_value[0])
                except Exception as e:
                    logger.exception("Failed to decrypt value from database.")
                    raise EncryptionError("Failed to decrypt value from database.") from e
            else:
                logger.warning(f"Key '{key}' not found in the database.")
                return None

    def delete(self, key: str):
        with self.lock:
            self.cursor.execute('DELETE FROM kv_store WHERE key = ?', (key,))
            if self.cursor.rowcount == 0:
                logger.warning(f"Key '{key}' not found. Cannot delete.")
                raise KeyNotFoundError(f"Key '{key}' not found.")
            self.connection.commit()
            logger.info(f"Deleted key '{key}' from the database.")

    def add(self, key1: str, key2: str, result_key: str):
        with self.lock:
            encrypted_value1 = self._get_encrypted_value(key1)
            encrypted_value2 = self._get_encrypted_value(key2)

            try:
                # Perform homomorphic addition
                encrypted_result = self.HE_context.add_circuit.encrypt(
                    encrypted_value1,
                    encrypted_value2,
                )
                # Serialize the encrypted result
                encrypted_blob = self.HE_context.serialize(encrypted_result)

                self.cursor.execute('''
                    INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)
                ''', (result_key, encrypted_blob))
                self.connection.commit()
                logger.info(f"Stored the sum of '{key1}' and '{key2}' in '{result_key}'.")
            except Exception as e:
                logger.exception("Failed to perform addition.")
                raise DatabaseError("Failed to perform addition.") from e

    def multiply(self, key1: str, key2: str, result_key: str):
        with self.lock:
            encrypted_value1 = self._get_encrypted_value(key1)
            encrypted_value2 = self._get_encrypted_value(key2)

            try:
                # Perform homomorphic multiplication
                encrypted_result = self.HE_context.multiply_circuit.encrypt(
                    encrypted_value1,
                    encrypted_value2,
                )
                # Serialize the encrypted result
                encrypted_blob = self.HE_context.serialize(encrypted_result)

                self.cursor.execute('''
                    INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)
                ''', (result_key, encrypted_blob))
                self.connection.commit()
                logger.info(f"Stored the product of '{key1}' and '{key2}' in '{result_key}'.")
            except Exception as e:
                logger.exception("Failed to perform multiplication.")
                raise DatabaseError("Failed to perform multiplication.") from e

    def _get_encrypted_value(self, key: str):
        self.cursor.execute('SELECT value FROM kv_store WHERE key = ?', (key,))
        row = self.cursor.fetchone()
        if row:
            encrypted_blob = row[0]
            try:
                # Deserialize the encrypted value
                encrypted_value = self.HE_context.deserialize(encrypted_blob)
                return encrypted_value
            except Exception as e:
                logger.exception(f"Failed to deserialize encrypted value for key '{key}'.")
                raise EncryptionError(f"Failed to deserialize encrypted value for key '{key}'.") from e
        else:
            logger.error(f"Key '{key}' not found in the database.")
            raise KeyNotFoundError(f"Key '{key}' not found in the database.")

    def close(self):
        with self.lock:
            self.connection.close()
            logger.info("Database connection closed.")