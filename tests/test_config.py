import base64
import importlib
import os
import tempfile
import unittest
from unittest.mock import patch

import config


class ConfigTiDBSSLTests(unittest.TestCase):
    def test_config_reads_env_from_project_root_when_cwd_changes(self):
        original_cwd = os.getcwd()
        temp_dir = tempfile.mkdtemp()
        try:
            os.chdir(temp_dir)
            with patch.dict(os.environ, {}, clear=True):
                reloaded = importlib.reload(config)
                self.assertTrue(reloaded.Config.TIDB_HOST)
                self.assertTrue(reloaded.Config.TIDB_USER)
                self.assertTrue(reloaded.Config.TIDB_DB)
        finally:
            os.chdir(original_cwd)
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_tidb_ssl_ca_b64_invalid_rejected(self):
        invalid_b64 = 'not-a-valid-base64'

        with patch.dict(os.environ, {'TIDB_SSL_CA_B64': invalid_b64}, clear=False):
            reloaded = importlib.reload(config)
            self.assertIsNone(reloaded.Config.TIDB_SSL_CA)

    def test_tidb_ssl_ca_b64_valid_certificate_sets_path(self):
        cert = (
            '-----BEGIN CERTIFICATE-----\n'
            'MIIDdzCCAl+gAwIBAgIEbCUNeTANBgkqhkiG9w0BAQsFADBvMQswCQYDVQQGEwJV\n'
            'UzELMAkGA1UECAwCTlkxEDAOBgNVBAcMB05ldyBZb3JrMRcwFQYDVQQKDA5FeGFt\n'
            'cGxlIENvbXBhbnkxETAPBgNVBAsMCERldm9wczEVMBMGA1UEAwwMTXkgVGVzdCBD\n'
            'QTAeFw0yMTAzMjQwMDAwMDBaFw0yMjAzMjQwMDAwMDBaMG8xCzAJBgNVBAYTAlVT\n'
            'MQswCQYDVQQIDAJOWTEQMA4GA1UEBwwHTmV3IFlvcmsxFzAVBgNVBAoMDkV4YW1w\n'
            'bGUgQ29tcGFueTERMA8GA1UECwwIRGV2b3BzMRUwEwYDVQQDDAxNeSBUZXN0IENB\n'
            'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm2jZl9S7y3tZy1vzhZHk\n'
            'Z0C6y6HJj3Zk5o5+7Jcz2UwNfF1dF03lo+ncDlY7Zwjgpz9XunK0R0KDLcJxCoqE\n'
            'P1zugJHsua0w0od2lXn0GwQpZ1cZ2AdxnnK6eh7nP5SLbbZ5klXeyr3YN9t/8c4ov\n'
            'g5YI0vPl5ejyZeVxevLT0S1PBfZqBb0vX2bQIDAQABo1AwTjAdBgNVHQ4EFgQU7D+\n'
            '5Y+4+1tkYJfM0Bcs92xxU3O4kwHwYDVR0jBBgwFoAU7D+5Y+4+1tkYJfM0Bcs92xx\n'
            'U3O4kwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEALzGuK5RpYx1Oyv\n'
            'O8/XsIL1h2U3V4NCkBzzP65B0zYFU8+9YVP0H5H0Qx7zUgW9eQj2nC+gz2A0PKv5N\n'
            'q2YdeZc7T8ZPG9hcz2kT4AJ9Qj8xq/LQjjoIhR6T0TjPq+wbpCI0nYodzA==\n'
            '-----END CERTIFICATE-----\n'
        )
        encoded = base64.b64encode(cert.encode('utf-8')).decode('utf-8')

        with patch.dict(os.environ, {'TIDB_SSL_CA_B64': encoded}, clear=False):
            reloaded = importlib.reload(config)
            self.assertIsNotNone(reloaded.Config.TIDB_SSL_CA)
            self.assertTrue(reloaded.Config.TIDB_SSL_CA.endswith('.pem'))
            self.assertTrue(os.path.exists(reloaded.Config.TIDB_SSL_CA))
            os.remove(reloaded.Config.TIDB_SSL_CA)


if __name__ == '__main__':
    unittest.main()
