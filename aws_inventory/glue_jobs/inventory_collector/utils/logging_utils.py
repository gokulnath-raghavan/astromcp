import logging
import sys
from typing import Optional
from datetime import datetime

class GlueJobLogger:
    """Custom logger for AWS Glue jobs"""
    
    def __init__(
        self,
        job_name: str,
        log_level: int = logging.INFO,
        log_format: Optional[str] = None
    ):
        """Initialize the logger
        
        Args:
            job_name: Name of the Glue job
            log_level: Logging level (default: INFO)
            log_format: Optional custom log format
        """
        self.job_name = job_name
        self.logger = logging.getLogger(job_name)
        self.logger.setLevel(log_level)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Set log format
        if log_format is None:
            log_format = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "Job: %(job_name)s - %(message)s"
            )
            
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(console_handler)
        
        # Add job name to log context
        self.logger = logging.LoggerAdapter(
            self.logger,
            {"job_name": job_name}
        )
        
    def info(self, message: str, **kwargs) -> None:
        """Log info message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.info(message, extra=kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.warning(message, extra=kwargs)
        
    def error(self, message: str, **kwargs) -> None:
        """Log error message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.error(message, extra=kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.critical(message, extra=kwargs)
        
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.debug(message, extra=kwargs)
        
    def exception(self, message: str, **kwargs) -> None:
        """Log exception message
        
        Args:
            message: Log message
            **kwargs: Additional context
        """
        self.logger.exception(message, extra=kwargs)
        
    def log_metric(self, metric_name: str, value: float, **kwargs) -> None:
        """Log custom metric
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            **kwargs: Additional context
        """
        self.info(
            f"METRIC: {metric_name}={value}",
            metric_name=metric_name,
            metric_value=value,
            **kwargs
        )
        
    def log_duration(self, operation: str, start_time: datetime, **kwargs) -> None:
        """Log operation duration
        
        Args:
            operation: Name of the operation
            start_time: Start time of the operation
            **kwargs: Additional context
        """
        duration = (datetime.now() - start_time).total_seconds()
        self.log_metric(
            f"{operation}_duration_seconds",
            duration,
            operation=operation,
            **kwargs
        )
        
    def log_data_quality(
        self,
        table_name: str,
        total_records: int,
        valid_records: int,
        invalid_records: int,
        **kwargs
    ) -> None:
        """Log data quality metrics
        
        Args:
            table_name: Name of the table
            total_records: Total number of records
            valid_records: Number of valid records
            invalid_records: Number of invalid records
            **kwargs: Additional context
        """
        self.log_metric(
            f"{table_name}_total_records",
            total_records,
            table_name=table_name,
            **kwargs
        )
        self.log_metric(
            f"{table_name}_valid_records",
            valid_records,
            table_name=table_name,
            **kwargs
        )
        self.log_metric(
            f"{table_name}_invalid_records",
            invalid_records,
            table_name=table_name,
            **kwargs
        )
        if total_records > 0:
            quality_score = (valid_records / total_records) * 100
            self.log_metric(
                f"{table_name}_quality_score",
                quality_score,
                table_name=table_name,
                **kwargs
            )
            
    def log_job_status(
        self,
        status: str,
        start_time: datetime,
        records_processed: int = 0,
        **kwargs
    ) -> None:
        """Log job status and metrics
        
        Args:
            status: Job status
            start_time: Job start time
            records_processed: Number of records processed
            **kwargs: Additional context
        """
        self.info(
            f"Job status: {status}",
            job_status=status,
            **kwargs
        )
        if records_processed > 0:
            self.log_metric(
                "records_processed",
                records_processed,
                **kwargs
            )
        self.log_duration(
            "job_execution",
            start_time,
            **kwargs
        ) 