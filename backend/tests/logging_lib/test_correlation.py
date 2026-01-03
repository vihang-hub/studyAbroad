"""
Tests for Correlation ID Management

Tests context-based correlation ID tracking.
"""

from logging_lib.correlation import (
    get_correlation_id,
    set_correlation_id,
    clear_correlation_id,
    CorrelationContext,
)


class TestCorrelationID:
    """Test correlation ID management"""

    def setup_method(self):
        """Clear correlation ID before each test"""
        clear_correlation_id()

    def teardown_method(self):
        """Clear correlation ID after each test"""
        clear_correlation_id()

    def test_get_correlation_id_generates_if_none(self):
        """get_correlation_id() generates new ID if none set"""
        correlation_id = get_correlation_id()

        assert correlation_id is not None
        assert len(correlation_id) > 0

    def test_get_correlation_id_returns_same_id(self):
        """get_correlation_id() returns same ID in same context"""
        id1 = get_correlation_id()
        id2 = get_correlation_id()

        assert id1 == id2

    def test_set_correlation_id(self):
        """set_correlation_id() sets custom ID"""
        custom_id = 'custom-correlation-id'
        set_correlation_id(custom_id)

        assert get_correlation_id() == custom_id

    def test_clear_correlation_id(self):
        """clear_correlation_id() removes ID"""
        set_correlation_id('test-id')
        clear_correlation_id()

        # Next call generates new ID
        new_id = get_correlation_id()
        assert new_id != 'test-id'

    def test_correlation_context_generates_id(self):
        """CorrelationContext generates new ID"""
        with CorrelationContext() as ctx:
            correlation_id = get_correlation_id()
            assert correlation_id == ctx.correlation_id

    def test_correlation_context_uses_custom_id(self):
        """CorrelationContext uses provided ID"""
        custom_id = 'my-custom-id'

        with CorrelationContext(correlation_id=custom_id):
            assert get_correlation_id() == custom_id

    def test_correlation_context_restores_previous_id(self):
        """CorrelationContext restores previous ID on exit"""
        original_id = 'original-id'
        set_correlation_id(original_id)

        with CorrelationContext(correlation_id='temporary-id'):
            assert get_correlation_id() == 'temporary-id'

        assert get_correlation_id() == original_id

    def test_nested_correlation_contexts(self):
        """Nested contexts maintain separate IDs"""
        with CorrelationContext(correlation_id='outer'):
            assert get_correlation_id() == 'outer'

            with CorrelationContext(correlation_id='inner'):
                assert get_correlation_id() == 'inner'

            assert get_correlation_id() == 'outer'
