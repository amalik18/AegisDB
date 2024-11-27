from aegis_db import AegisDB, Config
import pytest

class AegisDBTest():
    def __init__(self) -> None:
        self.config = Config(DATABASE_FILE='fhe_db_test.sqlite')
        self.db = AegisDB(config=self.config)
    
    @pytest.parametrize('key, value', [('a', 10), ('b', 20), ('c', 10), ('d', 30)])
    def test_put(self, key: str, value: int) -> None:
        self.db.put(key, value)
        assert self.db.get(key) == value
        
