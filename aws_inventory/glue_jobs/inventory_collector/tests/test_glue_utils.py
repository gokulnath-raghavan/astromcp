import pytest
from unittest.mock import Mock, patch
from utils.glue_utils import GlueJobManager

@pytest.fixture
def glue_job_manager():
    """Create a GlueJobManager instance"""
    return GlueJobManager(region="us-east-1")

@pytest.fixture
def job_config():
    """Create a sample job configuration"""
    return {
        "name": "test-job",
        "description": "Test job",
        "role": "test-role",
        "glue_version": "3.0",
        "worker_type": "G.1X",
        "number_of_workers": 2,
        "timeout": 3600,
        "max_retries": 0,
        "max_concurrent_runs": 1,
        "s3_bucket": "test-bucket",
        "job_args": {
            "--job-language": "python",
            "--job-bookmark-option": "job-bookmark-enable"
        },
        "tags": {
            "Project": "Test",
            "Environment": "Dev"
        },
        "connections": ["test-connection"]
    }

@pytest.fixture
def trigger_config():
    """Create a sample trigger configuration"""
    return {
        "name": "test-trigger",
        "type": "SCHEDULED",
        "schedule": "cron(0 12 * * ? *)",
        "description": "Test trigger",
        "job_name": "test-job",
        "start_on_creation": True
    }

def test_create_job(glue_job_manager, job_config):
    """Test creating a Glue job"""
    with patch.object(glue_job_manager.glue_client, "create_job") as mock_create_job:
        mock_create_job.return_value = {"Name": "test-job"}
        job_name = glue_job_manager.create_job(job_config)
        assert job_name == "test-job"
        mock_create_job.assert_called_once()

def test_create_trigger(glue_job_manager, trigger_config):
    """Test creating a Glue trigger"""
    with patch.object(glue_job_manager.glue_client, "create_trigger") as mock_create_trigger:
        mock_create_trigger.return_value = {"Name": "test-trigger"}
        trigger_name = glue_job_manager.create_trigger(trigger_config)
        assert trigger_name == "test-trigger"
        mock_create_trigger.assert_called_once()

def test_start_job_run(glue_job_manager):
    """Test starting a Glue job run"""
    with patch.object(glue_job_manager.glue_client, "start_job_run") as mock_start_job_run:
        mock_start_job_run.return_value = {"JobRunId": "jr_123"}
        run_id = glue_job_manager.start_job_run("test-job")
        assert run_id == "jr_123"
        mock_start_job_run.assert_called_once()

def test_get_job_run_status(glue_job_manager):
    """Test getting Glue job run status"""
    with patch.object(glue_job_manager.glue_client, "get_job_run") as mock_get_job_run:
        mock_get_job_run.return_value = {
            "JobRun": {
                "JobRunState": "RUNNING"
            }
        }
        status = glue_job_manager.get_job_run_status("test-job", "jr_123")
        assert status == "RUNNING"
        mock_get_job_run.assert_called_once()

def test_get_job_run_metrics(glue_job_manager):
    """Test getting Glue job run metrics"""
    with patch.object(glue_job_manager.glue_client, "get_job_run") as mock_get_job_run:
        mock_get_job_run.return_value = {
            "JobRun": {
                "ExecutionTime": 100,
                "MaxCapacity": 2.0,
                "NumberOfWorkers": 2,
                "WorkerType": "G.1X",
                "CompletedOn": "2023-01-01T00:00:00",
                "StartedOn": "2023-01-01T00:00:00",
                "ErrorMessage": None
            }
        }
        metrics = glue_job_manager.get_job_run_metrics("test-job", "jr_123")
        assert metrics["ExecutionTime"] == 100
        assert metrics["MaxCapacity"] == 2.0
        assert metrics["NumberOfWorkers"] == 2
        assert metrics["WorkerType"] == "G.1X"
        mock_get_job_run.assert_called_once()

def test_stop_job_run(glue_job_manager):
    """Test stopping a Glue job run"""
    with patch.object(glue_job_manager.glue_client, "batch_stop_job_run") as mock_stop_job_run:
        glue_job_manager.stop_job_run("test-job", "jr_123")
        mock_stop_job_run.assert_called_once()

def test_delete_job(glue_job_manager):
    """Test deleting a Glue job"""
    with patch.object(glue_job_manager.glue_client, "delete_job") as mock_delete_job:
        glue_job_manager.delete_job("test-job")
        mock_delete_job.assert_called_once()

def test_list_jobs(glue_job_manager):
    """Test listing Glue jobs"""
    with patch.object(glue_job_manager.glue_client, "list_jobs") as mock_list_jobs:
        mock_list_jobs.return_value = {"JobNames": ["test-job-1", "test-job-2"]}
        jobs = glue_job_manager.list_jobs()
        assert len(jobs) == 2
        assert "test-job-1" in jobs
        assert "test-job-2" in jobs
        mock_list_jobs.assert_called_once()

def test_update_job(glue_job_manager, job_config):
    """Test updating a Glue job"""
    with patch.object(glue_job_manager.glue_client, "update_job") as mock_update_job:
        glue_job_manager.update_job("test-job", job_config)
        mock_update_job.assert_called_once()

def test_create_job_error(glue_job_manager, job_config):
    """Test error handling when creating a Glue job"""
    with patch.object(glue_job_manager.glue_client, "create_job") as mock_create_job:
        mock_create_job.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.create_job(job_config)

def test_create_trigger_error(glue_job_manager, trigger_config):
    """Test error handling when creating a Glue trigger"""
    with patch.object(glue_job_manager.glue_client, "create_trigger") as mock_create_trigger:
        mock_create_trigger.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.create_trigger(trigger_config)

def test_start_job_run_error(glue_job_manager):
    """Test error handling when starting a Glue job run"""
    with patch.object(glue_job_manager.glue_client, "start_job_run") as mock_start_job_run:
        mock_start_job_run.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.start_job_run("test-job")

def test_get_job_run_status_error(glue_job_manager):
    """Test error handling when getting Glue job run status"""
    with patch.object(glue_job_manager.glue_client, "get_job_run") as mock_get_job_run:
        mock_get_job_run.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.get_job_run_status("test-job", "jr_123")

def test_get_job_run_metrics_error(glue_job_manager):
    """Test error handling when getting Glue job run metrics"""
    with patch.object(glue_job_manager.glue_client, "get_job_run") as mock_get_job_run:
        mock_get_job_run.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.get_job_run_metrics("test-job", "jr_123")

def test_stop_job_run_error(glue_job_manager):
    """Test error handling when stopping a Glue job run"""
    with patch.object(glue_job_manager.glue_client, "batch_stop_job_run") as mock_stop_job_run:
        mock_stop_job_run.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.stop_job_run("test-job", "jr_123")

def test_delete_job_error(glue_job_manager):
    """Test error handling when deleting a Glue job"""
    with patch.object(glue_job_manager.glue_client, "delete_job") as mock_delete_job:
        mock_delete_job.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.delete_job("test-job")

def test_list_jobs_error(glue_job_manager):
    """Test error handling when listing Glue jobs"""
    with patch.object(glue_job_manager.glue_client, "list_jobs") as mock_list_jobs:
        mock_list_jobs.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.list_jobs()

def test_update_job_error(glue_job_manager, job_config):
    """Test error handling when updating a Glue job"""
    with patch.object(glue_job_manager.glue_client, "update_job") as mock_update_job:
        mock_update_job.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            glue_job_manager.update_job("test-job", job_config) 