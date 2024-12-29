import pytest
from datetime import datetime
from main import (
    BaseScheduler,
    DataBackupScheduled,
    DataProcessingScheduled,
    create_schedule,
    DynamicJobSchedule,
    getdynamicpriority
)

# Test `create_schedule` function
def test_create_schedule_backup():
    backup_data = {
        "job_name": "backup",
        "scheduled_time": "2024-12-25T02:00:00",
        "priority": 2,
        "backup_location": "lucknow"
    }
    job = create_schedule("backup", backup_data)
    assert isinstance(job, DataBackupScheduled)
    assert job.job_name == "backup"
    assert job.backup_location == "lucknow"

# def test_create_schedule_processing():
#     processing_data = {
#         "job_name": "processing",
#         "scheduled_time": "2024-12-25T02:00:00",
#         "priority": 2,
#         "processing_type": "process",
#         "input_files": ['file1.csv', 'file2.csv']
#     }
#     job = create_schedule("processing", processing_data)
#     assert isinstance(job, DataProcessingScheduled)
#     assert job.job_name == "processing"
#     assert job.processing_type == "process"
#     assert job.input_files == ['file1.csv', 'file2.csv']

def test_create_schedule_invalid_job():
    with pytest.raises(ValueError, match="Invalid job type"):
        create_schedule("invalid", {})

# Test `DynamicJobSchedule` priority calculation
def test_dynamic_job_schedule():
    job = DynamicJobSchedule(
        job_name="backup",
        scheduled_time="2024-12-25T12:00:00"
    )
    assert job.job_name == "backup"
    assert job.priority == 3  # Low priority, as the scheduled time is in the future

# Test `getdynamicpriority` function
def test_getdynamicpriority_future_time():
    scheduled_time = "2099-12-25T12:00:00"
    priority = getdynamicpriority(scheduled_time)
    assert priority == 1  # Low priority for future time

def test_getdynamicpriority_past_time():
    scheduled_time = "1999-12-25T12:00:00"
    priority = getdynamicpriority(scheduled_time)
    assert priority == 3  # High priority for past time
