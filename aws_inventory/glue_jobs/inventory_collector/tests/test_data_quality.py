import pytest
from pyspark.sql import SparkSession
from datetime import datetime
from ..utils.data_quality import DataQualityChecker

@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession for testing.
    """
    spark = SparkSession.builder \
        .appName("test_data_quality") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_data(spark):
    """
    Create sample data for testing.
    """
    data = [
        (1, "John", 25, 1000.0, datetime(2023, 1, 1), None),
        (2, "Jane", 30, 2000.0, datetime(2023, 1, 2), "A"),
        (3, "Bob", None, 3000.0, datetime(2023, 1, 3), "B"),
        (4, "Alice", 35, None, datetime(2023, 1, 4), "C"),
        (5, "Eve", 40, 5000.0, None, "D"),
        (6, "John", 25, 1000.0, datetime(2023, 1, 1), None)  # Duplicate
    ]
    
    return spark.createDataFrame(
        data,
        ["id", "name", "age", "salary", "hire_date", "department"]
    )

def test_check_null_values(spark, sample_data):
    """
    Test null value checks.
    """
    checker = DataQualityChecker()
    null_counts = checker.check_null_values(sample_data, ["age", "salary", "hire_date", "department"])
    
    assert null_counts["age"] == 1
    assert null_counts["salary"] == 1
    assert null_counts["hire_date"] == 1
    assert null_counts["department"] == 2

def test_check_empty_dataframe(spark):
    """
    Test empty DataFrame check.
    """
    checker = DataQualityChecker()
    empty_df = spark.createDataFrame([], "id: int, name: string")
    
    assert checker.check_empty_dataframe(empty_df) is True
    assert checker.check_empty_dataframe(sample_data) is False

def test_check_duplicates(spark, sample_data):
    """
    Test duplicate check.
    """
    checker = DataQualityChecker()
    duplicate_count = checker.check_duplicates(sample_data, ["id", "name", "age", "salary"])
    
    assert duplicate_count == 1

def test_check_value_ranges(spark, sample_data):
    """
    Test value range checks.
    """
    checker = DataQualityChecker()
    column_ranges = {
        "age": (18, 65),
        "salary": (0, 10000)
    }
    
    out_of_range_counts = checker.check_value_ranges(sample_data, column_ranges)
    assert out_of_range_counts["age"] == 0
    assert out_of_range_counts["salary"] == 0

def test_check_data_types(spark, sample_data):
    """
    Test data type checks.
    """
    checker = DataQualityChecker()
    expected_types = {
        "id": "integer",
        "name": "string",
        "age": "integer",
        "salary": "double",
        "hire_date": "timestamp",
        "department": "string"
    }
    
    type_matches = checker.check_data_types(sample_data, expected_types)
    assert all(type_matches.values())

def test_check_required_columns(spark, sample_data):
    """
    Test required columns check.
    """
    checker = DataQualityChecker()
    required_columns = ["id", "name", "age", "salary", "hire_date", "department", "missing_column"]
    
    missing_columns = checker.check_required_columns(sample_data, required_columns)
    assert "missing_column" in missing_columns
    assert len(missing_columns) == 1

def test_run_all_checks(spark, sample_data):
    """
    Test running all checks.
    """
    checker = DataQualityChecker()
    config = {
        "required_columns": ["id", "name", "age", "salary", "hire_date", "department"],
        "expected_types": {
            "id": "integer",
            "name": "string",
            "age": "integer",
            "salary": "double",
            "hire_date": "timestamp",
            "department": "string"
        },
        "null_check_columns": ["age", "salary", "hire_date", "department"],
        "key_columns": ["id", "name", "age", "salary"],
        "column_ranges": {
            "age": (18, 65),
            "salary": (0, 10000)
        }
    }
    
    results = checker.run_all_checks(sample_data, config)
    
    assert not results["is_empty"]
    assert len(results["missing_columns"]) == 0
    assert all(results["type_matches"].values())
    assert results["null_counts"]["age"] == 1
    assert results["duplicate_count"] == 1
    assert all(count == 0 for count in results["out_of_range_counts"].values())

def test_generate_report(spark, sample_data):
    """
    Test report generation.
    """
    checker = DataQualityChecker()
    config = {
        "required_columns": ["id", "name", "age", "salary", "hire_date", "department"],
        "expected_types": {
            "id": "integer",
            "name": "string",
            "age": "integer",
            "salary": "double",
            "hire_date": "timestamp",
            "department": "string"
        },
        "null_check_columns": ["age", "salary", "hire_date", "department"],
        "key_columns": ["id", "name", "age", "salary"],
        "column_ranges": {
            "age": (18, 65),
            "salary": (0, 10000)
        }
    }
    
    results = checker.run_all_checks(sample_data, config)
    report = checker.generate_report(results)
    
    assert "Data Quality Check Report" in report
    assert "Null Value Checks" in report
    assert "Duplicate Rows" in report
    assert "Data Type Checks" in report
    assert "Value Range Checks" in report 