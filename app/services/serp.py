from typing import List
from app.models import SERPResult

async def fetch_serp_data(topic: str) -> List[SERPResult]:
    # Mock SERP data - replace with real API call in production
    mock_results = [
        SERPResult(
            rank=i,
            url=f"https://example.com/guide-{i}-{topic.replace(' ', '-')}",
            title=f"The Ultimate Guide to {topic} - Rank {i}",
            snippet=f"This comprehensive guide covers everything you need to know about {topic}. We explore the best strategies, tools, and tips for success in 2025."
        )
        for i in range(1, 11)
    ]
    return mock_results
