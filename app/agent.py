from openai import OpenAI
import os
from dotenv import load_dotenv
from app.models import Article, JobStatus, ArticleJob, ArticleJobRequest, SEOData, InternalLink, ExternalReference
import json
from app.services.storage import storage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
else:
    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
    MODEL = OLLAMA_MODEL

async def generate_article(job: ArticleJob):
    try:
        job.update_status(JobStatus.RUNNING)
        storage.save_job(job)

        serp_context = "\n".join([
            f"{r.rank}. {r.title} - {r.snippet}"
            for r in job.serp_data
        ])

        prompt = f"""
        You are an expert SEO Content Strategist and Writer.
        Your task is to generate a high-quality, SEO-optimized article based on search results.

        TOPIC: {job.request.topic}
        TARGET WORD COUNT: {job.request.word_count}
        LANGUAGE: {job.request.language}

        SERP ANALYSIS (Top 10 results):
        {serp_context}

        INSTRUCTIONS:
        1. Analyze the competitive landscape and identify common themes.
        2. Generate a structured article with proper H1, H2, and H3 tags.
        3. Ensure the primary keyword is in the title and introduction.
        4. The article must be publish-ready and feel human-written.
        5. Provide SEO metadata (title tag, meta description).
        6. Identify 3-5 internal link opportunities (with anchor text and suggested target topic/page).
        7. Cite 2-4 authoritative external references relevant to the content.
        8. Return the response in RAW JSON format strictly matching the schema below.

        JSON SCHEMA:
        {{
            "title": "Article Title",
            "content_markdown": "# Title\\n\\n## Introduction\\n...",
            "seo_metadata": {{
                "title_tag": "...",
                "meta_description": "...",
                "primary_keywords": ["..."],
                "secondary_keywords": ["..."]
            }},
            "internal_links": [
                {{"anchor_text": "...", "suggested_page": "..."}}
            ],
            "external_references": [
                {{"source_name": "...", "url": "...", "context": "..."}}
            ]
        }}
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional SEO writer. You must output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        article_data = json.loads(response.choices[0].message.content)
        job.result = Article.model_validate(article_data)
        job.update_status(JobStatus.COMPLETED)
        storage.save_job(job)

    except Exception as e:
        job.update_status(JobStatus.FAILED, error=str(e))
        storage.save_job(job)
        print(f"Error in generate_article: {e}")
