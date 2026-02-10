from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Language(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"

class InternalLink(BaseModel):
    anchor_text: str
    suggested_page: str

class ExternalReference(BaseModel):
    source_name: str
    url: str
    context: str

class SEOData(BaseModel):
    title_tag: str
    meta_description: str
    primary_keywords: List[str]
    secondary_keywords: List[str]

class Article(BaseModel):
    title: str
    content_markdown: str
    seo_metadata: SEOData
    internal_links: List[InternalLink]
    external_references: List[ExternalReference]

class SERPResult(BaseModel):
    rank: int
    url: str
    title: str
    snippet: str

class ArticleJobRequest(BaseModel):
    topic: str
    word_count: int = 1500
    language: Language = Language.ENGLISH

class ArticleJob(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request: ArticleJobRequest
    status: JobStatus = JobStatus.PENDING
    result: Optional[Article] = None
    serp_data: Optional[List[SERPResult]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def update_status(self, status: JobStatus, error: Optional[str] = None):
        self.status = status
        self.error = error
        self.updated_at = datetime.now()
