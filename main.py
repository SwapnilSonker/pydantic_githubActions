from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Union

class BaseScheduler(BaseModel):
    job_name : str
    scheduled_time : str
    priority: Optional[int] = 1
    
class DataBackupScheduled(BaseScheduler):
    backup_location : str
    
class DataProcessingScheduled(BaseScheduler):
    processing_type : str
    input_files : List[str]
    
def create_schedule(job:str , data: dict)-> Union['DataBackupScheduled', 'DataProcessingScheduled']:
    if job == "backup":
        return DataBackupScheduled(**data)
    elif job == "processing":
        return DataProcessingScheduled(**data)
    else:
        raise ValueError("Invalid job type")
    
backup_data = {
    "job_name": "processing",
    "scheduled_time": "2024-12-25T02:00:00",
    "priority": 2,
    "backup_location": "lucknow"
} 

# processing_data = {
#     "job_name": "processing",
#     "scheduled_time": "2024-12-25T02:00:00",
#     "priority": 2,
#     "processing_type": "process",
#     "input_list":['file1.csv', 'file2.csv']
# }        
      
      
# Using Fields with dynamic defaults 
from datetime import datetime
def getdynamicpriority(scheduled_time: str) -> int:
    currentTime = datetime.now()
    print(currentTime)
    if scheduled_time > currentTime.strftime('%Y-%m-%dT%H:%M:%S'):
        return 1   #low priority
    return 3 #high priority

class DynamicJobSchedule(BaseModel):
    job_name : str
    scheduled_time : str
    priority: int = Field(default_factory=lambda:3)
    
    @model_validator(mode="after")
    def set_dynamic_priority(self):
        self.priority = getdynamicpriority(self.scheduled_time)
        return self   
          
    
if __name__ == "__main__":
    # job1 = create_schedule("processing", processing_data)
    # print("processing job ->", job1)
    job2 = create_schedule("backup" , backup_data)
    print("backup job ->" , job2)
    schedule = DynamicJobSchedule(job_name="backup", scheduled_time="2024-12-25T12:00:00")
    print("schedule", schedule)