import json
import os
from uuid import UUID
from typing import Dict, Optional
from app.models import ArticleJob

STORAGE_FILE = "jobs.json"

class Storage:
    def __init__(self):
        self.jobs: Dict[UUID, ArticleJob] = {}
        self._load()

    def _load(self):
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, "r") as f:
                    data = json.load(f)
                    for job_id, job_data in data.items():
                        self.jobs[UUID(job_id)] = ArticleJob.model_validate(job_data)
            except Exception as e:
                print(f"Error loading jobs: {e}")

    def _save(self):
        try:
            with open(STORAGE_FILE, "w") as f:
                json_data = {str(k): v.model_dump(mode="json") for k, v in self.jobs.items()}
                json.dump(json_data, f, indent=2)
        except Exception as e:
            print(f"Error saving jobs: {e}")

    def save_job(self, job: ArticleJob):
        self.jobs[job.id] = job
        self._save()

    def get_job(self, job_id: UUID) -> Optional[ArticleJob]:
        return self.jobs.get(job_id)

storage = Storage()
