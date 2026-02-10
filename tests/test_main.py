from fastapi.testclient import TestClient
from app.main import app
import time
import pytest

client = TestClient(app)

def test_create_and_poll_job():
    response = client.post("/jobs", json={
        "topic": "best productivity tools for remote teams",
        "word_count": 500,
        "language": "English"
    })
    assert response.status_code == 201
    job_id = response.json()["id"]
    
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        status_response = client.get(f"/jobs/{job_id}")
        assert status_response.status_code == 200
        job_data = status_response.json()
        
        if job_data["status"] == "completed":
            assert "result" in job_data
            assert job_data["result"]["title"] is not None
            assert len(job_data["serp_data"]) == 10
            return
        elif job_data["status"] == "failed":
            pytest.fail(f"Job failed: {job_data['error']}")
            
        time.sleep(1)
        
    pytest.fail("Job timed out")

def test_list_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
