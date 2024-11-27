from threading import Lock
from concrete import fhe
from logger import logger
import numpy as np
from exceptions import EncryptionError
import time

class AegisEncryptorContext:
    """
    Manages the encryption context and compiled circuits for homomorphic operations.
    Thread-safe singleton implementation to ensure only one context exists.
    """
    _instance = None
    _lock: Lock = Lock()
    encryptor_circuit: fhe.Circuit
    add_circuit: fhe.Circuit
    multiply_circuit: fhe.Circuit

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        print('made it in the context class')
        if self._initialized:
            return  # Avoid re-initialization

        try:
            # Define FHE functions
            @fhe.compiler({"x": "encrypted"})
            def encrypt_func(x):
                return x

            @fhe.compiler({"x": "encrypted", "y": "encrypted"})
            def add_func(x, y):
                return x + y

            @fhe.compiler({"x": "encrypted", "y": "encrypted"})
            def multiply_func(x, y):
                return x * y

            # Use minimal input set for testing
            inputset = [np.array([i], dtype=np.uint8) for i in range(256)]

            # Compile circuits
            logger.info("Compiling encryption circuit...")
            self.encryptor_circuit = encrypt_func.compile(
                inputset=inputset
            )

            logger.info("Compiling addition circuit...")
            self.add_circuit = add_func.compile(
                inputset=[(i, j) for i in inputset for j in inputset]
            )

            logger.info("Compiling multiplication circuit...")
            self.multiply_circuit = multiply_func.compile(
                inputset=[(i, j) for i in inputset for j in inputset],
            )

            self._initialized = True
            print('made it past initiation and compilation')
            time.sleep(5)
        except Exception as e:
            logger.exception("Failed to initialize encryption context.")
            raise EncryptionError("Failed to initialize encryption context.") from e
    
    def serialize(self, encrypted_value: fhe.Value) -> bytes:
        return encrypted_value.serialize()
    
    def deserialize(self, encrypted_blob: bytes) -> fhe.Value:
        return fhe.Value.deserialize(encrypted_blob)
    