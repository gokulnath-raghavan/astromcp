from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnull, sum as spark_sum
from typing import Dict, List, Optional
import logging

class DataQualityChecker:
    """
    Perform data quality checks on Spark DataFrames.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the data quality checker.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def check_null_values(self, df: DataFrame, columns: List[str]) -> Dict[str, int]:
        """
        Check for null values in specified columns.
        
        Args:
            df: Spark DataFrame
            columns: List of columns to check
            
        Returns:
            Dictionary with null counts per column
        """
        null_counts = {}
        for column in columns:
            null_count = df.filter(col(column).isNull()).count()
            null_counts[column] = null_count
            self.logger.info(f"Null values in {column}: {null_count}")
        
        return null_counts
    
    def check_empty_dataframe(self, df: DataFrame) -> bool:
        """
        Check if DataFrame is empty.
        
        Args:
            df: Spark DataFrame
            
        Returns:
            True if DataFrame is empty, False otherwise
        """
        is_empty = df.count() == 0
        if is_empty:
            self.logger.warning("DataFrame is empty")
        return is_empty
    
    def check_duplicates(self, df: DataFrame, key_columns: List[str]) -> int:
        """
        Check for duplicate rows based on key columns.
        
        Args:
            df: Spark DataFrame
            key_columns: List of columns to use as key
            
        Returns:
            Number of duplicate rows
        """
        duplicate_count = df.count() - df.dropDuplicates(key_columns).count()
        self.logger.info(f"Number of duplicate rows: {duplicate_count}")
        return duplicate_count
    
    def check_value_ranges(self, df: DataFrame, column_ranges: Dict[str, tuple]) -> Dict[str, int]:
        """
        Check if values in columns are within specified ranges.
        
        Args:
            df: Spark DataFrame
            column_ranges: Dictionary of column names and (min, max) tuples
            
        Returns:
            Dictionary with counts of values outside range per column
        """
        out_of_range_counts = {}
        for column, (min_val, max_val) in column_ranges.items():
            count = df.filter(
                (col(column) < min_val) | (col(column) > max_val)
            ).count()
            out_of_range_counts[column] = count
            self.logger.info(f"Values outside range in {column}: {count}")
        
        return out_of_range_counts
    
    def check_data_types(self, df: DataFrame, expected_types: Dict[str, str]) -> Dict[str, bool]:
        """
        Check if columns have expected data types.
        
        Args:
            df: Spark DataFrame
            expected_types: Dictionary of column names and expected types
            
        Returns:
            Dictionary indicating if each column's type matches expected
        """
        type_matches = {}
        for column, expected_type in expected_types.items():
            actual_type = df.schema[column].dataType.typeName()
            matches = actual_type == expected_type
            type_matches[column] = matches
            self.logger.info(f"Type match for {column}: {matches} (Expected: {expected_type}, Actual: {actual_type})")
        
        return type_matches
    
    def check_required_columns(self, df: DataFrame, required_columns: List[str]) -> List[str]:
        """
        Check if all required columns are present.
        
        Args:
            df: Spark DataFrame
            required_columns: List of required column names
            
        Returns:
            List of missing columns
        """
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.logger.warning(f"Missing required columns: {missing_columns}")
        return missing_columns
    
    def run_all_checks(self, df: DataFrame, config: Dict) -> Dict:
        """
        Run all data quality checks based on configuration.
        
        Args:
            df: Spark DataFrame
            config: Dictionary containing check configurations
            
        Returns:
            Dictionary with results of all checks
        """
        results = {}
        
        # Check for empty DataFrame
        results["is_empty"] = self.check_empty_dataframe(df)
        
        # Check required columns
        if "required_columns" in config:
            results["missing_columns"] = self.check_required_columns(df, config["required_columns"])
        
        # Check data types
        if "expected_types" in config:
            results["type_matches"] = self.check_data_types(df, config["expected_types"])
        
        # Check null values
        if "null_check_columns" in config:
            results["null_counts"] = self.check_null_values(df, config["null_check_columns"])
        
        # Check duplicates
        if "key_columns" in config:
            results["duplicate_count"] = self.check_duplicates(df, config["key_columns"])
        
        # Check value ranges
        if "column_ranges" in config:
            results["out_of_range_counts"] = self.check_value_ranges(df, config["column_ranges"])
        
        return results
    
    def generate_report(self, check_results: Dict) -> str:
        """
        Generate a human-readable report from check results.
        
        Args:
            check_results: Dictionary containing results of all checks
            
        Returns:
            Formatted report string
        """
        report = ["Data Quality Check Report", "=" * 50]
        
        if check_results.get("is_empty", False):
            report.append("\nWARNING: DataFrame is empty")
        
        if "missing_columns" in check_results and check_results["missing_columns"]:
            report.append("\nMissing Required Columns:")
            for col in check_results["missing_columns"]:
                report.append(f"  - {col}")
        
        if "type_matches" in check_results:
            report.append("\nData Type Checks:")
            for col, matches in check_results["type_matches"].items():
                status = "✓" if matches else "✗"
                report.append(f"  {status} {col}")
        
        if "null_counts" in check_results:
            report.append("\nNull Value Checks:")
            for col, count in check_results["null_counts"].items():
                report.append(f"  {col}: {count} null values")
        
        if "duplicate_count" in check_results:
            report.append(f"\nDuplicate Rows: {check_results['duplicate_count']}")
        
        if "out_of_range_counts" in check_results:
            report.append("\nValue Range Checks:")
            for col, count in check_results["out_of_range_counts"].items():
                report.append(f"  {col}: {count} values outside range")
        
        return "\n".join(report) 