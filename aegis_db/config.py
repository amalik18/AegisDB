import os

class Config:
    # Database settings
    DATABASE_FILE = os.getenv('DATABASE_FILE', 'fhe_db.sqlite')

    # Encryption settings
    INPUT_RANGE_START = int(os.getenv('INPUT_RANGE_START', 0))
    INPUT_RANGE_END = int(os.getenv('INPUT_RANGE_END', 255))  # Adjusted for uint8

    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')