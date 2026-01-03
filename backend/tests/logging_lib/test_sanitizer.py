"""
Tests for Log Data Sanitizer

Tests sensitive data redaction.
"""

from logging_lib.sanitizer import sanitize_log_data


class TestSanitizeLogData:
    """Test log data sanitization"""

    def test_sanitize_password_field(self):
        """Password field is redacted"""
        data = {'username': 'john', 'password': 'secret123'}
        sanitized = sanitize_log_data(data)

        assert sanitized['username'] == 'john'
        assert sanitized['password'] == '[REDACTED]'

    def test_sanitize_api_key_field(self):
        """API key field is redacted"""
        data = {'service': 'google', 'api_key': 'AIzaSyXXXXX'}
        sanitized = sanitize_log_data(data)

        assert sanitized['service'] == 'google'
        assert sanitized['api_key'] == '[REDACTED]'

    def test_sanitize_token_field(self):
        """Token field is redacted"""
        data = {'user_id': '123', 'access_token': 'eyJhbGc...'}
        sanitized = sanitize_log_data(data)

        assert sanitized['user_id'] == '123'
        assert sanitized['access_token'] == '[REDACTED]'

    def test_sanitize_secret_field(self):
        """Secret field is redacted"""
        data = {'app': 'myapp', 'client_secret': 'abcdef123456'}
        sanitized = sanitize_log_data(data)

        assert sanitized['app'] == 'myapp'
        assert sanitized['client_secret'] == '[REDACTED]'

    def test_sanitize_credit_card_field(self):
        """Credit card field is redacted"""
        data = {'user': 'john', 'credit_card': '4111111111111111'}
        sanitized = sanitize_log_data(data)

        assert sanitized['user'] == 'john'
        assert sanitized['credit_card'] == '[REDACTED]'

    def test_sanitize_nested_dict(self):
        """Nested dictionaries are sanitized"""
        data = {
            'user': {'username': 'john', 'password': 'secret123'},
            'auth': {'token': 'xyz789'},
        }
        sanitized = sanitize_log_data(data)

        assert sanitized['user']['username'] == 'john'
        assert sanitized['user']['password'] == '[REDACTED]'
        assert sanitized['auth']['token'] == '[REDACTED]'

    def test_sanitize_list_of_dicts(self):
        """Lists of dictionaries are sanitized"""
        data = [
            {'user': 'alice', 'api_key': 'key1'},
            {'user': 'bob', 'api_key': 'key2'},
        ]
        sanitized = sanitize_log_data(data)

        assert sanitized[0]['user'] == 'alice'
        assert sanitized[0]['api_key'] == '[REDACTED]'
        assert sanitized[1]['user'] == 'bob'
        assert sanitized[1]['api_key'] == '[REDACTED]'

    def test_sanitize_case_insensitive(self):
        """Sanitization is case insensitive"""
        data = {'Password': 'secret', 'API_KEY': 'key123', 'Token': 'xyz'}
        sanitized = sanitize_log_data(data)

        assert sanitized['Password'] == '[REDACTED]'
        assert sanitized['API_KEY'] == '[REDACTED]'
        assert sanitized['Token'] == '[REDACTED]'

    def test_primitives_unchanged(self):
        """Primitive values are unchanged"""
        assert sanitize_log_data('hello') == 'hello'
        assert sanitize_log_data(123) == 123
        assert sanitize_log_data(45.67) == 45.67
        assert sanitize_log_data(True) is True
        assert sanitize_log_data(None) is None

    def test_non_sensitive_dict_unchanged(self):
        """Dictionaries without sensitive fields are unchanged"""
        data = {'user_id': '123', 'email': 'test@example.com', 'count': 42}
        sanitized = sanitize_log_data(data)

        assert sanitized == data
