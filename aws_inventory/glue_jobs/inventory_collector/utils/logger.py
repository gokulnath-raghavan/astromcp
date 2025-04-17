import logging
from typing import Optional
from datetime import datetime

class GlueJobLogger:
    """
    Custom logger for AWS Glue jobs.
    """
    
    def __init__(self, job_name: str, log_level: int = logging.INFO):
        """
        Initialize the logger.
        
        Args:
            job_name: Name of the Glue job
            log_level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger(job_name)
        self.logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Initialize metrics
        self.metrics = {
            "start_time": None,
            "end_time": None,
            "records_processed": 0,
            "errors": []
        }
    
    def start_job(self):
        """Log job start and initialize metrics."""
        self.metrics["start_time"] = datetime.utcnow()
        self.logger.info("Starting Glue job")
    
    def end_job(self):
        """Log job end and calculate duration."""
        self.metrics["end_time"] = datetime.utcnow()
        duration = (self.metrics["end_time"] - self.metrics["start_time"]).total_seconds()
        self.logger.info(f"Job completed in {duration:.2f} seconds")
        self.logger.info(f"Total records processed: {self.metrics['records_processed']}")
        if self.metrics["errors"]:
            self.logger.warning(f"Encountered {len(self.metrics['errors'])} errors")
    
    def log_metric(self, metric_name: str, value: int):
        """
        Log a metric value.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
        """
        self.metrics[metric_name] = value
        self.logger.info(f"{metric_name}: {value}")
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """
        Log an error with context.
        
        Args:
            error: Exception object
            context: Optional context information
        """
        error_msg = str(error)
        if context:
            error_msg = f"{context}: {error_msg}"
        self.metrics["errors"].append(error_msg)
        self.logger.error(error_msg)
    
    def log_info(self, message: str):
        """
        Log an info message.
        
        Args:
            message: Info message
        """
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """
        Log a warning message.
        
        Args:
            message: Warning message
        """
        self.logger.warning(message)
    
    def get_metrics(self) -> dict:
        """
        Get all collected metrics.
        
        Returns:
            Dictionary of metrics
        """
        return self.metrics 