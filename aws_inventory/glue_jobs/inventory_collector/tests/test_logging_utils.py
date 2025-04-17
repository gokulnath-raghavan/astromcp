import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from utils.logging_utils import GlueJobLogger

@pytest.fixture
def logger():
    """Create a GlueJobLogger instance"""
    return GlueJobLogger("test-job")

def test_logger_initialization():
    """Test logger initialization"""
    logger = GlueJobLogger("test-job", log_level=10)
    assert logger.job_name == "test-job"
    assert logger.logger.logger.level == 10

def test_info_logging(logger):
    """Test info logging"""
    with patch.object(logger.logger, "info") as mock_info:
        logger.info("Test message", extra_context="value")
        mock_info.assert_called_once()
        assert "Test message" in str(mock_info.call_args[0])
        assert "extra_context" in str(mock_info.call_args[1])

def test_warning_logging(logger):
    """Test warning logging"""
    with patch.object(logger.logger, "warning") as mock_warning:
        logger.warning("Test warning", extra_context="value")
        mock_warning.assert_called_once()
        assert "Test warning" in str(mock_warning.call_args[0])

def test_error_logging(logger):
    """Test error logging"""
    with patch.object(logger.logger, "error") as mock_error:
        logger.error("Test error", extra_context="value")
        mock_error.assert_called_once()
        assert "Test error" in str(mock_error.call_args[0])

def test_critical_logging(logger):
    """Test critical logging"""
    with patch.object(logger.logger, "critical") as mock_critical:
        logger.critical("Test critical", extra_context="value")
        mock_critical.assert_called_once()
        assert "Test critical" in str(mock_critical.call_args[0])

def test_debug_logging(logger):
    """Test debug logging"""
    with patch.object(logger.logger, "debug") as mock_debug:
        logger.debug("Test debug", extra_context="value")
        mock_debug.assert_called_once()
        assert "Test debug" in str(mock_debug.call_args[0])

def test_exception_logging(logger):
    """Test exception logging"""
    with patch.object(logger.logger, "exception") as mock_exception:
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("Test exception", extra_context="value")
        mock_exception.assert_called_once()
        assert "Test exception" in str(mock_exception.call_args[0])

def test_metric_logging(logger):
    """Test metric logging"""
    with patch.object(logger.logger, "info") as mock_info:
        logger.log_metric("test_metric", 42.0, extra_context="value")
        mock_info.assert_called_once()
        assert "METRIC: test_metric=42.0" in str(mock_info.call_args[0])
        assert "metric_name" in str(mock_info.call_args[1])
        assert "metric_value" in str(mock_info.call_args[1])

def test_duration_logging(logger):
    """Test duration logging"""
    with patch.object(logger.logger, "info") as mock_info:
        start_time = datetime.now() - timedelta(seconds=5)
        logger.log_duration("test_operation", start_time, extra_context="value")
        mock_info.assert_called_once()
        assert "test_operation_duration_seconds" in str(mock_info.call_args[0])
        assert "operation" in str(mock_info.call_args[1])

def test_data_quality_logging(logger):
    """Test data quality logging"""
    with patch.object(logger.logger, "info") as mock_info:
        logger.log_data_quality(
            "test_table",
            100,
            90,
            10,
            extra_context="value"
        )
        assert mock_info.call_count == 4
        calls = [str(call[0]) for call in mock_info.call_args_list]
        assert any("test_table_total_records=100" in call for call in calls)
        assert any("test_table_valid_records=90" in call for call in calls)
        assert any("test_table_invalid_records=10" in call for call in calls)
        assert any("test_table_quality_score=90.0" in call for call in calls)

def test_job_status_logging(logger):
    """Test job status logging"""
    with patch.object(logger.logger, "info") as mock_info:
        start_time = datetime.now() - timedelta(seconds=5)
        logger.log_job_status(
            "COMPLETED",
            start_time,
            1000,
            extra_context="value"
        )
        assert mock_info.call_count == 3
        calls = [str(call[0]) for call in mock_info.call_args_list]
        assert any("Job status: COMPLETED" in call for call in calls)
        assert any("records_processed=1000" in call for call in calls)
        assert any("job_execution_duration_seconds" in call for call in calls)

def test_custom_log_format():
    """Test custom log format"""
    custom_format = "%(levelname)s - %(message)s"
    logger = GlueJobLogger("test-job", log_format=custom_format)
    assert logger.logger.logger.handlers[0].formatter._fmt == custom_format

def test_logger_with_multiple_handlers():
    """Test logger with multiple handlers"""
    logger = GlueJobLogger("test-job")
    assert len(logger.logger.logger.handlers) == 1
    logger = GlueJobLogger("test-job")
    assert len(logger.logger.logger.handlers) == 1 