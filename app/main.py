from fastapi import FastAPI, BackgroundTasks, HTTPException
from app.models import ArticleJobRequest, ArticleJob, JobStatus
from app.services.storage import storage
from app.services.serp import fetch_serp_data
from app.agent import generate_article
from uuid import UUID
from typing import List

app = FastAPI(title="SEO Article Generator API")

@app.post("/jobs", response_model=ArticleJob, status_code=201)
async def create_job(request: ArticleJobRequest, background_tasks: BackgroundTasks):
    job = ArticleJob(request=request)
    storage.save_job(job)
    background_tasks.add_task(process_job, job)
    return job

@app.get("/jobs/{job_id}", response_model=ArticleJob)
async def get_job(job_id: UUID):
    job = storage.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs", response_model=List[ArticleJob])
async def list_jobs():
    return list(storage.jobs.values())

async def process_job(job: ArticleJob):
    try:
        job.serp_data = await fetch_serp_data(job.request.topic)
        storage.save_job(job)
        await generate_article(job)
    except Exception as e:
        job.update_status(JobStatus.FAILED, error=str(e))
        storage.save_job(job)
