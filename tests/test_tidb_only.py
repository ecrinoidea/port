import unittest
from unittest.mock import patch

import model


class TiDBOnlyDatabaseTests(unittest.TestCase):
    def test_get_db_requires_tidb_configuration(self):
        config_stub = type(
            "ConfigStub",
            (),
            {
                "TIDB_HOST": None,
                "TIDB_PORT": 4000,
                "TIDB_USER": None,
                "TIDB_PASSWORD": None,
                "TIDB_DB": "db_porto",
                "TIDB_SSL_CA": None,
            },
        )

        with patch.object(model, "Config", config_stub):
            with self.assertRaisesRegex(RuntimeError, "TiDB"):
                model.get_db()


if __name__ == "__main__":
    unittest.main()
