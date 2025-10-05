"""
Unit tests for data_pipeline_agent_lib.utils.logging_config module.
"""

import pytest
import logging
from datetime import datetime, timedelta
from data_pipeline_agent_lib.utils.logging_config import DPLLogger, setup_logging


class TestDPLLogger:
    """Test suite for DPLLogger class."""
    
    def test_logger_initialization(self):
        """Test that logger initializes correctly."""
        logger = DPLLogger("test_module")
        assert logger.logger is not None
        assert logger.logger.name == "data_pipeline_agent.test_module"
    
    def test_logger_default_level(self):
        """Test that default logging level is INFO."""
        logger = DPLLogger("test_module")
        assert logger.logger.level == logging.INFO
    
    def test_logger_custom_level(self):
        """Test that custom logging level is set correctly."""
        logger = DPLLogger("test_module", level=logging.DEBUG)
        assert logger.logger.level == logging.DEBUG
    
    def test_debug_logging(self, caplog):
        """Test DEBUG level logging."""
        logger = DPLLogger("test_module", level=logging.DEBUG)
        
        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message", test_key="test_value")
        
        assert "Debug message" in caplog.text
    
    def test_info_logging(self, caplog):
        """Test INFO level logging."""
        logger = DPLLogger("test_module")
        
        with caplog.at_level(logging.INFO):
            logger.info("Info message", component="test")
        
        assert "Info message" in caplog.text
    
    def test_warning_logging(self, caplog):
        """Test WARNING level logging."""
        logger = DPLLogger("test_module")
        
        with caplog.at_level(logging.WARNING):
            logger.warning("Warning message", issue="test_issue")
        
        assert "Warning message" in caplog.text
    
    def test_error_logging(self, caplog):
        """Test ERROR level logging."""
        logger = DPLLogger("test_module")
        
        with caplog.at_level(logging.ERROR):
            logger.error("Error message", error_code=500)
        
        assert "Error message" in caplog.text
    
    def test_critical_logging(self, caplog):
        """Test CRITICAL level logging."""
        logger = DPLLogger("test_module")
        
        with caplog.at_level(logging.CRITICAL):
            logger.critical("Critical message")
        
        assert "Critical message" in caplog.text
    
    def test_logging_with_extra_context(self, caplog):
        """Test logging with additional context."""
        logger = DPLLogger("test_module")
        
        with caplog.at_level(logging.INFO):
            logger.info(
                "Processing pipeline",
                pipeline_name="test_pipeline",
                entity="visits",
                records=1000
            )
        
        assert "Processing pipeline" in caplog.text
    
    def test_log_timing(self, caplog):
        """Test log_timing method."""
        logger = DPLLogger("test_module")
        start_time = datetime.utcnow() - timedelta(seconds=2)
        
        with caplog.at_level(logging.INFO):
            logger.log_timing(start_time, "test_operation")
        
        assert "test_operation" in caplog.text
        assert "completed" in caplog.text


class TestSetupLogging:
    """Test suite for setup_logging function."""
    
    def test_setup_logging_default_level(self):
        """Test setup_logging with default level."""
        setup_logging()
        root_logger = logging.getLogger("data_pipeline_agent")
        assert root_logger.level == logging.INFO
    
    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level."""
        setup_logging(logging.DEBUG)
        root_logger = logging.getLogger("data_pipeline_agent")
        assert root_logger.level == logging.DEBUG
    
    def test_setup_logging_idempotent(self):
        """Test that setup_logging can be called multiple times safely."""
        setup_logging(logging.INFO)
        setup_logging(logging.DEBUG)
        # Should not raise any errors
        assert True


@pytest.mark.integration
class TestLoggingIntegration:
    """Integration tests for logging system."""
    
    def test_multiple_loggers_isolation(self, caplog):
        """Test that multiple loggers work independently."""
        logger1 = DPLLogger("module1")
        logger2 = DPLLogger("module2")
        
        with caplog.at_level(logging.INFO):
            logger1.info("Message from module1")
            logger2.info("Message from module2")
        
        assert "module1" in caplog.text
        assert "module2" in caplog.text
    
    def test_logging_performance(self):
        """Test that logging doesn't significantly impact performance."""
        logger = DPLLogger("performance_test")
        
        start = datetime.utcnow()
        for i in range(1000):
            logger.debug(f"Test message {i}")
        duration = (datetime.utcnow() - start).total_seconds()
        
        # Should complete 1000 log calls in less than 1 second
        assert duration < 1.0

